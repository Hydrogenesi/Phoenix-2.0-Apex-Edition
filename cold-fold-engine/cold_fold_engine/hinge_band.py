"""Plate 3 -- HingeBand: open the next echo band on a folded state.

Requires a fold to hinge against, and refuses to run at the top echo band.
"""

from __future__ import annotations

from .plate import Plate
from .state import ECHO_BANDS, EngineState


class HingeBand(Plate):
    number = 3
    label = "HingeBand"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if not state.folded:
            unmet.append("no fold present to hinge against")
        if state.echo >= ECHO_BANDS[-1]:
            unmet.append(f"echo band saturated at {state.echo}")
        if state.sealed:
            unmet.append("state is sealed; hinge is fixed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        # Opening the hinge advances one echo band and lifts the state to at
        # least HA-3 (Frame) -- recursion boundaries exist once a hinge does.
        return state.evolve(
            echo=state.echo + 1,
            band=max(state.band, 3),
            folded=False,
        )

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if after.echo != before.echo + 1:
            unmet.append(f"echo must advance by exactly 1: {before.echo} -> {after.echo}")
        if after.band < 3:
            unmet.append(f"hinge must reach at least HA-3, got {after.band_id}")
        return tuple(unmet)
