"""Cold Fold CLI.

Replaces both `runner.txt` (cycle CLI) and `import datetime.py` (organism
runner). Fixes carried over from those files:

  * `runner.txt` imported `engine.cycles.{relativistic,collapse,demo}`, which
    did not exist -- all three lived as shadowed defs in one file.
  * `import datetime.py` wrote to a hardcoded absolute path that
    only exists on one machine, and crashed on any other. The output
    directory is now a `--out` argument defaulting to `./runs`.
  * That runner also reported every plate as COMPLETE unconditionally, because
    `PlateStub.run_to_completion()` returned a literal. It now reports real
    per-plate outcomes and exits non-zero if anything failed.

Usage:
    python runner.py cycle --cycle demo --verbose --max-steps 5
    python runner.py organism --out ./runs
    python runner.py runtime --max-steps 120
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

# Put this script's directory on sys.path explicitly. Python normally does this
# for you, but not under PYTHONSAFEPATH=1 / `python -P`, which some managed
# environments set. Without this the script cannot import its own package.
_HERE = str(Path(__file__).resolve().parent)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from cold_fold_engine import (
    DEFAULT_SCENARIO,
    CosmogenicEngine,
    EngineState,
    Runtime,
    Status,
    __version__,
)
from cold_fold_engine.cycles import CYCLES


def log(msg: str) -> None:
    print(f"[cold-fold v{__version__}] {msg}")


def artifact_name(prefix: str = "000-075") -> str:
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    return f"{prefix}_{stamp}_Cosmogenic_Run"


def write_artifact(out_dir: Path, lines: list[str], payload: dict) -> tuple[Path, Path]:
    """Write the human-readable log and the machine-readable trace."""
    out_dir.mkdir(parents=True, exist_ok=True)
    name = artifact_name()
    txt = out_dir / f"{name}.txt"
    js = out_dir / f"{name}.json"
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    js.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    log(f"wrote {txt}")
    log(f"wrote {js}")
    return txt, js


# -- subcommands -----------------------------------------------------------


def cmd_cycle(args: argparse.Namespace) -> int:
    if args.cycle not in CYCLES:
        raise SystemExit(
            f"Unknown cycle: {args.cycle!r}. Available: {', '.join(sorted(CYCLES))}"
        )
    state = EngineState(tension=args.tension) if args.tension else None
    trace = CYCLES[args.cycle](
        verbose=args.verbose,
        delay=args.delay,
        max_steps=args.max_steps,
        state=state,
    )
    log(f"cycle={args.cycle} steps={len(trace)} digest={trace.digest()[:16]}")
    if trace.final_state:
        log(f"final state: {trace.final_state.to_dict()}")
    return 0


def cmd_organism(args: argparse.Namespace) -> int:
    """Run the full plate pipeline and report real outcomes."""
    engine = CosmogenicEngine()
    log("=== COSMOGENIC ORGANISM RUN START ===")

    state = EngineState()
    all_results = []
    for pass_no in range(1, args.passes + 1):
        before = state
        state, results, halt = engine.pass_once(state)
        all_results.append((pass_no, results))

        for r in results:
            marker = {
                Status.COMPLETE: "ok  ",
                Status.BLOCKED: "wait",
                Status.FAILED: "FAIL",
            }[r.status]
            detail = "; ".join(r.history if r.ok else r.reasons)
            log(f"  pass {pass_no} [plate {r.plate:>2} {r.label:<14}] {marker} {detail}")

        if halt:
            log(f"  HALT: {halt}")
            break
        if state.sealed:
            log(f"  sealed at {state.band_id} after pass {pass_no}")
            break
        if state == before:
            log(f"  fixed point after pass {pass_no}; no further progress possible")
            break

    summary = engine.run_to_completion()
    lines = [
        f"Cosmogenic Organism Run -- cold_fold_engine v{__version__}",
        "",
        "SCOPE: dimensionless state machine. No physical model is evaluated.",
        "",
        f"Final status : {summary['final_state']}",
        f"Trace digest : {summary['digest']}",
        f"Status counts: {summary['statuses']}",
        "",
        "=== HISTORY ===",
    ]
    lines += [f"- {h}" for h in summary["history"]]

    failed = [
        r
        for _, results in all_results
        for r in results
        if r.status is Status.FAILED
    ]
    write_artifact(Path(args.out), lines, summary)
    log(f"=== RUN COMPLETE: {summary['final_state']} ===")
    return 1 if failed else 0


def cmd_runtime(args: argparse.Namespace) -> int:
    """Step the pipeline under the default perturbation schedule."""
    rt = Runtime(perturbations=DEFAULT_SCENARIO)
    trace = rt.run(args.max_steps)
    log(f"steps {len(trace)}")
    log(f"digest {trace.digest()}")
    log(f"statuses {trace.statuses()}")
    if trace.records:
        last = trace.records[-1]
        log(f"final [{last.source}] {last.status.value}: {'; '.join(last.notes)}")
    if args.out:
        write_artifact(Path(args.out), [f"steps {len(trace)}"], trace.to_dict())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="runner.py", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_cycle = sub.add_parser("cycle", help="run a single cycle")
    p_cycle.add_argument("--cycle", required=True, choices=sorted(CYCLES))
    p_cycle.add_argument("--verbose", action="store_true")
    p_cycle.add_argument("--delay", type=float, default=0.0)
    p_cycle.add_argument("--max-steps", type=int, default=10, dest="max_steps")
    p_cycle.add_argument("--tension", type=int, default=0, help="initial tension")
    p_cycle.set_defaults(func=cmd_cycle)

    p_org = sub.add_parser("organism", help="run the full plate pipeline")
    p_org.add_argument("--out", default="./runs", help="output directory")
    p_org.add_argument("--passes", type=int, default=8)
    p_org.set_defaults(func=cmd_organism)

    p_rt = sub.add_parser("runtime", help="step the pipeline with perturbations")
    p_rt.add_argument("--max-steps", type=int, default=120, dest="max_steps")
    p_rt.add_argument("--out", default=None, help="output directory (optional)")
    p_rt.set_defaults(func=cmd_runtime)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
