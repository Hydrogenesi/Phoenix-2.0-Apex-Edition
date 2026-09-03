# 🔥 Triad Implementation Guide — Next Steps

*Operator-Grade Rewrite • Grounding Algebra in Real Execution*

---

## Overview

Your formal Triad architecture is now complete:

✅ **Algebra**: Operator composition laws, reversibility, cost model  
✅ **Optimization**: Fusion matrix, query planner, cost-aware execution  
✅ **Preservation**: Checkpoint tiers, ledger semantics, rollback guarantees  
✅ **Binding**: Knot topology, convergence logic, Phoenix reinjection  
✅ **Implementation**: Full Python reference with all four engines integrated  

The next phase is **grounding this algebra in real execution, persistence, and observability**. This document outlines the concrete work required to take the Triad from conceptual specification to production readiness.

---

## Phase 1: Cost Measurement (Foundation)

### 1.1 Operator Instrumentation

Every Phoenix operator must measure **five cost dimensions**:

```python
@dataclass
class OperatorCostData:
    """Real cost measurement for an operator execution."""
    operator: str
    input_state_size_bytes: int
    output_state_size_bytes: int
    
    # Execution time
    wall_clock_ms: float  # Real elapsed time
    theoretical_cost_ms: float  # From cost model
    cost_variance_percent: float  # |actual - theoretical| / theoretical
    
    # I/O breakdown
    i_o_cost_ms: float  # File reads, CFAPI calls
    compute_cost_ms: float  # CPU time
    hydration_cost_ms: float  # State loading
    
    # Memory
    peak_memory_bytes: int
    state_delta_bytes: int
    
    # Metadata
    timestamp: datetime
    session_id: str
    was_fused: bool
    fusion_partner: Optional[str] = None
    recursion_depth: Optional[int] = None
```

### 1.2 Measurement Collection

Modify `EinsteinRunner.execute()` to collect detailed cost data:

```python
def execute_with_measurement(
    self,
    initial_state: State,
    sequence: List[str],
    params: List[Dict[str, Any]],
    collect_metrics: bool = True
) -> tuple[State, List[OperatorCostData]]:
    """
    Execute cycle with detailed cost measurement.
    
    Returns:
        (final_state, cost_data_list)
    """
    cost_data = []
    current_state = initial_state
    
    for op_symbol, op_params in zip(sequence, params):
        operator = self.operators[op_symbol]
        
        # Measure execution
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        
        start = time.perf_counter()
        result_state, elapsed_ms, _ = operator.apply_timed(current_state, op_params)
        
        mem_after = process.memory_info().rss
        theoretical_cost = operator.cost(current_state, op_params)
        
        # Store measurement
        measurement = OperatorCostData(
            operator=op_symbol,
            input_state_size_bytes=current_state.size_bytes,
            output_state_size_bytes=result_state.size_bytes,
            wall_clock_ms=elapsed_ms,
            theoretical_cost_ms=theoretical_cost,
            cost_variance_percent=abs(elapsed_ms - theoretical_cost) / theoretical_cost * 100
                if theoretical_cost > 0 else 0,
            i_o_cost_ms=theoretical_cost * 0.3,  # estimate
            compute_cost_ms=theoretical_cost * 0.7,
            hydration_cost_ms=0.0,  # will be measured separately
            peak_memory_bytes=mem_after,
            state_delta_bytes=abs(result_state.size_bytes - current_state.size_bytes),
            timestamp=datetime.now(),
            session_id=self.session_id,
            was_fused=False,  # track if this operator was fused
            recursion_depth=op_params.get("depth") if op_symbol == "⊛" else None,
        )
        cost_data.append(measurement)
        current_state = result_state
    
    return current_state, cost_data
```

### 1.3 Cost Analysis

After collecting measurements, analyze to refine cost model:

