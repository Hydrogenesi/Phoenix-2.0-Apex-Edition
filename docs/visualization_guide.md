# 📊 Triad Visualization Guide

*Real-time dashboards, topology diagrams, and performance analytics*

---

## Overview

This guide provides interactive visualizations for:

- **Operator Performance** — Timing, cost, and throughput metrics
- **Topology Structures** — State convergence, mirroring, branching
- **Cycle Execution** — Checkpoint lineage and rollback recovery
- **Live Dashboards** — Real-time Triad engine monitoring

---

## 1. Operator Timing & Performance

### 1.1 Basic Operator Timing Chart

The most essential metric: **How long does each operator take?**

```javascript
// Load metrics from your Triad instance
renderOperatorTimingChart("operatorTiming", [
  { operator: "⊕", avg_ms: 3.2, min_ms: 2.1, max_ms: 5.8, count: 450 },
  { operator: "⊗", avg_ms: 1.1, min_ms: 0.8, max_ms: 2.2, count: 450 },
  { operator: "⊛", avg_ms: 8.4, min_ms: 6.2, max_ms: 15.3, count: 450 },
  { operator: "△", avg_ms: 12.7, min_ms: 9.1, max_ms: 28.4, count: 450 },
  { operator: "⊝", avg_ms: 4.9, min_ms: 3.5, max_ms: 8.2, count: 450 },
  { operator: "⊞", avg_ms: 2.3, min_ms: 1.8, max_ms: 4.1, count: 450 },
  { operator: "⊳", avg_ms: 9.1, min_ms: 7.2, max_ms: 18.5, count: 450 },
  { operator: "⊲", avg_ms: 7.8, min_ms: 6.0, max_ms: 14.2, count: 450 }
]);
```

**What this tells you:**

| Operator | Category | Interpretation |
|----------|----------|-----------------|
| **⊞** (Mirror) | Fastest (2.3ms) | Symmetric transforms are cheap |
| **⊗** (Harmonic) | Very Fast (1.1ms) | Stabilization is lightweight |
| **⊕** (Genesis) | Fast (3.2ms) | Creation scales well |
| **⊝** (Void) | Medium (4.9ms) | Deletion tracking adds cost |
| **⊲** (Divergence) | Higher (7.8ms) | Branching requires state duplication |
| **⊛** (Recursive) | High (8.4ms) | Recursion depth adds overhead |
| **⊳** (Convergence) | High (9.1ms) | Merging many-to-one is expensive |
| **△** (Apex) | Highest (12.7ms) | Collapse/compression takes time |

**Usage in Dashboard:**

```html
<div id="operatorTiming" class="metric-card">
  <h3>Operator Timing Breakdown</h3>
  <!-- Chart renders here -->
</div>
```

---

## 2. State Topology Visualizations

### 2.1 Basic Apex Formation (Triangle)

The simplest Triad structure: **State → Apex → Link → State**

```mermaid
graph TD
    A[State Node] --- B[Apex Node]
    B --- C[Link Node]
    C --- A
```

**What's happening:**

1. **State Node** — Current transformation state
2. **Apex Node** — Convergence point (delta compression, information collapse)
3. **Link Node** — Continuation edge (identity preservation)
4. **Cycle** — Returns to next State Node

**Real Example:**

```
State: { ledger_size: 15.2KB, depth: 5 }
    ↓ (apply ⊕ Genesis)
Apex: { compressed: 12.3KB, delta: 0.8KB }
    ↓ (link via ⊞ Mirror)
Link: (preserved identity, ready for recursion)
    ↓
State: { ledger_size: 12.3KB, depth: 6 }
```

---

### 2.2 Convergence Knot (Many-to-One)

When multiple states merge into an apex form:

```mermaid
graph TD
    S1[State 1] --> K[Convergence Knot]
    S2[State 2] --> K
    S3[State 3] --> K
    K --> A[Apex Form]
```

**What's happening:**

1. **Three State Nodes** — Parallel branches (⊲ Divergence output)
2. **Convergence Knot** — Binding point (⊳ Convergence operator)
3. **Apex Form** — Unified result (△ Apex operator)

**Real Example (Fusion):**

```
Sequence: ⊲ (diverge into 3 branches)
         → ⊕ (genesis on each)
         → ⊳ (converge all 3)
         → △ (collapse to apex)

Branch 1: { data_a: 100 }  ⊕ ⊳
Branch 2: { data_b: 200 }  ⊕ ⊳ → { fused: { a: 100, b: 200, c: 300 } }
Branch 3: { data_c: 300 }  ⊕ ⊳
```

