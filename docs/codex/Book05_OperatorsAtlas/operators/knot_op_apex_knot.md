# Apex Knot

## Symbol
`A`

## Name & Pillar
- **Name**: Apex Knot
- **Pillar**: Knot

## Type
`knot -> apex_knot`

## Definition
For state `x`, `A(x)` applies the canonical apex knot transform while preserving admissible invariants.

## Axioms
1. Deterministic under fixed parameters.
2. Compatible with triadic composition.
3. Monotonic contribution toward apex distance reduction in valid chains.

## Invariants
- Identity trace remains auditable.
- Harmonic phase labels remain valid.
- Safety constraints remain bounded.

## Preconditions
- Input state has valid schema and harmonic tag.
- Required context vector and threshold window are provided.

## Postconditions
- Output state records operator lineage.
- Verification checkpoint is emitted for ceremony replay.

## Invocation Patterns
```text
prepare(state)
state' = A(state)
verify_invariants(state')
```

## Examples
```text
state = load_seed("plate-A")
state = A(state)
state = verify(state, mode="strict")
```

## Tri-Link Dashboard
- **Engine module**: [Module reference](../../../engines/architecture.md#multi-engine-reference-plate-map)
- **Ceremony sequence**: [Linked ceremony](../../Book09_PhoenixArchive/ceremonies/ceremony_apex_knot_crowning.md)
- **Sigil**: [Sigil dictionary](../../Book09_PhoenixArchive/ceremonies/sigils.md#sigil-apex-knot)
- **Gesture**: [Gesture dictionary](../../Book09_PhoenixArchive/ceremonies/gestures.md#gesture-apex-crown)
- **Codex references**: [Operators index](index.md), [Composition system](composition.md), [Book 09 ceremonies](../../Book09_PhoenixArchive/ceremonies/index.md)

## Cross-References
- [Master operator index](index.md)
- [Operator composition system](composition.md)

## Chapter References
- [Book 05 — Operator Foundations](../chapters/chapter_01_operator_foundations.md)
- [Book 11 — Advanced Composition](../../Book11_OperatorsTestament/INDEX.md)
- [Book 12 — Implementation Patterns](../../Book12_PhoenixOdyssey/INDEX.md)