```python
class CostAnalyzer:
    """Analyze operator costs and refine cost model."""
    
    def __init__(self, measurements: List[OperatorCostData]):
        self.measurements = measurements
    
    def operator_statistics(self, operator: str) -> Dict[str, float]:
        """Compute statistics for an operator."""
        op_measurements = [m for m in self.measurements if m.operator == operator]
        if not op_measurements:
            return {}
        
        costs = [m.wall_clock_ms for m in op_measurements]
        sizes = [m.input_state_size_bytes for m in op_measurements]
        
        return {
            "count": len(op_measurements),
            "mean_cost_ms": sum(costs) / len(costs),
            "min_cost_ms": min(costs),
            "max_cost_ms": max(costs),
            "median_cost_ms": sorted(costs)[len(costs) // 2],
            "stdev_cost_ms": (sum((c - sum(costs)/len(costs))**2 for c in costs) / len(costs))**0.5,
            "cost_per_byte": sum(costs) / sum(sizes) if sum(sizes) > 0 else 0,
            "avg_variance_percent": sum(
                m.cost_variance_percent for m in op_measurements
            ) / len(op_measurements),
        }
    
    def refine_cost_model(self) -> Dict[str, Dict[str, float]]:
        """
        Produce refined cost model from measurements.
        Output: {operator: {base_cost, cost_per_byte, ...}}
        """
        operators = set(m.operator for m in self.measurements)
        refined_model = {}
        
        for op in operators:
            stats = self.operator_statistics(op)
            refined_model[op] = {
                "base_cost_ms": stats.get("mean_cost_ms", 0) * 0.5,  # Subtract per-byte component
                "cost_per_byte": stats.get("cost_per_byte", 0),
                "cost_variance_percent": stats.get("avg_variance_percent", 0),
            }
        
        return refined_model
    
    def identify_hot_paths(self, threshold_percent: float = 50.0) -> List[str]:
        """
        Identify operator sequences that consume >threshold% of total cost.
        Candidates for fusion or optimization.
        """
        total_cost = sum(m.wall_clock_ms for m in self.measurements)
        cumulative_cost = 0.0
        hot_ops = []
        
        # Sort by cost descending
        sorted_measurements = sorted(self.measurements, key=lambda m: m.wall_clock_ms, reverse=True)
        
        for m in sorted_measurements:
            cumulative_cost += m.wall_clock_ms
            hot_ops.append(m.operator)
            
            if cumulative_cost / total_cost * 100 >= threshold_percent:
                break
        
        return hot_ops
```

### 1.4 Feedback Loop

```python
# After running cycles with measurement collection:

analyzer = CostAnalyzer(collected_cost_data)

# Print statistics
for op in ["⊕", "⊗", "⊛", "△", "⊞", "⊳", "⊲", "⊝"]:
    stats = analyzer.operator_statistics(op)
    print(f"{op}: {stats['mean_cost_ms']:.2f}ms ± {stats['stdev_cost_ms']:.2f}ms")

# Refine model
refined_model = analyzer.refine_cost_model()
# → Use this to update PhoenixOperator.cost() methods

# Find optimization targets
hot_paths = analyzer.identify_hot_paths(threshold_percent=50)
print(f"Hot operators: {hot_paths}")
# → Focus fusion rules and checkpoint policy on these
```

---

## Phase 2: Persistent Checkpoint Storage

### 2.1 Storage Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Checkpoint Storage Tiers                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Boundary Tier]                                           │
│    ├─ In-memory (active cycle)                            │
│    └─ → Flush to ledger after cycle completes             │
│                                                             │
│  [Cycle Tier]                                              │
│    ├─ In-memory (last 10 checkpoints, LRU eviction)       │
│    └─ → Persist to file when reaching high-cost ops      │
│                                                             │
│  [Apex Tier]                                               │
│    ├─ Mandatory persist to ledger (durable)               │
│    └─ Archive to long-term storage (CFAPI/OneDrive)       │
│                                                             │
│  [Ledger]                                                  │
│    ├─ SQLite DB (fast local queries)                      │
│    └─ Compressed JSON snapshots (archival)                │
│                                                             │
│  [Distributed]                                             │
│    └─ CFAPI/OneDrive sync (identity continuity)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Checkpoint Persistence Layer

