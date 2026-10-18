"""AU operators: curvature residue, AGN replication and the q-desic bridge."""
import math

import pytest

from src.au.ops import agn_replication, curvature_residue, q_desic

# CODATA 2018 / IAU values (SI)
G, c, m_p, sigma_T, M_sun = 6.67430e-11, 2.99792458e8, 1.67262192e-27, 6.6524587e-29, 1.98847e30


@pytest.mark.physics
def test_eddington_factor_matches_physics():
    """L_Edd / M = 4πG m_p c / σ_T  ≈ 1.26e31 W per solar mass."""
    expected = 4 * math.pi * G * M_sun * m_p * c / sigma_T
    assert agn_replication.EDDINGTON_FACTOR == pytest.approx(expected, rel=0.01)


def test_replication_gradient_formula():
    out = agn_replication.run({"mass_solar": 1e6, "redshift": 1.0, "eta": 0.1})
    assert out["replication_gradient"] == pytest.approx(0.1 * 1.26e37 / 4)


@pytest.mark.physics
def test_stress_energy_coupling_units():
    """8πG/c² ρ for the critical density (~1e-26 kg/m³) is ~1e-52 m⁻², the same order as Λ."""
    term = 8 * math.pi * G / c**2 * 1e-26
    assert 1e-53 < term < 1e-51


def test_residue_formula():
    out = curvature_residue.run({"kappa": 0.0, "rho": 0.0, "lambda_c": 2.0})
    assert out["residue"] == pytest.approx(2.0)


def test_q_desic_coupling_is_bounded():
    out = q_desic.run()
    cr = out["curvature_residue"]["residue"]
    assert 0 <= out["coupling_coefficient"] <= abs(cr)


def test_ops_are_deterministic():
    assert q_desic.run() == q_desic.run()
