"""Stellar-structure physics checked against textbook values (SI units).

Reference for the formulas: Carroll & Ostlie, *An Introduction to Modern
Astrophysics*, 2nd ed., chapters 9–10. Solar-centre conditions used throughout:
ρ_c ≈ 1.5e5 kg m⁻³, T_c ≈ 1.57e7 K, X ≈ 0.7.
"""
import math

import pytest

import boundary_conditions as bc
import energy_generation as eg
import equation_of_state as eos
import hydrostatic_equilibrium as hse
import radiative_transfer as rt
import stellar_evolution_refactor as sev

pytestmark = pytest.mark.physics

RHO_C, T_C, X = 1.5e5, 1.57e7, 0.7
CODATA = {"G": 6.67430e-11, "k_B": 1.380649e-23, "m_p": 1.67262192e-27, "a": 7.5657e-16}


# --- Constants ------------------------------------------------------------------

@pytest.mark.parametrize("name,value", [
    ("G", hse.G), ("G", bc.G), ("G", sev.G), ("k_B", eos.k_B), ("m_p", eos.m_p),
])
def test_constants_match_codata(name, value):
    assert value == pytest.approx(CODATA[name], rel=1e-3)


# --- Equation of state ---------------------------------------------------------

def test_ideal_gas_pressure_formula():
    assert eos.ideal_gas_pressure(RHO_C, T_C, mu=0.6) == pytest.approx(
        RHO_C * CODATA["k_B"] * T_C / (0.6 * CODATA["m_p"]), rel=1e-3)


def test_radiation_pressure_formula():
    assert eos.radiation_pressure(T_C) == pytest.approx(CODATA["a"] * T_C**4 / 3, rel=1e-3)


def test_solar_core_gas_pressure_dominates_radiation():
    assert eos.ideal_gas_pressure(RHO_C, T_C) > 1000 * eos.radiation_pressure(T_C)


# --- Hydrostatic equilibrium -----------------------------------------------------

def test_mass_continuity():
    assert hse.mass_gradient(2.0, 3.0) == pytest.approx(4 * math.pi * 4 * 3)


def test_pressure_decreases_outward():
    assert hse.pressure_gradient(1e8, 1e29, 1e3) < 0


def test_virial_ratio_half_is_stable():
    stable, ratio = hse.virial_theorem_check(E_grav=-2.0, E_thermal=1.0)
    assert stable and ratio == pytest.approx(0.5)


def test_central_mass_taylor_term():
    M = bc.central_boundary_conditions(10.0, RHO_C, T_C, 1e-3)[1]
    assert M == pytest.approx(4 / 3 * math.pi * RHO_C * 10.0**3)


def test_adiabatic_gradient_monatomic():
    assert rt.adiabatic_gradient() == pytest.approx(0.4)


# --- Known defects ---------------------------------------------------------------
# Each test asserts the textbook behaviour. They are expected to fail until the code
# is fixed; with xfail_strict, a fix makes them "XPASS" -> remove the marker then.

@pytest.mark.known_defect
@pytest.mark.xfail(reason="0.2(1+X) is the cgs value (cm²/g); in SI it is 0.02(1+X) m²/kg")
def test_electron_scattering_opacity_si():
    assert rt.electron_scattering_opacity(X) == pytest.approx(0.02 * (1 + X), rel=1e-3)


@pytest.mark.known_defect
@pytest.mark.xfail(reason="pp-chain power law uses T⁴ in kelvin; it must be T6 = T/1e6 "
                          "(and include X²). Result is ~1e22 W/kg instead of ~5e-3 W/kg")
def test_pp_chain_rate_at_solar_core_is_physical():
    assert 1e-4 < eg.pp_chain_rate(RHO_C, T_C) < 1.0      # W/kg


@pytest.mark.known_defect
@pytest.mark.xfail(reason="CNO power law uses T¹⁸ in kelvin; it must be T6^19.9 with X·X_CNO")
def test_cno_rate_at_solar_core_is_physical():
    assert 1e-6 < eg.cno_rate(RHO_C, T_C) < 1.0           # W/kg


@pytest.mark.known_defect
@pytest.mark.xfail(reason="Kramers coefficient 4.34e21 needs the Z(1+X)/t factor; without it the "
                          "solar-centre opacity is ~50 m²/kg instead of ~0.1–1 m²/kg")
def test_solar_core_opacity_is_physical():
    assert 0.05 < rt.total_opacity(RHO_C, T_C, X) < 5.0


@pytest.mark.known_defect
@pytest.mark.xfail(reason="central_boundary_conditions returns P = -(2/3)πGρ²r² and drops P_c, "
                          "so the integration starts from (near-)zero pressure")
def test_central_pressure_starts_at_core_pressure():
    P_r = bc.central_boundary_conditions(10.0, RHO_C, T_C, 1e-3)[0]
    assert P_r == pytest.approx(eos.total_pressure(RHO_C, T_C), rel=1e-3)


@pytest.mark.known_defect
@pytest.mark.xfail(reason="the stellar model stops after ~1 km (1e-6 R_sun) instead of reaching a surface")
def test_stellar_model_reaches_surface(capsys):
    result = sev.run()
    assert result["converged"]
    assert result["r"][-1] > 0.5 * sev.SOLAR_RADIUS
