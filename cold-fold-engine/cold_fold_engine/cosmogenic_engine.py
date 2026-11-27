"""Plate 75 -- CosmogenicEngine: the Cold Fold governor.

This is the orchestrator the original code called the "Shadow Governor". It
does two jobs:

  1. Runs the plate pipeline in dependency order (not numeric order) and
     records a real outcome for every plate.
  2. Acts as a governor: if banked tension exceeds TENSION_CAP the run is
     halted and the trip is logged. This is the only place the engine stops
     itself, and it stops on a computed condition, not a decree.

A BLOCKED plate does not abort the pass -- the pass continues so the operator
sees every gate that did not open. A FAILED plate does abort, because failure
means a plate produced illegal state and continuing would compound it.
"""

from __future__ import annotations

from typing import Any

from .crest_genesis import CrestGenesis
from .division import DivisionAttempt
from .galaxy_genesis import GalaxyGenesis
from .hinge_band import HingeBand
from .master_plate import MasterPlate
from .origin import OriginNucleus
from .plate import Plate, PlateResult
from .stalled_fold import StalledFold
from .star_genesis import StarGenesis
from .state import EngineState, Status, StepRecord, Trace
from .vacuum_dynamo import VacuumDynamo


def default_pipeline() -> tuple[Plate, ...]:
    """Plates in dependency order.

    Note this is NOT ascending plate number: VacuumDynamo (4) must run after
    HingeBand (3) but before CrestGenesis (5), and the 71/72/74 engine-set
    plates run last. Execution order is set by data dependency.
    """
    return (
        OriginNucleus(),
        DivisionAttempt(),
        StalledFold(),
        HingeBand(),
        VacuumDynamo(),
        CrestGenesis(),
        StarGenesis(),
        GalaxyGenesis(),
        MasterPlate(),
    )


class CosmogenicEngine:
    """Ordered pipeline runner with a tension governor."""

    number = 75
    label = "ColdFoldGovernor"

    #: Banked tension above this value trips the governor and halts the run.
    TENSION_CAP: int = 64

    def __init__(
        self,
        pipeline: tuple[Plate, ...] | None = None,
        tension_cap: int | None = None,
        bus: Any = None,
    ) -> None:
        # `bus` is accepted and ignored: the original call site was
        # ColdFoldV7(bus=None). Kept so that signature keeps working.
        self.pipeline = pipeline if pipeline is not None else default_pipeline()
        self.tension_cap = self.TENSION_CAP if tension_cap is None else tension_cap
        self.bus = bus

    # -- governor -----------------------------------------------------------

    def governor_trip(self, state: EngineState) -> str | None:
        """Return a trip reason if the state violates a governor bound."""
        if state.tension > self.tension_cap:
            return (
                f"tension {state.tension} exceeds cap {self.tension_cap}; "
                "run halted by Cold Fold governor"
            )
        return None

    # -- one pass -----------------------------------------------------------

    def pass_once(
        self, state: EngineState
    ) -> tuple[EngineState, list[PlateResult], str | None]:
        """Run every plate once, in order. Returns (state, results, halt_reason)."""
        results: list[PlateResult] = []
        for plate in self.pipeline:
            result = plate.run(state)
            results.append(result)

            if result.status is Status.FAILED:
                return state, results, (
                    f"plate {plate.number} ({plate.label}) FAILED: "
                    f"{'; '.join(result.reasons)}"
                )

            if result.ok:
                state = result.state_after
                trip = self.governor_trip(state)
                if trip:
                    return state, results, trip

        return state, results, None

    # -- full run -----------------------------------------------------------

    def run(self, max_passes: int = 8, state: EngineState | None = None) -> Trace:
        """Run passes until the state seals, stops advancing, or halts.

        Returns a Trace with one record per plate execution. Halts when:
          * the state is sealed (success),
          * a pass produces no state change (fixed point -- further passes
            would be identical, so continuing would only pad the trace),
          * the governor trips, or
          * a plate FAILS.
        """
        state = EngineState() if state is None else state
        trace = Trace()
        index = 0

        for _ in range(max_passes):
            before = state
            state, results, halt = self.pass_once(state)

            for result in results:
                plate = next(p for p in self.pipeline if p.number == result.plate)
                trace.append(plate.as_record(index, result))
                index += 1

            if halt:
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.FAILED,
                        state=state,
                        notes=(halt,),
                    )
                )
                break

            if state.sealed:
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.COMPLETE,
                        state=state,
                        notes=("sealed at apex",),
                    )
                )
                break

            if state == before:
                trace.append(
                    StepRecord(
                        index=index,
                        source="governor:75",
                        status=Status.BLOCKED,
                        state=state,
                        notes=("fixed point: pass produced no state change",),
                    )
                )
                break

        return trace

    # -- compatibility ------------------------------------------------------

    def run_to_completion(self, state: EngineState | None = None) -> dict[str, Any]:
        """Dict-returning form matching the original stub API.

        The original runner read ``result['final_state']`` and
        ``result['history']``. Both keys are present. Unlike the stub,
        `final_state` reports the real outcome and can be BLOCKED or FAILED.
        """
        trace = self.run(state=state)
        final = trace.final_state
        if final is None:
            status = Status.BLOCKED.value
        elif final.sealed:
            status = Status.COMPLETE.value
        else:
            status = trace.records[-1].status.value

        history = [
            f"[{r.source}] {r.status.value}: {'; '.join(r.notes) or 'no notes'}"
            for r in trace.records
        ]
        return {
            "plate": self.number,
            "final_state": status,
            "history": history,
            "digest": trace.digest(),
            "state": final.to_dict() if final else None,
            "statuses": trace.statuses(),
        }

    def __repr__(self) -> str:
        return (
            f"<CosmogenicEngine plates={len(self.pipeline)} "
            f"tension_cap={self.tension_cap}>"
        )
