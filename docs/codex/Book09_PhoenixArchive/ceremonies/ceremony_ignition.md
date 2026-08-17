# Ceremony: Ignition

## Purpose and Outcome
Initialize Phoenix sequence from void state. Expected outcome is a verifiable state transition with logged evidence.

## Prerequisites
- Knowledge: Books 05, 09, and 11 references.
- Operators: [op_genesis](../../Book05_OperatorsAtlas/operators/op_genesis.md), [op_harmonic](../../Book05_OperatorsAtlas/operators/op_harmonic.md)
- Materials: operator ledger, harmonic timing chart, and verification checklist.

## Sequence
1. Pre-check invariants and baseline state.
2. Invoke operators in prescribed order with harmonic cues.
3. Capture state snapshots after each major step.
4. Execute final verification and archive the result.

## Diagram
- [Flow chart](../../../diagrams/ceremonies/ceremony_flows/ceremony_ignition_flow.md)
- [Timing chart](../../../diagrams/ceremonies/timing_charts/ceremony_ignition_timing.md)

## Verification
Use [verification_matrix.md](verification_matrix.md) and confirm pass criteria for `Ignition`.

## Variation Options
- Short-form local execution (single-node)
- Full triadic execution (multi-engine)

## See Also
- [Ceremony Index](index.md)
- [Operator Dashboard](../../Book05_OperatorsAtlas/operators/index.md)
- [Animation Guides](../../../../diagrams/animations/)
- [Engine Comparison](../../../engines/engine_comparison.md)