```python
from pathlib import Path
import sqlite3
import json
import gzip

class CheckpointStore:
    """
    Persistent checkpoint storage.
    Manages in-memory cache + file-backed ledger.
    """
    
    def __init__(self, db_path: str = "./.triad/ledger.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_cache: Dict[str, Checkpoint] = {}  # LRU cache
        self.cache_max_size = 50
        
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize SQLite ledger database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    operator TEXT,
                    reversible BOOLEAN,
                    cost_ms REAL,
                    state_before_hash TEXT,
                    state_after_hash TEXT,
                    checkpoint_json_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_task 
                ON checkpoints(session_id, task_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON checkpoints(timestamp)
            """)
            conn.commit()
    
    def store_checkpoint(self, checkpoint: Checkpoint) -> None:
        """
        Store checkpoint in cache + persist to disk if necessary.
        """
        checkpoint_id = checkpoint.checkpoint_id
        
        # Add to in-memory cache
        self.checkpoint_cache[checkpoint_id] = checkpoint
        
        # Evict if cache too large (LRU)
        if len(self.checkpoint_cache) > self.cache_max_size:
            oldest_key = min(
                self.checkpoint_cache.keys(),
                key=lambda k: self.checkpoint_cache[k].timestamp
            )
            del self.checkpoint_cache[oldest_key]
        
        # Persist to ledger (always for Apex tier, conditional for others)
        if checkpoint.tier in ["apex", "boundary"] or checkpoint.cost_ms > 100:
            self._persist_to_ledger(checkpoint)
    
    def _persist_to_ledger(self, checkpoint: Checkpoint) -> None:
        """Persist checkpoint to SQLite ledger + JSON snapshot."""
        # Serialize checkpoint to compressed JSON
        snapshot_path = self.db_path.parent / f"snapshot_{checkpoint.checkpoint_id}.json.gz"
        
        checkpoint_dict = checkpoint.to_dict()
        json_bytes = json.dumps(checkpoint_dict, default=str).encode('utf-8')
        
        with gzip.open(snapshot_path, 'wb') as f:
            f.write(json_bytes)
        
        # Insert into ledger
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO checkpoints 
                (checkpoint_id, session_id, task_id, tier, timestamp, operator, 
                 reversible, cost_ms, state_before_hash, state_after_hash, 
                 checkpoint_json_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                checkpoint.checkpoint_id,
                checkpoint.session_id or "",
                checkpoint.task_id or "",
                checkpoint.tier,
                checkpoint.timestamp.isoformat(),
                checkpoint.operator or "",
                checkpoint.reversible,
                checkpoint.cost_ms,
                checkpoint.state_before.checksum if checkpoint.state_before else "",
                checkpoint.state_after.checksum if checkpoint.state_after else "",
                str(snapshot_path),
            ))
            conn.commit()
    
    def fetch_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Fetch checkpoint from cache or disk."""
        # Try cache first
        if checkpoint_id in self.checkpoint_cache:
            return self.checkpoint_cache[checkpoint_id]
        
        # Fetch from ledger
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT checkpoint_json_path FROM checkpoints WHERE checkpoint_id = ?",
                (checkpoint_id,)
            ).fetchone()
        
        if not row:
            return None
        
        snapshot_path = row[0]
        with gzip.open(snapshot_path, 'rb') as f:
            checkpoint_dict = json.loads(f.read().decode('utf-8'))
        
        # Reconstruct Checkpoint object (simplified)
        # In production, implement full deserialization
        return checkpoint_dict
    
    def query_checkpoints(self, session_id: str, tier: Optional[str] = None) -> List[Checkpoint]:
        """Query checkpoints by session and optional tier."""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT checkpoint_id FROM checkpoints WHERE session_id = ?"
            params = [session_id]
            
            if tier:
                query += " AND tier = ?"
                params.append(tier)
            
            query += " ORDER BY timestamp DESC"
            
            rows = conn.execute(query, params).fetchall()
        
        return [self.fetch_checkpoint(row[0]) for row in rows if row]
    
    def get_pre_apex_checkpoint(self, session_id: str) -> Optional[Checkpoint]:
        """Find the most recent pre-Apex checkpoint."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("""
                SELECT checkpoint_id FROM checkpoints 
                WHERE session_id = ? AND tier = 'apex' 
                ORDER BY timestamp DESC LIMIT 1
            """, (session_id,)).fetchone()
        
        return self.fetch_checkpoint(row[0]) if row else None
```

