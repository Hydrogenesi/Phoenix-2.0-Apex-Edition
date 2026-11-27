"""Plate 71 -- StarGenesis: first scale-up above the crest.

Named for the plate slot the original runner labelled "Einstein Engine".
No physical model is implemented here; this is a band transition.
"""

from __future__ import annotations

from .plate import Plate
from .state import EngineState


class StarGenesis(Plate):
    number = 71
    label = "StarGenesis"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band < 5:
            unmet.append(f"star genesis needs HA-5 crest, state is at {state.band_id}")
        if not state.canonized:
            unmet.append(f"echo band {state.echo} is not canonical")
        if state.stalled:
            unmet.append("unresolved stall")
        if state.sealed:
            unmet.append("state is sealed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        # HA-6 (Engine): fractal traversal becomes available.
        return state.evolve(band=max(state.band, 6))

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        if after.band < 6:
            return (f"star genesis must reach HA-6, got {after.band_id}",)
        return ()
