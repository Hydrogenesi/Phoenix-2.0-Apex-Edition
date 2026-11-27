"""Plate 4 -- VacuumDynamo: convert banked tension into echo bands.

Exchange rate is fixed at RATE tension units per echo band, integer division.
Blocks below one full band's worth, rather than reporting a no-op as success.

(The original runner listed a separate "Dynamo Engine" at plate 73. This is
that stage; see MANIFEST.md for the numbering map.)
"""

from __future__ import annotations

from .plate import Plate
from .state import ECHO_BANDS, EngineState


class VacuumDynamo(Plate):
    number = 4
    label = "VacuumDynamo"

    #: Tension units consumed per echo band gained.
    RATE: int = 2

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band < 3:
            unmet.append(f"dynamo needs at least HA-3, state is at {state.band_id}")
        if state.tension < self.RATE:
            unmet.append(
                f"insufficient tension: {state.tension} < {self.RATE} (one band)"
            )
        if state.echo >= ECHO_BANDS[-1]:
            unmet.append(f"echo band saturated at {state.echo}")
        if state.sealed:
            unmet.append("state is sealed; dynamo is offline")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        headroom = ECHO_BANDS[-1] - state.echo
        gain = min(state.tension // self.RATE, headroom)
        return state.evolve(
            echo=state.echo + gain,
            tension=state.tension - gain * self.RATE,
        )

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        gain = after.echo - before.echo
        spent = before.tension - after.tension
        unmet: list[str] = []
        if gain <= 0:
            unmet.append("dynamo ran without producing an echo band")
        if spent != gain * self.RATE:
            unmet.append(
                f"exchange rate violated: spent {spent} for {gain} band(s) "
                f"at rate {self.RATE}"
            )
        if after.tension < 0:
            unmet.append(f"tension went negative: {after.tension}")
        return tuple(unmet)
