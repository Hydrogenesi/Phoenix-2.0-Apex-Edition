"""Runtime: step the pipeline one plate at a time under a perturbation schedule.

`coldfold.ps1` calls:

    rt = cf.Runtime(perturbations=cf.DEFAULT_SCENARIO)
    tr = rt.run(120)
    print('steps', len(tr))

Neither `Runtime` nor `DEFAULT_SCENARIO` existed in the original prototype files -- the
launcher referenced a `cold_fold_engine` module that was never included. This
supplies both with that exact API.

Where CosmogenicEngine.run() advances a whole pass at a time, Runtime advances
one plate per step, so a step budget of 120 is meaningful and the trace has one
record per step. It records every step honestly, including steps where nothing
opened.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .cosmogenic_engine import CosmogenicEngine
from .plate import Plate
from .state import EngineState, Status, StepRecord, Trace

PERTURBATION_KINDS = ("tension", "unseal", "reset")


@dataclass(frozen=True)
class Perturbation:
    """A scheduled, deterministic external nudge.

    Perturbations are the only source of non-monotonic change in a run. They
    are declared up front with fixed step indices and magnitudes -- there is no
    randomness anywhere in the engine, which is what makes the trace digest
    reproducible.
    """

    step: int
    kind: str
    magnitude: int = 0

    def __post_init__(self) -> None:
        if self.kind not in PERTURBATION_KINDS:
            raise ValueError(
                f"unknown perturbation kind {self.kind!r}; expected one of {PERTURBATION_KINDS}"
            )
        if self.step < 0:
            raise ValueError(f"perturbation step must be non-negative, got {self.step}")

    def apply(self, state: EngineState) -> tuple[EngineState, str]:
        if self.kind == "tension":
            new = state.evolve(tension=state.tension + self.magnitude)
            return new, f"injected tension +{self.magnitude} -> {new.tension}"
        if self.kind == "unseal":
            if not state.sealed:
                return state, "unseal requested but state was not sealed (no-op)"
            new = state.evolve(sealed=False, band=7)
            return new, "seal released; state reopened at HA-7"
        new = EngineState()
        return new, "state reset to origin"

    def to_dict(self) -> dict[str, Any]:
        return {"step": self.step, "kind": self.kind, "magnitude": self.magnitude}


#: Reproducible demonstration schedule. Exercises all three halt paths:
#: the run seals on its own, is reopened, climbs back, and is finally driven
#: past the governor's tension cap of 64.
DEFAULT_SCENARIO: tuple[Perturbation, ...] = (
    Perturbation(step=40, kind="tension", magnitude=6),
    Perturbation(step=60, kind="unseal"),
    Perturbation(step=95, kind="tension", magnitude=200),
)


class Runtime:
    """Plate-at-a-time driver with a perturbation schedule."""

    def __init__(
        self,
        perturbations: tuple[Perturbation, ...] = (),
        engine: CosmogenicEngine | None = None,
        state: EngineState | None = None,
    ) -> None:
        self.engine = engine if engine is not None else CosmogenicEngine()
        self.perturbations = tuple(perturbations)
        self.initial_state = EngineState() if state is None else state
        self.state = self.initial_state
        self._cursor = 0

        self._schedule: dict[int, list[Perturbation]] = {}
        for p in self.perturbations:
            self._schedule.setdefault(p.step, []).append(p)

    @property
    def pipeline(self) -> tuple[Plate, ...]:
        return self.engine.pipeline

    def _pending_after(self, index: int) -> bool:
        return any(p.step > index for p in self.perturbations)

    def reset(self) -> None:
        self.state = self.initial_state
        self._cursor = 0

    def run(self, max_steps: int = 120) -> Trace:
        """Advance up to `max_steps` plate executions.

        Returns a Trace; `len(trace)` is the number of steps actually taken,
        which may be fewer than `max_steps` if the run halts. Halts on a
        governor trip, a plate FAILURE, or a sealed state with no further
        perturbations scheduled.
        """
        if max_steps < 0:
            raise ValueError(f"max_steps must be non-negative, got {max_steps}")

        self.reset()
        trace = Trace()

        for index in range(max_steps):
            # 1. Scheduled perturbations for this step.
            notes: list[str] = []
            for p in self._schedule.get(index, []):
                self.state, note = p.apply(self.state)
                notes.append(note)

            # 2. Governor check on the perturbed state, before any plate runs.
            trip = self.engine.governor_trip(self.state)
            if trip:
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.FAILED,
                        state=self.state,
                        notes=tuple(notes + [trip]),
                    )
                )
                break

            # 3. Held at apex: idle while future perturbations remain, else halt.
            if self.state.sealed:
                if not self._pending_after(index):
                    trace.append(
                        StepRecord(
                            index=index,
                            source="governor:75",
                            status=Status.COMPLETE,
                            state=self.state,
                            notes=tuple(notes + ["sealed at apex; no perturbations pending"]),
                        )
                    )
                    break
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.BLOCKED,
                        state=self.state,
                        notes=tuple(notes + ["held at apex, awaiting perturbation"]),
                    )
                )
                continue

            # 4. Run the plate under the cursor.
            plate = self.pipeline[self._cursor]
            self._cursor = (self._cursor + 1) % len(self.pipeline)

            result = plate.run(self.state)
            if result.ok:
                self.state = result.state_after

            record = plate.as_record(index, result)
            if notes:
                record.notes = tuple(notes) + record.notes
            trace.append(record)

            if result.status is Status.FAILED:
                break

            trip = self.engine.governor_trip(self.state)
            if trip:
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.FAILED,
                        state=self.state,
                        notes=(trip,),
                    )
                )
                break

        return trace

    def __repr__(self) -> str:
        return (
            f"<Runtime plates={len(self.pipeline)} "
            f"perturbations={len(self.perturbations)} state={self.state.band_id}>"
        )
