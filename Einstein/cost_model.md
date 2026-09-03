# 🔹 Einstein Cost Model

*Deterministic Execution Costs for Mixed File-Backed + In-Memory State*

---

## 1. State Representation: Mixed Model

Einstein operates on a **hybrid state** that bridges file-backed (Hydrogenesi ledger, OneDrive/CFAPI) and in-memory (operator graphs, transformation matrices).

### State Layers

```
┌─────────────────────────────────────────────┐
│ File-Backed (Persistent)                    │
│  - Hydrogenesi Identity Ledger              │
│  - CFAPI-synced files + metadata            │
│  - Checkpoint archive                       │
└─────────────────────────────────────────────┘
         ↓ Hydration (Boundary Tier)
┌─────────────────────────────────────────────┐
│ In-Memory (Active Cycle)                    │
│  - Operator graph (DAG of transformations)  │
│  - State delta matrices                     │
│  - Curvature transforms                     │
│  - Temporary recursion stacks               │
└─────────────────────────────────────────────┘
         ↓ Ledger Emit (Apex Tier)
┌─────────────────────────────────────────────┐
│ File-Backed (Persisted Result)              │
│  - Apex state + metadata                    │
│  - Replay log                               │
│  - Checkpoint for resume                    │
└─────────────────────────────────────────────┘
```

### Cost Separation

All costs decompose into:

```
Total Cost = I/O Cost + Compute Cost + Hydration Cost

I/O Cost          [Dominant]  File read/write, CFAPI sync, ledger append
Compute Cost      [Variable]  Operator application, graph traversal
Hydration Cost    [Boundary]  Loading persistent state into memory
```

---

## 2. Operator Cost Functions (Concrete)

### Notation

- `state_size` = bytes of active in-memory state
- `file_size` = bytes of file-backed input
- `depth` = recursion depth for `⊛`
- `branch_count` = number of branches for `⊲`
- `ledger_entries` = historical entries in Hydrogenesi ledger

---

### Cost Table with Formulas

| Operator | Symbol | Cost Formula | Notes |
|----------|--------|--------------|-------|
| **Genesis** | `⊕` | `I/O: 20ms + (file_size * 0.0001) + Compute: 5 + (state_size * 0.0001)` | Allocation + provenance tag + file check |
| **Harmonic** | `⊗` | `Compute: 2 + (state_size * 0.00001)` | In-memory stabilization, negligible I/O |
| **Recursive** | `⊛` | `Compute: 10 * depth + (state_size * 0.00001 * depth)` | Linear in recursion depth |
| **Apex** | `△` | `Compute: 50 + (state_size * 0.0001) + I/O: 30ms` | Collapse + synthesis, then async ledger emit |
| **Void** | `⊝` | `Mark: Compute 1ms; Delete: I/O 15ms + (file_size * 0.00005)` | Non-destructive (mark) or destructive (delete) |
| **Mirror** | `⊞` | `Compute: 3 + (state_size * 0.000005)` | Involutive, minimal overhead |
| **Convergence** | `⊳` | `I/O: 10ms + Compute: 5 + (state_size * 0.00002)` | Ledger append for merge record |
| **Divergence** | `⊲` | `Compute: 5 + (state_size * branch_count * 0.00001)` | Branch tagging, in-memory |

---

### Cost Class Mapping

```
Low Cost          [<5ms]        Mirror, Harmonic
Low-Medium Cost   [5-20ms]      Void (mark), Recursive (shallow)
Medium Cost       [20-50ms]     Genesis, Void (delete), Divergence
High Cost         [50-200ms]    Convergence, Recursive (deep), Apex
Very High Cost    [>200ms]      Hydration (first-time), large Apex
```

---

## 3. Hydration Cost (Boundary Tier)

Hydration loads file-backed state into memory. It's a **Boundary operator** and must complete before any Cycle tier operator runs.

### Hydration Cost Formula

```
cost_hydration = I/O_time + Validation_time

I/O_time = 
  - Cold cache: 50ms + (file_size * 0.0001)
  - Warm cache: 5ms + (file_size * 0.00001)

Validation_time = 
  - Checksum: 5ms
  - Lineage check: 5ms per Hydrogenesi ledger entry
  - Total: 10ms + (ledger_entries * 1ms)
```

### Example: Hydrating a 10MB file with 100 ledger entries

```
Cold cache I/O:  50 + (10,000,000 * 0.0001) = 50 + 1000 = 1050ms
Warm cache I/O:  5 + (10,000,000 * 0.00001) = 5 + 100 = 105ms
Validation:      10 + (100 * 1) = 110ms
────────────────────────────────────────────────
Total (cold):    1050 + 110 = 1160ms
Total (warm):    105 + 110 = 215ms
```

**Implication**: Hydration dominates cycle cost. Einstein must reuse hydrated state across multiple cycles when possible.

---

## 4. Composition Cost Model

### Deterministic Composition

For a sequence of operators, total cost is **additive**:

```
cost(O_n ∘ O_{n-1} ∘ ... ∘ O_1) = Σ cost(O_i)

Example:
cost(△ ∘ ⊛(3) ∘ ⊗ ∘ ⊕) 
  = cost(⊕) + cost(⊗) + cost(⊛, depth=3) + cost(△)
  = (20 + 5) + (2) + (30 + ...) + (50 + 30)
  ≈ 25 + 2 + 30 + 80 = 137ms
```

### Interruptible Composition

If both `A` and `B` are interruptible (not Apex, not Convergence):

```
(A ∘ B)_t(s) = 
  if t < cost(A):
    resume A for time t
  else:
    A(s) → apply B for remaining time (t - cost(A))
```

