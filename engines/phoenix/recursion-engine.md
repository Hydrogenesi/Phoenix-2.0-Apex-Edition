# Recursion Engine - Phoenix Core

## Overview

The Recursion Engine is the **computational heart** of the Phoenix system—the component that implements the Law of Recursive Identity through bounded, identity-preserving self-reference. Where ignition operators start the process, the recursion engine sustains and controls it, ensuring that patterns evolve while maintaining their essential nature.

## Core Principle

**Recursion** in the Phoenix context means more than simple function self-call. It means:

```
RECURSION = SELF-REFERENCE + TRANSFORMATION + IDENTITY_PRESERVATION

⊛(x) produces x' such that:
  1. x' contains the pattern of x
  2. x' ≠ x (transformation occurred)
  3. trace(x') includes x (identity preserved)
```

## Architecture

### Recursion Engine Components

```
┌─────────────────────────────────────────┐
│         RECURSION ENGINE                │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  OPERATOR CORE                    │ │
│  │  - ⊛ implementation               │ │
│  │  - Context-aware recursion        │ │
│  │  - Mutual recursion support       │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  IDENTITY SYSTEM                  │ │
│  │  - Trace maintenance              │ │
│  │  - Parent linkage                 │ │
│  │  - Reconstruction capability      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  DEPTH TRACKER                    │ │
│  │  - Current depth                  │ │
│  │  - Depth limits                   │ │
│  │  - Conservation verification      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  CONVERGENCE DETECTOR             │ │
│  │  - Pattern comparison             │ │
│  │  - Stability metrics              │ │
│  │  - Early termination              │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

## Recursive Operator (⊛) Implementation

### Single-Pattern Recursion

```python
class RecursionEngine:
    """
    Core recursion engine implementing Law of Recursive Identity.
    """
    
    def __init__(self, config=None):
        self.config = config or DEFAULT_RECURSION_CONFIG
        self.active_processes = {}
        
    def apply_recursive_operator(self, pattern, context=None):
        """
        Apply ⊛ operator to pattern.
        
        Args:
            pattern: Input pattern with identity trace
            context: Optional context patterns for mutual recursion
        
        Returns:
            Transformed pattern with updated trace
        """
        # Check depth limit
        if pattern.depth >= self.config.max_depth:
            raise RecursionDepthExceededError(
                f"Depth limit {self.config.max_depth} reached"
            )
        
        # Store pre-recursion state for conservation check
        pre_conservation = self._calculate_conservation_metric(pattern)
        
        # Apply transformation
        if context is None:
            # Simple self-reference
            new_value = self._self_reference_transformation(pattern)
        else:
            # Context-aware recursion
            new_value = self._contextual_transformation(pattern, context)
        
        # Create recursive pattern
        recursive_pattern = self._create_recursive_pattern(
            value=new_value,
            parent=pattern,
            context=context
        )
        
        # Verify conservation if enabled
        if self.config.verify_conservation:
            post_conservation = self._calculate_conservation_metric(
                recursive_pattern
            )
            if not self._conservation_maintained(
                pre_conservation, 
                post_conservation
            ):
                raise ConservationViolationError(
                    f"Conservation broken: {pre_conservation} → {post_conservation}"
                )
        
        return recursive_pattern
```

### Self-Reference Transformation

Multiple transformation strategies available:

```python
def _self_reference_transformation(self, pattern):
    """
    Core self-referential transformation.
    
    Strategy depends on pattern type and characteristics.
    """
    # Numeric patterns: Squared self-reference
    if isinstance(pattern.value, (int, float, complex)):
        return pattern.value ** 2
    
    # Vector patterns: Dot product with self
    elif isinstance(pattern.value, np.ndarray):
        return np.dot(pattern.value, pattern.value)
    
    # Symbolic patterns: Compositional self-reference
    elif isinstance(pattern.value, SymbolicPattern):
        return pattern.value.compose(pattern.value)
    
    # General patterns: Recursive folding
    else:
        return self._recursive_fold(pattern.value)
