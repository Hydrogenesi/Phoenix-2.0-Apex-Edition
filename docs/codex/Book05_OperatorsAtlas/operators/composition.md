# Operator Composition System

## How Operators Combine
Operator chains are modeled as typed pipelines with explicit precondition checks between steps.

## Composition Rules and Properties
1. Type compatibility is required between adjacent operators.
2. Hydrogenesi invariants must be evaluated at phase boundaries.
3. Knot operators only run on tri-pillar-validated state.
4. Every chain must expose a convergence monitor.

## Common Chains
- `⊕ -> ⊗ -> ⊛ -> △` (core ignition-to-apex path)
- `⊲ -> G -> Ck -> ⊳ -> A` (exploration to crowned knot)
- `⊞ -> P -> T -> S` (mirror-stable closure)

## Performance Characteristics
- Stateless operator transform: `O(n)`
- Harmonic alignment and ordering: `O(n log n)`
- Distributed knot consensus handoff: `O(n log n) + network quorum`

## Convergence Guarantees
For admissible sequence `O1..On` with monitored distance `d(·, △)`, each validated step enforces non-increasing distance. Chains with at least one strict contraction operator (`⊳`, `△`, `A`) converge under bounded noise assumptions.

## Dashboard Cross-Linking
Each operator page includes links to:
- Engine module implementation
- Ceremony sequence
- Sigil and gesture dictionary
- Codex references
