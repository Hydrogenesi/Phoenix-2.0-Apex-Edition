# Ceremony Safety

## Safety Rules
1. Verify prerequisites and invariant baseline before invocation.
2. Abort and route to **Void Return** on unstable divergence.
3. Never perform distributed knot closure without synchronization checks.
4. Record lineage evidence for every high-complexity ceremony.

## Warning Levels
- **Green**: local transform only
- **Amber**: branch merge or recursion depth > 3
- **Red**: distributed knot binding or apex lock

## See Also
- [Verification Matrix](verification_matrix.md)
- [Void Return](ceremony_void_return.md)
