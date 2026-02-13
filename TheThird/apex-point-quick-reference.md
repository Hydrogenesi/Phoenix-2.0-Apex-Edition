# Apex Point Quick Reference

*Essential Formulas and Properties at a Glance*

---

## Core Definitions

### The Apex Point (X)
```
X = unique fixed point of Triadic Knot topology
A(X) = X  (fixed under Apex Knot operator)
d(X, X) = 0  (zero distance to itself)
```

### Distance Metric
```
d: K × {X} → ℝ⁺

Properties:
  d(K, X) ≥ 0  (non-negative)
  d(X, X) = 0  (identity)
  d(O(K), X) < d(K, X)  (contraction for all operators O)
```

---

## Operator Notation

### Phoenix Operators
```
⊕  Genesis         ⊗  Harmonic        ⊛  Recursive       △  Apex
⊝  Void            ⊞  Mirror          ⊳  Convergence     ⊲  Divergence
```

### Knot Operators
```
B  Knot-Binding (left corridor)         λ_B = 0.618
C  Cross-Pillar Knot (symmetry axis)    λ_C = 0.500
T  Triadic Closure (full envelope)      λ_T = 0.333
A  Apex Knot (apex neighborhood)        λ_A ≈ 0.400
S  Stability Knot (crossing regions)    λ_S < 1.000
```

### State Variables
```
Ψ, Ψ₀, Ψₙ    Pattern states (Phoenix)
K, K₀, Kₙ    Knot states (The Third)
H            Hydrogenesi structures
X, △         Apex Point
```

---

## Convergence Formulas

### Basic Convergence
```
Kₙ₊₁ = O(Kₙ)  for operator O

lim (n→∞) Kₙ = X  (always converges to apex)
```

### Distance After n Iterations
```
d(Kₙ, X) ≤ λⁿ · d(K₀, X)

where λ is the operator's contraction constant
```

### Convergence Time Estimates
```
For 99% convergence (d < 0.01 · d₀):

Operator B: n > 10 iterations
Operator C: n > 7 iterations
Operator T: n > 5 iterations
```

---

## Fixed Point Property

### Operator Invariance
```
For all knot operators O:
  O(X) = X

Apex is fixed under all operations
```

### Contraction Mapping
```
For operator O with constant λ < 1:
  d(O(K), X) ≤ λ · d(K, X)

Strict inequality when K ≠ X
```

---

## Symmetry Properties

### 120° Rotation
```
R₁₂₀(Phoenix) = Hydrogenesi
R₁₂₀(Hydrogenesi) = Third
R₁₂₀(Third) = Phoenix
R₁₂₀(X) = X  (apex is fixed)
```

### Symmetry Group
```
G = {I, R₁₂₀, R₂₄₀}
|G| = 3  (cyclic group C₃)
R₁₂₀³ = I
```

---

## Common Sequences

### Simple Binding
```
K₀ = initial state
Kₙ₊₁ = B(P, Kₙ)  (repeat B operator)
lim Kₙ → X
```

### Optimal Sequence
```
K₁ = B(P, K₀)      [Knot-Binding]
K₂ = C(P, H, K₁)   [Cross-Pillar]
K₃ = T(P, H, K₂)   [Triadic Closure]
K₄₊ₙ = Aⁿ(K₃)      [Apex iterations]
lim Kₙ → X
```

### Full Triadic Loop
```
P = ⊕(∅) → ⊗ → ⊛ → △    [Phoenix transform]
H = lineage(P)           [Hydrogenesi preserve]
K = T(P, H, K₀)          [The Third bind]
X = lim Aⁿ(K)            [Apex converge]
```

---

## Key Theorems

### Theorem 1: Convergence
```
All operator sequences converge to X
```

### Theorem 2: Uniqueness
```
X is the unique fixed point
∄ Y ≠ X with A(Y) = Y
```

### Theorem 3: Stability
```
Small perturbations decay exponentially
X is a stable attractor
```

### Theorem 4: Path Independence
```
All paths lead to X
Different operators → different speeds → same destination
```

---

## Useful Inequalities

### Triangle Inequality (weak form)
```
d(K₁, X) ≤ d(K₁, K₂) + d(K₂, X)
```

### Monotone Decrease
```
d(K₀, X) > d(K₁, X) > d(K₂, X) > ... > 0
```

### Exponential Bound
```
d(Kₙ, X) ≤ λⁿ · d(K₀, X) < ε  for sufficiently large n
```

---

## Contraction Constants Summary

| Operator | Symbol | Constant λ | Convergence Speed |
|----------|--------|-----------|-------------------|
| Knot-Binding | B | 0.618 | Moderate |
| Cross-Pillar | C | 0.500 | Fast |
| Triadic Closure | T | 0.333 | Fastest |
| Apex Knot | A | ~0.400 | Fast (near apex) |
| Composite B→C→T | - | ~0.103 | Very fast |

---

## Quick Checks

### Is K at apex?
```
Check: d(K, X) < ε  for small ε
If true: K ≈ X (at apex)
```

### Is X a fixed point?
```
Check: A(X) = X
Check: d(A(X), X) = 0
Both should be true
```

### Does sequence converge?
```
Check: d(Kₙ₊₁, X) < d(Kₙ, X)  for all n
If true: sequence converges
```

---

## Common Calculations

### Iterations to reach threshold
```
Given: target distance d_target
Find: n such that λⁿ · d₀ < d_target

Solution: n > log(d_target / d₀) / log(λ)
```

### Distance after n steps
```
Given: initial distance d₀, operator λ, iterations n
Find: d(Kₙ, X)

Solution: dₙ = λⁿ · d₀
```

### Composite contraction constant
```
Given: sequence O₁ → O₂ → O₃
Find: effective λ

Solution: λ_composite = λ₁ · λ₂ · λ₃
```

---

## Typical Values

### Initial Distance
```
d₀ = 1.0  (normalized, typical starting point)
```

### Apex Tolerance
```
ε = 0.001  (within 0.1% considered "at apex")
ε = 0.01   (within 1% considered "near apex")
```

### Iteration Counts
```
Typical: 5-10 iterations for T operator
Typical: 10-15 iterations for B operator
Typical: 3-5 iterations for B→C→T sequence
```

---

## Visual Symbols

```
●  Knot state K
△  Apex point X
→  Operator application
↓  Convergence direction
⟡  Apex emphasis
```

---

## Cross-References

### Detailed Documentation
- [Apex Point Mathematics](./apex-point-mathematics.md) - Complete mathematical treatment
- [Apex Convergence Visualization](./Diagrams/apex-convergence-visualization.md) - Visual diagrams
- [Apex Convergence Example](./Examples/apex-convergence.md) - Numerical examples

### Operators
- [Knot-Binding (B)](./Operators/knot-binding.md)
- [Cross-Pillar Knot (C)](./Operators/cross-pillar-knot.md)
- [Triadic Closure (T)](./Operators/triadic-closure.md)
- [Apex Knot (A)](./Operators/apex-knot.md)
- [Stability Knot (S)](./Operators/stability-knot.md)

### Laws
- [Apex Formation](./Universal-Laws/universal/apex-formation.md)
- [Apex Continuity](./Universal-Laws/apex/apex-continuity.md)
- [Apex Recursion Limit](./Universal-Laws/apex/apex-recursion-limit.md)

---

[◀ Apex Point Mathematics](./apex-point-mathematics.md) | [Main README](../README.md) | [Visualization ▶](./Diagrams/apex-convergence-visualization.md)
