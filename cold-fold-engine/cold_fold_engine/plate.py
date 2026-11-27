"""Plate base class.

Replaces the original `PlateStub`, whose `run_to_completion()` returned a
hardcoded ``{"final_state": "COMPLETE"}``. That made every plate pass
unconditionally, so a run carried no information: a green result was
indistinguishable from a plate that had never executed.

A Plate here has three parts:

  * `check(state)`  -> tuple of unmet precondition descriptions. Non-empty
                       means the plate is BLOCKED and `apply` is not called.
  * `apply(state)`  -> a new EngineState. Must be pure: no mutation of the
                       input, no I/O, no clock, no randomness. This is what
                       keeps replay deterministic.
  * `verify(before, after)` -> tuple of postcondition violations. Non-empty
                       means FAILED: the plate ran but left illegal state.

The distinction matters operationally. BLOCKED means "not my turn yet --
upstream did not deliver what I need." FAILED means "I ran and produced
something invalid," which is a bug in the plate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .state import EngineState, Status, StepRecord


@dataclass
class PlateResult:
    """Outcome of one plate execution."""

    plate: int
    label: str
    status: Status
    state_before: EngineState
    state_after: EngineState
    reasons: tuple[str, ...] = ()
    history: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return self.status is Status.COMPLETE

    @property
    def final_state(self) -> str:
        """Backwards-compatible accessor.

        The original runner read ``result['final_state']`` as a status string.
        `PlateResult.final_state` returns that status; the actual engine state
        is `state_after`. The old name is kept so existing scripts keep working,
        but note it now reports real outcomes including BLOCKED and FAILED.
        """
        return self.status.value

    def to_dict(self) -> dict[str, Any]:
        return {
            "plate": self.plate,
            "label": self.label,
            "final_state": self.status.value,
            "reasons": list(self.reasons),
            "history": list(self.history),
            "state_before": self.state_before.to_dict(),
            "state_after": self.state_after.to_dict(),
        }


class Plate:
    """A single named stage in the pipeline.

    Subclasses set `number` and `label` and override `apply`. Override `check`
    to declare preconditions and `verify` to declare postconditions.
    """

    number: int = -1
    label: str = "unnamed"

    def check(self, state: EngineState) -> tuple[str, ...]:
        """Return descriptions of unmet preconditions. Empty tuple = runnable."""
        return ()

    def apply(self, state: EngineState) -> EngineState:
        """Pure transition. Must not mutate `state`."""
        raise NotImplementedError(
            f"Plate {self.number} ({self.label}) does not implement apply()"
        )

    def verify(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        """Return descriptions of violated postconditions. Empty tuple = valid."""
        return ()

    def narrate(self, before: EngineState, after: EngineState) -> tuple[str, ...]:
        """Human-readable summary of what changed. Derived, never authoritative."""
        lines: list[str] = []
        for key, old in before.to_dict().items():
            new = after.to_dict()[key]
            if old != new:
                lines.append(f"{key}: {old} -> {new}")
        if not lines:
            lines.append("no state change")
        return tuple(lines)

    def run(self, state: EngineState) -> PlateResult:
        """Execute the plate against `state`, returning a real outcome."""
        unmet = tuple(self.check(state))
        if unmet:
            return PlateResult(
                plate=self.number,
                label=self.label,
                status=Status.BLOCKED,
                state_before=state,
                state_after=state,
                reasons=unmet,
                history=(f"{self.label} blocked: {'; '.join(unmet)}",),
            )

        after = self.apply(state)

        violations = tuple(self.verify(state, after))
        if violations:
            return PlateResult(
                plate=self.number,
                label=self.label,
                status=Status.FAILED,
                state_before=state,
                state_after=state,
                reasons=violations,
                history=(f"{self.label} failed: {'; '.join(violations)}",),
            )

        return PlateResult(
            plate=self.number,
            label=self.label,
            status=Status.COMPLETE,
            state_before=state,
            state_after=after,
            reasons=(),
            history=self.narrate(state, after),
        )

    def run_to_completion(self, state: EngineState | None = None) -> PlateResult:
        """Compatibility alias for the original stub API.

        The original name is misleading -- a plate may legitimately end BLOCKED
        or FAILED -- but it is preserved so existing call sites keep working.
        """
        return self.run(state if state is not None else EngineState())

    def as_record(self, index: int, result: PlateResult) -> StepRecord:
        return StepRecord(
            index=index,
            source=f"plate:{self.number}:{self.label}",
            status=result.status,
            state=result.state_after,
            notes=result.history if result.ok else result.reasons,
        )

    def __repr__(self) -> str:
        return f"<Plate {self.number} {self.label}>"
