```
╔══════════════════════════════════════════════════════════════════╗
║         PHOENIX 2.0 APEX EDITION — HYDROGENESI FRAMEWORK        ║
║                                                                  ║
║   A Scale-Invariant Cosmological Framework                       ║
║   Three-Pillar Architecture: Phoenix · Hydrogenesi · The Third  ║
╚══════════════════════════════════════════════════════════════════╝
```

# 🎬 Fractal Engine — Production Pipeline

*From Codex concept to rendered cinematic output*

---

## 🎯 Overview

This document maps how content moves from the Codex's theoretical layer through the [Fractal Engine](./README.md) rig to a finished render. It is the production counterpart to [`FractalEngine_Master_Preset.jsx`](./FractalEngine_Master_Preset.jsx): the preset builds the rig, this pipeline describes how to drive it.

The pipeline is scale-invariant by design — the same five stages apply whether the sequence is illustrating a single operator or the full Triad convergence.

---

## 🔺 Three-Pillar Input Mapping

Each pillar of the Triad feeds a distinct part of the rig:

| Pillar | Role | Feeds |
|---|---|---|
| 🔥 **Phoenix** — Ignition Engine | Transformation, recursion, emergence | `RECURSION_DEPTH`, `PHASE_OFFSET`, `MACRO/MESO/SUB/MICRO_SPEED` (Dynamo Core) |
| 🌊 **Hydrogenesi** — Structural Engine | Continuity, lineage, identity preservation | `FIELD_INTENSITY` (Field Shell — the persisting structural envelope) |
| 🔗 **The Third** — Binding Engine | Convergence, topology, the Triadic Knot | `AURORA_RATE` + `CEREMONIAL_MODE` (Aurora / HUD Ritual — the convergence signal) |

See [Atlases/TheTriadIntegration.md](../Atlases/TheTriadIntegration.md) for the full three-engine convergence model this mapping is drawn from.

---

## 🪜 Pipeline Stages

### Stage 1 — Codex Input

Source material: the operator, law, or ceremony being visualized (e.g. an entry from [OperatorSystem](../OperatorSystem/), [UniversalLaws](../UniversalLaws/), or [ceremonies](../ceremonies/)).

**Output**: a parameter sheet — which Codex values map to which `FRACTAL_ENGINE_CTRL` sliders, per the Three-Pillar Input Mapping above.

### Stage 2 — Rig Build

Run [`FractalEngine_Master_Preset.jsx`](./FractalEngine_Master_Preset.jsx) (`File > Scripts > Run Script File...`) to generate the full comp stack: `CTRL`, `DYNAMO_CORE`, `DYNAMO_TORUS`, `FIELD_SHELL`, `AURORA`, `RECURSION`, `HUD_RITUAL`, assembled into `FRACTAL_ENGINE_MASTER_4K`.

**Output**: an unrendered `.aep` project with the rig wired and placeholder geometry in place.

### Stage 3 — Parameter Pass

Apply the Stage 1 parameter sheet to `FRACTAL_ENGINE_CTRL`. Swap placeholder solids/text for real fractal artwork or footage — the rig's expressions and parenting are untouched by this swap.

**Output**: a scene-specific `.aep`, ready to preview.

### Stage 4 — Render

Render `FRACTAL_ENGINE_MASTER_4K` through the AE render queue. Sound hooks (`MACRO_SPEED` → low drone, `AURORA_RATE` → mid pulse, `RECURSION_DEPTH` → high shimmer) and the VO line are documented on the `CTRL` comp marker for the audio pass.

**Output**: rendered video + a scratch audio guide track.

### Stage 5 — Delivery

Mix final audio against the sound hooks, drop in VO, and hand off the sequence for its cinematic slot (Codex ceremony recording, shot-by-shot sequence, etc.).

**Output**: finished cinematic asset.

---

## 🔗 See Also

- [Fractal Engine — Master Architecture](./README.md)
- [Fractal Engine Preset Builder](./FractalEngine_Master_Preset.jsx)
- [The Triad Integration](../Atlases/TheTriadIntegration.md)
- [Phoenix — The Ignition Engine](../Phoenix/README.md)
- [Hydrogenesi — The Structural Engine](../Hydrogenesi/README.md)
- [The Third — The Binding Engine](../TheThird/README.md)

---

*Fractal Engine Pipeline — Concept to Convergence*
