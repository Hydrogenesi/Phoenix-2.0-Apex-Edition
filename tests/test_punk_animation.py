from __future__ import annotations

import json
from pathlib import Path
import sys
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from punk_animation import PhoenixAnimator, load_simulation_data, validate_stage_transitions


def test_load_simulation_data_supports_dict_wrapper(tmp_path: Path):
    payload = {"iterations": [{"iteration": 1, "stage_energies": [0.2] * 8}]}
    path = tmp_path / "sim.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    records = load_simulation_data(path)
    assert len(records) == 1
    assert records[0]["iteration"] == 1


def test_animator_progresses_across_stage_thresholds():
    animator = PhoenixAnimator()

    record_1 = {
        "iteration": 1,
        "stage_energies": [0.25, 0.10, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0],
        "stage_thresholds": [0.12, 0.22, 0.34, 0.46, 0.58, 0.70, 0.82, 0.92],
    }
    assert animator.step(record_1)["active_stage"] == 1

    record_2 = {
        "iteration": 2,
        "stage_energies": [0.40, 0.30, 0.35, 0.10, 0.0, 0.0, 0.0, 0.0],
        "stage_thresholds": [0.12, 0.22, 0.34, 0.46, 0.58, 0.70, 0.82, 0.92],
    }
    assert animator.step(record_2)["active_stage"] == 3


def test_validate_stage_transitions_rejects_regression():
    with pytest.raises(ValueError, match="Invalid regression"):
        validate_stage_transitions([
            {"active_stage": 1},
            {"active_stage": 2},
            {"active_stage": 1},
        ])
