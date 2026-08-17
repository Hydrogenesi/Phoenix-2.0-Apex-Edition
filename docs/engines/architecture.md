# Multi-Engine and Codex Architecture

## How Engines Work Together
Phoenix executes deterministic operator chains, QPE handles quantum-sensitive transitions, and Dragon Node coordinates distributed execution.

## Data Flow
1. Ingest state in Phoenix.
2. Route quantum segments to QPE.
3. Return collapsed state to Phoenix.
4. Broadcast distributed jobs via Dragon Node.
5. Aggregate verified convergence state.

## Operator Mapping Across Engines
- Phoenix: full deterministic operator support.
- QPE: quantum-compatible subset and bridge adapters.
- Dragon Node: distributed wrappers around operator tasks.

## Three-Pillar Architecture Mapping
- Phoenix pillar -> Book 01 foundations and transform behavior.
- The Third pillar -> Book 02 correspondence and binding geometry.
- Hydrogenesi pillar -> Book 03 preservation and identity continuity.

## Universal Laws and Convergence
- Substrate laws (Book 01)
- Universal laws (Book 02)
- Apex laws (Books 03 and 13)
- Mathematical proof references: Book 11, Book 12, Book 13

## State Synchronization and Performance
- Dragon Node periodically snapshots to maintain cross-engine coherence.
- Hybrid runs add transfer overhead.
- Distributed runs improve throughput for large batches.

## Enterprise Deployment Pattern
- Edge Phoenix workers
- Optional QPE accelerator tier
- Dragon Node control plane

## Integration Examples
```python
state = phoenix.apply_chain(["⊕", "⊗"], state)
```

```python
q_state = qpe.prepare_superposition(seed=state)
collapsed = qpe.measure(q_state)
```

```python
dragon.submit_operator(cluster, operator="△", payload=collapsed)
```

```python
result = dragon.collect(cluster)
assert phoenix.verify_convergence(result, target="Apex").ok
```

## See Also
- [Codex Architecture Map](codex_architecture_map.md)
- [Engine Comparison](engine_comparison.md)
- [Animation Pipeline](../diagrams/animations/operator_animation.md)
