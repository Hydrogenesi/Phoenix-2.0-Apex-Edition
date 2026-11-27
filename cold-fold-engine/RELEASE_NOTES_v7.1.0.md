# cold-fold-engine v7.1.0

First public release of the Cold Fold engine. It's a deterministic, verifiable state machine written in pure Python, with no dependencies.

## Highlights
- **Plate pipeline.** Every stage is a plate with preconditions (`check`), a pure transition (`apply`), and postconditions (`verify`).
- **Three real outcomes.** `COMPLETE` (it ran and the postconditions hold), `BLOCKED` (upstream hasn't delivered yet, so the state is left untouched) and `FAILED` (the plate left an illegal state, which aborts the run).
- **Reproducible by test.** State is immutable, and every run produces a SHA-256 trace digest.
- **Computed stall.** The 127-node substrate is a Mersenne prime (2⁷−1), so every attempt at an even split leaves a residue. That residue is banked as tension. A default run stalls on pass 1 and seals at HA-8 Apex on pass 2.
- **Separate cycle modules:** `relativistic`, `collapse` and `demo`.
- **Tooling.** A command-line runner (`organism`, `runtime`, `cycle`), a Windows PowerShell launcher (`coldfold.ps1`), and an API reference in `docs/API.md`.

## Fixed since the prototype
- The three cycle functions shared one name, so only `demo` was reachable. Each now has its own module.
- `runner` imported a package that didn't exist. The CLI now starts.
- Plates were hardcoded to `COMPLETE` and could never fail. They now check real pre- and postconditions.
- An output path was hardcoded to one user's OneDrive folder. Output now goes to `--out`, which defaults to `./runs`.
- The PowerShell launcher referenced an API that didn't exist. `Runtime` and `DEFAULT_SCENARIO` are now supplied.
- `runner.py` couldn't import its own package when `PYTHONSAFEPATH` was set. It now can.

Full details are in [docs/HISTORY.md](docs/HISTORY.md).

## Verify it yourself
```bash
pip install -e ".[test]"
python -m pytest tests -q        # 41 passed
python -c "import cold_fold_engine as cf; print(cf.Runtime(perturbations=cf.DEFAULT_SCENARIO).run(120).digest())"
# 6b7c0a54ffdc7a7cc89f3363334e414aa97685a7fbdc6839c29c46acc8ff9d52
```
CI covers Python 3.9 to 3.13 on Linux and Windows.

## Scope
This package contains no physical model. `tension`, `band` and `echo` are dimensionless integer tokens that drive state transitions. The names `relativistic` and `collapse` describe the shape of a state machine, not physical processes.

## License
MIT
