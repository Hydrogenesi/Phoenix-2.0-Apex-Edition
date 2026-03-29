# Invariance Metrics Dashboard

*Real-Time Monitoring of Crown-Level Governance*

---

## Overview

The **Invariance Metrics Dashboard** provides real-time visibility into the health and status of Meta-Operator I and the five core invariants. This specification defines the metrics, visualizations, and alerting mechanisms required for effective invariance monitoring.

---

## Dashboard Architecture

### Core Components

1. **Invariant Health Panel** — Real-time status of all five invariants
2. **Violation Timeline** — Historical view of all detected violations
3. **Recovery Metrics** — Performance of fracture recovery protocol
4. **System Health Overview** — Overall system integrity status
5. **Alert Management** — Active alerts and notification settings

---

## Section 1: Invariant Health Panel

### Layout
```
╔═══════════════════════════════════════════════════════════════╗
║         INVARIANT HEALTH STATUS - STRATUM IV CROWN            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [I₁] Structure         ████████████████████ 100% ✓          ║
║       Topology checks: 1,247,891 | Violations: 0             ║
║                                                               ║
║  [I₂] Conservation      ████████████████████  99.8% ✓         ║
║       Energy balance: 1.0000 | Drift: 0.2%                   ║
║                                                               ║
║  [I₃] Identity          ████████████████████ 100% ✓          ║
║       Unique IDs: 45,231 | Collisions: 0                     ║
║                                                               ║
║  [I₄] Causality         ████████████████████ 100% ✓          ║
║       Temporal checks: 892,445 | Violations: 0               ║
║                                                               ║
║  [I₅] Symmetry          ███████████████████░  98.5% ⚠         ║
║       Symmetry groups: 12,847 | Minor drift: 2               ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  Overall System Health: 99.66% ✓          Last Scan: 0.1s ago║
╚═══════════════════════════════════════════════════════════════╝
```

### Metrics Definitions

#### I₁: Structure Health
```python
structure_health = (
    (topology_checks_passed / total_topology_checks) * 0.5 +
    (connectivity_tests_passed / total_connectivity_tests) * 0.5
) * 100

thresholds = {
    'green': >= 99.5%,
    'yellow': >= 95.0%,
    'red': < 95.0%
}
```

#### I₂: Conservation Health
```python
energy_balance = sum(energy_in) - sum(energy_out)
conservation_health = (1 - abs(energy_balance) / total_energy) * 100

thresholds = {
    'green': >= 99.0%,
    'yellow': >= 95.0%,
    'red': < 95.0%
}
```

#### I₃: Identity Health
```python
identity_health = (
    (unique_ids / total_patterns) * 0.6 +
    (1 - id_collisions / total_patterns) * 0.4
) * 100

thresholds = {
    'green': >= 99.9%,
    'yellow': >= 99.0%,
    'red': < 99.0%
}
```

#### I₄: Causality Health
```python
causality_health = (temporal_order_checks_passed / total_causal_checks) * 100

thresholds = {
    'green': >= 99.9%,
    'yellow': >= 99.0%,
    'red': < 99.0%
}
```

#### I₅: Symmetry Health
```python
symmetry_health = (symmetry_preservations / total_transformations) * 100

thresholds = {
    'green': >= 98.0%,
    'yellow': >= 95.0%,
    'red': < 95.0%
}
```

---

## Section 2: Violation Timeline

### Layout
```
╔═══════════════════════════════════════════════════════════════╗
║                     VIOLATION TIMELINE (24H)                  ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Violations by Severity                                       ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Level 4: ▂                                              │ ║
║  │ Level 3: ▂▃▂                                            │ ║
║  │ Level 2: ▂▄▅▃▄▅▄▃                                       │ ║
║  │ Level 1: ▄▆█▆▅▇▆▅▄▅▆▇▅▄▆█▆                             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║    00:00  04:00  08:00  12:00  16:00  20:00  24:00          ║
║                                                               ║
║  Recent Violations:                                           ║
║  • 20:24:15 | Level 1 | I₅ Symmetry | Self-corrected        ║
║  • 19:47:32 | Level 2 | I₂ Conservation | Manual review      ║
║  • 18:15:08 | Level 1 | I₅ Symmetry | Self-corrected        ║
║                                                               ║
║  Total (24h): L1: 127 | L2: 8 | L3: 2 | L4: 0                ║
╚═══════════════════════════════════════════════════════════════╝
```

