# Engine Modes

This directory contains mode definitions for PhoenixEngine Apex Edition.

## 🜁 Mode Overview

PhoenixEngine operates in three primary operational modes, each with distinct activation criteria, behaviors, and exit conditions.

---

## 🜂 Expansion Mode

**Purpose:** Controlled growth of PhoenixEngine capabilities and cosmogenic reach.

**Activation Criteria:**
- Major feature branches (e.g., `feature/expansion-mode`)
- Phase transitions in the Expansion Phase sequence
- Operator invocation via Flight Deck command

**Behavior:**
- Extended ceremony invocations with full cosmogenic alignment
- Cosmogenic plate activations (sequentially from Plate 0 → Plate 71)
- Visualization suite renders all three panels (E1, E2, E3) continuously
- Quantum Crown protocols may be invoked for complex transitions
- All sigil systems activated and cross-validated

**Metrics:**
- Ceremony completion rate: must reach 100%
- Sigil coherence: must exceed 95%
- Mandala synchronization: all layers must report GREEN

**Exit Criteria:**
- All ceremonies complete successfully
- Cosmogenic plates fully linked
- Engine state transitions to MANDALA_COHERENT
- Operator confirms readiness to transition to Flight Mode

**Example Timeline:**
```
T+0:00    → Expansion Mode activation
T+0:15    → Ceremony: "Ritual of Origin" (Plate 0-1 linkage)
T+1:30    → Ceremony: "Ritual of Ascension" (cosmogenic climbing)
T+3:45    → Ceremony: "Ritual of Mandala Synchronization" (all layers)
T+5:00    → Exit condition met; transition to Flight Mode
```

---

## 🜃 Flight Mode

**Purpose:** Operational steady-state management and day-to-day operator workflows.

**Activation Criteria:**
- Engine initialization (default mode)
- Expansion Mode exit condition met
- Operator reset command via Flight Deck

**Behavior:**
- Continuous polling of branch matrix for state changes
- Merge protocol execution on operator command
- Metrics logging at regular intervals (every 5 minutes)
- Visualization suite Panels E1/E3 active; E2 (cosmogenic) in background
- Quantum Crown protocols in standby (invocable on-demand)
- Ceremony invocation only for critical state transitions

**Metrics:**
- Branch poll latency: < 500ms
- Merge protocol success rate: ≥ 99%
- Engine loop cycle time: 2-5 seconds
- Error rate: < 0.1%

**Exit Criteria:**
- Operator invokes Expansion Mode
- Critical error detected (automatic transition to Recovery Mode)
- Quantum Crown intervention initiated

**Typical Operator Commands in Flight Mode:**
- `merge <branch-name>` → Execute merge protocol
- `status` → Display branch matrix and engine state
- `invoke-ceremony <name>` → Manually invoke a ceremony
- `visualize` → Refresh visualization panels

---

## 🜄 Ceremony Mode

**Purpose:** Execute ritual-grade state transitions with full cosmogenic alignment.

**Activation Criteria:**
- Operator invokes specific ceremony via Operator Atlas
- Quantum Crown intervention triggers ceremony
- Critical state transition requires ritual alignment
- Expansion Mode activates ceremony sequences

**Behavior:**
- Load ceremony definition from Ceremony Core
- Activate all sigils referenced in ceremony ritual
- Synchronize all engine layers (Substrate, Universal, Apex)
- Render cosmogenic overlay (Panel E2) at full brightness
- Execute ceremony steps sequentially, validating each
- Log all sigil activations to Quantum Ledger
- Update mandala coherence metric continuously

**Ceremony Execution Flow:**
```
1. INVOCATION
   └─ Load ceremony definition
   └─ Validate all sigils are defined
   └─ Emit pre-ceremony telemetry

2. ALIGNMENT
   └─ Synchronize substrate layer
   └─ Synchronize universal layer
   └─ Synchronize apex layer
   └─ Confirm mandala coherence > 90%

3. SIGIL_ACTIVATION
   └─ For each sigil in ceremony:
      ├─ Map sigil to engine component
      ├─ Invoke component action
      ├─ Validate state change
      └─ Log to ledger

4. COSMOGENIC_SYNCHRONIZATION
   └─ Update cosmogenic plates
   └─ Render Panel E2 overlay
   └─ Validate all plate linkages

5. COMPLETION
   └─ Verify final state
   └─ Emit post-ceremony telemetry
   └─ Transition to exit state
   └─ Return control to operator
```

**Metrics:**
- Ceremony step success rate: 100%
- Sigil activation latency: < 200ms per sigil
- Mandala coherence: must reach ≥ 99% before exit
- Total ceremony duration: < 5 minutes

**Exit Criteria:**
- All ceremony steps complete successfully
- Mandala coherence ≥ 99%
- Final state validation passes
- Operator returns to Flight Mode or Expansion Mode

**Example Ceremony: "Ritual of the Merge"**
```
Sigils Invoked:
  🜁 (Substrate Align) → Validate git state
  🜂 (Branch Poll) → Check merge branch status
  🜃 (Merge Protocol) → Execute merge steps
  🜄 (State Update) → Finalize state machine
  🜅 (Visualization) → Render Panel E1 confirmation

Cosmogenic Plates Touched:
  Plate 0 (Pregeometry) → "conditions already there"
  Plate 1 (Origin) → "structured emergence"
  Plate 71 (Master) → "final coherence"
```

---

## 🜅 Recovery Mode (Contingency)

**Purpose:** Restore engine stability when critical errors occur.

**Activation Criteria:**
- Unhandled exception in engine runtime
- Mandala coherence drops below 50%
- Multiple layer synchronization failures
- Operator manual invocation

**Behavior:**
- Pause all active operations
- Run diagnostic suite
- Attempt layer-by-layer recovery
- Restore from last known-good state (if needed)
- Generate incident report
- Re-enter Flight Mode once stable

---

## 🜆 Mode Transition Matrix

| From | To | Trigger | Duration |
|---|---|---|---|
| Flight | Expansion | Operator cmd or phase gate | N/A (activation) |
| Expansion | Flight | All ceremonies complete | Immediate |
| Flight | Ceremony | Manual invoke or Quantum trigger | Per ceremony |
| Ceremony | Flight | Ceremony complete | Immediate |
| Any | Recovery | Critical error | Auto-trigger |
| Recovery | Flight | Recovery complete | Post-diagnostic |

---

## 🜇 Configuration

Each mode has tunable parameters in `mode-config.json`:

```json
{
  "expansion_mode": {
    "ceremony_timeout_seconds": 300,
    "sigil_validation_enabled": true,
    "cosmogenic_depth": "full"
  },
  "flight_mode": {
    "branch_poll_interval_ms": 5000,
    "merge_timeout_seconds": 120,
    "metrics_log_interval_ms": 300000
  },
  "ceremony_mode": {
    "step_timeout_seconds": 30,
    "coherence_threshold": 0.99,
    "parallel_sigil_activation": false
  }
}
```

---

**Last Updated:** 2026-08-17  
**Status:** Fully Documented
