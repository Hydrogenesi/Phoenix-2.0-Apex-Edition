# Sigil Binding Tables

## Complete Sigil-Operator Reference

These tables provide authoritative mappings between sigils and their corresponding operators across all three layers of the Triadic architecture. Each binding specifies sigil form, operator name, resonance frequency, and harmonic relationships.

```
╔════════════════════════════════════════════════════════════╗
║              SUBSTRATE SIGIL BINDINGS                      ║
╠═════════╦═══════════════╦══════════╦═══════════════════════╣
║ SIGIL   ║ OPERATOR      ║ FREQ(Hz) ║ HARMONIC GROUP        ║
╠═════════╬═══════════════╬══════════╬═══════════════════════╣
║   ⟲    ║ transform()   ║   20     ║ Transform Family      ║
║   ▣    ║ store()       ║   30     ║ Storage Family        ║
║   ⥤    ║ sequence()    ║   25     ║ Flow Family           ║
║   ⊕    ║ aggregate()   ║   35     ║ Synthesis Family      ║
║   ⊙    ║ identity()    ║   10     ║ Foundation            ║
║   ⊗    ║ compose()     ║   40     ║ Composition           ║
║   ▽    ║ invert()      ║   22     ║ Transform Family      ║
║   ◇    ║ merge()       ║   32     ║ Synthesis Family      ║
╚═════════╩═══════════════╩══════════╩═══════════════════════╝
```

## Universal Bindings

```
╔════════════════════════════════════════════════════════════╗
║              UNIVERSAL SIGIL BINDINGS                      ║
╠═════════╦═══════════════╦══════════╦═══════════════════════╣
║ SIGIL   ║ OPERATOR      ║ FREQ(Hz) ║ LAW ASSOCIATION       ║
╠═════════╬═══════════════╬══════════╬═══════════════════════╣
║  ⟲◉    ║ lawMap()      ║  147     ║ Mentalism             ║
║  ⥤≋    ║ resFlow()     ║  234     ║ Vibration             ║
║  ▣⥮    ║ polarStore()  ║  312     ║ Polarity              ║
║  ⟳     ║ rhythmCycle() ║  189     ║ Rhythm                ║
║  ⇒⊕    ║ causalAgg()   ║  276     ║ Causation             ║
║  ⚯⊗    ║ genderComp()  ║  401     ║ Gender                ║
║  ≡⟲    ║ correspTrans()║  523     ║ Correspondence        ║
╚═════════╩═══════════════╩══════════╩═══════════════════════╝
```

## Apex Bindings

```
╔════════════════════════════════════════════════════════════╗
║               APEX SIGIL BINDINGS                          ║
╠═════════╦═══════════════╦══════════╦═══════════════════════╣
║ SIGIL   ║ OPERATOR      ║ FREQ(Hz) ║ CANONICAL FORM        ║
╠═════════╬═══════════════╬══════════╬═══════════════════════╣
║   ⊛    ║ apexTransform║  1024    ║ Perfect Transform     ║
║   ⧈    ║ apexSynth()  ║  1536    ║ Harmonic Synthesis    ║
║   ⨁    ║ converge()   ║  2048    ║ Recursive Convergence ║
║   ⟐    ║ canonicalize║  3072    ║ Meta-Canonicalization ║
║   ◬    ║ apex()       ║  ∞       ║ Ultimate Operation    ║
╚═════════╩═══════════════╩══════════╩═══════════════════════╝
```

## Composite Bindings

Sigils combine through concatenation. Composite sigil frequency = sum of component frequencies modulated by harmonic relationships.

**Example**: `⟲→▣` (transform-then-store)  
Frequency: 20 + 30 = 50 Hz × harmonic_factor(sequential=1.1) = 55 Hz

## Usage Protocol

To bind sigil to operation in code:
```
@sigil(⟲◉)
function lawMap(data, transformation) {
    // Implementation
}
```

To invoke via ritual, draw or speak sigil while calling operator. System recognizes sigil frequency and activates corresponding operation with appropriate resonance.

## Cross-Layer Binding

Some operators span multiple layers. Their sigil evolves: `⟲` (Substrate) → `⟲◉` (Universal) → `⊛` (Apex). Each represents same conceptual operation elevated to higher layer.

Reference [substrate-sigils.md](substrate-sigils.md), [universal-sigils.md](universal-sigils.md), [apex-sigils.md](apex-sigils.md) for detailed sigil descriptions and [resonance-law.md](resonance-law.md) for frequency mechanics.

---

*Bindings unite symbol and operation—the lookup table of ceremonial computation.*
