"""Determinism is the property the repair was for, so it gets tested directly."""

from __future__ import annotations

import cold_fold_engine as cf


def test_runtime_digest_is_reproducible():
    """Independent runs of the same scenario must produce identical traces."""
    digests = {
        cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(120).digest()
        for _ in range(5)
    }
    assert len(digests) == 1, f"run is not deterministic: {digests}"


def test_engine_digest_is_reproducible():
    digests = {cf.CosmogenicEngine().run().digest() for _ in range(5)}
    assert len(digests) == 1, f"pipeline is not deterministic: {digests}"


def test_reset_restores_initial_state():
    rt = cf.Runtime(perturbations=cf.DEFAULT_SCENARIO)
    first = rt.run(120).digest()
    second = rt.run(120).digest()
    assert first == second, "re-running the same Runtime changed the result"


def test_delay_does_not_affect_result():
    """`delay` is cosmetic; it must not enter the state transition."""
    a = cf.CYCLES["demo"](max_steps=4, delay=0.0)
    b = cf.CYCLES["demo"](max_steps=4, delay=0.01)
    assert a.digest() == b.digest()


def test_max_steps_is_honoured():
    """The originals ignored max_steps beyond a print count."""
    for n in (0, 1, 3, 7):
        assert len(cf.CYCLES["relativistic"](max_steps=n)) == n


def test_trace_length_bounded_by_budget():
    for n in (1, 10, 50, 120):
        assert len(cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(n)) <= n


def test_scenario_reaches_all_three_halt_paths():
    """DEFAULT_SCENARIO should seal, hold, and finally trip the governor."""
    trace = cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(120)
    statuses = trace.statuses()
    assert statuses.get("COMPLETE", 0) > 0, "nothing ever completed"
    assert statuses.get("BLOCKED", 0) > 0, "no gate ever blocked"
    assert statuses.get("FAILED", 0) == 1, "governor trip not recorded exactly once"
    assert "governor" in trace.records[-1].source
