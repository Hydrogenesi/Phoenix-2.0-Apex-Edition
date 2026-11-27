# cold_fold_engine

[![tests](https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition/actions/workflows/cold-fold-engine.yml/badge.svg)](https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition/actions/workflows/cold-fold-engine.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
<!-- After the first Zenodo release, add the DOI badge here -->

A deterministic, verifiable state machine for the Cold Fold framework, written in pure Python with no dependencies.

Every stage of the pipeline is a *plate*. A plate declares three things: **preconditions** (`check`), a **pure transition** (`apply`), and **postconditions** (`verify`). Running a plate ends in one of three outcomes: `COMPLETE`, `BLOCKED`, or `FAILED`. State is immutable, and every run produces a SHA-256 trace digest. You can therefore check reproducibility with a test instead of taking it on trust.

## Statement of need

Staged simulation and workflow scripts often report success unconditionally. When that happens, a "green" run cannot be told apart from a run in which nothing happened. `cold_fold_engine` is built on the rule that **a stage that cannot fail cannot inform**:

- It separates expected waiting (`BLOCKED`, where upstream has not delivered yet) from defects (`FAILED`, where a stage produced illegal state).
- It makes determinism checkable: replaying the same run gives the same digest.
- It keeps every transition pure, so runs can be replayed, compared, and audited.

**Who it is for:** researchers and developers who build staged or iterated computational models and want each stage's outcome to be explicit and the whole run to be reproducible bit for bit. It is also the computational core of the Cold Fold framework.

## Scope

This package contains **no physical model**. `tension`, `band`, and `echo` are dimensionless integer tokens that drive state transitions. They are not energy, temperature, or any other physical quantity. Nothing in the package integrates an equation of motion. The module names `relativistic` and `collapse` describe the *shape* of a state machine (a cyclic sweep and a geometric decay). They do not describe physical processes.

## Installation

Python 3.9 or later is required. There are no runtime dependencies.

```bash
git clone https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition
cd Phoenix-2.0-Apex-Edition/cold-fold-engine
pip install -e ".[test]"        # pytest is needed only for the tests
python -m pytest tests -q       # expect: 41 passed
```

## Quick start

```bash
python runner.py organism                     # full plate pipeline; seals at HA-8
python runner.py runtime --max-steps 120      # stepped run with perturbations
python runner.py cycle --cycle collapse --tension 100 --verbose
```

```python
import cold_fold_engine as cf
trace = cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(120)
print(len(trace), trace.digest()[:16])        # digest: 6b7c0a54ffdc7a7c...
```

On Windows: `.\coldfold.ps1`

On iPhone/iPad (Pyto): open `cold_fold_pyto.py` and tap Run. It bundles the whole package in one file and ends with a digest self-check.

Full API reference: [docs/API.md](docs/API.md).

## What a run does

The substrate is 127 nodes. 127 is a Mersenne prime (2⁷−1), so it has no
divisors but 1 and itself — every attempt to split it into `echo + 1` equal
groups leaves a residue. That residue is banked as `tension`, and the stall is
*computed*, not declared. You can check it by hand.

Each pass walks the nine plates in dependency order. Pass 1 stalls, folds,
and opens one echo band, then blocks: the crest gate needs echo band 3
(`canonicalThreshold` in the project configuration) and only band 2 is available.
Pass 2 banks a second residue, the dynamo trades it for another band, the gate
opens, and the run seals at HA-8 Apex.

```
pass 1  plate  0 Origin         ok    HA-0 -> HA-1
        plate  1 Division       ok    tension 0 -> 1, stalled
        plate  2 StalledFold    ok    HA-1 -> HA-2, folded
        plate  3 HingeBand      ok    HA-2 -> HA-3, echo 1 -> 2
        plate  4 VacuumDynamo   wait  insufficient tension: 1 < 2
        plate  5 CrestGenesis   wait  echo band 2 below canonical threshold 3
        ... 71, 72, 74          wait
pass 2  plate  1 Division       ok    tension 1 -> 2, stalled
        plate  4 VacuumDynamo   ok    tension 2 -> 0, echo 3 -> 4
        plate  5 CrestGenesis   ok    HA-4 -> HA-5
        plate 74 MasterPlate    ok    HA-7 -> HA-8, sealed
```

Five of nine plates blocking on pass 1 is the point. In the original code
every plate reported `COMPLETE` unconditionally, so this information did not
exist.

## Design

**Immutable state.** `EngineState` is a frozen dataclass; plates return new
states via `evolve()`. A plate cannot corrupt shared state, which is what
makes replay and the trace digest meaningful.

**Three real outcomes.** `COMPLETE` / `BLOCKED` / `FAILED`. `BLOCKED` means
"upstream did not deliver what I need" and leaves state untouched; `FAILED`
means "I ran and produced illegal state" and aborts the run.

**Determinism.** There is no randomness, no clock, and no I/O in any
transition. `Trace.digest()` is a SHA-256 over the trace's canonical JSON, so
"deterministic" is machine-checkable rather than asserted:

```python
>>> import cold_fold_engine as cf
>>> cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(120).digest()[:16]
'6b7c0a54ffdc7a7c'
```

**The governor.** `CosmogenicEngine` (plate 75) halts the run when banked
tension exceeds `TENSION_CAP` (64). This is the only place the engine stops
itself, and it stops on a computed condition. `DEFAULT_SCENARIO` deliberately
drives it past the cap at step 95 so the trip path is exercised.

## Layout

```
cold_fold_framework/
├── cold_fold_engine/
│   ├── state.py              EngineState, Status, StepRecord, Trace, constants
│   ├── plate.py              Plate contract: check / apply / verify
│   ├── origin.py             plate 0   OriginNucleus
│   ├── division.py           plate 1   DivisionAttempt
│   ├── stalled_fold.py       plate 2   StalledFold
│   ├── hinge_band.py         plate 3   HingeBand
│   ├── vacuum_dynamo.py      plate 4   VacuumDynamo
│   ├── crest_genesis.py      plate 5   CrestGenesis
│   ├── star_genesis.py       plate 71  StarGenesis
│   ├── galaxy_genesis.py     plate 72  GalaxyGenesis
│   ├── master_plate.py       plate 74  MasterPlate
│   ├── cosmogenic_engine.py  plate 75  orchestrator + governor
│   ├── runtime.py            Runtime, Perturbation, DEFAULT_SCENARIO
│   └── cycles/               one module per cycle
├── tests/                    41 tests
├── runner.py                 CLI
├── coldfold.ps1              PowerShell launcher
├── docs/                     API reference and development history
└── paper/                    JOSS paper
```

## Compatibility with the original call sites

| Original | Status |
|---|---|
| `ColdFoldV7(bus=None)` | works — alias for `CosmogenicEngine`; `bus` accepted and ignored |
| `plate.run_to_completion()` | works — but now returns real outcomes, not always `COMPLETE` |
| `result['final_state']`, `result['history']` | both keys present |
| `cf.Runtime(perturbations=cf.DEFAULT_SCENARIO)` | works |
| `rt.run(120)`, `len(tr)` | works — `len` ≤ budget, since a run may halt early |
| `from engine.cycles import relativistic, collapse, demo` | now `from cold_fold_engine.cycles import ...` |

## Extending it

Add a plate:

```python
from cold_fold_engine import Plate

class MyPlate(Plate):
    number, label = 42, "MyPlate"

    def check(self, state):
        return () if state.canonized else ("needs a canonical echo band",)

    def apply(self, state):                 # must be pure
        return state.evolve(band=state.band + 1)

    def verify(self, before, after):
        return () if after.band > before.band else ("no progress",)
```

Then insert it into `default_pipeline()` at the right dependency position.

Add a cycle: drop a module in `cycles/` subclassing `Cycle`, and add one entry
to `CYCLES` in `cycles/__init__.py`.


## Getting help and contributing

Bug reports, questions, and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Citation

If you use this software, please cite it. GitHub shows the citation details from [CITATION.cff](CITATION.cff) under "Cite this repository".

## License

MIT. See [LICENSE](LICENSE).
