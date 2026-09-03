# 📊 Observability & Visualization

*Metrics • Traces • Dashboards • Real-time Monitoring*

---

## Overview

The **Observability System** provides complete visibility into Triad execution with:

- **Metrics collection** — Operator timing, cost tracking, error rates
- **Distributed tracing** — Full cycle flow with latency breakdowns
- **Live dashboards** — D3.js visualizations with real-time updates
- **Alerting** — Anomaly detection and threshold violations
- **Historical analysis** — Trend analysis and performance regression detection

---

## 1. Metrics Collection Infrastructure

### 1.1 Core Observability Engine

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from enum import Enum
import time
import json

class MetricType(Enum):
    """Types of metrics."""
    COUNTER = "counter"      # Monotonically increasing
    GAUGE = "gauge"          # Current value
    HISTOGRAM = "histogram"  # Distribution of values
    SUMMARY = "summary"      # Aggregated statistics

@dataclass
class Metric:
    """Individual metric data point."""
    name: str
    value: float
    metric_type: MetricType
    tags: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "type": self.metric_type.value,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
        }

@dataclass
class TraceSpan:
    """Distributed trace span."""
    span_id: str
    parent_span_id: Optional[str]
    trace_id: str
    name: str
    service: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"  # running, success, error
    error_message: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "trace_id": self.trace_id,
            "name": self.name,
            "service": self.service,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "error_message": self.error_message,
            "attributes": self.attributes,
            "events": self.events,
        }

