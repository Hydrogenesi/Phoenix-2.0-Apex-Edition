"""Cycle registry.

One module per cycle, which is what the original `__init__.py` listing
described and what `runner.py` tried to import.
"""

from __future__ import annotations

from . import collapse, demo, relativistic
from .base import Cycle
from .collapse import CollapseCycle
from .demo import DemoCycle
from .relativistic import RelativisticCycle

#: Name -> module-level run() callable. The runner builds its CLI from this,
#: so adding a cycle module and one entry here is all a new cycle needs.
CYCLES = {
    "relativistic": relativistic.run,
    "collapse": collapse.run,
    "demo": demo.run,
}

__all__ = [
    "Cycle",
    "CollapseCycle",
    "DemoCycle",
    "RelativisticCycle",
    "CYCLES",
    "collapse",
    "demo",
    "relativistic",
]