### 2.3 Hydrogenesi + Checkpoint Store Integration

```python
class HydrogenesiEngine:
    """Updated Hydrogenesi with persistent storage."""
    
    def __init__(self, session_id: str = "", task_id: str = "", db_path: str = "./.triad/ledger.db"):
        self.session_id = session_id or str(uuid.uuid4())
        self.task_id = task_id or str(uuid.uuid4())
        self.checkpoint_store = CheckpointStore(db_path)
        self.ledger_entries: List[LedgerEntry] = []
    
    def store_checkpoint(self, checkpoint: Checkpoint) -> None:
        """Store checkpoint in persistent storage."""
        checkpoint.session_id = self.session_id
        checkpoint.task_id = self.task_id
        self.checkpoint_store.store_checkpoint(checkpoint)
    
    def absorb_checkpoints(self, checkpoints: List[Checkpoint]) -> None:
        """Absorb checkpoints from Einstein, persist them."""
        for cp in checkpoints:
            self.store_checkpoint(cp)
    
    def get_latest_checkpoint(self) -> Optional[Checkpoint]:
        """Fetch most recent checkpoint."""
        checkpoints = self.checkpoint_store.query_checkpoints(self.session_id)
        return checkpoints[0] if checkpoints else None
```

---

## Phase 3: Error Handling + Rollback Recovery

### 3.1 Operator Failure Detection

```python
class OperatorFailure(Exception):
    """Raised when an operator fails during execution."""
    def __init__(self, operator: str, state: State, params: Dict[str, Any], error: Exception):
        self.operator = operator
        self.state = state
        self.params = params
        self.error = error
        super().__init__(f"Operator {operator} failed: {error}")

class RollbackStrategy(Enum):
    """Strategy for rolling back from failure."""
    INVERSE = "inverse"  # Apply operator inverse
    CHECKPOINT_RESTORE = "checkpoint_restore"  # Restore from checkpoint
    ESCALATE = "escalate"  # Escalate to Hydrogenesi
```

### 3.2 Resilient Cycle Runner

