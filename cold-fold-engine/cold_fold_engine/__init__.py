"""cold_fold_engine -- deterministic staged state machine.

This package supplies the ten classes the original `__init__.py` imported and
the `Runtime` / `DEFAULT_SCENARIO` pair that `coldfold.ps1` calls. None of the
implementations existed in the original prototype files.

SCOPE
-----
This is a scaffold, not a physical model. `tension`, `band`, and `echo` are
dimensionless integer tokens driving state transitions; they are not energy,
temperature, pressure, curvature, or reactivity, and no module here integrates
an equation of motion. See state.py and MANIFEST.md.
"""

from __future__ import annotations

from .cosmogenic_engine import CosmogenicEngine, default_pipeline
from .crest_genesis import CrestGenesis
from .cycles import CYCLES
from .division import DivisionAttempt
from .galaxy_genesis import GalaxyGenesis
from .hinge_band import HingeBand
from .master_plate import MasterPlate
from .origin import OriginNucleus
from .plate import Plate, PlateResult
from .runtime import DEFAULT_SCENARIO, Perturbation, Runtime
from .stalled_fold import StalledFold
from .star_genesis import StarGenesis
from .state import (
    CANON_THRESHOLD,
    ECHO_BANDS,
    MAX_BAND,
    OCTAVE_LADDER,
    SUBSTRATE_NODES,
    EngineError,
    EngineState,
    Status,
    StepRecord,
    Trace,
)
from .vacuum_dynamo import VacuumDynamo

__version__ = "7.1.0"

#: Alias for the name the original runner imported (`ColdFoldV7`).
ColdFoldV7 = CosmogenicEngine

__all__ = [
    # the ten stages listed in the original Framework.py
    "OriginNucleus",
    "DivisionAttempt",
    "StalledFold",
    "HingeBand",
    "VacuumDynamo",
    "CrestGenesis",
    "StarGenesis",
    "GalaxyGenesis",
    "MasterPlate",
    "CosmogenicEngine",
    # runtime surface
    "Runtime",
    "Perturbation",
    "DEFAULT_SCENARIO",
    "ColdFoldV7",
    "default_pipeline",
    # core model
    "Plate",
    "PlateResult",
    "EngineState",
    "EngineError",
    "Status",
    "StepRecord",
    "Trace",
    "CYCLES",
    # configuration constants
    "SUBSTRATE_NODES",
    "ECHO_BANDS",
    "CANON_THRESHOLD",
    "OCTAVE_LADDER",
    "MAX_BAND",
    "__version__",
]
