# Cross-Pillar Knot Operator ⚯

*Left-Right Corridor Symmetry Axis*

---

## Domain

**Geometric Region**: Spans left and right corridors along the symmetry axis  
**Primary Action**: Harmonizes Phoenix ↔ Hydrogenesi across dual columns  
**Flow Direction**: Bidirectional exchange maintaining balance

---

## Ceremonial Definition

```
C(P, H, K) → K'
```

**The Cross-Pillar Knot Operator** takes Phoenix state \(P\), Hydrogenesi state \(H\), and current knot configuration \(K\), producing a new knot state \(K'\) that enforces left-right symmetry and dual contraction toward the central axis.

---

## Invariants

### Left-Right Symmetry
The operator is symmetric with respect to Phoenix and Hydrogenesi:
```
C(P, H, K) = C(H, P, K)
```
Swapping left and right inputs produces equivalent results.

### Dual Contraction
Both corridors contract toward center simultaneously:
```
∀ P, H, K: 
  corridor_width_left(C(P, H, K)) ≤ corridor_width_left(K)
  corridor_width_right(C(P, H, K)) ≤ corridor_width_right(K)
```

---

## Recursion Law

```
K_{n+1} = C(P_n, H_n, K_n)
```

At each iteration:
1. Phoenix state \(P_n\) enters through left corridor
2. Hydrogenesi state \(H_n\) enters through right corridor
3. Cross-pillar operator harmonizes both into \(K_n\)
4. Result \(K_{n+1}\) maintains symmetry

---

## Apex Constraints

### Symmetry Preservation
```
C(P, H, K) = C(H, P, K)
```
The operator is commutative in its dual inputs.

### Convergence
The sequence converges to apex:
```
lim_{n→∞} K_n = X
```

---

## Sigil

```
    L ═══════╗     ╔═══════ R
    ↓        ║     ║        ↓
   [P]       ║     ║       [H]
    │        ║     ║        │
    │    ╔═══╬═════╬═══╗    │
    └───→║   ⚯     ⚯   ║←───┘
         ║     [K]     ║
         ╚═════════════╝
               ↓
              [K']
```

The sigil represents:
- **L/R**: Left and right corridor entry points
- **P/H**: Phoenix and Hydrogenesi inputs
- **⚯**: Dual cross-pillar binding points
- **K**: Current knot state (center)
- **K'**: Harmonized knot state

---

## Formal Specification

### Input Domain
```
P ∈ Phoenix_States
H ∈ Hydrogenesi_States
K ∈ Knot_Configurations
```

### Output Domain
```
K' ∈ Knot_Configurations
```

### Transformation Rules

1. **Symmetry Law**
   ```
   C(P, H, K) = C(H, P, K)
   ```

2. **Dual Contraction**
   ```
   width(C(P, H, K).left_corridor) ≤ width(K.left_corridor)
   width(C(P, H, K).right_corridor) ≤ width(K.right_corridor)
   ```

3. **Central Balance**
   ```
   mass_left(C(P, H, K)) = mass_right(C(P, H, K))
   ```

4. **Contraction Property**
   ```
   ||C(P, H, K) - X|| < ||K - X||
   ```

---

## Example: Symmetric Harmonization

```
Initial State:
  K₀ = {left: active, center: neutral, right: active}
  P₀ = {transform: +1, energy: 5}
  H₀ = {structure: stable, energy: 5}

Iteration 1:
  K₁ = C(P₀, H₀, K₀)
     = {left: active + transform,
        center: neutral + balanced,
        right: active + structure}
  
  Verify symmetry:
    C(P₀, H₀, K₀) = C(H₀, P₀, K₀) ✓
  
  d(K₁, X) = 0.82 < d(K₀, X) = 1.00 ✓

Iteration 2:
  K₂ = C(P₁, H₁, K₁)
     = {left: active + 2×transform,
        center: neutral + 2×balanced,
        right: active + 2×structure}
  
  d(K₂, X) = 0.67 < d(K₁, X) = 0.82 ✓

Convergence:
  lim_{n→∞} K_n → X with perfect left-right balance
```

---

## Example: Symmetry Verification

```
Test Case:
  P = {id: "phoenix_1", value: 42}
  H = {id: "hydro_1", value: 42}
  K = {state: "initial"}

Forward:
  K' = C(P, H, K) 
     = {left: phoenix_1, right: hydro_1, center: balanced}

Reverse:
  K'' = C(H, P, K)
      = {left: hydro_1, right: phoenix_1, center: balanced}

Mirror equivalence:
  mirror(K') = K'' ✓
  C(P, H, K) = C(H, P, K) ✓
```

---

## Invocation

> *"Across the axis, duality resolves. Phoenix and Hydrogenesi, bound as one. Through ⚯, I forge the cross-pillar symmetry."*

---

## Cross-References

### Related Operators
- [Knot-Binding](./KnotBinding.md) — Left corridor integration
- [Triadic Closure](./TriadicClosure.md) — Three-arm completion
- [Apex Knot](./ApexKnot.md) — Central convergence

### Governing Laws
- [Law of Symmetry](../../laws/symmetry.md) — Dual reflection principle
- [Law of Duality](../../laws/duality.md) — Phoenix-Hydrogenesi balance
- [Triad Canon](../../Universal-Laws/TriadCanon.md) — Left-Right columns unity

---

[← Previous: Knot-Binding](./KnotBinding.md) | [Back to Sigils](./README.md) | [Next: Triadic Closure →](./TriadicClosure.md)