### Data Points
- **Timestamp**: Exact time of violation detection
- **Severity Level**: 1-4 classification
- **Invariant**: Which invariant was violated (I₁-I₅)
- **Status**: Self-corrected, Under review, Recovered, Failed
- **Duration**: Time from detection to resolution
- **Impact**: Number of affected transformations

---

## Section 3: Recovery Metrics

### Layout
```
╔═══════════════════════════════════════════════════════════════╗
║                    RECOVERY PERFORMANCE                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Recovery Success Rate                                        ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  L1: ████████████████████ 100.0% (127/127)             │ ║
║  │  L2: ███████████████████░  98.5%  (8/8)                │ ║
║  │  L3: █████████████████░░░  95.0%  (2/2)                │ ║
║  │  L4: ████████████████████ 100.0%  (0/0)                │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                               ║
║  Mean Time To Recovery (MTTR)                                 ║
║  • Level 1: 0.3 seconds    (target: < 1s)        ✓           ║
║  • Level 2: 45 seconds     (target: < 60s)       ✓           ║
║  • Level 3: 2.1 minutes    (target: < 5m)        ✓           ║
║  • Level 4: N/A            (target: < 30m)       -           ║
║                                                               ║
║  System Availability (7 days)                                 ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │  Uptime: 99.987%                                        │ ║
║  │  Downtime: 9.2 minutes                                  │ ║
║  │  Target: 99.99%                                         │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### Tracked Metrics
1. **Recovery Success Rate**: Percentage of violations successfully resolved
2. **Mean Time To Recovery (MTTR)**: Average time from detection to resolution
3. **System Availability**: Percentage of time system is fully operational
4. **False Positive Rate**: Incorrect violation detections
5. **Recovery Method Distribution**: Auto vs manual vs emergency recoveries

---

## Section 4: System Health Overview

### Layout
```
╔═══════════════════════════════════════════════════════════════╗
║                   SYSTEM HEALTH OVERVIEW                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Current Status: HEALTHY ✓                                    ║
║                                                               ║
║  Operator Status:                                             ║
║  • Genesis (⊕):        ACTIVE ✓  | Last used: 0.2s ago       ║
║  • Harmonic (⊗):       ACTIVE ✓  | Last used: 0.1s ago       ║
║  • Recursive (⊛):      ACTIVE ✓  | Last used: 0.5s ago       ║
║  • Convergence (⊳):    ACTIVE ✓  | Last used: 1.2s ago       ║
║  • Divergence (⊲):     ACTIVE ✓  | Last used: 3.7s ago       ║
║  • Mirror (⊞):         ACTIVE ✓  | Last used: 2.1s ago       ║
║  • Apex (△):           ACTIVE ✓  | Last used: 45s ago        ║
║  • Void (⊝):           ACTIVE ✓  | Last used: 127s ago       ║
║                                                               ║
║  Active Patterns: 45,231                                      ║
║  Active Transformations: 12,847/sec                           ║
║  Memory Usage: 2.4 GB / 16 GB (15%)                           ║
║  CPU Usage: 34%                                               ║
║                                                               ║
║  Monitoring Status:                                           ║
║  • Real-time scanning: ENABLED ✓                             ║
║  • Scan interval: 100ms                                       ║
║  • Last full scan: 15 minutes ago                             ║
║  • Next checkpoint: 3 minutes                                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Section 5: Alert Management

### Alert Levels

#### Critical Alerts (Level 4)
- **Trigger**: Any Level 4 violation
- **Actions**:
  - Immediate email/SMS to emergency team
  - System halt initiated
  - Incident log created
  - Dashboard turns RED with flashing indicator

#### Warning Alerts (Level 3)
- **Trigger**: Any Level 3 violation
- **Actions**:
  - Email to on-call team
  - Recovery protocol initiated
  - Detailed log entry created
  - Dashboard shows YELLOW warning

#### Notice Alerts (Level 2)
- **Trigger**: Any Level 2 violation
- **Actions**:
  - Dashboard notification
  - Log entry created
  - Queued for manual review
  - No immediate email

#### Info Logs (Level 1)
- **Trigger**: Any Level 1 violation
- **Actions**:
  - Log entry only
  - Auto-correction attempted
  - No notifications
  - Dashboard shows brief info message

### Alert Configuration
```yaml
alerts:
  level_4:
    enabled: true
    notifications:
      - email: emergency@phoenix.io
      - sms: +1-555-CROWN-00
      - slack: #critical-alerts
    sound: critical.wav
    
  level_3:
    enabled: true
    notifications:
      - email: oncall@phoenix.io
      - slack: #engineering-alerts
    sound: warning.wav
    
  level_2:
    enabled: true
    notifications:
      - dashboard: true
    sound: notice.wav
    
  level_1:
    enabled: true
    notifications:
      - log_only: true
```

