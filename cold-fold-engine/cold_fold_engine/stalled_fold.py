"""Plate 2 -- StalledFold: absorb an unresolved stall into a fold.

Blocks when there is no stall to absorb. That is the honest outcome: this
plate has nothing to do on a clean state, and reporting COMPLETE would be a
false green.
"""

from __future__ import annotations

from .plate import Plate
from .state import EngineState


class StalledFold(Plate):
    number = 2
    label = "StalledFold"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if not state.stalled:
            unmet.append("no active stall to fold")
        if state.sealed:
            unmet.append("state is sealed; folds are closed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        # The stall is converted into a fold and the band advances by one rung.
        # Tension is retained -- it is the residue the dynamo will later consume.
        return state.evolve(stalled=False, folded=True, band=state.band + 1)

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if after.stalled:
            unmet.append("stall survived the fold")
        if not after.folded:
            unmet.append("fold flag not set")
        if after.tension != before.tension:
            unmet.append(
                f"fold must conserve tension: {before.tension} -> {after.tension}"
            )
        return tuple(unmet)
