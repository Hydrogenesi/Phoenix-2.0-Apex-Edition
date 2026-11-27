"""Tests for the plate contract.

The central regression: the original `PlateStub.run_to_completion()` returned
a hardcoded COMPLETE, so no plate could report anything else. These tests
assert that BLOCKED and FAILED are genuinely reachable.
"""

from __future__ import annotations

import pytest

import cold_fold_engine as cf
from cold_fold_engine.state import Status


def test_blocked_is_reachable():
    """StalledFold has nothing to do on a clean state and must say so."""
    result = cf.StalledFold().run(cf.EngineState())
    assert result.status is Status.BLOCKED
    assert not result.ok
    assert "no active stall" in result.reasons[0]


def test_origin_refuses_to_reseed():
    """Re-seeding a live state would silently discard progress."""
    live = cf.EngineState(band=5, echo=4, tension=9)
    result = cf.OriginNucleus().run(live)
    assert result.status is Status.BLOCKED
    assert result.state_after == live, "blocked plate must not alter state"


def test_failed_is_reachable():
    """A plate that produces illegal state must report FAILED, not COMPLETE."""

    class BrokenPlate(cf.Plate):
        number = 999
        label = "Broken"

        def apply(self, state):
            return state.evolve(band=state.band)  # no progress

        def verify(self, before, after):
            return ("deliberate postcondition violation",)

    result = BrokenPlate().run(cf.EngineState())
    assert result.status is Status.FAILED
    assert result.state_after == result.state_before


def test_apply_does_not_mutate_input():
    """Purity of `apply` is what makes replay meaningful."""
    before = cf.EngineState(band=1, echo=1, tension=0)
    snapshot = before.to_dict()
    cf.DivisionAttempt().apply(before)
    assert before.to_dict() == snapshot


def test_state_is_frozen():
    state = cf.EngineState()
    with pytest.raises(Exception):
        state.band = 4  # type: ignore[misc]


def test_mersenne_substrate_never_divides_evenly():
    """127 is prime, so every split target 2..10 leaves a residue.

    This is the arithmetic the stall mechanism rests on -- if it ever became
    false the pipeline would stop generating tension.
    """
    plate = cf.DivisionAttempt()
    for echo in range(1, 9):
        state = cf.EngineState(band=1, echo=echo)
        target, group, residue = plate.partition(state)
        assert target == echo + 1
        assert residue != 0, f"127 divided evenly by {target}"
        assert group * target + residue == cf.SUBSTRATE_NODES


def test_division_banks_the_residue_as_tension():
    state = cf.EngineState(band=1, echo=1, tension=0)
    result = cf.DivisionAttempt().run(state)
    assert result.ok
    assert result.state_after.tension == 127 % 2 == 1
    assert result.state_after.stalled


def test_dynamo_blocks_below_one_band():
    result = cf.VacuumDynamo().run(cf.EngineState(band=4, tension=1))
    assert result.status is Status.BLOCKED
    assert "insufficient tension" in result.reasons[0]


def test_dynamo_conserves_exchange_rate():
    rate = cf.VacuumDynamo.RATE
    result = cf.VacuumDynamo().run(cf.EngineState(band=4, echo=1, tension=7))
    assert result.ok
    gain = result.state_after.echo - 1
    spent = 7 - result.state_after.tension
    assert spent == gain * rate


def test_crest_gate_requires_canonical_echo():
    """The canonicalThreshold=3 gate from config.json must actually gate."""
    below = cf.CrestGenesis().run(cf.EngineState(band=4, echo=2))
    assert below.status is Status.BLOCKED
    above = cf.CrestGenesis().run(cf.EngineState(band=4, echo=3))
    assert above.ok


def test_seal_is_terminal():
    """Every plate must refuse to run on a sealed state."""
    sealed = cf.EngineState(band=8, echo=4, sealed=True)
    for plate in cf.default_pipeline():
        result = plate.run(sealed)
        assert result.status is Status.BLOCKED, f"{plate.label} ran on a sealed state"


def test_pipeline_seals_in_two_passes():
    engine = cf.CosmogenicEngine()
    state = cf.EngineState()
    state, _, halt = engine.pass_once(state)
    assert halt is None
    assert not state.sealed, "sealed too early -- pass 1 gates should block"
    state, _, halt = engine.pass_once(state)
    assert halt is None
    assert state.sealed and state.at_apex


def test_governor_trips_above_cap():
    engine = cf.CosmogenicEngine(tension_cap=10)
    assert engine.governor_trip(cf.EngineState(tension=11)) is not None
    assert engine.governor_trip(cf.EngineState(tension=10)) is None


def test_run_to_completion_reports_real_status():
    """The compat shim must not resurrect the always-COMPLETE behaviour."""
    summary = cf.CosmogenicEngine().run_to_completion()
    assert summary["final_state"] == Status.COMPLETE.value
    assert summary["state"]["sealed"] is True
    assert len(summary["history"]) > 0

    # A run that cannot progress must not report COMPLETE.
    stuck = cf.CosmogenicEngine().run_to_completion(
        state=cf.EngineState(band=8, echo=4, sealed=True)
    )
    assert stuck["final_state"] != Status.COMPLETE.value or stuck["state"]["sealed"]


def test_coldfold_v7_alias_accepts_bus_kwarg():
    """The original call site was ColdFoldV7(bus=None)."""
    engine = cf.ColdFoldV7(bus=None)
    assert isinstance(engine, cf.CosmogenicEngine)
    assert engine.run_to_completion()["final_state"] == Status.COMPLETE.value
