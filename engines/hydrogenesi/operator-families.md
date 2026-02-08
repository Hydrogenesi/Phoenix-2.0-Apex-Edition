# Operator Families - Hydrogenesi Engine

## Purpose

The Operator Family system provides **systematic organization** for the Hydrogenesi Engine's transformation operators. Rather than treating operators as independent functions, v2.0 groups them into families based on their relationship to substrate laws, enabling easier learning, extension, and composition.

## Core Concept

**Operator Families** are collections of related operators that:
- Share a common purpose
- Relate to specific substrate laws
- Follow consistent patterns
- Enable compositional operations

```
FAMILY STRUCTURE:

Foundation Family ─────┐
   ⊝ (Void)           │
                       ├──→ SUBSTRATE LAW ENFORCEMENT
Reflection Family ─────┤
   ⊞ (Mirror)          │
                       │
Separation Family ─────┤
   ⊲ (Divergence)      │
                       │
Creation Family ────────┘
   ⊕ (Genesis)
```

## The Four Families

### 1. Foundation Family

**Purpose**: Return patterns to primordial state  
**Primary Law**: Law of Conservation  
**Symbol Theme**: Negative/Reduction  

#### Core Operator: Void (⊝)

The void operator reduces patterns to their primordial state while preserving conservation information.

```python
class FoundationFamily:
    """
    Operators that return patterns to substrate foundations.
    """
    
    def __init__(self):
        self.name = "Foundation"
        self.primary_law = "Conservation"
        self.operators = {}
        self._register_operators()
    
    def _register_operators(self):
        """Register all foundation operators."""
        
        # Primary: Void operator
        self.operators['void'] = {
            'symbol': '⊝',
            'function': self.void,
            'description': 'Reduce to primordial state',
            'inverse': 'genesis'  # ⊕ in Creation family
        }
        
        # Secondary: Reduction operator
        self.operators['reduce'] = {
            'symbol': '⊖',
            'function': self.reduce,
            'description': 'Partial reduction (not full void)',
            'inverse': None
        }
    
    def void(self, pattern):
        """
        ⊝ operator - reduce to primordial void.
        
        Returns VoidPattern with conservation fingerprint.
        """
        # Calculate what must be conserved
        fingerprint = {
            'total_depth': calculate_total_depth(pattern),
            'origin': pattern.trace.seed if hasattr(pattern, 'trace') else None,
            'timestamp': time.time()
        }
        
        # Create void state
        void_pattern = VoidPattern(
            fingerprint=fingerprint,
            original_pattern_ref=weakref.ref(pattern)  # Weak reference
        )
        
        # Verify conservation
        assert void_pattern.depth == fingerprint['total_depth']
        
        return void_pattern
    
    def reduce(self, pattern, level=1):
        """
        ⊖ operator - partial reduction.
        
        Reduces pattern by 'level' layers without going to full void.
        Useful for step-wise analysis.
        """
        current = pattern
        for _ in range(level):
            if hasattr(current, 'parent'):
                current = current.parent
            else:
                # Reached bottom, apply void
                return self.void(current)
        
        return current
```

#### Foundation Patterns

Operators in this family follow a common pattern:
1. Accept complex pattern
2. Extract conservation information
3. Return simpler pattern
4. Verify conservation maintained

#### Usage Examples

```python
# Full reduction to void
complex_apex = △(A, B, C)
void_state = ⊝(complex_apex)
print(f"Depth preserved: {void_state.depth} == {complex_apex.depth}")

# Partial reduction
recursive_pattern = ⊛⁷(seed)  # 7 levels deep
reduced = ⊖(recursive_pattern, level=3)  # Remove 3 layers
# reduced is now at depth 4
```

### 2. Reflection Family

**Purpose**: Reveal symmetric structure  
**Primary Law**: Law of Symmetry  
**Symbol Theme**: Bilateral/Mirroring  

#### Core Operator: Mirror (⊞)

The mirror operator reflects patterns to reveal symmetric structure and validate mirror property.

