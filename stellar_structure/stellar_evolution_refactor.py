"""
stellar_evolution_refactor.py

Refactored stellar evolution integrator for the Hydrogenesi Framework.

Integrates the four coupled stellar structure ODEs from the existing modules
into a single, clearly documented workflow:

    dP/dr = -G * M(r) * rho(r) / r^2         (hydrostatic equilibrium)
    dM/dr = 4 * pi * r^2 * rho(r)             (mass continuity)
    dL/dr = 4 * pi * r^2 * rho(r) * epsilon    (energy generation)
    dT/dr = -3 * kappa * rho * L / (64*pi*sigma*r^2*T^3)  (radiative transfer)

Central boundary conditions are derived via Taylor expansion near r=0,
replacing the previous arbitrary M_r = 1e20 starting value.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from scipy.integrate import solve_ivp

from boundary_conditions import central_boundary_conditions, surface_conditions
from energy_generation import total_energy
from equation_of_state import total_pressure, ideal_gas_pressure, is_metallic_hydrogen
from hydrostatic_equilibrium import pressure_gradient, mass_gradient, virial_theorem_check
from radiative_transfer import total_opacity, is_convective


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------

G = 6.674e-11        # gravitational constant  [m^3 kg^-1 s^-2]
SIGMA = 5.67e-8      # Stefan-Boltzmann constant [W m^-2 K^-4]
SOLAR_RADIUS = 6.957e8    # [m]
SOLAR_MASS = 1.989e30     # [kg]
SOLAR_LUMINOSITY = 3.828e26  # [W]


# ---------------------------------------------------------------------------
# StellarModel
# ---------------------------------------------------------------------------

class StellarModel:
    """
    Integrates the four coupled stellar-structure ODEs from the centre of a
    star to its surface.

    Parameters
    ----------
    rho_c : float
        Central density [kg m^-3].
    T_c : float
        Central temperature [K].
    r_start : float
        Small initial radius for Taylor-expansion boundary conditions [m].
        Must be > 0 and  much smaller than the stellar radius (default 1 km).
    r_end : float
        Outer boundary radius [m].  Integration stops here or when P ≈ 0.
    """

    def __init__(
        self,
        rho_c: float = 1.5e5,
        T_c: float = 1.5e7,
        r_start: float = 1e3,
        r_end: float = SOLAR_RADIUS,
        cache_physics: bool = True,
    ) -> None:
        self.rho_c = rho_c
        self.T_c = T_c
        self.r_start = r_start
        self.r_end = r_end
        self.cache_physics = cache_physics
        self.solution = None

    # ------------------------------------------------------------------
    # Density from equation of state (invert total_pressure for rho)
    # ------------------------------------------------------------------

    @staticmethod
    def _density_from_pressure(
        P: float | np.ndarray, T: float | np.ndarray, mu: float = 0.6
    ) -> float | np.ndarray:
        """
        Return gas density given pressure P and temperature T by solving
        the ideal-gas + radiation EOS for rho.

        The radiation term P_rad = a*T^4/3 is subtracted first; the
        remainder is the ideal-gas contribution which is linear in rho.
        """
        a = 7.566e-16          # radiation constant [J m^-3 K^-4]
        k_B = 1.381e-23        # Boltzmann constant [J K^-1]
        m_p = 1.673e-27        # proton mass [kg]
        P_arr = np.asarray(P, dtype=float)
        T_arr = np.asarray(T, dtype=float)
        P_rad = a * T_arr ** 4 / 3.0
        P_gas = np.maximum(P_arr - P_rad, 0.0)
        with np.errstate(divide="ignore", invalid="ignore"):
            rho = np.where(T_arr <= 0.0, 0.0, P_gas * mu * m_p / (k_B * T_arr))
        if np.isscalar(P) and np.isscalar(T):
            return float(rho)
        return rho

    @staticmethod
    @lru_cache(maxsize=4096)
    def _cached_total_energy(rho: float, T: float) -> float:
        return total_energy(rho, T)

    @staticmethod
    @lru_cache(maxsize=4096)
    def _cached_total_pressure(rho: float, T: float) -> float:
        return total_pressure(rho, T)

    @staticmethod
    @lru_cache(maxsize=4096)
    def _cached_total_opacity(rho: float, T: float) -> float:
        return total_opacity(rho, T)

    def _compute_total_energy(self, rho: float, T: float) -> float:
        if self.cache_physics:
            return self._cached_total_energy(rho, T)
        return total_energy(rho, T)

    def _compute_total_pressure(self, rho: float, T: float) -> float:
        if self.cache_physics:
            return self._cached_total_pressure(rho, T)
        return total_pressure(rho, T)

    def _compute_total_opacity(self, rho: float, T: float) -> float:
        if self.cache_physics:
            return self._cached_total_opacity(rho, T)
        return total_opacity(rho, T)

    # ------------------------------------------------------------------
    # ODE right-hand side
    # ------------------------------------------------------------------

    def _odes(self, r: float, state: list[float]) -> list[float]:
        """
        Evaluate the four stellar-structure ODEs at radius *r*.

        Parameters
        ----------
        r     : radial coordinate [m]
        state : [P, M, L, T]
            P – pressure [Pa]
            M – enclosed mass [kg]
            L – luminosity [W]
            T – temperature [K]

        Returns
        -------
        [dP/dr, dM/dr, dL/dr, dT/dr]
        """
        P, M, L, T = state

        # Guard against unphysical values
        P = max(P, 0.0)
        T = max(T, 1.0)
        M = max(M, 0.0)

        rho = self._density_from_pressure(P, T)

        # 1. Hydrostatic equilibrium
        dP_dr = pressure_gradient(r, M, rho)

        # 2. Mass continuity
        dM_dr = mass_gradient(r, rho)

        # 3. Energy generation
        epsilon = self._compute_total_energy(rho, T)
        dL_dr = 4.0 * np.pi * r ** 2 * rho * epsilon

        # 4. Radiative (or convective) temperature gradient
        kappa = self._compute_total_opacity(rho, T)
        if is_convective(rho, T, r, L, M, P):
            # Adiabatic gradient (gamma = 5/3 monatomic ideal gas)
            gamma = 5.0 / 3.0
            dT_dr = -(gamma - 1.0) / gamma * (G * M / r ** 2) * (T / P) * rho
        else:
            # Radiative diffusion
            denom = 64.0 * np.pi * SIGMA * r ** 2 * T ** 3
            if denom == 0:
                dT_dr = 0.0
            else:
                dT_dr = -3.0 * kappa * rho * L / denom

        return [dP_dr, dM_dr, dL_dr, dT_dr]

    # ------------------------------------------------------------------
    # Event: stop integration when pressure reaches zero (surface)
    # ------------------------------------------------------------------

    @staticmethod
    def _pressure_zero(r: float, state: list[float]) -> float:
        """Event function: triggers when P drops to zero (stellar surface)."""
        return state[0]

    _pressure_zero.terminal = True  # type: ignore[attr-defined]
    _pressure_zero.direction = -1   # type: ignore[attr-defined]

    def central_conditions(self) -> dict:
        """
        Compute and return all stellar-structure quantities at the centre
        analytically, without running the ODE integrator.

        This is useful for verifying the setup and as a quick sanity check
        on the central boundary values.

        Returns
        -------
        dict with keys:
            'P_c'           – central pressure [Pa]
            'rho_c'         – central density [kg m^-3]
            'T_c'           – central temperature [K]
            'epsilon_c'     – central energy generation rate [W kg^-1]
            'kappa_c'       – central opacity [m^2 kg^-1]
            'metallic_core' – True if P_c > metallic-hydrogen threshold
            'convective'    – True if centre is convectively unstable
        """
        P_c = self._compute_total_pressure(self.rho_c, self.T_c)
        epsilon_c = self._compute_total_energy(self.rho_c, self.T_c)
        kappa_c = self._compute_total_opacity(self.rho_c, self.T_c)
        return {
            "P_c": P_c,
            "rho_c": self.rho_c,
            "T_c": self.T_c,
            "epsilon_c": epsilon_c,
            "kappa_c": kappa_c,
            "metallic_core": is_metallic_hydrogen(P_c),
            "convective": is_convective(
                self.rho_c, self.T_c,
                r=self.r_start, L=0.0, M=0.0, P=P_c,
            ),
        }

    def integrate(self) -> dict:
        """
        Run the stellar structure integration from *r_start* to *r_end*.

        The solver uses the stiff-capable Radau method because the energy
        generation rates in the Hydrogenesi framework can produce sharp
        gradients near the stellar centre.

        Returns
        -------
        dict with keys:
            'r'         – radii [m]
            'P'         – pressure profile [Pa]
            'M'         – enclosed mass profile [kg]
            'L'         – luminosity profile [W]
            'T'         – temperature profile [K]
            'rho'       – density profile [kg m^-3] (derived)
            'converged' – True if integration reached r_end
            'message'   – solver status message
            'surface'   – dict of diagnostics at the outermost computed point
        """
        # Central boundary conditions via Taylor expansion.
        # central_boundary_conditions() returns [P_correction, M, L, T].
        # The pressure correction term alone is not the central pressure, so we
        # compute P_c from the equation of state and apply the Taylor correction.
        # We set L = 0 at the centre (exact boundary condition at r = 0); the
        # luminosity then builds up self-consistently through dL/dr as we
        # integrate outward.
        epsilon_c = self._compute_total_energy(self.rho_c, self.T_c)
        bc = central_boundary_conditions(self.r_start, self.rho_c, self.T_c, epsilon_c)
        P_c = self._compute_total_pressure(self.rho_c, self.T_c)
        # bc[0] is the Taylor correction  (≤ 0); add it to the central EOS pressure.
        state0 = [P_c + bc[0], bc[1], 0.0, bc[3]]

        sol = solve_ivp(
            self._odes,
            t_span=(self.r_start, self.r_end),
            y0=state0,
            method="Radau",        # stiff solver handles sharp initial gradients
            events=self._pressure_zero,
            dense_output=False,
            max_step=self.r_end / 500,
            rtol=1e-4,
            atol=1e-8,
        )

        self.solution = sol

        r = sol.t
        P, M, L, T = sol.y
        rho = self._density_from_pressure(P, T)

        # Diagnostics at the outermost computed point
        surf = surface_conditions()
        E_grav = -G * M[-1] ** 2 / r[-1] if r[-1] > 0 else 0.0
        E_thermal = 1.5 * P[-1] * (4.0 / 3.0) * np.pi * r[-1] ** 3
        virial_ok, virial_ratio = virial_theorem_check(E_grav, E_thermal)

        return {
            "r": r,
            "P": P,
            "M": M,
            "L": L,
            "T": T,
            "rho": rho,
            "converged": sol.success,
            "message": sol.message,
            "surface": {
                "R_final": r[-1],
                "M_final": M[-1],
                "L_final": L[-1],
                "T_surface": T[-1],
                "P_surface": surf["P"],
                "metallic_core": is_metallic_hydrogen(P[0]),
                "virial_ok": virial_ok,
                "virial_ratio": virial_ratio,
            },
        }

    def summary(self, result: dict) -> None:
        """Print a human-readable summary of the integration result."""
        s = result["surface"]
        print("=== Stellar Evolution Summary ===")
        print(f"  Central density:    {self.rho_c:.3e} kg/m^3")
        print(f"  Central temperature:{self.T_c:.3e} K")
        print(f"  Integration status: {'converged' if result['converged'] else 'partial — ' + result['message']}")
        print(f"  Outermost radius:   {s['R_final'] / SOLAR_RADIUS:.4e} R_sun")
        print(f"  Enclosed mass:      {s['M_final'] / SOLAR_MASS:.4e} M_sun")
        print(f"  Luminosity:         {s['L_final'] / SOLAR_LUMINOSITY:.4e} L_sun")
        print(f"  Temperature:        {s['T_surface']:.4e} K")
        print(f"  Metallic core:      {s['metallic_core']}")
        print(f"  Virial stable:      {s['virial_ok']} (ratio = {s['virial_ratio']:.3e})")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run() -> dict:
    """
    Convenience wrapper: build a solar-calibrated model, print central
    conditions, integrate, and print a summary.  Returns the full result
    dictionary.
    """
    model = StellarModel(
        rho_c=1.5e5,    # solar central density  ~1.5e5 kg/m^3
        T_c=1.5e7,      # solar central temperature ~1.5e7 K
        r_start=1e3,    # 1 km starting radius
        r_end=SOLAR_RADIUS,
    )

    cc = model.central_conditions()
    print("=== Central Conditions ===")
    print(f"  Central pressure:   {cc['P_c']:.3e} Pa")
    print(f"  Central density:    {cc['rho_c']:.3e} kg/m^3")
    print(f"  Central temperature:{cc['T_c']:.3e} K")
    print(f"  Energy generation:  {cc['epsilon_c']:.3e} W/kg")
    print(f"  Opacity:            {cc['kappa_c']:.3e} m^2/kg")
    print(f"  Metallic core:      {cc['metallic_core']}")
    print(f"  Convective centre:  {cc['convective']}")
    print()

    result = model.integrate()
    model.summary(result)
    return result


if __name__ == "__main__":
    run()