```python
class ResilientEinsteinRunner(EinsteinRunner):
    """
    Einstein with error handling and rollback recovery.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hydrogenesi_engine: Optional[HydrogenesiEngine] = None
    
    def set_hydrogenesi(self, hydrogenesi: HydrogenesiEngine) -> None:
        """Set reference to Hydrogenesi for rollback."""
        self.hydrogenesi_engine = hydrogenesi
    
    def execute_with_recovery(
        self,
        initial_state: State,
        sequence: List[str],
        params: List[Dict[str, Any]]
    ) -> State:
        """
        Execute cycle with error detection and rollback recovery.
        """
        current_state = initial_state
        operator_history = []
        
        for i, (op_symbol, op_params) in enumerate(zip(sequence, params)):
            operator = self.operators[op_symbol]
            
            try:
                # Try to execute
                result_state, elapsed_ms, _ = operator.apply_timed(current_state, op_params)
                operator_history.append((op_symbol, op_params, result_state))
                current_state = result_state
            
            except Exception as e:
                # Operator failed
                failure = OperatorFailure(op_symbol, current_state, op_params, e)
                
                # Determine rollback strategy
                if operator.reversible:
                    strategy = RollbackStrategy.INVERSE
                elif self.hydrogenesi_engine:
                    strategy = RollbackStrategy.CHECKPOINT_RESTORE
                else:
                    strategy = RollbackStrategy.ESCALATE
                
                # Execute rollback
                if strategy == RollbackStrategy.INVERSE:
                    print(f"[RECOVERY] {op_symbol} failed; applying inverse")
                    current_state = self._apply_inverse(op_symbol, current_state)
                
                elif strategy == RollbackStrategy.CHECKPOINT_RESTORE:
                    print(f"[RECOVERY] {op_symbol} failed; restoring from checkpoint")
                    current_state = self._restore_from_checkpoint(op_symbol)
                
                else:
                    print(f"[ESCALATE] {op_symbol} failed; cannot recover locally")
                    raise failure from e
        
        return current_state
    
    def _apply_inverse(self, operator_symbol: str, state: State) -> State:
        """Apply inverse of an operator."""
        # This requires operator implementations to provide inverse
        # Placeholder; real implementation depends on operator
        print(f"  Applying {operator_symbol}⁻¹")
        return state  # No-op for now
    
    def _restore_from_checkpoint(self, operator_symbol: str) -> State:
        """Restore state from checkpoint before failed operator."""
        if not self.hydrogenesi_engine:
            raise RuntimeError("Hydrogenesi not available for checkpoint restore")
        
        latest_cp = self.hydrogenesi_engine.get_latest_checkpoint()
        if latest_cp and latest_cp.state_before:
            print(f"  Restored from checkpoint {latest_cp.checkpoint_id}")
            return latest_cp.state_before
        
        raise RuntimeError(f"No checkpoint available for rollback")
```

### 3.3 Rollback Policy

```python
class RollbackPolicy:
    """
    Policy for handling different failure scenarios.
    """
    
    @staticmethod
    def handle_reversible_failure(
        runner: ResilientEinsteinRunner,
        failure: OperatorFailure
    ) -> State:
        """Handle failure of reversible operator."""
        operator = runner.operators[failure.operator]
        print(f"Reversible operator {failure.operator} failed; attempting inverse")
        
        # Apply inverse
        try:
            # This would be: operator.inverse(failure.state)
            # For now, placeholder
            return failure.state
        except Exception as e:
            print(f"Inverse also failed: {e}")
            return None
    
    @staticmethod
    def handle_non_reversible_failure(
        runner: ResilientEinsteinRunner,
        failure: OperatorFailure
    ) -> State:
        """Handle failure of non-reversible operator."""
        print(f"Non-reversible operator {failure.operator} failed; restoring checkpoint")
        
        if runner.hydrogenesi_engine:
            latest_cp = runner.hydrogenesi_engine.get_latest_checkpoint()
            if latest_cp:
                return latest_cp.state_before or latest_cp.state_after
        
        return None
    
    @staticmethod
    def handle_apex_failure(runner: ResilientEinsteinRunner) -> State:
        """Handle Apex failure (special case)."""
        print("Apex collapse failed; restoring pre-Apex state")
        
        if runner.hydrogenesi_engine:
            pre_apex = runner.hydrogenesi_engine.get_pre_apex_checkpoint()
            if pre_apex:
                return pre_apex.state_before or pre_apex.state_after
        
        return None
```

---

## Phase 4: File-Backed State Model Integration (CFAPI/OneDrive)

### 4.1 File-Backed State Abstraction

