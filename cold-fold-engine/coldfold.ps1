# ColdFold launcher -- deterministic.
#
# Fixes against the original coldfold.ps1:
#   * $engine pointed at a directory name that looks like a
#     mangled paste of a Windows path. Resolved from this
#     script's own location instead.
#   * $python hardcoded one interpreter path. Now falls back to whatever
#     `python` is on PATH if that path is absent.
#   * It called cf.Runtime / cf.DEFAULT_SCENARIO, which did not exist in the
#     supplied files. They exist now (cold_fold_engine/runtime.py).

$ErrorActionPreference = "Stop"

$engine = $PSScriptRoot
if (-not $engine) { $engine = (Get-Location).Path }

$python = Join-Path $HOME ".claude-science\conda\envs\python\python.exe"
if (-not (Test-Path $python)) {
    $found = Get-Command python -ErrorAction SilentlyContinue
    if (-not $found) {
        throw "No Python interpreter found. Set `$python in this script."
    }
    $python = $found.Source
}

$env:PYTHONPATH = $engine

Write-Host "ColdFold launcher"
Write-Host "  engine : $engine"
Write-Host "  python : $python"
Write-Host ""

& $python (Join-Path $engine "runner.py") runtime --max-steps 120
if ($LASTEXITCODE -ne 0) { throw "runtime failed with exit code $LASTEXITCODE" }

& $python (Join-Path $engine "runner.py") organism --out (Join-Path $engine "runs")
exit $LASTEXITCODE
