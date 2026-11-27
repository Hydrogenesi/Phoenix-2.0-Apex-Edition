"""Smallest working cycle: advances the echo band, two steps by default."""

from __future__ import annotations

from ..state import ECHO_BANDS, EngineState
from .base import Cycle


class DemoCycle(Cycle):
    name = "demo"

    def step(self, state: EngineState, index: int) -> tuple[EngineState, str]:
        new = state.evolve(echo=state.echo + 1)
        return new, (
            f"echo {state.echo}({state.echo_shape}) -> "
            f"{new.echo}({new.echo_shape}), canonized={new.canonized}"
        )

    def done(self, state: EngineState, index: int) -> bool:
        return state.echo >= ECHO_BANDS[-1]


_CYCLE = DemoCycle()


def run(verbose: bool = False, delay: float = 0.0, max_steps: int = 2, state=None):
    """Module-level entry point, matching the original signature."""
    return _CYCLE.run(verbose=verbose, delay=delay, max_steps=max_steps, state=state)
