"""Plate 5 -- CrestGenesis: form the crest once the echo band is canonical.

This is the pipeline's real gate. `canonicalThreshold` is 3 in config.json, so
the crest cannot form below echo band 3. Below it, this plate BLOCKS -- which
is why a single pass over the pipeline does not reach the apex.
"""

from __future__ import annotations

from .plate import Plate
from .state import CANON_THRESHOLD, EngineState


class CrestGenesis(Plate):
    number = 5
    label = "CrestGenesis"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if not state.canonized:
            unmet.append(
                f"echo band {state.echo} below canonical threshold {CANON_THRESHOLD}"
            )
        if state.band < 3:
            unmet.append(f"crest needs at least HA-3, state is at {state.band_id}")
        if state.stalled:
            unmet.append("unresolved stall; crest cannot form over a stall")
        if state.sealed:
            unmet.append("state is sealed; crest already fixed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        # Crest formation lifts the state to HA-5 (Operator).
        return state.evolve(band=max(state.band, 5))

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        if after.band < 5:
            return (f"crest must reach at least HA-5, got {after.band_id}",)
        if not after.canonized:
            return ("crest formed on a non-canonical echo band",)
        return ()