---

## API Endpoints

### Real-Time Metrics
```
GET /api/metrics/invariants
Returns: Current health status of all five invariants

GET /api/metrics/violations?since=timestamp
Returns: List of violations since given timestamp

GET /api/metrics/recovery?period=24h
Returns: Recovery statistics for given period

GET /api/metrics/system
Returns: Overall system health metrics
```

### WebSocket Stream
```javascript
// Real-time updates
ws://dashboard.phoenix.io/stream/metrics

Message format:
{
  "timestamp": "2024-02-13T20:24:15Z",
  "type": "invariant_update",
  "data": {
    "invariant": "I5",
    "health": 98.5,
    "status": "warning",
    "details": "Minor symmetry drift detected"
  }
}
```

---

## Dashboard Implementation

### Technology Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React + D3.js for visualizations
- **Database**: InfluxDB for time-series metrics
- **Real-time**: WebSocket (Socket.io)
- **Deployment**: Docker containers

### Data Collection
```python
# Metrics collector (runs in invariance_scanner.py)
class MetricsCollector:
    def __init__(self):
        self.db = InfluxDBClient()
        self.update_interval = 0.1  # 100ms
        
    def collect(self):
        metrics = {
            'structure_health': self.measure_structure(),
            'conservation_health': self.measure_conservation(),
            'identity_health': self.measure_identity(),
            'causality_health': self.measure_causality(),
            'symmetry_health': self.measure_symmetry(),
        }
        
        self.db.write(metrics)
        self.broadcast_to_dashboard(metrics)
```

### Dashboard Refresh Rate
- **Primary metrics**: 100ms (real-time)
- **Historical graphs**: 1 second
- **Statistical summaries**: 5 seconds
- **Long-term trends**: 1 minute

---

## Mobile Responsiveness

### Mobile View Priority
1. Overall health status (green/yellow/red)
2. Active critical alerts
3. Recent violations (last 5)
4. Quick action buttons (acknowledge alert, view details)

### Simplified Mobile Layout
```
┌─────────────────────────┐
│  SYSTEM HEALTH: 99.7% ✓ │
├─────────────────────────┤
│  Active Alerts: 0       │
│  Recent Violations: 3   │
├─────────────────────────┤
│  [View Full Dashboard]  │
│  [Acknowledge Alerts]   │
└─────────────────────────┘
```

---

## Access Control

### User Roles
1. **Crown Authority**: Full access, can modify alert settings
2. **System Administrator**: Read/write, can acknowledge alerts
3. **Engineer**: Read-only, can view all metrics
4. **Observer**: Limited read-only, only health overview

### Authentication
- OAuth 2.0 integration
- Multi-factor authentication for Crown Authority
- API key authentication for automated systems
- Session timeout: 30 minutes

---

## Compliance and Auditing

### Audit Log
All dashboard access and actions logged:
```
[2024-02-13 20:24:15] USER: admin@phoenix.io
                      ACTION: Acknowledged alert V-67890
                      RESULT: Success
                      IP: 192.168.1.100
```

### Data Retention
- Real-time metrics: 24 hours
- Hourly aggregates: 30 days
- Daily summaries: 1 year
- Incident reports: Permanent

---

## Performance Requirements

### Response Time Targets
- Initial dashboard load: < 2 seconds
- Metric updates: < 100ms latency
- Historical query: < 500ms
- Alert delivery: < 1 second

### Scalability
- Support 1000+ concurrent users
- Handle 10,000+ metrics/second
- Store 1 year of historical data
- Query performance maintained with data growth

---

## Cross-References

- [Meta-Operator I Specification](../operators/meta_operator_I_invariance.md) — Core invariant definitions
- [Invariance Validation Ceremony](../ceremonies/invariance_validation_ceremony.md) — Activation procedures
- [Fracture Recovery Protocol](../protocols/fracture_recovery_protocol.md) — Recovery procedures
- [Invariance Scanner Tool](../../tools/invariance_scanner.py) — Data collection implementation

---

## Dashboard URL

**Production**: `https://dashboard.phoenix.io/invariance`
**Staging**: `https://staging-dashboard.phoenix.io/invariance`
**Development**: `http://localhost:3000/invariance`

---

*Real-time visibility into the eternal laws. The dashboard watches. The metrics endure.*

---

[◀ Back to Recovery Protocol](../protocols/fracture_recovery_protocol.md) | [Next: Scanner Tool ▶](../../tools/invariance_scanner.py)
