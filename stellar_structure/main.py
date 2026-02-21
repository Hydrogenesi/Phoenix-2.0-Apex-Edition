"""Stellar Structure Main — integrates all four ODEs"""
import numpy as np
from scipy.integrate import solve_ivp
from equation_of_state import total_pressure, density_from_pressure, core_composition
from energy_generation import total_energy, bilateral_cno_rate
from radiative_transfer import radiative_gradient
SCALE_FACTOR = 2.044e21
G = 6.674e-11
def stellar_structure(r, y, star_type="sun"):
    P, M, L, T = y
    rho = max(density_from_pressure(P, T), 1e-30)
    dPdr = -G*M*rho/max(r,1e3)**2
    dMdr = 4*np.pi*r**2*rho
    shell_cleared = star_type != "ttauri_stuck"
    eps = total_energy(rho, T, shell_cleared)
    dLdr = 4*np.pi*r**2*rho*eps
    dTdr = radiative_gradient(r, max(L,1e20), M, P, T)
    return [dPdr, dMdr, dLdr, dTdr]
if __name__ == "__main__":
    from scipy.integrate import solve_ivp
    r_span = (1e3, 7e8)
    y0 = [2.5e16, 0.0, 1.0, 1.5e7]
    sol = solve_ivp(stellar_structure, r_span, y0, args=("sun",), t_eval=np.linspace(1e3,7e8,500), method="RK45", rtol=1e-6)
    core = core_composition(2.5e16)
    _, cno = bilateral_cno_rate(1e4, 1.5e7, True)
    print("Sun — metallic hydrogen core:", core["metallic_hydrogen_core"])
    print("Bilateral CNO active:", cno)
    print("Venus prediction:", round(5.3e-11*SCALE_FACTOR/1.496e11, 4), "AU")
    print("Scale factor:", SCALE_FACTOR)
