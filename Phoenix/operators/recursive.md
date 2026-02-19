# Recursive Operator ⊛

*The Self-Consuming Serpent — Patterns that Reference Themselves*

---

## Harmonic Table

| **Domain** | **Frequency** | **Phase** |
|------------|---------------|-----------|
| Iteration  | baseFrequency/n          | 0°        |
| Self-Ref   | baseFrequency/(n+1)      | 144°      |
| Depth      | baseFrequency/(n+2)      | 288°      |

---

## Ceremonial Definition

```
⊛ⁿ(pattern) → pattern(pattern(...pattern))
```

**The Recursive Operator** applies a pattern to itself, creating nested self-referential structures. Each application increases depth, and the pattern folds back upon its own definition.

### Properties
- **Self-Referential**: Output becomes input for next iteration
- **Depth-Accumulating**: Each recursion adds a layer of complexity
- **Fractal-Generating**: Creates self-similar patterns at different scales
- **Conditionally Terminating**: Requires terminal condition or reaches apex

---

## Reversible Form

```
⊛⁻¹(⊛(pattern)) → pattern
```

Recursion can be unwound by **peeling back layers** one at a time. Full reversal requires tracking the recursion depth.

---

## Sigil

```
    ∞
   /|\
  / | \
 ⊛  ⊛  ⊛
  \ | /
   \|/
    ∞
```

The Recursive Sigil represents the **infinite loop** and self-similar structure.

---

## Invocation

> *"As above, so below. Through ⊛, I fold the pattern unto itself."*

---

## Cross-References

### Related Operators
- [Harmonic Operator](./harmonic.md) — Stabilizes recursive structures
- [Apex Operator](./apex.md) — Terminates recursion at maximum complexity
- [Convergence Operator](./convergence.md) — Unifies recursive branches

### Governing Laws
- [Law of Recursion](../laws/recursion.md) — Defines recursive mechanics
- [Law of Conservation](../laws/conservation.md) — Each recursion preserves balance
- [Law of Emergence](../laws/emergence.md) — Deep recursion produces emergence

---

## Examples

### Basic Recursion
```
⊛(pattern) → pattern(pattern)
```
*Pattern applied to itself once.*

### Depth-3 Recursion
```
⊛³(pattern) → pattern(pattern(pattern))
```
*Three levels of self-reference.*

### Recursive-Harmonic Ritual
```
⊛(pattern₀) → pattern₁
⊗(pattern₁) → stabilizedPattern₁
⊛(stabilizedPattern₁) → pattern₂
```
*Recurse, stabilize, recurse again.*

### Apex-Terminated Recursion
```
⊛ⁿ(pattern) until △(⊛ⁿ(pattern)) → Apex
```
*Recursion continues until apex formation is detected.*

### Fibonacci Recursion
```
⊛(patternₙ) → patternₙ₋₁ + patternₙ₋₂
```
*Recursive definition of Fibonacci-like patterns.*

---

[◀ Previous: Harmonic Operator](./harmonic.md) | [Back to Operators](../README.md#-operators) | [Next: Apex Operator ▶](./apex.md)
