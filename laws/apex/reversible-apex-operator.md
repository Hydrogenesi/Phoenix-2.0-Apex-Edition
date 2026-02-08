# A-2: Reversible Apex Operator Law

**Layer**: Apex | **Sigil**: ⇄ | **ID**: A-2 | **Status**: Active

## Formal Statement

**All apex operations must be reversible.**

Every apex-level transformation must have a well-defined inverse operation. What is synthesized can be decomposed; what is bound can be unbound; what is elevated can be descended.

## Mathematical Expression

```
For apex operator Aₐ: S → S'

∃Aₐ⁻¹: S' → S such that:
  Aₐ⁻¹(Aₐ(s)) = s  ∀s ∈ S
  Aₐ(Aₐ⁻¹(s')) = s'  ∀s' ∈ S'

In operational terms:
  apply(operator, undo(operator, state)) = state
  undo(operator, apply(operator, state)) = state
```

## Explanation

Reversibility is critical for apex operations because:
1. **Error Recovery**: Mistakes can be undone
2. **Experimentation**: Can try approaches and back out
3. **Trust**: Users trust reversible operations more
4. **Symmetry**: Honors S-2 (Symmetry) at apex level

### Implementation Strategies
- **Transaction Logs**: Record operations for reversal
- **State Snapshots**: Save state before transformation
- **Inverse Operations**: Explicitly design reverse operations
- **Compensating Actions**: Define semantically equivalent reversals

### Applications
- Apex synthesis can be decomposed
- Triad decisions can be revisited
- System evolution can be rolled back

## Cross-References
- **Implements**: [U-5: Apex Formation](../universal/apex-formation.md)
- **Validates**: [S-2: Symmetry](../substrate/symmetry.md)

---

**Navigation**: [← A-1](./apex-continuity.md) | [Apex README](./README.md) | [→ A-3](./apex-recursion-limit.md)