```python
class ReflectionFamily:
    """
    Operators that reveal symmetric structure through reflection.
    """
    
    def __init__(self):
        self.name = "Reflection"
        self.primary_law = "Symmetry"
        self.operators = {}
        self._register_operators()
    
    def _register_operators(self):
        """Register all reflection operators."""
        
        # Primary: Mirror operator
        self.operators['mirror'] = {
            'symbol': '⊞',
            'function': self.mirror,
            'description': 'Reflect pattern across symmetry axis',
            'property': 'involutory',  # ⊞(⊞(x)) = x
            'inverse': 'self'  # Self-inverse
        }
        
        # Secondary: Symmetry test
        self.operators['symmetric'] = {
            'symbol': '⊟',
            'function': self.is_symmetric,
            'description': 'Test if pattern is self-symmetric',
            'returns': 'boolean'
        }
    
    def mirror(self, pattern, mode='symmetric'):
        """
        ⊞ operator - reflect pattern.
        
        Handles multiple pattern types:
        - Numeric: Negation
        - Complex: Conjugation
        - Vector: Element-wise negation
        - Structural: Recursive mirroring
        
        Args:
            pattern: Pattern to mirror
            mode: 'symmetric' or 'antisymmetric'
        
        Returns:
            Mirrored pattern satisfying ⊞(⊞(x)) = x
        """
        # Type-specific mirroring
        if isinstance(pattern.value, (int, float)):
            mirrored_value = -pattern.value
        
        elif isinstance(pattern.value, complex):
            if mode == 'symmetric':
                mirrored_value = pattern.value.conjugate()
            else:  # antisymmetric
                mirrored_value = -pattern.value.conjugate()
        
        elif isinstance(pattern.value, np.ndarray):
            mirrored_value = -pattern.value
        
        elif hasattr(pattern, 'components'):
            # Structural: mirror each component
            mirrored_components = [self.mirror(c, mode) 
                                  for c in pattern.components]
            mirrored_value = Pattern(components=mirrored_components)
        
        else:
            raise MirrorOperatorError(
                f"Cannot mirror pattern of type {type(pattern.value)}"
            )
        
        # Create mirrored pattern
        mirrored = Pattern(mirrored_value)
        
        # Verify mirror property
        self._verify_involution(pattern, mirrored)
        
        return mirrored
    
    def _verify_involution(self, original, mirrored):
        """Verify ⊞(⊞(x)) = x"""
        double_mirror = self.mirror(mirrored)
        
        if not patterns_equivalent(original, double_mirror):
            raise MirrorOperatorError(
                "Mirror property violated: ⊞(⊞(x)) ≠ x"
            )
    
    def is_symmetric(self, pattern):
        """
        ⊟ operator - test for self-symmetry.
        
        Returns True if pattern equals its own mirror.
        """
        try:
            mirrored = self.mirror(pattern)
            return patterns_equivalent(pattern, mirrored)
        except MirrorOperatorError:
            return False
```

#### Reflection Patterns

Operators in this family follow a common pattern:
1. Accept pattern of any type
2. Apply type-appropriate reflection
3. Verify mirror property
4. Return reflected pattern

#### Usage Examples

```python
# Simple mirroring
pattern = Pattern(5)
mirrored = ⊞(pattern)
assert mirrored.value == -5
assert ⊞(mirrored).value == 5  # Involution

# Complex mirroring
complex_pattern = Pattern(3 + 4j)
mirrored = ⊞(complex_pattern)
assert mirrored.value == 3 - 4j  # Conjugate

# Symmetry testing
if ⊟(pattern):
    print("Pattern is self-symmetric")
```

### 3. Separation Family

**Purpose**: Decompose complex patterns  
**Primary Law**: Law of Duality  
**Symbol Theme**: Splitting/Divergence  

#### Core Operator: Divergence (⊲)

The divergence operator separates patterns into components while preserving conservation and identity.

