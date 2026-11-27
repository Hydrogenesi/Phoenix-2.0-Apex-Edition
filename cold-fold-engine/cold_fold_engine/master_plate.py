"""Plate 74 -- MasterPlate: seal the run at the apex.

Named for the plate slot the original runner labelled "System Governor".
Sealing is terminal: every other plate refuses to run on a sealed state, so
the seal cannot be silently undone by a later pass. Only an explicit
perturbation (see runtime.py) can reopen it.
"""

from __future__ import annotations

from .plate import Plate
from .state import MAX_BAND, EngineState


class MasterPlate(Plate):
    number = 74
    label = "MasterPlate"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band < 7:
            unmet.append(f"seal needs HA-7 crown, state is at {state.band_id}")
        if state.stalled:
            unmet.append("cannot seal over an unresolved stall")
        if not state.canonized:
            unmet.append(f"cannot seal a non-canonical echo band ({state.echo})")
        if state.sealed:
            unmet.append("already sealed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        return state.evolve(band=MAX_BAND, sealed=True)

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if not after.at_apex:
            unmet.append(f"seal must land at HA-{MAX_BAND}, got {after.band_id}")
        if not after.sealed:
            unmet.append("seal flag not set")
        return tuple(unmet)
