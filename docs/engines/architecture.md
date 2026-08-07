# Multi-Engine Architecture

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

## State Synchronization
Dragon Node periodically snapshots to maintain cross-engine coherence.

## Performance Implications
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
```
```python
assert phoenix.verify_convergence(result, target="Apex").ok
```