class TriadObservability:
    """
    Central observability system for Triad.
    Collects metrics, traces, and exposes dashboards.
    """
    
    def __init__(self, service_name: str = "triad"):
        self.service_name = service_name
        
        # Storage
        self.metrics: List[Metric] = []
        self.spans: List[TraceSpan] = []
        self.alerts: List[Dict[str, Any]] = []
        
        # State
        self.active_spans: Dict[str, TraceSpan] = {}
        self.metric_aggregates: Dict[str, Dict[str, Any]] = {}
        
        # Configuration
        self.metric_retention_ms = 3600 * 1000  # 1 hour
        self.span_retention_ms = 3600 * 1000    # 1 hour
        self.export_callbacks: List[Callable] = []
    
    # --- Metrics API ---
    
    def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        tags: Dict[str, str] = None
    ) -> None:
        """Record a metric."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        self._update_aggregates(metric)
    
    def counter(self, name: str, value: float = 1.0, tags: Dict[str, str] = None) -> None:
        """Record counter (monotonically increasing)."""
        self.record_metric(name, value, MetricType.COUNTER, tags)
    
    def gauge(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record gauge (current value)."""
        self.record_metric(name, value, MetricType.GAUGE, tags)
    
    def histogram(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record histogram (distribution)."""
        self.record_metric(name, value, MetricType.HISTOGRAM, tags)
    
    def _update_aggregates(self, metric: Metric) -> None:
        """Update running aggregates for metrics."""
        key = f"{metric.name}:{','.join(f'{k}={v}' for k, v in sorted(metric.tags.items()))}"
        
        if key not in self.metric_aggregates:
            self.metric_aggregates[key] = {
                "count": 0,
                "sum": 0,
                "min": float('inf'),
                "max": float('-inf'),
                "last_value": None,
                "last_timestamp": None,
            }
        
        agg = self.metric_aggregates[key]
        agg["count"] += 1
        agg["sum"] += metric.value
        agg["min"] = min(agg["min"], metric.value)
        agg["max"] = max(agg["max"], metric.value)
        agg["last_value"] = metric.value
        agg["last_timestamp"] = metric.timestamp
    
    # --- Tracing API ---
    
    def start_span(
        self,
        name: str,
        trace_id: str = None,
        parent_span_id: str = None,
        attributes: Dict[str, Any] = None
    ) -> str:
        """Start a new trace span."""
        import uuid
        
        span_id = str(uuid.uuid4())[:8]
        trace_id = trace_id or str(uuid.uuid4())
        
        span = TraceSpan(
            span_id=span_id,
            parent_span_id=parent_span_id,
            trace_id=trace_id,
            name=name,
            service=self.service_name,
            start_time=datetime.now(),
            attributes=attributes or {}
        )
        
        self.active_spans[span_id] = span
        return span_id
    
    def add_event(self, span_id: str, event_name: str, attributes: Dict[str, Any] = None) -> None:
        """Add event to span."""
        if span_id in self.active_spans:
            self.active_spans[span_id].events.append({
                "name": event_name,
                "timestamp": datetime.now().isoformat(),
                "attributes": attributes or {}
            })
    
    def end_span(
        self,
        span_id: str,
        status: str = "success",
        error_message: str = None
    ) -> None:
        """End a trace span."""
        if span_id in self.active_spans:
            span = self.active_spans[span_id]
            span.end_time = datetime.now()
            span.status = status
            span.error_message = error_message
            
            self.spans.append(span)
            del self.active_spans[span_id]
            
            # Auto-export
            self._export_span(span)
    
    def _export_span(self, span: TraceSpan) -> None:
        """Export span to registered callbacks."""
        for callback in self.export_callbacks:
            try:
                callback("span", span.to_dict())
            except Exception as e:
                print(f"Export callback error: {e}")
    
    # --- Alerting ---
    
    def check_alert(
        self,
        metric_name: str,
        condition: Callable[[float], bool],
        alert_name: str = "",
        severity: str = "warning"
    ) -> bool:
        """
        Check if metric triggers alert.
        
        Args:
            metric_name: Name of metric to check
            condition: Function(value) -> bool
            alert_name: Alert name/description
            severity: "info", "warning", "critical"
        
        Returns:
            True if alert triggered
        """
        # Find latest metric value
        for metric in reversed(self.metrics):
            if metric.name == metric_name:
                if condition(metric.value):
                    self.alerts.append({
                        "alert_name": alert_name or metric_name,
                        "metric_name": metric_name,
                        "value": metric.value,
                        "severity": severity,
                        "timestamp": datetime.now().isoformat(),
                    })
                    return True
                return False
        
        return False
    
    def get_alerts(self, severity: str = None) -> List[Dict[str, Any]]:
        """Get active alerts, optionally filtered by severity."""
        if severity:
            return [a for a in self.alerts if a["severity"] == severity]
        return self.alerts
    
    # --- Queries ---
    
    def get_metric_stats(self, metric_name: str, tags: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """Get aggregated stats for a metric."""
        key_prefix = metric_name
        if tags:
            key_prefix += ":" + ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        
        matching_keys = [k for k in self.metric_aggregates if k.startswith(key_prefix)]
        
        if not matching_keys:
            return None
        
        # Merge matching keys
        total_count = 0
        total_sum = 0
        overall_min = float('inf')
        overall_max = float('-inf')
        
        for key in matching_keys:
            agg = self.metric_aggregates[key]
            total_count += agg["count"]
            total_sum += agg["sum"]
            overall_min = min(overall_min, agg["min"])
            overall_max = max(overall_max, agg["max"])
        
        return {
            "metric_name": metric_name,
            "count": total_count,
            "sum": total_sum,
            "avg": total_sum / total_count if total_count > 0 else 0,
            "min": overall_min if overall_min != float('inf') else None,
            "max": overall_max if overall_max != float('-inf') else None,
        }
    
    def get_traces(self, trace_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get traces, optionally filtered by trace_id."""
        if trace_id:
            spans = [s for s in self.spans if s.trace_id == trace_id]
        else:
            spans = self.spans[-limit:]
        
        return [s.to_dict() for s in spans]
    
    def get_trace_timeline(self, trace_id: str) -> List[Dict[str, Any]]:
        """Get trace as ordered timeline (parent -> child spans)."""
        spans = [s for s in self.spans if s.trace_id == trace_id]
        
        # Build tree
        root_spans = [s for s in spans if s.parent_span_id is None]
        
        timeline = []
        
        def traverse(span: TraceSpan, depth: int = 0) -> None:
            timeline.append({
                "depth": depth,
                "span": span.to_dict(),
            })
            
            children = [s for s in spans if s.parent_span_id == span.span_id]
            for child in sorted(children, key=lambda s: s.start_time):
                traverse(child, depth + 1)
        
        for root in sorted(root_spans, key=lambda s: s.start_time):
            traverse(root)
        
        return timeline
    
    # --- Cleanup ---
    
    def cleanup_old_data(self) -> None:
        """Remove old metrics and spans based on retention policy."""
        now = datetime.now()
        
        # Clean metrics
        self.metrics = [
            m for m in self.metrics
            if (now - m.timestamp).total_seconds() * 1000 < self.metric_retention_ms
        ]
        
        # Clean spans
        self.spans = [
            s for s in self.spans
            if (now - s.start_time).total_seconds() * 1000 < self.span_retention_ms
        ]
    
    def export_json(self) -> Dict[str, Any]:
        """Export all data as JSON."""
        return {
            "service": self.service_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": [m.to_dict() for m in self.metrics],
            "spans": [s.to_dict() for s in self.spans],
            "aggregates": self.metric_aggregates,
            "alerts": self.alerts,
        }
```

---

## 2. Integration with Triad Engines

### 2.1 Observable Einstein Runner

```python
class ObservableEinsteinRunner(SafeEinsteinRunner):
    """
    Einstein runner instrumented with observability.
    """
    
    def __init__(
        self,
        operators: Dict[str, Any],
        fusion_rules: Dict[tuple, str],
        hydrogenesi: HydrogenesiEngine,
        obs: TriadObservability
    ):
        super().__init__(operators, fusion_rules, hydrogenesi)
        self.obs = obs
    
    def execute_with_recovery(
        self,
        initial_state: Any,
        sequence: List[str],
        params: List[Dict[str, Any]],
        aggressive_checkpointing: bool = False,
        trace_id: str = None
    ) -> tuple[Any, bool]:
        """Execute with full tracing."""
        import uuid
        trace_id = trace_id or str(uuid.uuid4())
        
        # Start main trace
        cycle_span = self.obs.start_span(
            "einstein.cycle",
            trace_id=trace_id,
            attributes={
                "sequence_length": len(sequence),
                "sequence": "→".join(sequence),
            }
        )
        
        cycle_start = time.perf_counter()
        current_state = initial_state
        success = True
        
        # Boundary tier
        boundary_span = self.obs.start_span(
            "einstein.boundary",
            trace_id=trace_id,
            parent_span_id=cycle_span,
        )
        
        self.hydrogenesi.checkpoint(
            current_state,
            {"phase": "boundary", "sequence": sequence},
            checkpoint_type="boundary"
        )
        
        self.obs.end_span(boundary_span, status="success")
        
        # Execute operators
        cycle_tier_span = self.obs.start_span(
            "einstein.cycle_tier",
            trace_id=trace_id,
            parent_span_id=cycle_span,
        )
        
        for op_index, (op_symbol, op_params) in enumerate(zip(sequence, params)):
            try:
                operator = self._get_operator(op_symbol)
                
                # Operator span
                op_span = self.obs.start_span(
                    f"operator.{op_symbol}",
                    trace_id=trace_id,
                    parent_span_id=cycle_tier_span,
                    attributes={
                        "operator_name": getattr(operator, 'name', op_symbol),
                        "index": op_index,
                    }
                )
                
                # Execute
                start_time = time.perf_counter()
                result_state = self._execute_operator(operator, current_state, op_params)
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                
                # Record metrics
                self.obs.histogram(
                    "operator_duration_ms",
                    elapsed_ms,
                    tags={"operator": op_symbol}
                )
                
                self.obs.gauge(
                    "operator_state_size_bytes",
                    len(str(result_state).encode()),
                    tags={"operator": op_symbol}
                )
                
                self.obs.end_span(op_span, status="success")
                current_state = result_state
            
            except Exception as e:
                success = False
                self.obs.end_span(op_span, status="error", error_message=str(e))
                self.obs.counter("operator_errors", tags={"operator": op_symbol})
                
                # Attempt recovery
                recovery_result = self._attempt_recovery(
                    e, op_symbol, current_state, op_index, sequence, params
                )
                
                if not recovery_result:
                    self.obs.end_span(cycle_tier_span, status="error")
                    self.obs.end_span(cycle_span, status="error", error_message=str(e))
                    raise
        
        self.obs.end_span(cycle_tier_span, status="success")
        
        # Apex tier
        apex_span = self.obs.start_span(
            "einstein.apex",
            trace_id=trace_id,
            parent_span_id=cycle_span,
        )
        
        self.hydrogenesi.checkpoint(
            current_state,
            {"phase": "apex"},
            checkpoint_type="apex"
        )
        
        self.obs.end_span(apex_span, status="success")
        
        # Record cycle metrics
        total_ms = (time.perf_counter() - cycle_start) * 1000
        self.obs.histogram(
            "cycle_duration_ms",
            total_ms,
            tags={"sequence_length": str(len(sequence))}
        )
        
        self.obs.end_span(cycle_span, status="success" if success else "partial")
        
        return current_state, success
```

### 2.2 Observable Hydrogenesi

```python
class ObservableHydrogenesiEngine(HydrogenesiEngine):
    """Hydrogenesi with observability."""
    
    def __init__(self, obs: TriadObservability = None):
        super().__init__()
        self.obs = obs or TriadObservability()
    
    def checkpoint(self, state: Any, context: Dict[str, Any], checkpoint_type: str = "cycle") -> str:
        """Checkpoint with metrics."""
        start = time.perf_counter()
        checkpoint_id = super().checkpoint(state, context, checkpoint_type)
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        state_size = len(str(state).encode())
        
        self.obs.histogram(
            "checkpoint_duration_ms",
            elapsed_ms,
            tags={"type": checkpoint_type}
        )
        
        self.obs.gauge(
            "checkpoint_state_size_bytes",
            state_size,
            tags={"type": checkpoint_type}
        )
        
        self.obs.gauge(
            "checkpoint_count",
            len(self.checkpoints),
            tags={"type": checkpoint_type}
        )
        
        return checkpoint_id
```

---

## 3. D3.js Dashboard Visualizations

### 3.1 Operator Timing Chart

```javascript
// operator_timing.js

export function renderOperatorTimingChart(containerId, metrics) {
  /**
   * metrics = [
   *   { operator: "⊕", avg_ms: 3.2, min_ms: 2.1, max_ms: 5.3, count: 150 },
   *   { operator: "⊗", avg_ms: 1.1, min_ms: 0.9, max_ms: 2.2, count: 150 },
   *   ...
   * ]
   */
  
  const width = 800;
  const height = metrics.length * 40 + 60;
  const margin = { top: 20, right: 20, bottom: 20, left: 80 };
  
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const chartWidth = width - margin.left - margin.right;
  const chartHeight = height - margin.top - margin.bottom;
  
  // Scales
  const x = d3.scaleLinear()
    .domain([0, d3.max(metrics, d => d.max_ms)])
    .range([0, chartWidth]);
  
  const y = d3.scaleBand()
    .domain(metrics.map(d => d.operator))
    .range([0, chartHeight])
    .padding(0.3);
  
  // Bars (average)
  g.selectAll("rect.bar")
    .data(metrics)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("y", d => y(d.operator))
    .attr("x", 0)
    .attr("width", d => x(d.avg_ms))
    .attr("height", y.bandwidth())
    .attr("fill", "#4A90E2")
    .attr("opacity", 0.8);
  
  // Min-Max range (error bars)
  g.selectAll("line.range")
    .data(metrics)
    .enter()
    .append("line")
    .attr("class", "range")
    .attr("x1", d => x(d.min_ms))
    .attr("x2", d => x(d.max_ms))
    .attr("y1", d => y(d.operator) + y.bandwidth() / 2)
    .attr("y2", d => y(d.operator) + y.bandwidth() / 2)
    .attr("stroke", "#999")
    .attr("stroke-width", 2)
    .attr("opacity", 0.5);
  
  // Y-axis (operators)
  g.append("g")
    .call(d3.axisLeft(y))
    .attr("class", "axis");
  
  // X-axis (timing)
  g.append("g")
    .attr("transform", `translate(0,${chartHeight})`)
    .call(d3.axisBottom(x))
    .attr("class", "axis");
  
  // Labels (average value + count)
  g.selectAll("text.value")
    .data(metrics)
    .enter()
    .append("text")
    .attr("class", "value")
    .attr("x", d => x(d.avg_ms) + 6)
    .attr("y", d => y(d.operator) + y.bandwidth() / 2 + 4)
    .attr("font-size", "12px")
    .text(d => `${d.avg_ms.toFixed(2)} ms (n=${d.count})`);
  
  // Title
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", 15)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .attr("font-weight", "bold")
    .text("Operator Timing (Average with Min-Max Range)");
}
```

### 3.2 Cycle Timeline

```javascript
// cycle_timeline.js

export function renderCycleTimeline(containerId, spans) {
  /**
   * spans (from get_trace_timeline) = [
   *   { depth: 0, span: { name: "einstein.cycle", duration_ms: 50, ... } },
   *   { depth: 1, span: { name: "operator.⊕", duration_ms: 3.2, ... } },
   *   { depth: 1, span: { name: "operator.⊗", duration_ms: 1.1, ... } },
   *   ...
   * ]
   */
  
  const width = 1000;
  const rowHeight = 24;
  const height = spans.length * rowHeight + 40;
  const margin = { top: 30, right: 20, bottom: 20, left: 200 };
  
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const chartWidth = width - margin.left - margin.right;
  
  // Find total duration
  const totalDuration = d3.max(spans, d => d.span.start_time
    ? new Date(d.span.end_time) - new Date(d.span.start_time)
    : 0) / 1000; // Convert to ms
  
  // Time scale
  const xScale = d3.scaleLinear()
    .domain([0, totalDuration])
    .range([0, chartWidth]);
  
  // Base time (first span start)
  const baseTime = new Date(spans[0].span.start_time).getTime();
  
  // Bars
  g.selectAll("rect.span")
    .data(spans)
    .enter()
    .append("rect")
    .attr("class", "span")
    .attr("y", (_, i) => i * rowHeight)
    .attr("x", d => {
      const start = new Date(d.span.start_time).getTime();
      return xScale((start - baseTime) / 1000);
    })
    .attr("width", d => xScale(d.span.duration_ms / 1000))
    .attr("height", rowHeight - 2)
    .attr("fill", d => {
      if (d.span.status === "error") return "#E74C3C";
      if (d.depth === 0) return "#3498DB";
      if (d.depth === 1) return "#2ECC71";
      return "#F39C12";
    })
    .attr("opacity", 0.8);
  
  // Labels (span names)
  g.selectAll("text.label")
    .data(spans)
    .enter()
    .append("text")
    .attr("class", "label")
    .attr("x", -10)
    .attr("y", (_, i) => i * rowHeight + rowHeight / 2 + 4)
    .attr("text-anchor", "end")
    .attr("font-size", "11px")
    .text(d => "  ".repeat(d.depth) + d.span.name);
  
  // Duration labels
  g.selectAll("text.duration")
    .data(spans)
    .enter()
    .append("text")
    .attr("class", "duration")
    .attr("x", d => {
      const start = new Date(d.span.start_time).getTime();
      return xScale((start - baseTime) / 1000) + xScale(d.span.duration_ms / 1000) + 6;
    })
    .attr("y", (_, i) => i * rowHeight + rowHeight / 2 + 4)
    .attr("font-size", "10px")
    .text(d => `${d.span.duration_ms.toFixed(2)}ms`);
  
  // Time axis
  g.append("g")
    .call(d3.axisBottom(xScale))
    .attr("transform", `translate(0,${spans.length * rowHeight})`)
    .attr("class", "axis");
  
  // Title
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", 15)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .attr("font-weight", "bold")
    .text("Cycle Timeline (Trace Waterfall)");
}
```

### 3.3 Error Rate & Alert Dashboard

```javascript
// alerts_dashboard.js

export function renderAlertsDashboard(containerId, metrics, alerts) {
  /**
   * metrics = { 
   *   "cycle_duration_ms": { count: 100, avg: 45.2, min: 30, max: 120 },
   *   "operator_errors": { count: 5 }
   * }
   * alerts = [
   *   { alert_name: "High latency", metric_name: "cycle_duration_ms", value: 125, severity: "warning", timestamp: "..." },
   *   ...
   * ]
   */
  
  const width = 600;
  const height = 400;
  
  const container = d3.select(`#${containerId}`);
  
  // Metrics summary
  const metricsSummary = container.append("div")
    .attr("class", "metrics-summary");
  
  metricsSummary.append("h3").text("Metrics");
  
  const metricsList = metricsSummary.append("ul");
  Object.entries(metrics).forEach(([name, stats]) => {
    metricsList.append("li")
      .html(`<strong>${name}</strong>: avg=${stats.avg?.toFixed(2) || '?'} ms, count=${stats.count || '?'}`);
  });
  
  // Alerts
  const alertsDiv = container.append("div")
    .attr("class", "alerts");
  
  alertsDiv.append("h3").text("Active Alerts");
  
  if (alerts.length === 0) {
    alertsDiv.append("p").text("✓ No active alerts");
  } else {
    const alertsList = alertsDiv.append("ul");
    alerts.forEach(alert => {
      const severityColor = {
        "info": "#3498DB",
        "warning": "#F39C12",
        "critical": "#E74C3C"
      }[alert.severity] || "#95A5A6";
      
      alertsList.append("li")
        .style("border-left", `4px solid ${severityColor}`)
        .style("padding-left", "10px")
        .html(`<strong>${alert.alert_name}</strong> (${alert.severity}): ${alert.metric_name} = ${alert.value.toFixed(2)}`);
    });
  }
}
```

### 3.4 Checkpoint Storage Dashboard

```javascript
// checkpoint_storage.js

export function renderCheckpointStorageDashboard(containerId, checkpoints) {
  /**
   * checkpoints = [
   *   { id: "cp_000001", state_size_bytes: 15234, type: "cycle", timestamp: "..." },
   *   { id: "cp_000002", state_size_bytes: 15456, type: "apex", timestamp: "..." },
   * ]
   */
  
  const width = 800;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 60, left: 60 };
  
  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const chartWidth = width - margin.left - margin.right;
  const chartHeight = height - margin.top - margin.bottom;
  
  // Scales
  const x = d3.scaleLinear()
    .domain([0, checkpoints.length - 1])
    .range([0, chartWidth]);
  
  const y = d3.scaleLinear()
    .domain([0, d3.max(checkpoints, d => d.state_size_bytes)])
    .range([chartHeight, 0]);
  
  // Line generator
  const line = d3.line()
    .x((_, i) => x(i))
    .y(d => y(d.state_size_bytes));
  
  // Path
  g.append("path")
    .datum(checkpoints)
    .attr("fill", "none")
    .attr("stroke", "#3498DB")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  // Points
  g.selectAll("circle")
    .data(checkpoints)
    .enter()
    .append("circle")
    .attr("cx", (_, i) => x(i))
    .attr("cy", d => y(d.state_size_bytes))
    .attr("r", 4)
    .attr("fill", d => d.type === "apex" ? "#E74C3C" : "#2ECC71");
  
  // Axes
  g.append("g")
    .attr("transform", `translate(0,${chartHeight})`)
    .call(d3.axisBottom(x));
  
  g.append("g")
    .call(d3.axisLeft(y));
  
  // Labels
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", 15)
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text("State Size Over Checkpoints");
  
  svg.append("text")
    .attr("x", -height / 2)
    .attr("y", -margin.left + 15)
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Size (bytes)");
}
```

---

## 4. Real-Time Dashboard Server

### 4.1 Dashboard Endpoint

```python
from flask import Flask, jsonify, render_template
from flask_cors import CORS

