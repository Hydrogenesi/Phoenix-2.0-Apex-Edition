"""The Hydrogenesi scale factor S = 2.044e21 and its planetary-orbit claims.

S is described as (Moon radius) / (proton radius). Bohr radius × S lands near
Venus's orbit; Earth is then predicted as √2 × that. These tests pin the claims
to numbers so any change to S or the constants shows up immediately.
"""
import importlib.util
import math
from pathlib import Path

import pytest

import radiative_transfer as rt
from src.au.ops import curvature_residue

pytestmark = pytest.mark.physics

_spec = importlib.util.spec_from_file_location(
    "stellar_main", Path(__file__).resolve().parents[1] / "stellar_structure" / "main.py")
stellar_main = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stellar_main)

R_MOON = 1.7374e6               # m, IAU mean radius
R_PROTON_CODATA2018 = 0.8414e-15
R_PROTON_CODATA2014 = 0.8751e-15
BOHR = 5.29177210903e-11        # m, CODATA 2018
AU = 1.495978707e11             # m
VENUS_AU, EARTH_AU = 0.723332, 1.000001


def test_scale_factor_is_consistent_across_modules():
    assert stellar_main.SCALE_FACTOR == curvature_residue.SCALE_FACTOR == 2.044e21


def test_scale_factor_matches_moon_over_proton():
    """S equals R_moon / r_p for r_p ≈ 0.85 fm; with CODATA 2018 r_p it is ~1 % higher."""
    assert stellar_main.SCALE_FACTOR == pytest.approx(R_MOON / R_PROTON_CODATA2018, rel=0.02)


def test_venus_claim():
    predicted, delta = stellar_main.venus_prediction()
    assert delta < 0.5                                   # percent


def test_earth_claim_sqrt2():
    predicted, delta = stellar_main.earth_prediction()
    assert delta < 5.0                                   # percent; currently ~2.4 %


@pytest.mark.parametrize("r_p,max_pct", [(R_PROTON_CODATA2018, 2.0), (R_PROTON_CODATA2014, 4.0)])
def test_venus_match_depends_on_proton_radius(r_p, max_pct):
    """Recompute from first principles: the Venus match moves by percent-level amounts
    depending on which measured proton radius is used. Report this in any write-up."""
    venus_pred = BOHR * (R_MOON / r_p) / AU
    assert abs(venus_pred - VENUS_AU) / VENUS_AU * 100 < max_pct


def test_em_scale_check_accepts_venus_orbit():
    assert rt.em_scale_check(VENUS_AU * AU)
    assert not rt.em_scale_check(EARTH_AU * AU)
