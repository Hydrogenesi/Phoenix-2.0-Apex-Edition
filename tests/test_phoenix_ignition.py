"""Phoenix operators and the five substrate laws (phoenix_ignition.py)."""
import pytest

from phoenix_ignition import (
    LawViolation, Pattern, PhoenixIgnition, law_conservation, law_duality,
    law_emergence, law_recursion, law_symmetry, op_apex, op_convergence,
    op_divergence, op_genesis, op_harmonic, op_mirror, op_recursive, op_void,
)


# --- Pattern ---------------------------------------------------------------

def test_void_pattern():
    v = Pattern.void()
    assert v.is_void() and v.energy == 0.0 and v.complexity() == 0.0


def test_complexity_grows_with_depth():
    shallow = Pattern(id="a", state="x", energy=1.0, depth=0)
    deep = Pattern(id="b", state="x", energy=1.0, depth=5)
    assert deep.complexity() > shallow.complexity() == 1.0


def test_id_defaults_to_state_hash():
    assert Pattern(id="", state="seed").id == Pattern(id="", state="seed").id
    assert Pattern(id="", state="a").id != Pattern(id="", state="b").id


# --- Operators -------------------------------------------------------------

def test_genesis_is_deterministic():
    assert op_genesis("s").id == op_genesis("s").id
    assert op_genesis().state == "Ψ₀"


def test_genesis_rejects_negative_energy():
    with pytest.raises(LawViolation):
        op_genesis("s", energy=-1.0)


def test_harmonic_scales_energy():
    p = op_genesis("s", energy=2.0)
    assert op_harmonic(p).energy == 2.0
    assert op_harmonic(p, amplify=1.5).energy == 3.0


def test_recursive_increments_depth_and_enforces_limit():
    p = op_genesis("s")
    assert op_recursive(p).depth == 1
    with pytest.raises(LawViolation):
        op_recursive(Pattern(id="d", state="x", depth=64))


def test_apex_threshold():
    with pytest.raises(LawViolation):
        op_apex(op_genesis("s"), threshold=2.0)        # complexity 1.0
    assert op_apex(op_genesis("s", energy=3.0)).state == "Apex"


def test_void_and_mirror():
    p = op_genesis("s", energy=0.7)
    assert op_void(p).is_void()
    assert law_symmetry(p, op_mirror(p))


def test_convergence_sums_energy_and_needs_two():
    a, b = op_genesis("a", energy=1.0), op_genesis("b", energy=2.5)
    assert op_convergence(a, b).energy == pytest.approx(3.5)
    with pytest.raises(ValueError):
        op_convergence(a)


def test_divergence_conserves_energy():
    p = op_genesis("s", energy=3.0)
    left, right = op_divergence(p)
    assert left.energy + right.energy == pytest.approx(p.energy)


# --- Laws ------------------------------------------------------------------

def test_duality_energies_sum_to_one():
    p, dual = law_duality(Pattern(id="p", state="x", energy=0.3))
    assert p.energy + dual.energy == pytest.approx(1.0)


def test_emergence_threshold():
    ps = [Pattern(id=str(i), state=i, energy=1.0) for i in range(2)]
    assert law_emergence(ps, threshold=2.0)
    assert not law_emergence(ps[:1], threshold=2.0)


def test_recursion_limit_boundary():
    law_recursion(Pattern(id="x", state=1, depth=64))  # at the limit is allowed
    with pytest.raises(LawViolation):
        law_recursion(Pattern(id="x", state=1, depth=65))


# --- Rituals ---------------------------------------------------------------

def test_ignite_reaches_apex():
    assert PhoenixIgnition().ignite("seed").state == "Apex"


def test_ignite_is_deterministic():
    a, b = PhoenixIgnition().ignite("seed"), PhoenixIgnition().ignite("seed")
    assert (a.id, a.energy, a.depth) == (b.id, b.energy, b.depth)


def test_cycle_renews_pattern():
    out = PhoenixIgnition().cycle("seed")
    assert out.state == "renewed:seed" and out.energy == 1.0


def test_converge_requires_two_seeds():
    assert PhoenixIgnition().converge(["a", "b"]).state == "Apex"
    with pytest.raises(ValueError):
        PhoenixIgnition().converge(["a"])


# --- Known defects ---------------------------------------------------------

@pytest.mark.known_defect
@pytest.mark.xfail(reason="law_conservation only checks energy >= 0; it never compares input "
                          "and output, so op_harmonic(amplify=1.5) creates energy unchallenged")
def test_conservation_law_catches_energy_creation():
    p = op_genesis("s", energy=1.0)
    with pytest.raises(LawViolation):
        law_conservation(p, Pattern(id="q", state="x", energy=5.0))