```

### Contextual Transformation

For mutual recursion scenarios:

```python
def _contextual_transformation(self, pattern, context):
    """
    Transform pattern with awareness of context patterns.
    
    Used in mutual recursion for apex convergence.
    """
    # Calculate context influence
    context_values = [c.value for c in context]
    context_centroid = sum(context_values) / len(context_values)
    
    # Blend self-reference with context
    self_component = self._self_reference_transformation(pattern)
    context_component = (pattern.value * context_centroid)
    
    # Weighted combination (favors self but includes context)
    blended = (0.7 * self_component + 0.3 * context_component)
    
    return blended
```

## Identity Trace System

### Complete Trace Maintenance

```python
class IdentityTrace:
    """
    Maintains complete transformation history for a pattern.
    """
    
    def __init__(self, seed):
        self.seed = seed
        self.transformations = [seed]
        self.operators_applied = []
        self.timestamps = [time.time()]
    
    def append(self, pattern, operator):
        """Add transformation to trace."""
        self.transformations.append(pattern)
        self.operators_applied.append(operator)
        self.timestamps.append(time.time())
    
    def reconstruct_at_depth(self, depth):
        """Reconstruct pattern at specific depth."""
        if depth >= len(self.transformations):
            raise ValueError(f"Depth {depth} exceeds trace length")
        return self.transformations[depth]
    
    def trace_backward(self):
        """Return trace in reverse order."""
        return list(reversed(self.transformations))
    
    def verify_continuity(self):
        """Verify trace is continuous (no gaps)."""
        for i in range(len(self.transformations) - 1):
            current = self.transformations[i]
            next_pattern = self.transformations[i + 1]
            
            if not self._patterns_linked(current, next_pattern):
                return False
        return True
```

### Parent Linkage

Every recursive pattern maintains reference to its parent:

```python
class RecursivePattern:
    """
    Pattern with full recursive metadata.
    """
    
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        
        # Depth calculation
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        
        # Identity trace
        if parent is None:
            self.trace = IdentityTrace(value)
        else:
            self.trace = parent.trace
            self.trace.append(value, operator='⊛')
    
    def ancestors(self):
        """Return list of all ancestors."""
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def root(self):
        """Return root pattern (depth 0)."""
        current = self
        while current.parent is not None:
            current = current.parent
        return current
```

## Depth Tracking and Limits

### Depth Management

```python
class DepthTracker:
    """
    Tracks and enforces recursion depth limits.
    """
    
    def __init__(self, max_depth=7):
        self.max_depth = max_depth
        self.current_depth = 0
        self.depth_history = [0]
    
    def increment(self):
        """Increment depth, raising error if limit exceeded."""
        self.current_depth += 1
        self.depth_history.append(self.current_depth)
        
        if self.current_depth > self.max_depth:
            raise RecursionDepthExceededError(
                f"Maximum depth {self.max_depth} exceeded"
            )
    
    def decrement(self):
        """Decrement depth (for backtracking)."""
        if self.current_depth > 0:
            self.current_depth -= 1
    
    def reset(self):
        """Reset to depth 0."""
        self.current_depth = 0
```

### Conservation Through Depth

The Law of Conservation of Essence manifests as depth preservation:

```python
def verify_depth_conservation(pattern_before, pattern_after):
    """
    Verify that total recursive depth is conserved.
    
    ∑depth(before) must equal ∑depth(after)
    """
    def total_depth(pattern):
        """Calculate total depth across all components."""
        if hasattr(pattern, 'components'):
            return sum(p.depth for p in pattern.components)
        return pattern.depth
    
    depth_before = total_depth(pattern_before)
    depth_after = total_depth(pattern_after)
    
    return abs(depth_before - depth_after) < CONSERVATION_TOLERANCE
