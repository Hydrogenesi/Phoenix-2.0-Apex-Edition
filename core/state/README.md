# Engine State Schemas

This directory contains JSON schemas, diagrams, and formal specifications for PhoenixEngine state transitions.

---

## 🜁 Core State Schema

**File:** `engine-state.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PhoenixEngine State Schema",
  "type": "object",
  "required": ["version", "timestamp", "state", "substrate", "ceremonies", "mandala"],
  "properties": {
    "version": {
      "type": "string",
      "description": "Engine version (e.g., '2.0-apex')"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of state snapshot"
    },
    "phase": {
      "type": "string",
      "enum": [
        "Phase 1: Substrate Establishment",
        "Phase 2: Ceremony Anchoring",
        "Phase 3: Cockpit Realization",
        "Phase 4: Cosmogenic Integration"
      ]
    },
    "state": {
      "type": "string",
      "enum": [
        "IDLE",
        "WAITING",
        "PROCESSING",
        "CEREMONY",
        "STABLE",
        "COCKPIT_ACTIVE",
        "QUANTUM_ALIGNED",
        "MANDALA_COHERENT",
        "RECOVERY"
      ],
      "description": "Current engine state"
    },
    "substrate": {
      "type": "object",
      "description": "Git/CI substrate layer state",
      "properties": {
        "repo_state": {
          "type": "string",
          "enum": ["CLEAN", "DIRTY", "CONFLICT", "ERROR"]
        },
        "branch_matrix": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "status": {
                "type": "string",
                "enum": ["GREEN", "YELLOW", "RED"]
              },
              "ci_passing": { "type": "boolean" },
              "needs_review": { "type": "boolean" },
              "last_commit": { "type": "string" }
            }
          }
        },
        "approvals_pending": { "type": "integer" }
      }
    },
    "ceremonies": {
      "type": "object",
      "description": "Active ceremony state",
      "properties": {
        "last_invoked": { "type": "string", "format": "date-time" },
        "name": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["QUEUED", "RUNNING", "COMPLETE", "FAILED"]
        },
        "sigils_activated": {
          "type": "array",
          "items": { "type": "string" },
          "description": "List of activated sigil symbols"
        }
      }
    },
    "visualization": {
      "type": "object",
      "description": "Visualization suite panel status",
      "properties": {
        "panel_e1_active": { "type": "boolean" },
        "panel_e2_active": { "type": "boolean" },
        "panel_e3_active": { "type": "boolean" },
        "overlays": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "quantum": {
      "type": "object",
      "description": "Quantum Crown protocol state",
      "properties": {
        "last_session": { "type": "string", "format": "date-time" },
        "protocols_aligned": { "type": "boolean" },
        "ledger_entries": { "type": "integer" }
      }
    },
    "mandala": {
      "type": "object",
      "description": "Overall mandala synchronization state",
      "properties": {
        "coherence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Mandala coherence metric (0.0 to 1.0)"
        },
        "all_layers_synchronized": { "type": "boolean" }
      }
    }
  }
}
```

---

## 🜂 State Transition Diagram

```
                    ┌─────────────────────────────────────┐
                    │                                       │
                    ▼                                       │
              ┌──────────┐                                 │
              │   IDLE   │◄─────────────────────────────┐  │
              └──────────┘                              │  │
                    │                                   │  │
       (operator or │ merge command                     │  │
        quantum     │ OR polling trigger)               │  │
        trigger)    │                                   │  │
                    ▼                                   │  │
              ┌──────────┐                              │  │
              │ WAITING  │──────────────────────────┐   │  │
              └──────────┘                          │   │  │
                    │                               │   │  │
                    │ (timeout or queue ready)      │   │  │
                    │                               │   │  │
                    ▼                               │   │  │
              ┌──────────────┐                      │   │  │
              │  PROCESSING  │                      │   │  │
              └──────────────┘                      │   │  │
                    │                               │   │  │
         ┌──────────┼──────────┐                    │   │  │
         │                     │                    │   │  │
    (validation)          (ceremony                 │   │  │
         │              required?)                  │   │  │
         │                     │                    │   │  │
         ▼                     ▼                    │   │  │
    ┌────────┐            ┌──────────┐             │   │  │
    │ STABLE │────────────│ CEREMONY │             │   │  │
    └────────┘            └──────────┘             │   │  │
         │                     │                    │   │  │
         │                     │ (ceremony complete)│   │  │
         │                     │                    │   │  │
         │                     └────────────────┐   │   │  │
         │                                      │   │   │  │
         └──────────────────────────────────────┴───┴───┘  │
                                                            │
                     ┌─────────────────────────────────────┘
                     │
              (metrics logged)
              
  COCKPIT_ACTIVE ──────────────────────── QUANTUM_ALIGNED ─────────────► MANDALA_COHERENT
       │                                          │
       │ (Operator Flight Mode)                   │ (Quantum Crown invoked)
       │                                          │
       └──────────────────────────────────────────┘
```

---

## 🜃 State Lifecycle (Detailed)

### **IDLE → WAITING**
- **Trigger:** Operator merge command or automated polling interval
- **Actions:** 
  - Load merge request from branch matrix
  - Queue merge operation
  - Reserve resources
