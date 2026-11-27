# Repair manifest

What was wrong in the original prototype files, and what replaced it. Every entry is a
defect that would stop the code running or make its output misleading.

## 1. `cycles.txt` — three functions, one name

```python
def run(verbose=False, delay=0.0, max_steps=10):   # relativistic
def run(verbose=False, delay=0.3, max_steps=10):   # collapse
def run(verbose=False, delay=0.0, max_steps=2):    # demo
```

All three bound the same module-level name `run`. Python rebinds on each
`def`, so the first two were discarded when the module finished loading and
only the demo was reachable. Nothing raised an error; the two cycles were
simply gone.

Separately, none of the three carried state between iterations — each printed
a fixed string, so `max_steps` controlled only the number of lines and the
`delay` parameter was accepted but never used.

**Replaced by** `cold_fold_engine/cycles/{base,relativistic,collapse,demo}.py`
— one module per cycle, as the `__init__.py` listing intended. Each is an
iterated map over `EngineState` with a defined fixed point. `delay` now sleeps
but is excluded from the state transition, so it cannot affect results.
Regression test: `tests/test_cycles.py::test_cycles_are_distinct_callables`.

## 2. `runner.txt` — imported modules that did not exist

```python
from engine.cycles import relativistic, collapse, demo
```

There was no `engine` package and no such submodules (see defect 1). This
import failed at load, so the CLI could not start.

**Replaced by** `runner.py`, which builds its CLI from the `CYCLES` registry.

## 3. `import datetime.py` — plates that could not fail

```python
def run_to_completion(self):
    return {"plate": self.plate_number, "final_state": "COMPLETE", ...}
```

`PlateStub` returned a hardcoded `COMPLETE`. Plates 0–5 and 71–74 therefore
passed unconditionally, and a green run was indistinguishable from a run where
nothing happened. A stage that cannot fail cannot inform.

**Replaced by** `plate.py`, where a `Plate` has `check` (preconditions),
`apply` (a pure transition), and `verify` (postconditions), yielding three
real outcomes:

| Status | Meaning |
|---|---|
| `COMPLETE` | ran, postconditions hold |
| `BLOCKED` | preconditions unmet — upstream did not deliver; state untouched |
| `FAILED` | ran but left illegal state — a bug in the plate |

The distinction is load-bearing: `BLOCKED` is expected traffic, `FAILED` aborts
the run. In a default run, five of nine plates legitimately block on pass 1.

## 4. `import datetime.py` — hardcoded single-machine path

```python
LANE = Path(r"C:\Users\<user>\OneDrive\<folder>")
```

An absolute path into one user's OneDrive. The script raised on any other
machine, and on that machine it wrote into a syncing folder.

**Replaced by** a `--out` argument defaulting to `./runs`.

## 5. `coldfold.ps1` — launcher for a module that was never supplied

```powershell
& $python -c "import cold_fold_engine as cf; rt = cf.Runtime(perturbations=cf.DEFAULT_SCENARIO); ..."
```

Neither `Runtime` nor `DEFAULT_SCENARIO` existed anywhere in the attached
files, and the `$engine` path pointed at a directory name that looks like a
mangled paste . The launcher could not work.

**Replaced by** `runtime.py` supplying that exact API, and `coldfold.ps1`
resolving its own location instead of hardcoding one.

## 6. `Framework.py` — a file listing saved as Python

The file contained ten bare filenames. As Python it is a syntax error; as a
manifest it described modules that did not exist, while the package
`__init__.py` tried to import a class from each.

**Replaced by** the ten actual modules, and this document.

## 7. `PYTHONSAFEPATH` fragility

Under `PYTHONSAFEPATH=1` (or `python -P`), Python does not prepend a script's
own directory to `sys.path`, so `runner.py` could not import its own package.
This environment sets that variable. `runner.py` now inserts its directory
explicitly.

---

## Plate numbering

The attached files used two different naming schemes — `Framework.py` listed
ten class names, while `import datetime.py` used numbered plates with
different labels. Both are preserved:

| # | Class | Original label | Role |
|---|---|---|---|
| 0 | `OriginNucleus` | Origin | seed the 127-node substrate |
| 1 | `DivisionAttempt` | Topology | attempt an even partition; bank the residue |
| 2 | `StalledFold` | Condition | absorb a stall into a fold |
| 3 | `HingeBand` | Identity | open the next echo band |
| 4 | `VacuumDynamo` | Symmetry / "Dynamo Engine" (73) | trade tension for echo bands |
| 5 | `CrestGenesis` | Seal | form the crest once the echo band is canonical |
| 71 | `StarGenesis` | Einstein Engine | HA-5 → HA-6 |
| 72 | `GalaxyGenesis` | Phoenix Engine | HA-6 → HA-7 |
| 74 | `MasterPlate` | System Governor | seal at HA-8 |
| 75 | `CosmogenicEngine` | Cold Fold Shadow Governor | orchestrator + tension cap |

Execution order follows data dependency, not plate number: `VacuumDynamo` (4)
must run after `HingeBand` (3) but before `CrestGenesis` (5). See
`default_pipeline()`.

Plate 73 is not a separate stage — the "Dynamo Engine" of the original runner
is `VacuumDynamo` at slot 4.

## Values inherited from your own config

Rather than inventing constants, the engine reads what your files already
declared:

| Constant | Value | Source |
|---|---|---|
| `SUBSTRATE_NODES` | 127 | `config.json` → `substrate.nodes` |
| `ECHO_BANDS` | 1–9 | `config.json` → `echoes` |
| `CANON_THRESHOLD` | 3 | `config.json` → `canonicalThreshold` |
| `OCTAVE_LADDER` | HA-0 … HA-8 | `fractal-engine.js` → `OCTAVE_LADDER` |
| echo shapes | point … nona | `fractal-engine.js` → `ECHO_LADDER` |

`tests/test_state.py::test_config_constants_match_project_config` fails if
these drift out of sync with the JS/JSON side.