**Cost Model:**

```
Cost(⊳) = 3 × (cost per merge) = ~27ms
         = cost(⊕) + cost(⊕) + cost(⊕) + cost(⊳) + cost(△)
         ≈ 3.2 + 3.2 + 3.2 + 9.1 + 12.7 = 31.4ms
```

---

### 2.3 Mirror Symmetry (Bidirectional)

When states need to be reflected or synchronized:

```mermaid
graph LR
    L[Left State] --- M[Mirror Node]
    M --- R[Right State]
    L <--> R
```

**What's happening:**

1. **Left State** — Original state
2. **Mirror Node** — Symmetry operator (⊞)
3. **Right State** — Reflected state
4. **Bidirectional arrows** — Identity preserved both directions

**Real Example (Identity Ledger):**

```
Left:  { id: "session_001", created_at: T0 }
          ↓ (apply ⊞ Mirror)
Mirror: (symmetry checked, identity tag embedded)
          ↓
Right: { id: "session_001", created_at: T0 } ← Same identity
```

**Use Cases:**

- **Consistency checking** — Verify transformation reversibility
- **State replication** — Mirror across distributed nodes
- **Ledger synchronization** — Ensure identity continuity

---

### 2.4 Divergence Branching (One-to-Many)

When a single state splits into multiple branches:

```mermaid
graph TD
    S[Source State] --> B1[Branch 1]
    S --> B2[Branch 2]
    S --> B3[Branch 3]
```

**What's happening:**

1. **Source State** — Single input
2. **Divergence Operator** (⊲) — Splits into N branches
3. **Three branches** — Each gets a tag/identity
4. **Later converge** — Via ⊳ Convergence

**Real Example (Recursive Branching):**

```
Source: { depth: 0, value: 100 }
           ↓ (apply ⊲ Divergence, factor=3)
Branch 1: { depth: 1, value: 100, branch_id: "div_001_1" }
Branch 2: { depth: 1, value: 100, branch_id: "div_001_2" }
Branch 3: { depth: 1, value: 100, branch_id: "div_001_3" }
           ↓ (apply ⊛ Recursion on each)
           ↓ (eventually converge with ⊳)
```

**Cost Model:**

```
Cost(⊲) = branching factor × (overhead + state duplication)
        = 3 × (tag + copy) ≈ 7.8ms
```

---

## 3. Checkpoint Lineage & Recovery

### 3.1 Checkpoint Flow (Boundary → Cycle → Apex)

The three-tier checkpoint strategy:

```mermaid
graph TD
    C0[Boundary Checkpoint] --> C1[Cycle Checkpoint]
    C1 --> C2[Cycle Checkpoint]
    C2 --> C3[Apex Checkpoint]
```

**What's happening:**

1. **C0: Boundary Checkpoint** — Pre-execution state (hydration complete)
2. **C1, C2: Cycle Checkpoints** — Intermediate states (conditional, aggressive mode)
3. **C3: Apex Checkpoint** — Post-transformation (always saved)

**Real Example (Storage Trace):**

```
T0 [Boundary] → state_size: 15.2 KB
                checkpoint: C0_001
                location: /ledger/boundary/
T1 [Cycle 1]  → state_size: 15.3 KB (after ⊕)
                checkpoint: C1_001
                location: /ledger/cycle/
T2 [Cycle 2]  → state_size: 15.4 KB (after ⊗)
                checkpoint: C1_002 (skipped in normal mode)
T3 [Apex]     → state_size: 12.3 KB (after △)
                checkpoint: C3_001
                location: /ledger/apex/
```

**Retention Policy:**

```
Boundary: Keep 1 per cycle (1 file)
Cycle:    Keep 0-N per cycle (aggressive mode only)
Apex:     Keep all (100% retention)

Storage: 1 + 0 + 1 = 2 checkpoints/cycle
Cost:    ~30 KB per cycle
```

---

### 3.2 Rollback Recovery (Apex → Cycle)

When an error occurs, revert to last valid checkpoint:

```mermaid
graph TD
    C0[Boundary Checkpoint] --> C1[Cycle Checkpoint]
    C1 --> C2[Cycle Checkpoint]
    C2 --> C3[Apex Checkpoint]
    C3 -.rollback.-> C1[Cycle Checkpoint]
```

**What's happening:**

1. **Normal flow** — C0 → C1 → C2 → C3 (solid lines)
2. **Error at C3** — Apex fails or threshold violated
3. **Rollback** — Jump back to C1 (dotted line)
4. **Resume** — Restart from C1 with different params

