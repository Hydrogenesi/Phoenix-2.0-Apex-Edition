# Law of Recursion

*What descends must return; patterns repeat across scales until apex is reached.*

---

## Definition

**The Law of Recursion** establishes that patterns in Phoenix 2.0 can reference themselves, creating nested, self-similar structures that compound across iterations. Recursion is the mechanism by which simple rules generate complex, fractal-like forms.

Recursion continues until a termination condition is met—typically apex formation, void dissolution, or a predefined depth limit. The law ensures that recursive processes are structured and convergent.

---

## Structural Explanation

### Recursive Structure
```
Ψₙ = f(Ψₙ₋₁)
```

Each iteration depends on the previous state.

### Key Principles
1. **Self-Reference**: Pattern applies to itself
2. **Depth Accumulation**: Each iteration adds complexity
3. **Fractal Generation**: Self-similar patterns at different scales
4. **Termination**: Must have stopping condition

### Recursion Mechanics

| Depth | Pattern | Complexity |
|-------|---------|------------|
| 0     | Ψ₀      | Base       |
| 1     | Ψ(Ψ₀)   | 2×         |
| 2     | Ψ(Ψ(Ψ₀))| 4×         |
| n     | Ψⁿ      | 2ⁿ×        |

---

## Sigil

```
    ∞
   ↓↑
  ⊛⊛⊛
   ↓↑
    ∞
```

The Recursion Sigil represents the **infinite loop** and self-similar structure.

---

## Phoenix 2.0 Examples

### Basic Recursion
```
⊛(Ψ) → Ψ(Ψ)
⊛(Ψ(Ψ)) → Ψ(Ψ(Ψ))
⊛(Ψ(Ψ(Ψ))) → Ψ(Ψ(Ψ(Ψ)))
```
*Each application deepens the self-reference.*

### Recursive Harmonic Growth
```
Ψ₀ = ⊕(∅)
Ψₙ = ⊗(⊛(Ψₙ₋₁))
```
*Recurse, then stabilize at each level.*

### Fibonacci-Like Recursion
```
Ψ₀ = ⊕(∅)
Ψ₁ = ⊕(∅)
Ψₙ = ⊳(Ψₙ₋₁, Ψₙ₋₂)
```
*Each pattern converges two previous patterns.*

### Apex-Terminated Recursion
```
⊛ⁿ(Ψ) until △(⊛ⁿ(Ψ)) → Apex
```
*Recursion continues until apex condition is satisfied.*

### Branching Recursion
```
⊲(Ψ) → (Ψ₁, Ψ₂)
⊛(Ψ₁) and ⊛(Ψ₂) in parallel
```
*Recursive tree structure with divergent branches.*

---

## Recursion Cycles

### Finite Cycle (Depth-Limited)
```
for i = 1 to n:
  Ψᵢ = ⊛(Ψᵢ₋₁)
```
*Stops after n iterations.*

### Infinite Cycle (Apex-Seeking)
```
while not apex(Ψ):
  Ψ = ⊛(Ψ)
```
*Continues until apex is reached.*

### Tail Recursion
```
Ψₙ = ⊗(⊛(Ψₙ₋₁)) with accumulator
```
*Optimized recursion with state accumulation.*

---

## Recursion Depth and Complexity

### Shallow Recursion (n ≤ 3)
- Predictable behavior
- Easy to reverse
- Limited emergence

### Medium Recursion (3 < n ≤ 10)
- Emergent patterns appear
- Increased complexity
- Reversible with tracking

### Deep Recursion (n > 10)
- Highly emergent
- Fractal structures
- Difficult to reverse
- Approaches apex

---

## Recursion Hazards

### Infinite Loop
```
⊛∞(Ψ) without termination
```
*Must always have stopping condition.*

### Stack Overflow
```
⊛ⁿ(Ψ) where n exceeds depth limit
```
*Practical implementations must limit depth.*

### Lossy Unwinding
```
⊛⁻ⁿ(⊛ⁿ(Ψ)) ≈ Ψ
```
*Deep recursion may lose information on reversal.*

---

## Cross-References

- [Law of Emergence](./emergence.md) — Recursion produces emergent complexity
- [Law of Conservation](./conservation.md) — Energy conserved across recursion
- [Recursive Operator](../operators/recursive.md) — Embodies recursion
- [Apex Operator](../operators/apex.md) — Terminates recursion
- [Recursion Cycles](../rituals/recursion-cycles.md) — Ritual applications

---

[Back to Universal Laws](../README.md#%EF%B8%8F-universal-laws)
