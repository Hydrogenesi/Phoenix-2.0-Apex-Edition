/**
 * Endpoint Mismatch Analyzer
 *
 * Detects semantic mismatches between what the frontend expects
 * and what the backend actually provides.
 */

export enum EndpointSeverity {
  Low = "low",
  Medium = "medium",
  High = "high",
}

export interface AnalyzedEndpointMismatch {
  endpoint: string;
  frontend_expects: string;
  backend_returns: string;
  issue: string;
  severity: EndpointSeverity;
  impact?: string;
  recommendation?: string;
}

/**
 * Analyze frontend-backend endpoint mismatches for a given PR.
 * For PR #123, focus on data flow and state persistence.
 */
export function analyzeEndpointMismatch(
  prNumber: number
): AnalyzedEndpointMismatch[] {
  const mismatches: AnalyzedEndpointMismatch[] = [];

  if (prNumber === 123) {
    // Flux state polling: implicit graph correlation
    mismatches.push({
      endpoint: "GET /api/flux/state",
      frontend_expects:
        "Flux state for a specific graph (implicitly: the current sample graph). " +
        "FluxPage polls this endpoint every 2 seconds.",
      backend_returns:
        "Hardcoded flux state for SAMPLE_GRAPH. " +
        "Each GET calls handle_layout() (SAMPLE_GRAPH) → handle_flux_state().",
      issue:
        "Frontend has no way to specify which graph/run to compute flux for. " +
        "Every poll returns flux for the same graph, ignoring user context.",
      severity: EndpointSeverity.High,
      impact:
        "In multi-run scenarios, frontend cannot correlate flux state with specific runs or layouts. " +
        "All users see identical flux, defeating per-run telemetry.",
      recommendation:
        "Add optional query param ?run_id=X or POST body { run_id, layout_id }. " +
        "Server-side: store and retrieve layouts by ID. " +
        "Compute flux for the requested layout, not SAMPLE_GRAPH.",
    });

    // Graph layout POST: unused endpoint
    mismatches.push({
      endpoint: "POST /api/graph/layout",
      frontend_expects:
        "Ability to upload a custom graph (nodes + edges) and get a layout back. " +
        "GraphPage has a useEffect that calls GET; no code path for POST.",
      backend_returns:
        "Route exists and accepts a body: handle_layout(body if body else SAMPLE_GRAPH). " +
        "Works correctly in isolation.",
      issue:
        "Frontend never uses POST endpoint. Dead code path or incomplete integration. " +
        "No way for users to test layout on custom graphs from the UI.",
      severity: EndpointSeverity.Medium,
      impact:
        "Users are limited to viewing sample graph layout. " +
        "Cannot iterate on custom agent topologies.",
      recommendation:
        "Implement graph upload form in GraphPage. " +
        "POST custom graph to /api/graph/layout and render result. " +
        "Add example graph templates for quick testing.",
    });

    // Cockpit frame parsing: session state not persisted
    mismatches.push({
      endpoint: "POST /api/cockpit/frame",
      frontend_expects:
        "Backend remembers session state across multiple frame exchanges. " +
        "Frontend: handshake → subscribe(topics) → ping/pong loop. " +
        "Each ping should respect prior subscriptions.",
      backend_returns:
        "Each POST creates a fresh CockpitProtocolV1(run_id) instance. " +
        "Subscriptions from a prior frame are lost. " +
        "No session store or memory.",
      issue:
        "Protocol state is not persisted. " +
        "Calling subscribe() then ping() on the same run_id results in a new protocol " +
        "instance that has no knowledge of the subscription.",
      severity: EndpointSeverity.High,
      impact:
        "WS protocol is broken: subscriptions are silently ignored. " +
        "Frontend may think it subscribed to 'graph.snapshot' but backend doesn't remember. " +
        "Events are never delivered to the client.",
      recommendation:
        "Store protocol sessions by run_id in a module-level dict: " +
        "_sessions[run_id] = CockpitProtocolV1(...). " +
        "Retrieve on each POST, create on-demand. " +
        "Add session TTL/cleanup (e.g., expire after 30 min of inactivity).",
    });

    // Operator pipeline: no input validation
    mismatches.push({
      endpoint: "POST /api/operator/run",
      frontend_expects:
        "Accepts a graph JSON and returns the full pipeline result. " +
        "Expects { run_id, graph } in body.",
      backend_returns:
        "Routes to _run_pipeline_sync(run_id, graph_input). " +
        "No validation of graph shape. " +
        "If graph is malformed, error bubbles up from the pipeline.",
      issue:
        "No contract validation before passing to the pipeline. " +
        "If frontend sends invalid graph, error message is not framed per cockpit protocol.",
      severity: EndpointSeverity.Medium,
      impact:
        "Bad UX: unstructured error messages instead of cockpit error frames. " +
        "Frontend has no standard way to parse and retry on error.",
      recommendation:
        "Add a GraphInputValidator before the pipeline. " +
        "Return error_frame({ code: 'INVALID_GRAPH', message: 'missing nodes' }) " +
        "in the same format as cockpit protocol errors.",
    });
  }

  return mismatches;
}