class DashboardServer:
    """
    Serves observability dashboards via HTTP.
    """
    
    def __init__(self, obs: TriadObservability, port: int = 5000):
        self.obs = obs
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = port
        
        self._register_routes()
    
    def _register_routes(self):
        """Register Flask routes."""
        
        @self.app.route("/api/metrics", methods=["GET"])
        def get_metrics():
            return jsonify(self.obs.export_json()["metrics"])
        
        @self.app.route("/api/metrics/<metric_name>", methods=["GET"])
        def get_metric_stats(metric_name):
            stats = self.obs.get_metric_stats(metric_name)
            if stats:
                return jsonify(stats)
            return jsonify({"error": "metric not found"}), 404
        
        @self.app.route("/api/traces", methods=["GET"])
        def get_traces():
            trace_id = request.args.get("trace_id")
            traces = self.obs.get_traces(trace_id=trace_id)
            return jsonify(traces)
        
        @self.app.route("/api/trace/<trace_id>", methods=["GET"])
        def get_trace_timeline(trace_id):
            timeline = self.obs.get_trace_timeline(trace_id)
            return jsonify(timeline)
        
        @self.app.route("/api/alerts", methods=["GET"])
        def get_alerts():
            severity = request.args.get("severity")
            alerts = self.obs.get_alerts(severity=severity)
            return jsonify(alerts)
        
        @self.app.route("/api/export", methods=["GET"])
        def export_data():
            return jsonify(self.obs.export_json())
        
        @self.app.route("/dashboard", methods=["GET"])
        def dashboard():
            return render_template("dashboard.html")
    
    def run(self):
        """Start dashboard server."""
        print(f"Starting observability dashboard on http://localhost:{self.port}")
        self.app.run(host="0.0.0.0", port=self.port, debug=False)
