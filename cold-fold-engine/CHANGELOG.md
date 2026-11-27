# Changelog

## 7.1.0 — 2026-10
- Rebuilt the engine as an immutable, deterministic plate pipeline with three outcomes: COMPLETE, BLOCKED, and FAILED.
- Added `Runtime`, `DEFAULT_SCENARIO`, and a SHA-256 trace digest.
- Split the cycles into separate modules (`relativistic`, `collapse`, `demo`).
- Added a test suite of 41 tests, a CLI, and a PowerShell launcher.
- See docs/HISTORY.md for the defects fixed relative to the original prototype.
