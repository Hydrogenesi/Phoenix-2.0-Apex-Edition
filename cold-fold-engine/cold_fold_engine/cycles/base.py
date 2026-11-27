"""Cycle base class.

WHAT WAS BROKEN
---------------
The original `cycles.txt` defined `run()` three times in a single file:

    def run(verbose=False, delay=0.0, max_steps=10):   # relativistic
    def run(verbose=False, delay=0.3, max_steps=10):   # collapse
    def run(verbose=False, delay=0.0, max_steps=2):    # demo

In Python, each `def` rebinds the same module-level name, so the first two
were discarded the moment the file finished loading. Only the last one -- the
demo -- was reachable. Meanwhile `runner.py` imported three separate
submodules (`from engine.cycles import relativistic, collapse, demo`) that did
not exist. Splitting them into one module per cycle, as the `__init__.py`
listing intended, fixes both halves of that.

Each cycle also advances real state now. The originals only printed a
formatted string and carried nothing between iterations, so `max_steps` had no
effect beyond the line count.

NAMING
------
The cycle names are the project's own labels, kept so existing scripts keep
importing. They describe state-machine shapes, not physical processes: no
cycle in this package models relativity, wavefunction dynamics, or any other
physics. Printed output says what the state machine did.
"""

from __future__ import annotations

import time

from ..state import EngineState, Status, StepRecord, Trace


class Cycle:
    """A deterministic iterated map over EngineState."""

    name: str = "unnamed"

    def step(self, state: EngineState, index: int) -> tuple[EngineState, str]:
        """Advance one step. Pure: no I/O, no clock, no randomness."""
        raise NotImplementedError

    def done(self, state: EngineState, index: int) -> bool:
        """Return True when the cycle has reached its fixed point."""
        return False

    def run(
        self,
        verbose: bool = False,
        delay: float = 0.0,
        max_steps: int = 10,
        state: EngineState | None = None,
    ) -> Trace:
        """Iterate up to `max_steps` times, returning a Trace.

        `delay` inserts a sleep between steps for readability only. It does not
        enter the state transition, so it cannot change the result or the
        trace digest.
        """
        if max_steps < 0:
            raise ValueError(f"max_steps must be non-negative, got {max_steps}")

        state = EngineState() if state is None else state
        trace = Trace()

        for index in range(max_steps):
            if self.done(state, index):
                trace.append(
                    StepRecord(
                        index=index,
                        source=f"cycle:{self.name}",
                        status=Status.COMPLETE,
                        state=state,
                        notes=("fixed point reached",),
                    )
                )
                break

            state, note = self.step(state, index)
            trace.append(
                StepRecord(
                    index=index,
                    source=f"cycle:{self.name}",
                    status=Status.COMPLETE,
                    state=state,
                    notes=(note,),
                )
            )

            if verbose:
                print(f"[{self.name}] step={index} {note}")
            if delay:
                time.sleep(delay)

        return trace

    def __repr__(self) -> str:
        return f"<Cycle {self.name}>"
