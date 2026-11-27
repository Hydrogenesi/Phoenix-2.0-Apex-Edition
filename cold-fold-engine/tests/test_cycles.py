"""Regression tests for the `run()` shadowing bug in the original cycles.txt.

All three `run()` definitions lived in one module, so the first two were
unreachable. These tests fail if that ever regresses.
"""

from __future__ import annotations

import pytest

import cold_fold_engine as cf
from cold_fold_engine.cycles import CYCLES, collapse, demo, relativistic


def test_all_three_cycles_are_registered():
    assert set(CYCLES) == {"relativistic", "collapse", "demo"}


def test_cycles_are_distinct_callables():
    """The shadowing bug made these collapse to a single function."""
    fns = [CYCLES["relativistic"], CYCLES["collapse"], CYCLES["demo"]]
    assert len({id(f) for f in fns}) == 3
    assert relativistic.run is not collapse.run
    assert collapse.run is not demo.run


def test_cycles_have_distinct_behaviour():
    """Distinct identity is not enough -- they must do different things."""
    start = cf.EngineState(band=1, echo=1, tension=8)
    traces = {
        name: CYCLES[name](max_steps=3, delay=0.0, state=start) for name in CYCLES
    }
    digests = {name: t.digest() for name, t in traces.items()}
    assert len(set(digests.values())) == 3, f"cycles are not distinct: {digests}"


def test_relativistic_sweeps_the_octave_ladder():
    trace = relativistic.run(max_steps=12, state=cf.EngineState(band=0))
    bands = [r.state.band for r in trace]
    assert bands[: cf.MAX_BAND + 1] == list(range(1, cf.MAX_BAND + 1)) + [0]
    assert max(bands) == cf.MAX_BAND


def test_collapse_decays_tension_to_zero():
    trace = collapse.run(max_steps=10, delay=0.0, state=cf.EngineState(tension=100))
    tensions = [r.state.tension for r in trace]
    assert tensions[0] == 50
    assert tensions[-1] == 0
    assert all(b <= a for a, b in zip(tensions, tensions[1:])), "decay not monotonic"


def test_collapse_stops_at_fixed_point():
    """A zero-tension start is already at the fixed point."""
    trace = collapse.run(max_steps=10, delay=0.0, state=cf.EngineState(tension=0))
    assert len(trace) == 1
    assert trace.records[0].notes == ("fixed point reached",)


def test_demo_advances_echo_and_stops_at_saturation():
    trace = demo.run(max_steps=20, state=cf.EngineState(echo=1))
    echoes = [r.state.echo for r in trace]
    assert echoes[0] == 2
    assert max(echoes) == cf.ECHO_BANDS[-1]
    assert len(trace) < 20, "cycle did not stop at saturation"


def test_negative_max_steps_rejected():
    with pytest.raises(ValueError):
        demo.run(max_steps=-1)
