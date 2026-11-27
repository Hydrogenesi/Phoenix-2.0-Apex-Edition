"""Plate 1 -- DivisionAttempt: try to partition the substrate evenly.

The substrate is 127 nodes (config.json). 127 is a Mersenne prime (2**7 - 1),
so it has no divisors other than 1 and itself. Every attempt to split it into
`echo + 1` equal groups therefore leaves a non-zero residue, and the attempt
stalls. That is arithmetic, not decree: the stall is computed, and you can
check it by hand.

The residue is added to `tension`, which is what later stages consume. This is
the mechanism that drives the pipeline forward across repeated passes.
"""

from __future__ import annotations

from .plate import Plate
from .state import ECHO_BANDS, EngineState


class DivisionAttempt(Plate):
    number = 1
    label = "Division"

    def check(self, state: EngineState) -> tuple[str, ...]:
        unmet: list[str] = []
        if state.band < 1:
            unmet.append("substrate not seeded; run Origin first")
        if state.stalled:
            unmet.append("a prior stall is unresolved; run StalledFold first")
        if state.sealed:
            unmet.append("state is sealed; no further division")
        if state.echo >= ECHO_BANDS[-1]:
            unmet.append(f"echo band already at maximum ({state.echo}); no further split target")
        return tuple(unmet)

    def apply(self, state: EngineState) -> EngineState:
        target = state.echo + 1
        residue = state.nodes % target
        if residue:
            # Even partition impossible: bank the residue as tension and stall.
            return state.evolve(tension=state.tension + residue, stalled=True)
        # Clean partition: no residue to bank, nothing stalls.
        return state.evolve(stalled=False)

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        target = before.echo + 1
        residue = before.nodes % target
        expected = before.tension + residue
        if after.tension != expected:
            return (f"tension bookkeeping wrong: expected {expected}, got {after.tension}",)
        if residue and not after.stalled:
            return (f"residue {residue} must raise a stall",)
        return ()

    def partition(self, state: EngineState) -> tuple[int, int, int]:
        """Return (target_groups, group_size, residue) without changing state."""
        target = state.echo + 1
        return target, state.nodes // target, state.nodes % target
