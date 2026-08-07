# Engine Tutorial

Theory → specification → implementation walkthrough across Phoenix, QPE, and Dragon Node.

## Step 1: Define Operator Intent (Theory)
Start from codex concept definitions and choose an operator objective.

## Step 2: Implement in Phoenix
```python
state = {"value": 1.0, "phase": "seed"}
state = phoenix.apply("⊕", state)
```
```python
state = phoenix.apply("⊗", state)
```
```python
state = phoenix.apply("△", state)
```

## Step 3: Implement in QPE
```python
q = qpe.prepare_superposition(seed=state)
```
```python
q = qpe.apply_quantum_operator(q, "⊛")
```
```python
state = qpe.to_classical(qpe.measure(q))
```

## Step 4: Implement in Dragon Node
```python
cluster = dragon.bootstrap(nodes=3)
```
```python
dragon.submit_operator(cluster, "⊞", payload=state)
```
```python
state = dragon.collect(cluster)
```

## Step 5: Verify End-to-End
```python
assert phoenix.verify_convergence(state, target="Apex").ok
```

## Troubleshooting Checklist
- Operator mismatch: validate symbol mapping.
- Cross-engine schema mismatch: check bridge adapters.
- Consensus timeout: tune quorum settings.