```

## Convergence Detection

### Pattern Comparison

```python
def patterns_converged(pattern_a, pattern_b, threshold=0.001):
    """
    Determine if two patterns have converged.
    
    Convergence means successive recursive applications
    produce minimal change.
    """
    # Value comparison
    value_diff = abs(pattern_a.value - pattern_b.value)
    value_relative_diff = value_diff / max(abs(pattern_a.value), 1e-10)
    
    if value_relative_diff < threshold:
        # Phase comparison (if applicable)
        if hasattr(pattern_a, 'phase') and hasattr(pattern_b, 'phase'):
            phase_diff = abs(pattern_a.phase - pattern_b.phase)
            if phase_diff < threshold:
                return True
        else:
            return True
    
    return False
```

### Stability Metrics

```python
def calculate_stability_score(pattern_history, window=5):
    """
    Calculate stability score from recent pattern history.
    
    Returns value in [0, 1]:
    - 0 = highly unstable (diverging)
    - 1 = perfectly stable (converged)
    """
    if len(pattern_history) < window:
        return 0.5  # Insufficient data
    
    recent = pattern_history[-window:]
    
    # Calculate pairwise differences
    diffs = []
    for i in range(len(recent) - 1):
        diff = abs(recent[i+1].value - recent[i].value)
        relative_diff = diff / max(abs(recent[i].value), 1e-10)
        diffs.append(relative_diff)
    
    # Stability is inverse of average change
    avg_change = sum(diffs) / len(diffs)
    stability = 1.0 / (1.0 + avg_change)
    
    return stability
```

## Advanced Recursion Patterns

### Bounded Recursion

```python
def bounded_recursion(pattern, max_depth=7, convergence_threshold=0.001):
    """
    Apply recursion with depth limit and convergence detection.
    
    Automatically terminates when:
    1. Depth limit reached, OR
    2. Convergence detected
    """
    current = pattern
    history = [pattern]
    
    for depth in range(max_depth):
        # Apply recursion
        next_pattern = ⊛(current)
        history.append(next_pattern)
        
        # Check convergence
        if patterns_converged(current, next_pattern, convergence_threshold):
            return next_pattern, depth, "converged"
        
        current = next_pattern
    
    # Depth limit reached
    return current, max_depth, "depth_limit"
```

### Mutual Recursion

For triadic apex convergence:

```python
def mutual_recursion(pattern_A, pattern_B, pattern_C, iterations=3):
    """
    Three-way mutual recursion.
    
    Each pattern recursively transforms with awareness of others.
    """
    A, B, C = pattern_A, pattern_B, pattern_C
    
    for i in range(iterations):
        # Simultaneous transformation
        A_next = ⊛(A, context=[B, C])
        B_next = ⊛(B, context=[C, A])
        C_next = ⊛(C, context=[A, B])
        
        # Update for next iteration
        A, B, C = A_next, B_next, C_next
    
    return A, B, C
```

### Adaptive Depth Recursion

```python
def adaptive_recursion(pattern, target_complexity):
    """
    Recurse until target complexity achieved.
    
    Depth adapts to pattern characteristics rather than
    being fixed a priori.
    """
    current = pattern
    depth = 0
    
    while calculate_complexity(current) < target_complexity:
        current = ⊛(current)
        depth += 1
        
        # Safety limit
        if depth > MAX_ADAPTIVE_DEPTH:
            break
    
    return current, depth
```

## Performance Optimization

### Lazy Trace Pruning

```python
class PrunedTrace:
    """
    Identity trace with automatic pruning of old entries.
    """
    
    def __init__(self, seed, max_length=100):
        self.seed = seed
        self.max_length = max_length
        self.transformations = [seed]
        self.pruned_count = 0
    
    def append(self, pattern):
        self.transformations.append(pattern)
        
        # Prune if too long
        if len(self.transformations) > self.max_length:
            self._prune_old_entries()
    
    def _prune_old_entries(self):
        """Remove middle entries, keeping seed and recent."""
        keep_recent = self.max_length // 2
        keep_old = self.max_length // 4
        
        pruned = (
            self.transformations[:keep_old] +
            ['...pruned...'] +
            self.transformations[-keep_recent:]
        )
        
        self.pruned_count += (
            len(self.transformations) - len(pruned) + 1
        )
        self.transformations = pruned
