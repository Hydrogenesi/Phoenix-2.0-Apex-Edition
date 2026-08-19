import json
import time
from enum import Enum, auto
from pathlib import Path


class Stage(Enum):
    CELLULAR_POTENTIAL = auto()
    MOLECULAR_VALENCE_ORDER = auto()
    ENZYMATIC_REACTION_LOOPS = auto()
    LINEAGE_SPLIT_FIDELITY = auto()
    TISSUE_INTEGRATION_COHERENCE = auto()
    ORGANISMAL_THRESHOLD_METRIC = auto()
    EXOTIC_ADAPTATION_POTENTIAL = auto()
    EVOLUTIONARY_SINGULARITY_MASS = auto()


STAGE_NAMES = [
    "Cellular Potential",
    "Molecular Valence Order",
    "Enzymatic Reaction Loops",
    "Lineage Split Fidelity",
    "Tissue Integration Coherence",
    "Organismal Threshold Metric",
    "Exotic Adaptation Potential",
    "Evolutionary Singularity Mass",
]

ICONS = {
    Stage.CELLULAR_POTENTIAL: "●",
    Stage.MOLECULAR_VALENCE_ORDER: "●●",
    Stage.ENZYMATIC_REACTION_LOOPS: "✖",
    Stage.LINEAGE_SPLIT_FIDELITY: "⬢",
    Stage.TISSUE_INTEGRATION_COHERENCE: "⬡",
    Stage.ORGANISMAL_THRESHOLD_METRIC: "⬣",
    Stage.EXOTIC_ADAPTATION_POTENTIAL: "✦",
    Stage.EVOLUTIONARY_SINGULARITY_MASS: "★",
}

DEFAULT_THRESHOLDS = [0.12, 0.22, 0.34, 0.46, 0.58, 0.70, 0.82, 0.92]


class PhoenixAnimator:
    def __init__(self):
        self.active_stage = 1
        self.previous_energies = [0.0] * 8

    def _to_stage_energies(self, record):
        source = record.get("stage_energies")
        if isinstance(source, dict):
            values = [float(source.get(str(i), source.get(i, 0.0))) for i in range(1, 9)]
        elif isinstance(source, list) and len(source) == 8:
            values = [float(v) for v in source]
        else:
            values = [0.0] * 8
        return [max(0.0, min(1.0, v)) for v in values]

    def _thresholds(self, record):
        thresholds = record.get("stage_thresholds", DEFAULT_THRESHOLDS)
        if not isinstance(thresholds, list) or len(thresholds) != 8:
            return DEFAULT_THRESHOLDS
        return [max(0.0, min(1.0, float(v))) for v in thresholds]

    def _derive_active_stage(self, energies, thresholds):
        stage = self.active_stage
        for idx in range(self.active_stage, 9):
            if energies[idx - 1] >= thresholds[idx - 1]:
                stage = idx
            else:
                break
        return stage

    def step(self, record):
        energies = self._to_stage_energies(record)
        thresholds = self._thresholds(record)
        self.active_stage = self._derive_active_stage(energies, thresholds)
        flow = [energies[i] - self.previous_energies[i] for i in range(8)]
        self.previous_energies = energies

        return {
            "iteration": int(record.get("iteration", 0)),
            "active_stage": self.active_stage,
            "active_stage_name": STAGE_NAMES[self.active_stage - 1],
            "stage_energies": energies,
            "meaning_apex_index": float(record.get("meaning_apex_index", 0.0)),
            "entropic_negentropy": float(record.get("entropic_negentropy", 0.0)),
            "resonance_harmony": float(record.get("resonance_harmony", 0.0)),
            "flow": flow,
        }


def load_simulation_data(path="phoenix_simulation_output.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "iterations" in data:
        records = data["iterations"]
    elif isinstance(data, list):
        records = data
    else:
        raise ValueError("Simulation output must be a list or {\"iterations\": [...]} JSON")

    if not records:
        raise ValueError("Simulation output contains no iteration records")
    return records


def validate_stage_transitions(states):
    previous = 1
    for state in states:
        current = state["active_stage"]
        if current < previous:
            raise ValueError(f"Invalid regression: stage {previous} -> {current}")
        if current > previous + 1:
            raise ValueError(f"Invalid jump: stage {previous} -> {current}")
        previous = current


def _bar(value):
    value = max(0.0, min(1.0, float(value)))
    filled = int(round(value * 10))
    return "█" * filled + "░" * (10 - filled)


def _print_state(snapshot):
    stage_index = snapshot["active_stage"] - 1
    stage_enum = list(Stage)[stage_index]
    print(f"Stage {snapshot['active_stage']}: {snapshot['active_stage_name']}")
    print(f"{ICONS[stage_enum]} {snapshot['active_stage_name'].lower().replace(' ', '_')} (ACTIVE)")
    print(f"Energy: {snapshot['stage_energies'][stage_index] * 100:5.1f}% | "
          f"MAI: {snapshot['meaning_apex_index']:.3f} | "
          f"Harmony: {snapshot['resonance_harmony']:.3f}")

    for i, name in enumerate(STAGE_NAMES, start=1):
        marker = " ← ACTIVE" if i == snapshot["active_stage"] else ""
        energy = snapshot["stage_energies"][i - 1]
        print(f" {i}. {name:<30} {_bar(energy)} {energy * 100:5.1f}%{marker}")

    flow = " | ".join(
        f"S{i + 1}:{delta:+0.3f}" for i, delta in enumerate(snapshot["flow"])
    )
    print(f"Flow Δ: {flow}")
    print(
        f"Convergence: MAI={snapshot['meaning_apex_index']:.3f}, "
        f"EntropicNegentropy={snapshot['entropic_negentropy']:.3f}, "
        f"ResonanceHarmony={snapshot['resonance_harmony']:.3f}"
    )
    print()


def run(simulation_path="phoenix_simulation_output.json", delay=0.15):
    records = load_simulation_data(simulation_path)
    animator = PhoenixAnimator()

    snapshots = []
    for record in records:
        snapshot = animator.step(record)
        snapshots.append(snapshot)
        _print_state(snapshot)
        if delay > 0:
            time.sleep(delay)

    validate_stage_transitions(snapshots)


if __name__ == "__main__":
    run()