- **Duration:** Immediate
- **Next State:** WAITING (wait for processing slot)

### **WAITING → PROCESSING**
- **Trigger:** Processing slot becomes available
- **Actions:**
  - Lock git repository state
  - Begin merge validation
  - Initialize substrate layer checks
- **Duration:** < 100ms
- **Next State:** PROCESSING

### **PROCESSING → CEREMONY / STABLE**
- **Condition:** Does merge require ceremony alignment?
- **If YES:** Transition to CEREMONY
- **If NO:** Transition to STABLE
- **Actions:**
  - Validate merge conflicts
  - Check CI status
  - Determine ceremony requirements

### **CEREMONY → STABLE**
- **Trigger:** All ceremony steps complete successfully
- **Actions:**
  - Execute final merge commit
  - Update branch matrix
  - Log ceremony to Quantum Ledger
  - Render Panel E1 confirmation
- **Duration:** Per ceremony (typically 1-5 minutes)
- **Next State:** STABLE

### **STABLE → IDLE**
- **Trigger:** Metrics logging complete
- **Actions:**
  - Release git repository lock
  - Update mandala coherence metric
  - Emit post-operation telemetry
  - Return to polling state
- **Duration:** < 500ms
- **Next State:** IDLE

---

## 🜄 Sigil State Schema

```json
{
  "sigil": {
    "id": "string (unicode sigil symbol)",
    "name": "string",
    "phase_introduced": "integer (0-4)",
    "engine_component": "string (reference to engine subsystem)",
    "activation_order": "integer (in ceremony sequence)",
    "prerequisites": ["array of other sigil IDs"],
    "actions": [
      {
        "name": "string",
        "description": "string",
        "command": "shell or API call",
        "validation": "success criteria"
      }
    ],
    "cosmogenic_plates": ["array of plate numbers linked to this sigil"],
    "state": {
      "activated": "boolean",
      "last_invoked": "ISO 8601 timestamp",
      "invocation_count": "integer"
    }
  }
}
```

---

## 🜅 Branch State Schema

```json
{
  "branch": {
    "name": "string",
    "status": "string (GREEN|YELLOW|RED)",
    "ci_status": "string (passing|failing|unknown)",
    "requires_review": "boolean",
    "last_commit": {
      "sha": "string",
      "author": "string",
      "message": "string",
      "timestamp": "ISO 8601"
    },
    "pr_linked": "boolean",
    "pr_number": "integer (if linked)",
    "protected": "boolean",
    "merge_eligible": "boolean",
    "ceremony_required": "boolean",
    "estimated_ceremony": "string (ceremony name, if applicable)"
  }
}
```

---

## 🜆 Mandala Coherence Calculation

```
coherence = (
  (substrate_sync_score × 0.25) +
  (ceremony_completion_score × 0.30) +
  (visualization_sync_score × 0.20) +
  (quantum_alignment_score × 0.15) +
  (cosmogenic_link_score × 0.10)
) / 100

where:
  substrate_sync_score:     all layers report GREEN (0-100)
  ceremony_completion_score: % of ceremonies completed successfully
  visualization_sync_score:  % of panels synchronized
  quantum_alignment_score:   % of Quantum Crown protocols validated
  cosmogenic_link_score:     % of cosmogenic plates fully linked
```

**Thresholds:**
- `coherence ≥ 0.99` → Mandala fully coherent (MANDALA_COHERENT state)
- `coherence 0.90-0.98` → Mandala mostly aligned (normal operation)
- `coherence 0.50-0.89` → Mandala degraded (warnings issued)
- `coherence < 0.50` → Mandala critical (enter RECOVERY mode)

---

## 🜇 Example State Snapshot

```json
{
  "version": "2.0-apex",
  "timestamp": "2026-08-17T14:30:45Z",
  "phase": "Phase 3: Cockpit Realization",
  "state": "STABLE",
  "substrate": {
    "repo_state": "CLEAN",
    "branch_matrix": {
      "main": {
        "status": "GREEN",
        "ci_passing": true,
        "needs_review": false,
        "last_commit": "abc123def456"
      },
      "develop": {
        "status": "YELLOW",
        "ci_passing": true,
        "needs_review": true,
        "last_commit": "def456ghi789"
      }
    },
    "approvals_pending": 1
  },
  "ceremonies": {
    "last_invoked": "2026-08-17T14:25:00Z",
    "name": "Ritual of the Merge",
    "status": "COMPLETE",
    "sigils_activated": ["🜁", "🜂", "🜃", "🜄"]
  },
  "visualization": {
    "panel_e1_active": true,
    "panel_e2_active": true,
    "panel_e3_active": true,
    "overlays": ["cosmogenic", "operator-mode"]
  },
  "quantum": {
    "last_session": "2026-08-17T10:00:00Z",
    "protocols_aligned": true,
    "ledger_entries": 27
  },
  "mandala": {
    "coherence": 0.97,
    "all_layers_synchronized": true
  }
}
```

---

**Last Updated:** 2026-08-17  
**Status:** Schema Finalized