```

### Memoization

```python
class MemoizedRecursion:
    """
    Cache results of recursive transformations.
    """
    
    def __init__(self, recursion_engine):
        self.engine = recursion_engine
        self.cache = {}
    
    def recurse(self, pattern, context=None):
        """Apply recursion with caching."""
        # Create cache key
        key = self._cache_key(pattern, context)
        
        # Check cache
        if key in self.cache:
            return self.cache[key]
        
        # Compute
        result = self.engine.apply_recursive_operator(pattern, context)
        
        # Store in cache
        self.cache[key] = result
        
        return result
    
    def _cache_key(self, pattern, context):
        """Generate cache key from pattern and context."""
        pattern_hash = hash(pattern.value)
        context_hash = hash(tuple(c.value for c in context)) if context else 0
        return (pattern_hash, context_hash)
```

## Error Handling

### Recursive Errors

```python
class RecursionError(PhoenixError):
    """Base class for recursion-related errors."""
    pass

class RecursionDepthExceededError(RecursionError):
    """Maximum recursion depth exceeded."""
    pass

class RecursionDivergenceError(RecursionError):
    """Pattern diverging rather than converging."""
    pass

class IdentityLostError(RecursionError):
    """Identity trace corrupted or lost."""
    pass
```

### Recovery Strategies

```python
def safe_recursion_with_recovery(pattern, max_depth=7):
    """
    Apply recursion with automatic error recovery.
    """
    try:
        return bounded_recursion(pattern, max_depth)
    
    except RecursionDivergenceError:
        # Try with reduced depth
        return bounded_recursion(pattern, max_depth // 2)
    
    except IdentityLostError:
        # Reconstruct from last known good state
        last_good = find_last_valid_state(pattern)
        return bounded_recursion(last_good, max_depth)
    
    except RecursionDepthExceededError:
        # Return current state with warning
        warn("Depth limit reached without convergence")
        return pattern
```

## Integration Points

### With Ignition System

```python
# After ignition, recursion engine takes over
ignited = IGNITION_SEQUENCE(seed)
recursion_engine = RecursionEngine()
continued = recursion_engine.continue_recursion(ignited, max_depth=7)
```

### With Harmonic Stabilizers

```python
# Recursion engine reports to stabilizers
def recurse_with_monitoring(pattern):
    recursive_pattern = ⊛(pattern)
    HARMONIC_STABILIZER.notify_recursion(pattern, recursive_pattern)
    return recursive_pattern
```

### With Apex Convergence

```python
# Recursion engine enables mutual recursion for apex
A, B, C = mutual_recursion(engine_A, engine_B, engine_C)
apex = △(A, B, C)
```

## Configuration

```yaml
recursion_engine:
  max_depth: 7
  convergence_threshold: 0.001
  verify_conservation: true
  maintain_full_trace: true
  trace_max_length: 100
  enable_memoization: false
  adaptive_depth: false
```

## Further Reading

- [Ignition Operators](ignition-operators.md) - Starting recursion
- [Harmonic Stabilizers](harmonic-stabilizers.md) - Maintaining stability
- [v2.0 Apex Edition](v2-apex-edition.md) - Complete specifications
- [Phoenix Overview](README.md) - Full engine documentation

---

*"Recursion is the engine of becoming. Identity is the anchor of being. Together, they manifest recursive identity."*

[← Back to Phoenix Overview](README.md) | [Harmonic Stabilizers →](harmonic-stabilizers.md)
