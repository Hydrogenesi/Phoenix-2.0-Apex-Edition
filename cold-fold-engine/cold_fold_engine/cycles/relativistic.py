"""Band-sweep cycle, kept under the project's `relativistic` label.

This models no physics. It sweeps the octave ladder HA-0..HA-8 one rung per
step and wraps at the top -- a cyclic walk over nine states. The original
version printed "state=E=mc^2-frame", which named a physical relation the code
did not compute; the output now reports the band the machine is actually in.
"""

from __future__ import annotations

from ..state import MAX_BAND, EngineState
from .base import Cycle


class RelativisticCycle(Cycle):
    name = "relativistic"

    def step(self, state: EngineState, index: int) -> tuple[EngineState, str]:
        nxt = 0 if state.band >= MAX_BAND else state.band + 1
        new = state.evolve(band=nxt)
        return new, f"band {state.band_id}({state.band_name}) -> {new.band_id}({new.band_name})"


_CYCLE = RelativisticCycle()


def run(verbose: bool = False, delay: float = 0.0, max_steps: int = 10, state=None):
    """Module-level entry point, matching the original signature."""
    return _CYCLE.run(verbose=verbose, delay=delay, max_steps=max_steps, state=state)