```python
class SeparationFamily:
    """
    Operators that decompose complex patterns into components.
    """
    
    def __init__(self):
        self.name = "Separation"
        self.primary_law = "Duality"
        self.operators = {}
        self._register_operators()
    
    def _register_operators(self):
        """Register all separation operators."""
        
        # Primary: Divergence operator
        self.operators['divergence'] = {
            'symbol': '⊲',
            'function': self.divergence,
            'description': 'Separate pattern into components',
            'inverse': 'convergence'  # ⊳ in Phoenix
        }
        
        # Secondary: Binary split
        self.operators['split'] = {
            'symbol': '⊳|',
            'function': self.binary_split,
            'description': 'Split into exactly two components',
            'returns': 'tuple'
        }
        
        # Tertiary: Triadic separation
        self.operators['triad_separate'] = {
            'symbol': '⊲△',
            'function': self.triadic_separation,
            'description': 'Separate apex into three components',
            'requires': 'apex_pattern'
        }
    
    def divergence(self, pattern, strategy='balanced'):
        """
        ⊲ operator - separate into components.
        
        Handles multiple pattern types:
        - Apex: Three components (A, B, C from △)
        - Composite: Constituent components
        - Atomic: Returns [pattern] (cannot separate)
        
        Args:
            pattern: Pattern to separate
            strategy: 'balanced' or 'weighted'
        
        Returns:
            List of component patterns
        """
        # Check for apex structure
        if is_apex(pattern):
            return self.triadic_separation(pattern)
        
        # Check for explicit components
        elif hasattr(pattern, 'components'):
            components = pattern.components
        
        # Atomic pattern
        else:
            return [pattern]
        
        # Apply separation strategy
        if strategy == 'balanced':
            separated = [c.copy() for c in components]
        elif strategy == 'weighted':
            separated = self._apply_weights(components, pattern)
        
        # Verify conservation
        self._verify_separation_conservation(pattern, separated)
        
        return separated
    
    def triadic_separation(self, apex_pattern):
        """
        ⊲△ operator - separate apex into exactly three components.
        
        Specialized for apex structures from Phoenix convergence.
        """
        if not is_apex(apex_pattern):
            raise DivergenceError("Pattern is not an apex structure")
        
        # Extract three components
        A = apex_pattern.component_A
        B = apex_pattern.component_B
        C = apex_pattern.component_C
        
        # Preserve identities
        A.apex_origin = apex_pattern
        B.apex_origin = apex_pattern
        C.apex_origin = apex_pattern
        
        # Verify triadic conservation
        apex_depth = apex_pattern.depth
        component_depth = A.depth + B.depth + C.depth
        
        if abs(apex_depth - component_depth) > 1e-10:
            raise ConservationViolationError(
                f"Triadic separation violated conservation"
            )
        
        return [A, B, C]
    
    def binary_split(self, pattern):
        """
        ⊳| operator - split into exactly two components.
        
        Enforces duality by ensuring pattern can be represented
        as pair of complementary components.
        """
        components = self.divergence(pattern)
        
        if len(components) == 1:
            # Atomic pattern - create complement
            complement = calculate_complement(pattern)
            return (pattern, complement)
        
        elif len(components) == 2:
            return tuple(components)
        
        else:
            # Multiple components - combine into two groups
            mid = len(components) // 2
            group_a = combine_patterns(components[:mid])
            group_b = combine_patterns(components[mid:])
            return (group_a, group_b)
    
    def _verify_separation_conservation(self, original, separated):
        """Verify conservation maintained through separation."""
        original_depth = calculate_total_depth(original)
        separated_depth = sum(calculate_total_depth(c) for c in separated)
        
        if abs(original_depth - separated_depth) > 1e-10:
            raise ConservationViolationError(
                f"Separation violated conservation: "
                f"{original_depth} → {separated_depth}"
            )
```

#### Separation Patterns

Operators in this family follow a common pattern:
1. Accept complex pattern
2. Identify separable components
3. Apply separation strategy
4. Verify conservation

#### Usage Examples

```python
# Apex separation
apex = △(A, B, C)
components = ⊲(apex)
assert len(components) == 3
assert components == [A, B, C]

# Binary split
pattern = composite_pattern
a, b = ⊳|(pattern)
assert a and b  # Two components

# General divergence
complex_pattern = build_complex()
parts = ⊲(complex_pattern)
# parts is list of atomic components
```

### 4. Creation Family

**Purpose**: Validate emergence from substrate  
**Primary Law**: Law of Emergence  
**Symbol Theme**: Positive/Creation  

#### Core Operator: Genesis (⊕)

The genesis operator validates that patterns properly emerge from substrate state.

```python
class CreationFamily:
    """
    Operators that validate and facilitate emergence.
    """
    
    def __init__(self):
        self.name = "Creation"
        self.primary_law = "Emergence"
        self.operators = {}
        self._register_operators()
    
    def _register_operators(self):
        """Register all creation operators."""
        
        # Primary: Genesis operator
        self.operators['genesis'] = {
            'symbol': '⊕',
            'function': self.genesis,
            'description': 'Validate emergence from substrate',
            'inverse': 'void'  # ⊝ in Foundation family
        }
    
    def genesis(self, substrate_or_void):
        """
        ⊕ operator - validate emergence.
        
        Takes substrate or void state and creates validated pattern.
        Ensures proper emergence path exists.
        
        Args:
            substrate_or_void: VoidPattern or substrate pattern
        
        Returns:
            Valid pattern with verified emergence
        """
        # Handle void state
        if isinstance(substrate_or_void, VoidPattern):
            # Create pattern from void
            value = substrate_or_void.fingerprint['origin']
            if value is None:
                value = 0  # True genesis from nothing
            
            pattern = Pattern(value)
            pattern.origin_depth = substrate_or_void.depth
        
        # Handle substrate pattern
        else:
            pattern = substrate_or_void
        
        # Verify emergence law
        if not self._verify_emergence(pattern):
            raise EmergenceError("Pattern lacks valid emergence path")
        
        # Initialize identity trace if needed
        if not hasattr(pattern, 'trace'):
            pattern.trace = IdentityTrace(pattern.value)
        
        # Mark as genesis-validated
        pattern.genesis_validated = True
        pattern.genesis_timestamp = time.time()
        
        return pattern
    
    def _verify_emergence(self, pattern):
        """Verify pattern satisfies Law of Emergence."""
        # Must have origin
        if not hasattr(pattern, 'trace'):
            return False
        
        # Trace must not be empty
        if len(pattern.trace.transformations) == 0:
            return False
        
        # Seed must exist
        if pattern.trace.seed is None:
            return False
        
        return True
```

