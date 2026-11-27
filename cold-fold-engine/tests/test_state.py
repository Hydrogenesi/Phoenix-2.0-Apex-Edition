"""State model validation and the config values it inherits."""

from __future__ import annotations

import pytest

import cold_fold_engine as cf
from cold_fold_engine.state import EngineError


def test_config_constants_match_project_config():
    """These come from config.json and fractal-engine.js; keep them in sync."""
    assert cf.SUBSTRATE_NODES == 127 == 2**7 - 1
    assert cf.ECHO_BANDS == (1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert cf.CANON_THRESHOLD == 3
    assert len(cf.OCTAVE_LADDER) == 9
    assert cf.OCTAVE_LADDER[0] == ("HA-0", "Substrate")
    assert cf.OCTAVE_LADDER[-1] == ("HA-8", "Apex")
    assert cf.MAX_BAND == 8


def test_illegal_band_rejected():
    with pytest.raises(EngineError):
        cf.EngineState(band=9)
    with pytest.raises(EngineError):
        cf.EngineState(band=-1)


def test_illegal_echo_rejected():
    with pytest.raises(EngineError):
        cf.EngineState(echo=0)
    with pytest.raises(EngineError):
        cf.EngineState(echo=10)


def test_negative_nodes_rejected():
    with pytest.raises(EngineError):
        cf.EngineState(nodes=-1)


def test_evolve_clamps_rather_than_raising():
    """Plates advance bands freely; clamping keeps them from overshooting."""
    assert cf.EngineState(band=8).evolve(band=99).band == cf.MAX_BAND
    assert cf.EngineState(echo=9).evolve(echo=99).echo == 9
    assert cf.EngineState(echo=1).evolve(echo=-5).echo == 1


def test_canonized_tracks_threshold():
    assert not cf.EngineState(echo=2).canonized
    assert cf.EngineState(echo=3).canonized
    assert cf.EngineState(echo=9).canonized


def test_band_labels():
    state = cf.EngineState(band=7)
    assert state.band_id == "HA-7"
    assert state.band_name == "Crown"
    assert not state.at_apex
    assert cf.EngineState(band=8).at_apex


def test_echo_shapes_cover_all_bands():
    for echo in cf.ECHO_BANDS:
        assert cf.EngineState(echo=echo).echo_shape


def test_trace_len_and_digest_stability():
    trace = cf.Trace()
    assert len(trace) == 0
    empty = trace.digest()
    assert empty == cf.Trace().digest()

    trace.append(
        cf.StepRecord(index=0, source="test", status=cf.Status.COMPLETE, state=cf.EngineState())
    )
    assert len(trace) == 1
    assert trace.digest() != empty


def test_perturbation_validates_kind():
    with pytest.raises(ValueError):
        cf.Perturbation(step=1, kind="not_a_kind")
    with pytest.raises(ValueError):
        cf.Perturbation(step=-1, kind="tension")


def test_unseal_on_unsealed_state_is_a_noop():
    state = cf.EngineState(band=4)
    new, note = cf.Perturbation(step=0, kind="unseal").apply(state)
    assert new == state
    assert "no-op" in note
