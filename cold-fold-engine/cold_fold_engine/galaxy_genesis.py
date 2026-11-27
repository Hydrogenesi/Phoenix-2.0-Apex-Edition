"""Plate 72 -- GalaxyGenesis: second scale-up, unifying the bands.

Named for the plate slot the original runner labelled "Phoenix Engine".
No physical model is implemented here; this is a band transition.
"""

from __future__ import annotations

from .plate import Plate
from .state import EngineState


class GalaxyGenesis(Plate):
    number = 72
    label = "GalaxyGenesis"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band < 6:
            unmet.append(f"galaxy genesis needs HA-6, state is at {state.band_id}")
        if state.stalled:
            unmet.append("unresolved stall")
        if state.sealed:
            unmet.append("state is sealed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        # HA-7 (Crown): all bands unify.
        return state.evolve(band=max(state.band, 7))

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        if after.band < 7:
            return (f"galaxy genesis must reach HA-7, got {after.band_id}",)
        return ()
