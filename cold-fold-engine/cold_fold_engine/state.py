"""Core state model for the Cold Fold engine.

SCOPE NOTE
----------
Every quantity in this module is a dimensionless bookkeeping token. `tension`,
`band`, and `echo` are integers used to drive a finite-state machine. They are
NOT physical quantities: they carry no units, obey no conservation law, and
must not be read as energy, temperature, pressure, or reactivity. The engine
is a deterministic scaffold for organising a pipeline of named stages. Any
physical model must be added deliberately, with real units and real equations.

Constants below are read from the project's own configuration:
  - SUBSTRATE_NODES = 127        (config.json -> substrate.nodes; 2**7 - 1)
  - ECHO_BANDS      = 1..9       (config.json -> echoes)
  - CANON_THRESHOLD = 3          (config.json -> canonicalThreshold)
  - OCTAVE_LADDER   = HA-0..HA-8 (fractal-engine.js)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any

SUBSTRATE_NODES: int = 127
ECHO_BANDS: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
CANON_THRESHOLD: int = 3

OCTAVE_LADDER: tuple[tuple[str, str], ...] = (
    ("HA-0", "Substrate"),
    ("HA-1", "Spark"),
    ("HA-2", "Vector"),
    ("HA-3", "Frame"),
    ("HA-4", "Harmonic"),
    ("HA-5", "Operator"),
    ("HA-6", "Engine"),
    ("HA-7", "Crown"),
    ("HA-8", "Apex"),
)

MAX_BAND: int = len(OCTAVE_LADDER) - 1

ECHO_SHAPES: dict[int, str] = {
    1: "point",
    2: "line",
    3: "triangle",
    4: "quad",
    5: "penta",
    6: "hex",
    7: "hepta",
    8: "octa",
    9: "nona",
}


class Status(str, Enum):
    """Terminal status of a plate or cycle step.

    A stage that cannot fail cannot inform. BLOCKED and FAILED are real,
    reachable outcomes -- see `Plate.check`.
    """

    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class EngineError(Exception):
    """Raised on a structural misuse of the engine (not a modelled failure)."""


@dataclass(frozen=True)
class EngineState:
    """Immutable engine state.

    Frozen so that stages cannot mutate shared state by accident; every stage
    returns a new state via `EngineState.evolve`. This is what makes replay and
    the determinism digest meaningful.
    """

    tension: int = 0
    band: int = 0
    echo: int = 1
    nodes: int = SUBSTRATE_NODES
    folded: bool = False
    stalled: bool = False
    sealed: bool = False

    def __post_init__(self) -> None:
        if not 0 <= self.band <= MAX_BAND:
            raise EngineError(f"band {self.band} outside 0..{MAX_BAND}")
        if self.echo not in ECHO_BANDS:
            raise EngineError(f"echo {self.echo} not in {ECHO_BANDS}")
        if self.nodes < 0:
            raise EngineError(f"nodes must be non-negative, got {self.nodes}")

    @property
    def canonized(self) -> bool:
        """True once the echo band reaches the configured canonical threshold."""
        return self.echo >= CANON_THRESHOLD

    @property
    def band_id(self) -> str:
        return OCTAVE_LADDER[self.band][0]

    @property
    def band_name(self) -> str:
        return OCTAVE_LADDER[self.band][1]

    @property
    def echo_shape(self) -> str:
        return ECHO_SHAPES[self.echo]

    @property
    def at_apex(self) -> bool:
        return self.band == MAX_BAND

    def evolve(self, **changes: Any) -> EngineState:
        """Return a new state with `changes` applied, clamped to legal ranges."""
        if "band" in changes:
            changes["band"] = max(0, min(MAX_BAND, int(changes["band"])))
        if "echo" in changes:
            changes["echo"] = max(ECHO_BANDS[0], min(ECHO_BANDS[-1], int(changes["echo"])))
        return replace(self, **changes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tension": self.tension,
            "band": self.band,
            "band_id": self.band_id,
            "band_name": self.band_name,
            "echo": self.echo,
            "echo_shape": self.echo_shape,
            "nodes": self.nodes,
            "canonized": self.canonized,
            "folded": self.folded,
            "stalled": self.stalled,
            "sealed": self.sealed,
        }


@dataclass
class StepRecord:
    """One recorded transition."""

    index: int
    source: str
    status: Status
    state: EngineState
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "source": self.source,
            "status": self.status.value,
            "state": self.state.to_dict(),
            "notes": list(self.notes),
        }


@dataclass
class Trace:
    """An ordered list of StepRecords, plus a content digest.

    `len(trace)` is the number of recorded steps, so the launcher idiom
    `print('steps', len(tr))` works as written in coldfold.ps1.
    """

    records: list[StepRecord] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, i):
        return self.records[i]

    def append(self, record: StepRecord) -> None:
        self.records.append(record)

    @property
    def final_state(self) -> EngineState | None:
        return self.records[-1].state if self.records else None

    def statuses(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for r in self.records:
            counts[r.status.value] = counts.get(r.status.value, 0) + 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {"records": [r.to_dict() for r in self.records]}

    def digest(self) -> str:
        """SHA-256 over the canonical JSON form of the trace.

        Two runs of the same scenario must produce the same digest. This is the
        machine-checkable definition of "deterministic" used by the test suite.
        """
        blob = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()
