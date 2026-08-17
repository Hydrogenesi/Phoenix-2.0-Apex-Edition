/**
 * Missing Test Matrix Analyzer
 *
 * Suggests tests to close coverage gaps identified in multi-layer PR review.
 */

export enum TestGapSeverity {
  Low = "low",
  Medium = "medium",
  High = "high",
}

export interface AnalyzedTestGap {
  area: string;
  suggestion: string;
  why_matters: string;
  severity: TestGapSeverity;
  test_skeleton?: string;
}

/**
 * Analyze missing test coverage for a given PR.
 * For PR #123, focus on HTTP semantics, WS protocol state, concurrency, and contracts.
 */
export function analyzeMissingTestMatrix(
  prNumber: number
): AnalyzedTestGap[] {
  const gaps: AnalyzedTestGap[] = [];

  if (prNumber === 123) {
    // HTTP layer tests
    gaps.push({
      area: "HTTP",
      suggestion:
        "Add test for POST /api/graph/layout with malformed JSON " +
        "(missing 'nodes' or 'edges' key, extra fields).",
      why_matters:
        "Backend should return 400 with clear error message, not 500 or silent truncation.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_graph_layout_post_malformed():\n" +
        "  POST { nodes: [] } (missing edges)\n" +
        "  assert status == 400\n" +
        "  assert error message mentions 'edges'",
    });

    gaps.push({
      area: "HTTP",
      suggestion:
        "Add test for oversized payload (> 10 MB) to POST /api/operator/run.",
      why_matters:
        "Prevents DoS via memory exhaustion. Guards HTTP layer boundaries. " +
        "Server should reject with 413 Payload Too Large.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_operator_run_oversized_payload():\n" +
        "  payload = { graph: { nodes: [huge list] } }  # > 10 MB\n" +
        "  POST /api/operator/run\n" +
        "  assert status == 413 or 400",
    });

    gaps.push({
      area: "HTTP",
      suggestion:
        "Add test for missing Content-Length header or chunked encoding.",
      why_matters:
        "Ensures HTTP layer handles edge cases gracefully.",
      severity: TestGapSeverity.Low,
      test_skeleton:
        "test_post_without_content_length():\n" +
        "  POST with chunked encoding\n" +
        "  assert status 200 or 411 (Length Required)",
    });

    gaps.push({
      area: "HTTP",
      suggestion:
        "Add test for CORS preflight (OPTIONS) on all POST/GET routes.",
      why_matters:
        "Frontend on localhost:5173 makes cross-origin requests to :8000. " +
        "Browser enforces CORS; test ensures headers are correct.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_cors_preflight():\n" +
        "  OPTIONS /api/graph/layout\n" +
        "  assert Access-Control-Allow-Origin: *\n" +
        "  assert Access-Control-Allow-Methods: GET, POST, OPTIONS",
    });

    // WebSocket protocol tests
    gaps.push({
      area: "WS",
      suggestion:
        "Add test: subscribe → unsubscribe → resubscribe to same topic. " +
        "Verify no ghost subscriptions.",
      why_matters:
        "Detects session state bugs. Ensures cleanup works. " +
        "Prevents duplicate event delivery.",
      severity: TestGapSeverity.High,
      test_skeleton:
        "test_ws_subscribe_unsubscribe_resubscribe():\n" +
        "  POST /api/cockpit/frame { subscribe [graph.snapshot] }\n" +
        "  POST /api/cockpit/frame { unsubscribe [graph.snapshot] }\n" +
        "  POST /api/cockpit/frame { subscribe [graph.snapshot] }\n" +
        "  verify only one subscription active (no duplicate)",
    });

    gaps.push({
      area: "WS",
      suggestion:
        "Add test: send PING before SUBSCRIBE. Backend should queue or return error.",
      why_matters:
        "Validates protocol state machine. Prevents out-of-order races. " +
        "Ensures ping only responds if session exists.",
      severity: TestGapSeverity.High,
      test_skeleton:
        "test_ws_ping_before_subscribe():\n" +
        "  POST /api/cockpit/frame { ping }  # no prior subscribe\n" +
        "  assert error or queued (not silent drop)",
    });

    gaps.push({
      area: "WS",
      suggestion:
        "Add test: multiple clients with same run_id simultaneously " +
        "send SUBSCRIBE for different topics. Verify isolation.",
      why_matters:
        "Ensures session state is per-run-id and per-client, not global. " +
        "Prevents crosstalk between concurrent clients.",
      severity: TestGapSeverity.High,
      test_skeleton:
        "test_ws_concurrent_clients_same_runid():\n" +
        "  client1.subscribe([graph.snapshot])\n" +
        "  client2.subscribe([flux.state])\n" +
        "  verify client1 only sees graph events, client2 only sees flux events",
    });

    gaps.push({
      area: "WS",
      suggestion:
        "Add test: receive ERROR frame with retry_ms. Verify exponential backoff.",
      why_matters:
        "Ensures error handling is consistent. Frontend can rely on retry logic.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_ws_error_frame_retry():\n" +
        "  POST with invalid version → get ERROR { retry_ms: 1000 }\n" +
        "  verify frontend waits ~1s before retry\n" +
        "  verify exponential backoff on repeated errors",
    });

    // Concurrency and stress
    gaps.push({
      area: "Concurrency",
      suggestion:
        "Add test: two concurrent requests to POST /api/graph/layout. " +
        "Verify both complete correctly (no race condition).",
      why_matters:
        "Ensures thread safety of TriLayerDeterministicLayout. " +
        "Prevents corruption from parallel mutations.",
      severity: TestGapSeverity.High,
      test_skeleton:
        "test_concurrent_graph_layout_requests():\n" +
        "  run two POST /api/graph/layout in parallel\n" +
        "  assert both return valid, deterministic results",
    });

    gaps.push({
      area: "Concurrency",
      suggestion:
        "Add test: three clients with different run_ids. " +
        "Each makes 5 frame POSTs. Verify no cross-contamination.",
      why_matters:
        "Detects session state leakage. Ensures per-run-id isolation.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_three_parallel_sessions():\n" +
        "  session_a (run_id=a), session_b (run_id=b), session_c (run_id=c)\n" +
        "  each subscribes to different topics in interleaved order\n" +
        "  verify subscriptions remain isolated",
    });

    // Contract and compatibility
    gaps.push({
      area: "Contract",
      suggestion:
        "Add OpenAPI/JSON Schema spec for all route responses. " +
        "Validate frontend against spec on startup.",
      why_matters:
        "Prevents silent contract drift. Catches breaking changes early. " +
        "Enables auto-generation of TS types.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_openapi_schema_exists():\n" +
        "  GET /api/openapi.json\n" +
        "  assert all endpoints documented with request/response schemas",
    });

    // Security
    gaps.push({
      area: "Security",
      suggestion:
        "Add test: Plate71 SVG with node ID containing event handlers " +
        "(e.g., onclick='alert(1)'). Verify no script execution.",
      why_matters:
        "Prevents XSS in rendered SVG. Tests beyond basic HTML entity escaping. " +
        "Ensures all attributes are escaped.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_plate71_svg_xss_prevention_advanced():\n" +
        "  layout with node id=\"x\" onclick=\"alert(1)\"\n" +
        "  render SVG\n" +
        "  verify onclick is escaped, not executable",
    });

    gaps.push({
      area: "Security",
      suggestion:
        "Add test for SQL injection patterns in node IDs (if backend uses a DB).",
      why_matters:
        "Guards against injection attacks if backend stores graphs in a database.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_graph_layout_injection_prevention():\n" +
        "  node id=\"'; DROP TABLE nodes; --\"\n" +
        "  POST /api/graph/layout\n" +
        "  verify no DB mutation, safe error returned",
    });

    // Error recovery
    gaps.push({
      area: "Error Recovery",
      suggestion:
        "Add test: POST /api/cockpit/frame with invalid version (v='99.0'). " +
        "Verify error_frame returned with retry_ms.",
      why_matters:
        "Ensures error handling is consistent. Frontend can implement standard retry.",
      severity: TestGapSeverity.Medium,
      test_skeleton:
        "test_cockpit_frame_invalid_version():\n" +
        "  POST { v: '99.0', type: 'ping' }\n" +
        "  assert response.error { code: BAD_VERSION, retry_ms: 5000 }",
    });

    gaps.push({
      area: "Error Recovery",
      suggestion:
        "Add test: OperatorModePipeline timeout. If a stage takes > 30s, " +
        "return error frame to client.",
      why_matters:
        "Prevents indefinite hangs. Ensures frontend can timeout gracefully.",
      severity: TestGapSeverity.High,
      test_skeleton:
        "test_operator_pipeline_timeout():\n" +
        "  POST /api/operator/run with slow graph (forces timeout)\n" +
        "  assert response timeout error after ~30s",
    });
  }

  return gaps;
}