```

### 4.2 HTML Dashboard Template

```html
<!-- templates/dashboard.html -->

<!DOCTYPE html>
<html>
<head>
  <title>Triad Observability Dashboard</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f5f5f5;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .dashboard {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .card {
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .card h3 {
      margin-top: 0;
      color: #333;
    }
    .full-width {
      grid-column: 1 / -1;
    }
    svg {
      width: 100%;
      height: auto;
    }
    .alert {
      padding: 12px;
      border-radius: 4px;
      margin-bottom: 10px;
    }
    .alert.warning {
      background-color: #FFF3CD;
      border-left: 4px solid #F39C12;
    }
    .alert.critical {
      background-color: #F8D7DA;
      border-left: 4px solid #E74C3C;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>🔥 Triad Observability Dashboard</h1>
    <p id="status">Connecting...</p>
  </div>
  
  <div class="dashboard">
    <div class="card full-width">
      <h3>Recent Trace</h3>
      <div id="timeline"></div>
    </div>
    
    <div class="card">
      <h3>Operator Timing</h3>
      <div id="timing"></div>
    </div>
    
    <div class="card">
      <h3>Alerts & Metrics</h3>
      <div id="alerts"></div>
    </div>
    
    <div class="card full-width">
      <h3>Checkpoint Storage</h3>
      <div id="storage"></div>
    </div>
  </div>
  
  <script type="module">
    import { renderOperatorTimingChart } from './operator_timing.js';
    import { renderCycleTimeline } from './cycle_timeline.js';
    import { renderAlertsDashboard } from './alerts_dashboard.js';
    import { renderCheckpointStorageDashboard } from './checkpoint_storage.js';
    
    async function loadDashboard() {
      try {
        const exportData = await fetch('/api/export').then(r => r.json());
        
        document.getElementById('status').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        
        // Operator timing
        const operatorMetrics = {};
        exportData.metrics.forEach(m => {
          if (m.name === 'operator_duration_ms') {
            const op = m.tags.operator;
            if (!operatorMetrics[op]) {
              operatorMetrics[op] = { operator: op, values: [] };
            }
            operatorMetrics[op].values.push(m.value);
          }
        });
        
        const operatorData = Object.values(operatorMetrics).map(m => ({
          operator: m.operator,
          avg_ms: m.values.reduce((a,b) => a+b, 0) / m.values.length,
          min_ms: Math.min(...m.values),
          max_ms: Math.max(...m.values),
          count: m.values.length,
        }));
        
        renderOperatorTimingChart('timing', operatorData);
        
        // Latest trace
        const traces = await fetch('/api/traces?limit=1').then(r => r.json());
        if (traces.length > 0) {
          const trace = await fetch(`/api/trace/${traces[0].trace_id}`).then(r => r.json());
          renderCycleTimeline('timeline', trace);
        }
        
        // Alerts
        const alerts = await fetch('/api/alerts').then(r => r.json());
        renderAlertsDashboard('alerts', {}, alerts);
        
      } catch (e) {
        console.error('Dashboard error:', e);
        document.getElementById('status').textContent = 'Error loading dashboard';
      }
    }
    
    loadDashboard();
    setInterval(loadDashboard, 5000); // Refresh every 5 seconds
  </script>
</body>
</html>
```

---

## Summary

**Observability & Visualization** provides:

✅ **Comprehensive metrics collection** — Counter, gauge, histogram, summary  
✅ **Distributed tracing** — Full cycle flow with parent-child relationships  
✅ **D3.js dashboards** — Operator timing, cycle timeline, alerts  
✅ **Real-time monitoring** — Live updates, anomaly detection  
✅ **Production-grade** — Retention policies, cleanup, export  

**Next Steps**:
1. Deploy dashboard server alongside Triad
2. Configure alerting rules for your SLOs
3. Integrate with APM (Datadog, New Relic, etc.)
4. Build custom dashboards for your domain
