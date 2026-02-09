# Cross-Layer Mapping Tables

## Vertical Integration Mappings

These tables provide explicit mappings between Substrate, Universal, and Apex layers, enabling developers to understand operator correspondence, transformation pathways, and resonance relationships across the Triadic architecture.

```
╔════════════════════════════════════════════════════╗
║           OPERATOR LAYER MAPPING                   ║
╠═══════════════╦═══════════════╦═══════════════════╣
║   SUBSTRATE   ║   UNIVERSAL   ║      APEX         ║
╠═══════════════╬═══════════════╬═══════════════════╣
║ map()         ║ lawMap()      ║ apexMap()         ║
║ filter()      ║ lawFilter()   ║ apexFilter()      ║
║ reduce()      ║ lawReduce()   ║ apexReduce()      ║
║ store()       ║ resStore()    ║ canonStore()      ║
║ retrieve()    ║ resRetrieve() ║ canonRetrieve()   ║
║ sequence()    ║ lawSequence() ║ convergeSeq()     ║
║ branch()      ║ resBranch()   ║ apexBranch()      ║
║ aggregate()   ║ harmAggregate║ synthAggregate()  ║
╚═══════════════╩═══════════════╩═══════════════════╝
```

## Transformation Pathways

**Elevation Protocol**: When an operation requires elevation from Substrate to Universal, the system applies Law wrapping. Universal to Apex elevation applies canonical optimization. Each transition preserves semantic meaning while enhancing operational characteristics.

**Descent Protocol**: Apex operations may descend to Universal or Substrate for specific sub-operations. This maintains efficiency by executing primitives at appropriate layers. Descent unwraps enhancements while preserving core operation.

## Resonance Mapping

```
SUBSTRATE FREQUENCY → UNIVERSAL RESONANCE → APEX HARMONY

Base Hz Range        Law-Modulated Range    Canonical Range
[0-100 Hz]    →     [100-1000 Hz]    →    [1000+ Hz]

ψ_substrate   →     Σ(Laws) * ψ     →    ∫ ψ_canon
```

Each layer operates at characteristic frequency ranges. Universal layer modulates Substrate frequencies through Law application. Apex achieves harmonic convergence through integration. See [../sigils/resonance-law.md](../sigils/resonance-law.md) for detailed mechanics.

## Sigil Correspondence

Operators possess corresponding sigils across layers. Substrate sigils mark primitive operations, Universal sigils incorporate Law symbols, Apex sigils represent canonical forms. The [../sigils/binding-tables.md](../sigils/binding-tables.md) provides complete sigil mappings.

## Usage Examples

To invoke cross-layer operation: `apexMap(data)` internally calls `lawMap(map(data))`, passing through all three layers with appropriate transformations at each boundary.

Reference [operator-families.md](operator-families.md) for family-specific mappings and [canon-apex-edition.md](canon-apex-edition.md) for canonical specifications.

---

*Maps guide the journey between layers—transformation codified.*