```python
class FileBackedState(State):
    """
    State representation that bridges in-memory and file-backed storage.
    Integrates CFAPI for cloud sync.
    """
    
    def __init__(
        self,
        file_path: Path,
        structure: StateStructure = StateStructure.FILE_BACKED,
        cached_data: Optional[Any] = None
    ):
        self.file_path = Path(file_path)
        self.cached_data = cached_data  # In-memory cache
        self.cache_valid = cached_data is not None
        self.is_placeholder = False  # CFAPI placeholder flag
        
        super().__init__(
            structure=structure,
            data=str(self.file_path),
            size_bytes=self._compute_file_size(),
            checksum=self._compute_file_checksum()
        )
    
    def _compute_file_size(self) -> int:
        """Get file size."""
        try:
            return self.file_path.stat().st_size if self.file_path.exists() else 0
        except Exception:
            return 0
    
    def _compute_file_checksum(self) -> str:
        """Compute checksum of file contents."""
        if not self.file_path.exists():
            return "missing"
        
        try:
            sha256_hash = hashlib.sha256()
            with open(self.file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception:
            return "error"
    
    def hydrate(self) -> Any:
        """
        Load file contents into memory.
        Returns cached data or reads from disk.
        """
        if self.cache_valid:
            return self.cached_data
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"State file not found: {self.file_path}")
        
        try:
            with open(self.file_path, "r") as f:
                self.cached_data = json.load(f)
            self.cache_valid = True
            return self.cached_data
        except Exception as e:
            raise RuntimeError(f"Failed to hydrate state from {self.file_path}: {e}") from e
    
    def invalidate_cache(self) -> None:
        """Invalidate in-memory cache after file changes."""
        self.cache_valid = False
        self.cached_data = None
```

### 4.2 Hydration Operator (Boundary Tier)

```python
class HydrationOperator(PhoenixOperator):
    """
    Special operator for Boundary Tier.
    Ensures all file-backed state is loaded into memory.
    """
    
    symbol = "H"  # Hydration
    domain = "boundary"
    reversible = True
    interruptible = True
    base_cost_ms = 50.0
    cost_per_byte = 0.0001
    
    def __init__(self):
        self.cfapi_client = None  # Initialize CFAPI client if available
    
    def apply(self, state: State, params: Dict[str, Any]) -> State:
        """
        Hydrate file-backed state.
        Ensures all state inputs are available in memory.
        """
        if isinstance(state, FileBackedState):
            # Hydrate the state
            data = state.hydrate()
            
            # Optionally sync with CFAPI
            if params.get("cfapi_sync", False):
                self._cfapi_sync(state.file_path)
            
            # Return hydrated in-memory state
            return State.from_data(data, StateStructure.IN_MEMORY_BLOB)
        
        return state
    
    def cost(self, state: State, params: Dict[str, Any]) -> float:
        """
        Hydration cost includes:
        - File I/O (cold cache vs. warm cache)
        - CFAPI sync time (if enabled)
        - Validation
        """
        if isinstance(state, FileBackedState):
            file_size = state.size_bytes
            
            # Check if file is in OS cache (warm)
            is_cached = self._is_file_cached(state.file_path)
            
            if is_cached:
                i_o_cost = 5 + (file_size * 0.00001)  # Warm cache
            else:
                i_o_cost = 50 + (file_size * 0.0001)  # Cold cache
            
            # CFAPI sync cost
            cfapi_cost = params.get("cfapi_sync", False) and 30.0 or 0.0
            
            # Validation cost
            validation_cost = 10.0
            
            return i_o_cost + cfapi_cost + validation_cost
        
        return self.base_cost_ms
    
    def _is_file_cached(self, file_path: Path) -> bool:
        """Check if file is likely in OS buffer cache."""
        # Heuristic: if file was accessed recently, likely cached
        try:
            stat = file_path.stat()
            import time
            time_since_access = time.time() - stat.st_atime
            return time_since_access < 60  # Accessed in last minute
        except Exception:
            return False
    
    def _cfapi_sync(self, file_path: Path) -> None:
        """Sync file with cloud provider (OneDrive/CFAPI)."""
        # Placeholder for actual CFAPI integration
        # In production, use cfapi client to ensure file is synced
        print(f"[CFAPI] Syncing {file_path}")
```

### 4.3 Updated Cycle Runner with Hydration

