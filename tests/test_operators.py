"""NIP protocol, NG-Laws enforcement and Third Pillar operators."""
import pytest

import ng_laws_enforcement as ng
import nip_protocol as nip
import third_pillar_operators as tp


# --- NIP protocol: steps must run in order -------------------------------------

def test_nip_full_invocation():
    p = nip.NIPProtocol()
    p.nip_1_ground()
    p.nip_2_declare_nod_level(nip.NODLevel.NOD_3)
    p.nip_3_carry_coherence(1.0)
    p.nip_4_close("payload")
    assert p.is_valid_invocation()
    form = p.generate_full_form()
    assert form.startswith("Η → :") and "payload" in form and form.endswith("Return: ∮N")


@pytest.mark.parametrize("step", ["nip_2", "nip_3", "nip_4"])
def test_nip_rejects_out_of_order_steps(step):
    p = nip.NIPProtocol()
    calls = {
        "nip_2": lambda: p.nip_2_declare_nod_level(nip.NODLevel.NOD_3),
        "nip_3": lambda: p.nip_3_carry_coherence(1.0),
        "nip_4": lambda: p.nip_4_close("x"),
    }
    with pytest.raises(nip.InvocationError):
        calls[step]()


def test_nip_rejects_zero_coherence():
    p = nip.NIPProtocol()
    p.nip_1_ground(); p.nip_2_declare_nod_level(nip.NODLevel.NOD_3)
    with pytest.raises(nip.InvocationError):
        p.nip_3_carry_coherence(0.0)


def test_incomplete_invocation_has_no_full_form():
    p = nip.NIPProtocol(); p.nip_1_ground()
    assert not p.is_complete()
    assert p.generate_full_form() == "[Invocation incomplete or invalid]"


@pytest.mark.known_defect
@pytest.mark.xfail(reason="NIP-3 only rejects exactly 0.0; negative coherence passes, "
                          "although NG-Law II forbids it")
def test_nip_rejects_negative_coherence():
    p = nip.NIPProtocol()
    p.nip_1_ground(); p.nip_2_declare_nod_level(nip.NODLevel.NOD_3)
    with pytest.raises(nip.InvocationError):
        p.nip_3_carry_coherence(-1.0)


# --- NG-Laws enforcement ------------------------------------------------------

def C(nod, coherence=1.0, chain=("NOD-0",)):
    return ng.Construct(f"c{nod}", ng.NODLevel(nod), coherence, list(chain))


def test_law_i_lower_nod_wins():
    assert ng.NGLawI.resolve_conflict(C(3), C(1)).nod_level.value == 1


def test_law_i_tie_goes_to_longer_derivation():
    long = C(2, chain=("a", "b", "c"))
    assert ng.NGLawI.resolve_conflict(C(2), long) is long


def test_law_i_only_nucleus_is_sovereign():
    assert ng.NGLawI.sub_nuclear_authority_check(C(0))
    assert not ng.NGLawI.sub_nuclear_authority_check(C(1))


@pytest.mark.parametrize("coherence", [0.0, -0.5])
def test_law_ii_rejects_broken_coherence(coherence):
    with pytest.raises(ng.NGLawViolation):
        ng.NGLawII.verify_operation(C(0), C(1, coherence))


def test_law_ii_chain_validation():
    assert ng.NGLawII.validate_coherence_chain([C(0), C(1, 0.5)])
    assert not ng.NGLawII.validate_coherence_chain([C(0), C(1, 0.0)])


# --- Third Pillar operators: round trip ∂N then ∮N ------------------------------

def test_differentiate_then_cohere_round_trip():
    nucleus = tp.NucleusState()
    assert nucleus.nod_level == tp.NODLevel.NOD_0 and nucleus.verify_nucleus_traceability()
    proton, neutron = tp.DifferentiationOperator.apply(nucleus)
    assert {proton.nod_level, neutron.nod_level} == {tp.NODLevel.NOD_1}
    unified = tp.CohesionOperator.apply([proton, neutron])
    assert unified.nod_level == tp.NODLevel.NOD_0
    assert unified.coherence_state == pytest.approx((proton.coherence_state + neutron.coherence_state) / 2)


def test_cohesion_needs_components():
    with pytest.raises(tp.NGLawViolation):
        tp.CohesionOperator.apply([])
