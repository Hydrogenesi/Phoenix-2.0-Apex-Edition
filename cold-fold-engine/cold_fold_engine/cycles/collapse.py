"""Tension-decay cycle, kept under the project's `collapse` label.

This models no physics -- in particular it has nothing to do with quantum
measurement, despite the original's "state=wavefunction-collapse" string. It
halves the integer `tension` accumulator each step until it reaches zero, a
deterministic geometric decay to a fixed point. Starting from a tension of T
it terminates in floor(log2(T)) + 2 steps.
"""

from __future__ import annotations

from ..state import EngineState
from .base import Cycle


class CollapseCycle(Cycle):
    name = "collapse"

    def step(self, state: EngineState, index: int) -> tuple[EngineState, str]:
        new = state.evolve(tension=state.tension // 2)
        return new, f"tension {state.tension} -> {new.tension}"

    def done(self, state: EngineState, index: int) -> bool:
        return state.tension == 0


_CYCLE = CollapseCycle()


def run(verbose: bool = False, delay: float = 0.3, max_steps: int = 10, state=None):
    """Module-level entry point, matching the original signature.

    Note the original default `delay=0.3` is preserved. A default start state
    has tension 0, so this cycle reports its fixed point immediately -- pass a
    state with non-zero tension to see it decay.
    """
    return _CYCLE.run(verbose=verbose, delay=delay, max_steps=max_steps, state=state)