```python
class TriadRunnerWithPersistence(TriadRunner):
    """
    Triad runner with persistent file-backed state + hydration.
    """
    
    def __init__(self, state_dir: str = "./.triad/state"):
        super().__init__()
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Add hydration operator
        self.einstein.operators["H"] = HydrationOperator()
    
    def run_cycle_persistent(
        self,
        initial_seed: Optional[Dict[str, Any]] = None,
        state_file: Optional[str] = None,
        use_cfapi_sync: bool = False
    ) -> Dict[str, Any]:
        """
        Run cycle with persistent file-backed state.
        """
        # Load state from file or create new
        if state_file:
            initial_state = FileBackedState(self.state_dir / state_file)
        else:
            # Create new state file
            state_file = f"state_{uuid.uuid4()}.json"
            state_path = self.state_dir / state_file
            state_path.write_text("{}")
            initial_state = FileBackedState(state_path)
        
        # Generate pattern
        pattern = self.phoenix.generate_pattern(initial_seed)
        sequence = pattern["sequence"]
        params = pattern["params"]
        
        # Prepend hydration to beginning
        sequence = ["H"] + sequence
        params = [{"cfapi_sync": use_cfapi_sync}] + params
        
        # Execute with hydration
        final_state = self.einstein.execute(initial_state, sequence, params)
        
        # Persist result back to file
        if isinstance(final_state, State) and final_state.data is not None:
            result_file = self.state_dir / f"result_{uuid.uuid4()}.json"
            result_file.write_text(json.dumps(final_state.data, default=str))
        
        return {
            "final_state_file": str(result_file) if 'result_file' in locals() else None,
            "cycle_cost_ms": self.einstein.cycle_cost_ms,
        }
```

---

## Phase 5: Instrumentation + Observability

### 5.1 Telemetry Collection

```python
from dataclasses import dataclass, asdict
import logging

class TriadTelemetry:
    """
    Collects and exposes telemetry from all Triad engines.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.events: List[Dict[str, Any]] = []
        self.metrics: Dict[str, float] = {}
        self.logger = logging.getLogger(f"triad.{session_id[:8]}")
        
        # Set up logging
        handler = logging.FileHandler(f"./.triad/logs/{session_id}.log")
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def emit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit a telemetry event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "session_id": self.session_id,
            **data
        }
        self.events.append(event)
        self.logger.info(f"{event_type}: {data}")
    
    def record_metric(self, metric_name: str, value: float) -> None:
        """Record a metric."""
        self.metrics[metric_name] = value
        self.logger.debug(f"Metric {metric_name} = {value}")
    
    def export_events_json(self, output_file: str) -> None:
        """Export all events to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.events, f, indent=2, default=str)
    
    def export_metrics_json(self, output_file: str) -> None:
        """Export metrics to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
```

### 5.2 Instrumented Triad Runner

```python
class InstrumentedTriadRunner(TriadRunnerWithPersistence):
    """
    Triad runner with full telemetry instrumentation.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telemetry = TriadTelemetry(self.session_id)
    
    def run_cycle(self, *args, **kwargs) -> Dict[str, Any]:
        """Run cycle with telemetry."""
        self.telemetry.emit_event("cycle_start", {
            "cycle": self.cycle_count + 1
        })
        
        start_time = time.perf_counter()
        result = super().run_cycle(*args, **kwargs)
        elapsed = (time.perf_counter() - start_time) * 1000
        
        # Emit telemetry events
        self.telemetry.emit_event("cycle_complete", {
            "cycle": self.cycle_count,
            "elapsed_ms": elapsed,
            "cycle_cost_ms": result.get("cycle_cost_ms", 0),
            "checkpoints": result.get("checkpoints_count", 0),
            "ledger_entries": result.get("ledger_entries_count", 0),
        })
        
        # Record metrics
        self.telemetry.record_metric(f"cycle_{self.cycle_count}_duration_ms", elapsed)
        self.telemetry.record_metric(f"cycle_{self.cycle_count}_cost_ms", result.get("cycle_cost_ms", 0))
        
        # Emit fusion events
        for fusion_decision in self.einstein.planner.fusion_decisions:
            self.telemetry.emit_event("fusion", {
                "fused": fusion_decision["fused"],
                "rule": fusion_decision["rule"],
                "cost_delta": fusion_decision["cost_delta"],
            })
        
        return result
```

