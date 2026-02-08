# A-3: Apex Recursion Limit Law

**Layer**: Apex | **Sigil**: ⊢ | **ID**: A-3 | **Status**: Active

## Formal Statement

**Depth is bounded to prevent infinite loops.**

Recursive apex operations must have enforced depth limits. Unbounded recursion leads to stack overflow, infinite loops, and system instability. Practical bounds ensure termination.

## Mathematical Expression

```
Let MAX_APEX_DEPTH = system-defined constant

For recursive apex operation R:

depth(R(input, d)) where:
  if d ≥ MAX_APEX_DEPTH:
    raise RecursionLimitError
  if base_case(input):
    return base_value(input)
  else:
    return combine(R(decompose(input), d+1))

Guarantee: ∀input: ∃n < MAX_APEX_DEPTH: reaches base case within n steps
```

## Explanation

While recursion is powerful (S-3, U-1), unbounded recursion is dangerous. A-3 provides practical limits that enable the power of recursion while preventing its pathologies.

### Typical Limits
- **Operator Composition**: 100-1000 levels
- **Ritual Nesting**: 10-50 levels
- **Triad Deliberation**: 3-10 recursive reviews
- **Synthesis Depth**: 5-20 levels

### When Limits Hit
If recursion limit reached:
1. Log the occurrence
2. Attempt graceful degradation
3. Return partial result if possible
4. Raise clear error if not

### Applications
- Prevents infinite loops in apex synthesis
- Guards against runaway recursion
- Ensures timely termination

## Cross-References
- **Constrains**: [U-1: Recursive Identity](../universal/recursive-identity.md)
- **Validates**: [S-3: Recursion](../substrate/recursion.md)

---

**Navigation**: [← A-2](./reversible-apex-operator.md) | [Apex README](./README.md) | [→ A-4](./apex-harmonic-convergence.md)
