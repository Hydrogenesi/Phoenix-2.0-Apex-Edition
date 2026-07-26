# 🌀 Fractal Engine — Master Architecture

*The recursive cinematic system: Galactic → Solar → Jupiter → Earth → Micro-field*

---

## 🎯 Overview

The **Fractal Engine** is the operator-grade production system that drives Phoenix 2.0's cinematic and visualization layer. Where the [Apex Engine](../Phoenix/apex-engine/README.md) formalizes the theoretical convergence mechanics of the Triadic Cycle, the Fractal Engine is the **rendering instrument** — an AE-ready (Adobe After Effects), modular, recursive rig that turns those mechanics into a scalable visual sequence, from galactic scale down to micro-field detail.

It is not a single module — it is the entire recursive architecture, structured so it can be dropped into any Dynamo rig, any Codex ceremonial sequence, or any cinematic timeline.

**Domain**: Cinematic rendering / visualization layer
**Classification**: Production Engine (AE-ready, operator-grade, recursive)
**Related**: [Reproduction Engine](../Phoenix/apex-engine/engines/reproduction-engine.md) (fractal/self-similar pattern generation), [Apex Formation Operator (△)](../ApexLaw/)

---

## 🧩 1 — Master Comps

The backbone of the engine. Every sub-comp nests into `FRACTAL_ENGINE_MASTER_4K`.

- `FRACTAL_ENGINE_MASTER_4K`
- `FRACTAL_ENGINE_CTRL`
- `FRACTAL_ENGINE_RECURSION`
- `FRACTAL_ENGINE_DYNAMO_CORE`
- `FRACTAL_ENGINE_DYNAMO_TORUS`
- `FRACTAL_ENGINE_FIELD_SHELL`
- `FRACTAL_ENGINE_AURORA`
- `FRACTAL_ENGINE_HUD_RITUAL`

---

## 🔧 2 — Control Hub (Rig Brain)

Inside `FRACTAL_ENGINE_CTRL` — the global conductor every other layer listens to:

| Control | Type | Scale |
|---|---|---|
| `MACRO_SPEED` | Slider | Galactic |
| `MESO_SPEED` | Slider | Solar |
| `SUB_SPEED` | Slider | Jupiter |
| `MICRO_SPEED` | Slider | Earth |
| `FIELD_INTENSITY` | Slider | Field shell |
| `AURORA_RATE` | Slider | Aurora pulse |
| `RECURSION_DEPTH` | Slider (0–12) | Recursion layers |
| `PHASE_OFFSET` | Slider | Recursion layers |
| `CEREMONIAL_MODE` | Checkbox | Global amplification |

---

## 🔁 3 — Recursive Motion Engine

Inside `FRACTAL_ENGINE_RECURSION`. Applied to the rotation of each recursion layer — deeper layers rotate faster, phase offsets stack, and the recursion reads as alive:

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
var depth = ctrl.effect("RECURSION_DEPTH")("Slider");
var phase = ctrl.effect("PHASE_OFFSET")("Slider");
var speed = (index * 0.1) * depth;
(time * speed * 20) + (phase * index);
```

---

## 🌀 4 — Dynamo Core Block

Inside `FRACTAL_ENGINE_DYNAMO_CORE`. Merges all dynamo layers into one unified rotation:

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
var macro = ctrl.effect("MACRO_SPEED")("Slider");
var meso = ctrl.effect("MESO_SPEED")("Slider");
var sub = ctrl.effect("SUB_SPEED")("Slider");
var micro = ctrl.effect("MICRO_SPEED")("Slider");
(time * (macro + meso + sub + micro)) * 10;
```

---

## 🧿 5 — Torus Block (Counter-Rotation)

Inside `FRACTAL_ENGINE_DYNAMO_TORUS`. Counter-rotation gives the engine its signature dynamo feel:

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
var sub = ctrl.effect("SUB_SPEED")("Slider");
-(time * sub * 15);
```

---

## 🌐 6 — Field Shell Block

Ties the EM shell's opacity/glow intensity to the global field state:

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
ctrl.effect("FIELD_INTENSITY")("Slider");
```

---

## 🌈 7 — Aurora Block (Pulse Engine)

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
var rate = ctrl.effect("AURORA_RATE")("Slider");
40 + Math.sin(time * rate * 2) * 60;
```

Ceremonial mode adds amplification:

```javascript
var ceremonial = ctrl.effect("CEREMONIAL_MODE")("Checkbox");
ceremonial ? value + 20 : value;
```

---

## 🔮 8 — HUD Ritual Layer

Opacity, tied to ceremonial mode:

```javascript
var ctrl = thisComp.layer("FRACTAL_ENGINE_CTRL");
ctrl.effect("CEREMONIAL_MODE")("Checkbox") ? 100 : 0;
```

Text fields:

- "Fractal Engine — Turning of All Plates"
- "Macro → Meso → Sub → Micro → Consciousness"

---

## 🎨 9 — Color Script

| Layer | Color |
|---|---|
| Macro | Deep crimson |
| Meso | Gold |
| Sub | Amber |
| Micro | Electric teal |
| Field | Ultraviolet |
| Aurora | Violet-blue |

Matches the Phoenix-Codex palette.

---

## 🔊 10 — Sound Hooks

| Hook | Driven by |
|---|---|
| Low drone | `MACRO_SPEED` |
| Mid pulse | `AURORA_RATE` |
| High shimmer | `RECURSION_DEPTH` |

---

## 🎙️ 11 — VO Hook

Standard invocation line:

> "The plates turn. The recursion awakens. The engine remembers itself."

---

## 🔥 12 — Plug-In Instructions

Drop all sub-comps into `FRACTAL_ENGINE_MASTER_4K`, in this order:

1. Dynamo Core
2. Torus
3. Field Shell
4. Aurora
5. Recursion layers (duplicated N times, per `RECURSION_DEPTH`)
6. HUD Ritual

Parent everything to a single null: `FRACTAL_ENGINE_MASTER_NULL`.

**Camera**:
- Slow orbital
- Slight dolly-in
- 15% drift

---

## 🔗 Cross-References

- [Reproduction Engine](../Phoenix/apex-engine/engines/reproduction-engine.md) — theoretical basis for the fractal/self-similar pattern generation the Recursion Engine renders
- [Apex Formation Operator (△)](../ApexLaw/) — convergence mechanics visualized by the Dynamo Core / Torus counter-rotation
- [Identity Recursion Engine](../IdentityRecursionEngine/) — the recursive-identity model mirrored by `RECURSION_DEPTH` and phase-offset stacking
- [Ritual Mechanics](../RitualMechanics/) — invocation protocol pairing with the HUD Ritual Layer and VO Hook
- [Ceremonies](../ceremonies/) — ceremonial sequences that can drive `CEREMONIAL_MODE`

---

## 📊 Technical Specifications

| Property | Value |
|---|---|
| Target | Adobe After Effects (expression-driven) |
| Master Comp | `FRACTAL_ENGINE_MASTER_4K` |
| Scale Range | Galactic → Solar → Jupiter → Earth → Micro-field |
| Recursion Depth Range | 0–12 |
| Control Surface | Single rig brain (`FRACTAL_ENGINE_CTRL`) |
| Reversibility | N/A (rendering rig, not a state operator) |
| Category | Production / Cinematic Engine |

---

*Fractal Engine — Turning of All Plates*
