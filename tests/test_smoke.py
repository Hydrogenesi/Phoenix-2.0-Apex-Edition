"""Every Python module imports, and every runnable demo runs without crashing."""
import importlib
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    "phoenix_ignition",
    "third_pillar_operators",
    "ng_laws_enforcement",
    "nip_protocol",
    "integration_engine",
    "third_pillar_integration",
    "src.au.ops.curvature_residue",
    "src.au.ops.agn_replication",
    "src.au.ops.q_desic",
    "equation_of_state",
    "energy_generation",
    "radiative_transfer",
    "hydrostatic_equilibrium",
    "boundary_conditions",
    "stellar_evolution_refactor",
]

SCRIPTS = [
    "phoenix_ignition.py",
    "operators/third_pillar_operators.py",
    "operators/ng_laws_enforcement.py",
    "operators/nip_protocol.py",
    "code/integration/third_pillar_integration.py",
    "stellar_structure/main.py",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)


@pytest.mark.parametrize("script", SCRIPTS)
def test_script_runs(script, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", [script])          # don't hand pytest's flags to argparse
    try:
        runpy.run_path(str(ROOT / script), run_name="__main__")
    except SystemExit as exc:                          # some demos end with exit(0)
        assert exc.code in (0, None), f"{script} exited with code {exc.code}"
    assert capsys.readouterr().out                     # every demo prints something