#### Creation Patterns

Operators in this family follow a common pattern:
1. Accept substrate or void
2. Verify emergence law compliance
3. Initialize identity trace
4. Return validated pattern

#### Usage Examples

```python
# Genesis from void
void = ⊝(complex_pattern)
recreated = ⊕(void)
# recreated has valid emergence path

# Genesis validation
substrate = raw_input
validated = ⊕(substrate)
# Raises EmergenceError if invalid

# Use with Phoenix
substrate = ⊕(⊝(seed))
ignited = IGNITION_SEQUENCE(substrate)
# Clean handoff to Phoenix
```

## Family Relationships

### Inverse Pairs

Some families contain inverse operators:

```
Foundation ⊝ ←──inverse──→ ⊕ Creation
   (void)                    (genesis)

Separation ⊲ ←──inverse──→ ⊳ (Phoenix Convergence)
 (divergence)              (convergence)

Reflection ⊞ ←──inverse──→ ⊞ Self
  (mirror)                  (mirror)
```

### Composition Chains

Families enable operator composition:

```
COMPLETE DESCENSION CHAIN:

Apex Pattern
     ↓ ⊲ (Separation)
Components [A, B, C]
     ↓ ⊞ (Reflection) - applied to each
Mirrored [A', B', C']
     ↓ ⊝ (Foundation) - applied to each
Substrate States
```

## Family-Based API

### Accessing Operators

```python
# By family
foundation = OPERATOR_FAMILIES['foundation']
void_op = foundation.get_operator('void')
result = void_op(pattern)

# Direct symbol access
result = ⊝(pattern)

# Family queries
print(foundation.list_operators())
# [('void', '⊝'), ('reduce', '⊖')]

print(foundation.primary_law)
# 'Conservation'
```

### Family Extensions

New operators can be registered:

```python
# Define custom operator
def custom_reduction(pattern):
    """Custom reduction strategy."""
    # Implementation
    pass

# Register in family
OPERATOR_FAMILIES['foundation'].register_operator(
    name='custom_reduce',
    operator_func=custom_reduction,
    symbol='⊖*'
)

# Now accessible
custom_reduce = OPERATOR_FAMILIES['foundation'].get_operator('custom_reduce')
```

## Design Patterns

### The Family Pattern

All operator families follow this structure:

```python
class OperatorFamilyTemplate:
    def __init__(self):
        self.name = "FamilyName"
        self.primary_law = "PrimarySubstrateLaw"
        self.operators = {}
        self._register_operators()
    
    def _register_operators(self):
        """Register all operators in this family."""
        self.operators['primary'] = {
            'symbol': '⊙',
            'function': self.primary_operator,
            'description': 'Primary operation',
            'inverse': 'some_other_operator'
        }
    
    def primary_operator(self, pattern):
        """Primary operator implementation."""
        pass
```

### Benefits of Family Organization

1. **Discoverability**: Related operators grouped together
2. **Learnability**: Clear structure aids learning
3. **Extensibility**: Easy to add new operators to existing families
4. **Composability**: Family relationships enable operator chains
5. **Maintainability**: Clear organization simplifies maintenance

## Usage Guidelines

### When to Use Each Family

**Foundation Family**: When you need to:
- Reduce patterns to substrate
- Check conservation
- Prepare for re-ignition

**Reflection Family**: When you need to:
- Reveal symmetric structure
- Test for symmetry
- Apply mirror transformations

**Separation Family**: When you need to:
- Analyze apex structures
- Decompose complex patterns
- Extract components

**Creation Family**: When you need to:
- Validate substrate patterns
- Initialize identity traces
- Hand off to Phoenix

## Further Reading

- [Substrate Integration](substrate-integration.md) - How families enforce laws
- [v2.0 Unified](v2-unified.md) - Complete operator implementations
- [Hydrogenesi Overview](README.md) - Full engine documentation
- [Operator System](../../operators/README.md) - Cross-engine operators

---

*"Four families, five laws, infinite combinations."*

**Status**: Production System (v2.0)  
**Families**: 4 (Foundation, Reflection, Separation, Creation)  
**Operators**: 8+ (extensible)  

[← Back to Hydrogenesi Overview](README.md) | [Substrate Integration →](substrate-integration.md)