**Critical Rule**: Apex is atomic. If `A ∘ Apex ∘ B` is the sequence:

```
(A ∘ Apex ∘ B)_t(s) =
  if t < cost(A):
    resume A
  else if t < cost(A) + cost(Apex):
    apply full Apex (cannot interrupt)
  else:
    resume B
```

---

## 5. Einstein Cycle Budget (Soft Target)

**Default assumption**: No hard realtime deadline.

**Soft targets**:

```
Most cycles:           < 100-200ms
Hydration (cold):      < 1500ms (acceptable outlier)
Single operator:       Flag if > 500ms

Decision rule:
  if cycle_cost > soft_target:
    log(WARNING, cycle_cost)
    defer to next window if queue depth > threshold
  else:
    execute immediately
```

**Tuning**: Einstein maintains a **rolling average** of cycle costs. If average drifts >20% above soft target, emit a Hydrogenesi anomaly record.

---

## 6. Cost-Aware Checkpoint Policy

Checkpoint selection is driven by cost + reversibility:

### Checkpoint Rules

1. **Boundary Tier (Hydration)**
   - Always checkpoint after hydration
   - Cost: negligible (one memory snapshot)
   - Purpose: can resume cycle from hydrated state if interrupted

2. **Cycle Tier**
   - Checkpoint before non-reversible operators (`Void`, `Convergence`, `Apex`)
   - Checkpoint if operator cost > 100ms AND interruptible
   - Skip checkpointing for low-cost reversible ops (`Harmonic`, `Mirror`)
   - Cost-benefit: only checkpoint if cost ≥ cost of reverting + re-running

3. **Apex Tier**
   - Always checkpoint pre-Apex state (full fidelity required for reversal)
   - Checkpoint post-Apex result (for ledger)
   - Cannot be interrupted; Apex is atomic

### Checkpoint Storage

```
Checkpoint Format:
  {
    checkpoint_id: UUID,
    session_id: str,
    operator_sequence: [Op1, Op2, ...],
    state_before: StateBlob,
    progress: { operator_index, iteration, elapsed_ms },
    timestamp: ISO8601,
  }

Storage:
  - Hydrated state → RAM (TTL: cycle duration)
  - Pre-Apex state → Hydrogenesi ledger (persistent)
  - Post-Apex state → Hydrogenesi ledger + archive
```

---

## 7. Cost Model Instrumentation

Einstein logs every operator invocation:

```python
class OperatorExecution:
    operator_name: str
    input_state_size: int
    output_state_size: int
    start_time: float
    end_time: float
    i_o_cost_ms: float
    compute_cost_ms: float
    total_cost_ms: float
    hydration_cost_ms: float
    was_interrupted: bool
    checkpoint_id: Optional[UUID]
    checkpoint_cost_ms: float

# Einstein runtime collects:
executions: List[OperatorExecution]
cycle_cost_ms: float
checkpoint_overhead_ms: float
effective_compute_ms: float
```

### Sample Metrics (to be measured)

```
Operator         Observed Cost (ms)    Variance    Notes
─────────────────────────────────────────────────────────
⊕ (Genesis)      25 ± 5                ±20%        File-dependent
⊗ (Harmonic)     2 ± 0.5               ±25%        In-memory
⊛ (Recursive)    30 per depth          ±10%        Consistent
△ (Apex)         80 ± 20               ±25%        Ledger emit varies
⊝ (Void, mark)   1 ± 0.5               ±50%        Negligible
⊝ (Void, del)    20 ± 5                ±25%        File-dependent
⊞ (Mirror)       3 ± 1                 ±33%        Very fast
⊳ (Convergence)  15 ± 5                ±33%        Ledger I/O
⊲ (Divergence)   8 ± 2                 ±25%        Branching overhead
```

*(These are estimates; actual measurement required.)*

---

## 8. Cost Model Integration with Fusion Rules

Einstein's **Query Planner** uses the cost model to decide fusion eligibility:

```
Fusion Candidate: ⊗ ∘ ⊗ (idempotent)

Before fusion:
  cost(⊗) + cost(⊗) = 2 + 2 = 4ms

After fusion:
  cost(⊗) = 2ms

Savings: 2ms (50% reduction)

Planner decision: FUSE (low overhead, measurable savings)

---

Fusion Candidate: ⊳ ∘ ⊳ (NOT fusible)

Before fusion:
  cost(⊳) + cost(⊳) = 15 + 15 = 30ms

Planner decision: SKIP (no fusion rule, no savings)

---

Fusion Candidate: △ ∘ △ (explicitly forbidden)

Planner decision: REJECT (non-fusible by law)
```

---

## 9. Summary: Cost Model Policy

| Aspect | Policy |
|--------|--------|
| **State Model** | Mixed file-backed (Hydrogenesi ledger, CFAPI) + in-memory (operator graphs, deltas) |
| **Cost Separation** | I/O + Compute + Hydration, all measured independently |
| **Cycle Budget** | Soft target <100-200ms; no hard deadline; optimize for determinism |
| **Checkpoint Granularity** | Hybrid: always at Boundary + Apex; selective in Cycle tier based on cost + reversibility |
| **Hydration Strategy** | Reuse hydrated state; cache warm to avoid repeated cold loads |
| **Fusion Policy** | Fuse only when cost savings > overhead + reversibility is preserved |
| **Instrumentation** | Log all operator executions; measure I/O vs. compute separately; track checkpoint overhead |

---

**Next**: [Fusion Matrix](./fusion_matrix.md) — All 8×8 operator combinations, their fusibility, and cost impact.