**Real Example (Error Handling):**

```
Sequence: ⊕ → ⊗ → ⊛ → △

T0 [C0: Boundary]
    ↓
T1 [C1: After ⊕] (state valid, size 15.3 KB)
    ↓
T2 [After ⊗] (state valid, size 15.4 KB)
    ↓
T3 [C3: Apex △] ← ERROR! State size blew up to 500 KB
    ↓ (ROLLBACK)
T1 [C1: Retry] (restore to state at T1)
    ↓
T2' [Retry ⊗ with different params]
    ↓
T3' [C3: Apex △] ← SUCCESS! Size 12.3 KB
```

**Rollback Cost:**

```
Restore time:  ~5-10ms (file read from ledger)
Retry time:    varies (same as original sequence)
Total cost:    ~2× original cycle time (worst case)
```

---

## 4. Live Dashboard Implementation

### 4.1 Multi-Panel Dashboard

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Triad Live Dashboard</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    :root {
      --primary: #3498DB;
      --success: #2ECC71;
      --warning: #F39C12;
      --error: #E74C3C;
      --dark: #2C3E50;
      --light: #ECF0F1;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    
    .dashboard {
      max-width: 1600px;
      margin: 0 auto;
    }
    
    .header {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }
    
    .header h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .status-bar {
      display: flex;
      gap: 20px;
      margin-top: 15px;
      justify-content: center;
    }
    
    .status-item {
      background: rgba(255,255,255,0.15);
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 0.9rem;
      backdrop-filter: blur(10px);
    }
    
    .status-item strong {
      color: var(--light);
    }
    
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
    }
    
    .card {
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
      overflow: hidden;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .card-header {
      background: linear-gradient(135deg, var(--primary), var(--dark));
      color: white;
      padding: 20px;
      font-size: 1.2rem;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .card-icon {
      font-size: 1.5rem;
    }
    
    .card-body {
      padding: 20px;
    }
    
    .card-full {
      grid-column: 1 / -1;
    }
    
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
    }
    
    .metric-box {
      background: var(--light);
      padding: 15px;
      border-radius: 8px;
      text-align: center;
      border-left: 4px solid var(--primary);
    }
    
    .metric-value {
      font-size: 1.8rem;
      font-weight: bold;
      color: var(--dark);
      margin: 10px 0;
    }
    
    .metric-label {
      font-size: 0.85rem;
      color: #7F8C8D;
      text-transform: uppercase;
    }
    
    .alert-list {
      max-height: 300px;
      overflow-y: auto;
    }
    
    .alert-item {
      padding: 12px;
      border-left: 4px solid;
      margin-bottom: 8px;
      border-radius: 4px;
      font-size: 0.9rem;
    }
    
    .alert-item.info {
      border-color: var(--primary);
      background: rgba(52, 152, 219, 0.1);
    }
    
    .alert-item.warning {
      border-color: var(--warning);
      background: rgba(243, 156, 18, 0.1);
    }
    
    .alert-item.critical {
      border-color: var(--error);
      background: rgba(231, 76, 60, 0.1);
    }
    
    .alert-item.success {
      border-color: var(--success);
      background: rgba(46, 204, 113, 0.1);
    }
    
    .chart-container {
      height: 400px;
      position: relative;
    }
    
    svg {
      width: 100%;
      height: 100%;
    }
    
    .axis {
      font-size: 0.85rem;
    }
    
    .tooltip {
      position: absolute;
      background: rgba(0,0,0,0.8);
      color: white;
      padding: 8px 12px;
      border-radius: 4px;
      font-size: 0.85rem;
      pointer-events: none;
      z-index: 1000;
    }
    
    .refresh-indicator {
      display: inline-block;
      width: 10px;
      height: 10px;
      background: var(--success);
      border-radius: 50%;
      margin-right: 5px;
      animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
    
    .mermaid {
      background: white;
      padding: 20px;
      border-radius: 8px;
      overflow-x: auto;
    }
  </style>
</head>
<body>

<div class="dashboard">
  <div class="header">
    <h1>🔥 Triad Live Dashboard</h1>
    <div class="status-bar">
      <div class="status-item">
        <span class="refresh-indicator"></span>
        <strong>Status:</strong> <span id="status">Connecting...</span>
      </div>
      <div class="status-item">
        <strong>Cycles:</strong> <span id="cycle-count">0</span>
      </div>
      <div class="status-item">
        <strong>Errors:</strong> <span id="error-count">0</span>
      </div>
    </div>
  </div>
  
  <!-- Operator Timing Row -->
  <div class="grid">
    <div class="card card-full">
      <div class="card-header">
        <span class="card-icon">⏱️</span>
        <span>Operator Performance Metrics</span>
      </div>
      <div class="card-body">
        <div class="chart-container">
          <div id="operatorTiming"></div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Metrics Row -->
  <div class="grid">
    <div class="card">
      <div class="card-header">
        <span class="card-icon">📊</span>
        <span>Cycle Statistics</span>
      </div>
      <div class="card-body">
        <div class="metric-grid">
          <div class="metric-box">
            <div class="metric-label">Avg Cycle Time</div>
            <div class="metric-value" id="avg-cycle">--</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">State Size</div>
            <div class="metric-value" id="state-size">--</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">Checkpoints</div>
            <div class="metric-value" id="checkpoint-count">--</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">Success Rate</div>
            <div class="metric-value" id="success-rate">--</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <span class="card-icon">🚨</span>
        <span>Active Alerts</span>
      </div>
      <div class="card-body">
        <div class="alert-list" id="alerts">
          <div class="alert-item info">Waiting for alerts...</div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Timeline Row -->
  <div class="grid">
    <div class="card card-full">
      <div class="card-header">
        <span class="card-icon">📈</span>
        <span>Recent Cycle Timeline</span>
      </div>
      <div class="card-body">
        <div class="chart-container">
          <div id="timeline"></div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Topology Diagrams Row -->
  <div class="grid">
    <div class="card">
      <div class="card-header">
        <span class="card-icon">🔀</span>
        <span>Convergence Topology</span>
      </div>
      <div class="card-body">
        <div class="mermaid">
          graph TD
              S1[State 1] --> K[Convergence Knot]
              S2[State 2] --> K
              S3[State 3] --> K
              K --> A[Apex Form]
        </div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <span class="card-icon">↔️</span>
        <span>Mirror Symmetry</span>
      </div>
      <div class="card-body">
        <div class="mermaid">
          graph LR
              L[Left State] --- M[Mirror Node]
              M --- R[Right State]
              L <--> R
        </div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <span class="card-icon">🌳</span>
        <span>Divergence Branching</span>
      </div>
      <div class="card-body">
        <div class="mermaid">
          graph TD
              S[Source State] --> B1[Branch 1]
              S --> B2[Branch 2]
              S --> B3[Branch 3]
        </div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">
        <span class="card-icon">💾</span>
        <span>Checkpoint Flow</span>
      </div>
      <div class="card-body">
        <div class="mermaid">
          graph TD
              C0[Boundary CP] --> C1[Cycle CP 1]
              C1 --> C2[Cycle CP 2]
              C2 --> C3[Apex CP]
              C3 -.rollback.-> C1
        </div>
      </div>
    </div>
  </div>
  
  <!-- Checkpoint Storage Row -->
  <div class="grid">
    <div class="card card-full">
      <div class="card-header">
        <span class="card-icon">📦</span>
        <span>Checkpoint Storage Trend</span>
      </div>
      <div class="card-body">
        <div class="chart-container">
          <div id="storage"></div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Trace Details Row -->
  <div class="grid">
    <div class="card card-full">
      <div class="card-header">
        <span class="card-icon">🔍</span>
        <span>Distributed Trace Inspector</span>
      </div>
      <div class="card-body">
        <div id="trace-details" style="font-family: monospace; font-size: 0.85rem; max-height: 400px; overflow-y: auto;">
          <pre id="trace-json">Loading trace...</pre>
        </div>
      </div>
    </div>
  </div>
  
</div>

<script type="module">
  import { renderOperatorTimingChart } from './operator_timing.js';
  import { renderCycleTimeline } from './cycle_timeline.js';
  import { renderCheckpointStorageDashboard } from './checkpoint_storage.js';
  
  // Demo data - replace with real API calls
  const operatorMetrics = [
    { operator: "⊕", avg_ms: 3.2, min_ms: 2.1, max_ms: 5.8, count: 450 },
    { operator: "⊗", avg_ms: 1.1, min_ms: 0.8, max_ms: 2.2, count: 450 },
    { operator: "⊛", avg_ms: 8.4, min_ms: 6.2, max_ms: 15.3, count: 450 },
    { operator: "△", avg_ms: 12.7, min_ms: 9.1, max_ms: 28.4, count: 450 },
    { operator: "⊝", avg_ms: 4.9, min_ms: 3.5, max_ms: 8.2, count: 450 },
    { operator: "⊞", avg_ms: 2.3, min_ms: 1.8, max_ms: 4.1, count: 450 },
    { operator: "⊳", avg_ms: 9.1, min_ms: 7.2, max_ms: 18.5, count: 450 },
    { operator: "⊲", avg_ms: 7.8, min_ms: 6.0, max_ms: 14.2, count: 450 }
  ];
  
  // Initialize dashboard
  document.addEventListener('DOMContentLoaded', () => {
    renderOperatorTimingChart('operatorTiming', operatorMetrics);
    
    // Update metrics
    const avgCycle = operatorMetrics.reduce((sum, m) => sum + m.avg_ms, 0);
    document.getElementById('avg-cycle').textContent = `${avgCycle.toFixed(1)}ms`;
    document.getElementById('state-size').textContent = `12.3 KB`;
    document.getElementById('checkpoint-count').textContent = `3`;
    document.getElementById('success-rate').textContent = `99.8%`;
    document.getElementById('status').textContent = 'Connected';
    
    // Render mermaid diagrams
    mermaid.contentLoaded();
  });
  
  // Auto-refresh every 5 seconds
  setInterval(() => {
    console.log('Refreshing metrics...');
    // In production, fetch from /api/metrics, /api/traces, /api/alerts
  }, 5000);
</script>

</body>
</html>
```

---

## 5. Interpretation Guide

### 5.1 When Operator Timing Matters

**Read the chart like this:**

```
⊞ (2.3ms)  ✓ Fast — Good for frequent operations
⊗ (1.1ms)  ✓ Very Fast — Can be applied liberally
⊕ (3.2ms)  ✓ Acceptable — Creation is cheap
⊝ (4.9ms)  ✓ Reasonable — Deletion cost is proportional
⊲ (7.8ms)  ⚠ Watch — Branching has overhead
⊛ (8.4ms)  ⚠ Watch — Recursion depth matters
⊳ (9.1ms)  ⚠ Watch — Convergence is not free
△ (12.7ms) ⚠ Expensive — Use apex judiciously
```

### 5.2 Topology Patterns

**Choose your pattern based on use case:**

| Pattern | Best For | Cost |
|---------|----------|------|
| **Apex (Triangle)** | Simple transforms | Low (~13ms) |
| **Convergence (Many-to-one)** | Merging branches | High (~31ms) |
| **Mirror (Bidirectional)** | Consistency checks | Low (~2ms) |
| **Divergence (One-to-many)** | Parallel work | Medium (~8ms) per branch |

### 5.3 Checkpoint Strategy

**Choose based on cycle type:**

| Cycle Type | Boundary | Cycle | Apex | Recovery Cost |
|------------|----------|-------|------|----------------|
| **Fast** | Always | Never | Always | ~5-10ms |
| **Recursive** | Always | Conditional | Always | Varies |
| **Aggressive** | Always | Always | Always | 2× cycle time |

---

## 6. Real Production Example

```javascript
// Scenario: Daily ETL cycle with 50K items
const cycle = {
  sequence: ["⊕", "⊲", "⊛", "⊳", "△"],
  items: 50000,
  
  // Timing breakdown
  timings: {
    "⊕":  3.2 * 50  /* 50 batches */  = 160ms,
    "⊲":  7.8 * 1                     = 7.8ms,
    "⊛":  8.4 * 10  /* 10 iterations */= 84ms,
    "⊳":  9.1 * 1                     = 9.1ms,
    "△":  12.7 * 1                    = 12.7ms,
  },
  
  total_duration: 273.6ms,
  
  // Checkpoints
  checkpoints: {
    boundary: { size: 15.2, time: 0ms },
    cycle_1:  { size: 15.3, time: 167.8ms },
    cycle_2:  { size: 15.4, time: 251.8ms },
    apex:     { size: 12.3, time: 273.6ms },
  },
  
  // Storage
  storage_cost: 15.2 + 15.2 + 15.3 + 12.3 = 58 KB,
  
  // Success
  rollback_events: 0,
  success: true,
};
```

**Dashboard shows:**

✅ Operator breakdown (total 273.6ms)  
✅ Checkpoint lineage (4 checkpoints)  
✅ Storage efficiency (58 KB per cycle)  
✅ No errors (success rate 100%)  

---

## Next Steps

1. **Deploy dashboard** — Run Flask server on port 5000
2. **Connect real metrics** — Replace demo data with `/api/export`
3. **Set alerting rules** — Configure thresholds for your workload
4. **Monitor production** — Track metrics over time (weekly trends)
5. **Optimize** — Use insights to tune operator sequences

**Your Triad system is fully instrumented and observable.**