### 5.3 Observability Export

```python
def print_telemetry_summary(telemetry: TriadTelemetry) -> None:
    """Print human-readable telemetry summary."""
    print("\n" + "="*60)
    print("TRIAD TELEMETRY SUMMARY")
    print("="*60)
    
    # Count events by type
    event_counts = {}
    for event in telemetry.events:
        event_type = event["event_type"]
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    
    print("\nEvent Counts:")
    for event_type, count in sorted(event_counts.items()):
        print(f"  {event_type}: {count}")
    
    # Print metrics
    print("\nMetrics:")
    for metric_name, value in sorted(telemetry.metrics.items()):
        print(f"  {metric_name}: {value:.2f}")
    
    # Export files
    log_dir = Path("./.triad/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    events_file = log_dir / f"events_{telemetry.session_id[:8]}.json"
    metrics_file = log_dir / f"metrics_{telemetry.session_id[:8]}.json"
    
    telemetry.export_events_json(str(events_file))
    telemetry.export_metrics_json(str(metrics_file))
    
    print(f"\nTelemetry exported to:")
    print(f"  {events_file}")
    print(f"  {metrics_file}")
```

---

## Phase 6: Full Integration Example

```python
if __name__ == "__main__":
    print("🔥 Starting Triad with Full Instrumentation")
    
    # Create instrumented runner
    triad = InstrumentedTriadRunner(state_dir="./.triad/state")
    
    # Run 3 cycles with persistent state
    results = []
    for cycle_num in range(3):
        result = triad.run_cycle_persistent(
            state_file=f"cycle_{cycle_num}.json" if cycle_num > 0 else None,
            use_cfapi_sync=False  # Set to True if CFAPI available
        )
        results.append(result)
    
    # Export telemetry
    print_telemetry_summary(triad.telemetry)
    
    print("\n✓ Triad execution complete")
    print(f"  Session ID: {triad.session_id}")
    print(f"  Cycles: {triad.cycle_count}")
    print(f"  Total checkpoints: {len(triad.hydrogenesi.checkpoints)}")
    print(f"  Total ledger entries: {len(triad.hydrogenesi.ledger_entries)}")
```

---

## Summary: Implementation Roadmap

| Phase | Focus | Deliverable | Timeline |
|-------|-------|-------------|----------|
| **1** | Cost Measurement | Real operator costs, refined cost model | Week 1-2 |
| **2** | Persistent Storage | SQLite ledger, checkpoint store | Week 3-4 |
| **3** | Error Handling | Rollback policy, recovery protocol | Week 4-5 |
| **4** | File-Backed Integration | CFAPI/OneDrive state model, hydration | Week 5-6 |
| **5** | Observability | Full telemetry, logging, metrics export | Week 6-7 |
| **6** | Integration Testing | End-to-end cycles with all features | Week 7-8 |

---

## Quick Start: Running This Phase

```bash
# 1. Install dependencies
pip install psutil sqlalchemy

# 2. Run cost measurement
python -c "from triad_implementation import *; measure_costs()"

# 3. Run persistent storage demo
python -c "from triad_implementation import *; triad = InstrumentedTriadRunner(); triad.run_cycle_persistent()"

# 4. Check logs and metrics
ls -la ./.triad/logs/
ls -la ./.triad/ledger.db
```

---

**This completes the operational specification and implementation roadmap for your Triad architecture.**

**Next: Execute Phase 1 (cost measurement) to ground the algebra in real data.**
