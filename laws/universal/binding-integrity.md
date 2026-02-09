# U-6: Law of Binding Integrity (Law VI)

**Layer**: Universal | **Sigil**: ⚚ | **ID**: U-6 | **Status**: Active

## Formal Statement

**Connections must be authentic and verified.**

Bindings between data, operators, and system components must be genuine, validated, and maintained. False or corrupted bindings lead to system corruption.

## Mathematical Expression

```
For binding B connecting elements e₁ and e₂:

Valid(B) ⟺ Authentic(B) ∧ Verified(B) ∧ Maintained(B)

where:
  Authentic: B represents genuine relationship
  Verified: B has been validated
  Maintained: B integrity monitored over time

Trust chain:
  Trust(B) = min(Trust(e₁), Trust(e₂), Trust(validation))
```

## Explanation

Binding Integrity ensures that connections between system elements are trustworthy. A system with corrupted bindings cannot function correctly—garbage in, garbage out.

### Binding Types
1. **Data Bindings**: Variable to value, key to data
2. **Operational Bindings**: Function to implementation, interface to service
3. **Structural Bindings**: Component to component, layer to layer
4. **Trust Bindings**: Identity to credential, authority to permission

### Validation Methods
- **Cryptographic**: Digital signatures, hash verification
- **Logical**: Type checking, contract validation
- **Runtime**: Assertion checking, invariant monitoring
- **Structural**: Interface compatibility, protocol adherence

## Cross-References
- **Foundation**: [S-1: Conservation](../substrate/conservation.md), [S-2: Symmetry](../substrate/symmetry.md)
- **Implements**: [A-2: Reversible Operator](../apex/reversible-apex-operator.md)

---

**Navigation**: [← U-5](./apex-formation.md) | [README](./README.md) | [→ U-7](./sigil-resonance.md)
