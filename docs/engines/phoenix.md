# Phoenix Engine

## Overview
Phoenix Engine executes classical operator pipelines for transformation and convergence workflows.

## Architecture
- Ingestion layer
- Operator scheduler
- State transition core
- Verification stage

## Operators
Maps Phoenix operators (`⊕ ⊗ ⊛ △ ⊝ ⊞ ⊳ ⊲`) to deterministic state transforms.

## Performance
- Typical complexity: `O(n log n)` for sorted transition paths.
- Streaming mode: amortized `O(1)` append + periodic `O(n)` checkpoint.

## Integration
- QPE handoff for superposition-sensitive segments.
- Dragon Node handoff for distributed execution.

## Examples
```python
state = {"energy": 0.2, "phase": "seed"}
state = phoenix.apply("⊕", state)
```
```python
state = phoenix.apply_chain(["⊗", "⊛", "△"], state)
```
```python
report = phoenix.verify_convergence(state, target="Apex")
```
```python
batch = phoenix.run_batch(states, operator="⊞")
```
```python
delta = phoenix.diff(before, after)
```

## Troubleshooting
- Drift too high: reduce chain length per cycle.
- Instability: insert `⊞` mirror stabilization step.
- Slow batch runtime: enable vectorized mode.

## Related Chapters
- [Codex Landing](../codex/index.md)
- [Operator references](CROSS_REFERENCES.md)
