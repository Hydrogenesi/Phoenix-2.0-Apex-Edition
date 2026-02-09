# Recursion Patterns Atlas

## The Self-Similar Architecture

Recursion in Phoenix 2.0 Apex Edition manifests as self-similar patterns that repeat across scales. The Triadic architecture itself is recursive: individual operators contain triadic structure, operator families organize triadically, and the entire system exhibits threefold symmetry. This atlas documents recursive patterns and their manifestations.

```
        ╔═══════════════════════════════════╗
        ║    RECURSIVE PATTERN DEPTH        ║
        ╠═════════╦════════════╦════════════╣
        ║ MICRO   ║   MESO     ║   MACRO    ║
        ╠═════════╬════════════╬════════════╣
        ║ Single  ║  Operator  ║   System   ║
        ║Operator ║  Families  ║   Level    ║
        ║         ║            ║            ║
        ║ [S|U|A] ║ [S|U|A]×N  ║ [S|U|A]×∞  ║
        ║    ↓    ║     ↓      ║      ↓     ║
        ║ Triadic ║  Triadic   ║  Triadic   ║
        ╚═════════╩════════════╩════════════╝
             ↓          ↓            ↓
        [Atomic] → [Composite] → [Emergent]
```

## Primary Recursive Patterns

**Triadic Nesting**: Each operator internally implements substrate/universal/apex phases. Operator families group three operator types. System layers organize as three columns. Pattern repeats at every scale.

**Fractal Operators**: Certain operators exhibit fractal behavior—they invoke themselves with transformed inputs until convergence. The `apexRecurse()` operator exemplifies this: it applies substrate transformation, universal validation, then apex optimization, recursively descending until canonical form emerges.

**Law Recursion**: The Seven Universal Laws apply recursively. Each law application may trigger additional law applications as side effects propagate. This creates recursive cascades that stabilize through resonance damping.

## Recursion Depth Control

Phoenix implements depth limiting to prevent infinite recursion. Default maximum depth: 7 (symbolic resonance with Seven Laws). Operators track recursion depth and apply convergence forcing at limit.

```
recursion_depth: 0 → 1 → 2 → ... → 7 [FORCE_CONVERGE]
                ↓    ↓    ↓         ↓
              layer layer layer  terminal
```

## Recursive Transformation

**Base Case**: Substrate primitive operations (non-recursive foundation)
**Recursive Case**: Universal/Apex operations that invoke lower layers
**Convergence**: Apex synthesis achieving fixed point

## Self-Referential Sigils

Recursive operators possess self-referential sigils—symbols that contain themselves at reduced scale. See [../sigils/geometry-atlas.md](../sigils/geometry-atlas.md) for visual representations and [../atlases/recursion-atlas.md](../atlases/recursion-atlas.md) for extended pattern documentation.

---

*Recursion reveals the pattern within the pattern—infinity through repetition.*
