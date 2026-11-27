"""Plate 0 -- OriginNucleus: seeds the substrate.

Runs only from an unseeded state (band 0). Re-running it on a live state is
BLOCKED rather than silently re-seeding, so a second pass cannot wipe
accumulated progress.
"""

from __future__ import annotations

from .plate import Plate
from .state import SUBSTRATE_NODES, EngineState


class OriginNucleus(Plate):
    number = 0
    label = "Origin"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band != 0:
            unmet.append(f"already seeded (band={state.band_id}); origin runs only from HA-0")
        if state.sealed:
            unmet.append("state is sealed; cannot re-seed")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        return state.evolve(
            band=1,          # HA-0 Substrate -> HA-1 Spark
            echo=1,          # first echo band: point
            tension=0,
            nodes=SUBSTRATE_NODES,
            folded=False,
            stalled=False,
        )

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if after.band != 1:
            unmet.append(f"origin must leave band at HA-1, got {after.band_id}")
        if after.nodes != SUBSTRATE_NODES:
            unmet.append(f"substrate must be {SUBSTRATE_NODES} nodes, got {after.nodes}")
        return tuple(unmet)
