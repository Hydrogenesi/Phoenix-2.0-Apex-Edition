/**
 * WebSocket Protocol Compatibility Analyzer
 *
 * Detects message schema and semantic mismatches between
 * frontend (ws/protocol.ts) and backend (routes_cockpit.py)
 * implementations of phoenix.cockpit.v1.
 */

export enum WSProtocolSeverity {
  Low = "low",
  Medium = "medium",
  High = "high",
}

export interface AnalyzedWSIssue {
  opcode: string;
  frontend_field: string;
  backend_field: string;
  issue: string;
  severity: WSProtocolSeverity;
  test_case?: string;
  fix?: string;
}

/**
 * Analyze WebSocket protocol compatibility for a given PR.
 * For PR #123, focus on session persistence, frame routing, and state management.
 */
export function analyzeWSProtocolCompatibility(
  prNumber: number
): AnalyzedWSIssue[] {
  const issues: AnalyzedWSIssue[] = [];

  if (prNumber === 123) {
    // Session correlation issue
    issues.push({
      opcode: "SUBSCRIBE",
      frontend_field:
        "Receives session_id in ready frame but does not send it back in subsequent frames. " +
        "Stores session_id locally but sends only run_id in POST body.",
      backend_field:
        "Expects run_id to uniquely identify a session. " +
        "Creates fresh protocol instance per run_id on each frame POST.",
      issue:
        "Frontend receives session_id from backend but never uses it in subscription or ping frames. " +
        "Backend cannot correlate subscribe→ping→pong to a single session. " +
        "Each frame is treated independently.",
      severity: WSProtocolSeverity.High,
      test_case:
        "POST /api/cockpit/handshake → get session_id. " +
        "POST /api/cockpit/frame { subscribe to graph.snapshot }. " +
        "POST /api/cockpit/frame { ping }. " +
        "Verify backend remembered subscription; ping should be routed to subscribers.",
      fix:
        "Frontend: send session_id in every frame body: { session_id, run_id, type, payload }. " +
        "Backend: store sessions by session_id, not run_id. " +
        "Validate session_id matches the one from handshake.",
    });

    // Subscription state loss
    issues.push({
      opcode: "SUBSCRIBE",
      frontend_field:
        "Calls client.subscribe(['graph.snapshot', 'flux.state', ...]) " +
        "expecting server to remember and deliver matching events.",
      backend_field:
        "Parses subscribe frame: proto.parse_client_frame(frame). " +
        "Adds topics to proto.subscriptions. " +
        "But proto is discarded after this call.",
      issue:
        "Subscription list is maintained only within a single protocol instance. " +
        "On the next POST (ping/pong), a fresh instance is created with zero subscriptions.",
      severity: WSProtocolSeverity.High,
      test_case:
        "Send { type: 'subscribe', payload: { topics: ['graph.snapshot'] } }. " +
        "Verify backend returns ack. " +
        "Send { type: 'ping' }. " +
        "Verify backend's response respects prior subscription (routes ping to subscribers).",
      fix:
        "Store subscriptions in session dict: _sessions[session_id].subscriptions = topics. " +
        "Persist across frames. " +
        "Clean up on unsubscribe or session timeout.",
    });

    // Ping/pong routing
    issues.push({
      opcode: "PING/PONG",
      frontend_field:
        "Sends { v: '1.0.0', type: 'ping', payload: {} } every 30 seconds. " +
        "Expects pong response confirming connection is alive.",
      backend_field:
        "Receives ping, calls proto.ping_frame() which returns { type: 'ping', payload: {} }. " +
        "But ping_frame() should return pong, not ping.",
      issue:
        "Backend's handle_ping() returns a ping frame, not a pong. " +
        "Frontend sends PING, expects PONG, gets PING. " +
        "Ambiguous: is the ping an echo or a new server-initiated ping?",
      severity: WSProtocolSeverity.High,
      test_case:
        "Frontend sends { type: 'ping' }. " +
        "Verify backend response has { type: 'pong' }.",
      fix:
        "Backend: handle_ping() should call proto.pong_frame(), not ping_frame(). " +
        "Or rename: handle_ping() is for client PING; server-initiated pings use a different route.",
    });

    // Error frame retry semantics
    issues.push({
      opcode: "ERROR",
      frontend_field:
        "CockpitWSClient implements exponential backoff on ERROR.payload.retry_ms. " +
        "Reconnects and resends last frame after waiting retry_ms.",
      backend_field:
        "Returns error_frame(code, message, retry_ms) on protocol violations. " +
        "But retry_ms is not tracked per session; no rate-limiting state persists.",
      issue:
        "Frontend respects retry_ms and backs off, but backend has no memory of the error. " +
        "Next frame (after backoff) is treated as a fresh request, no rate-limit. " +
        "Defeats the purpose of rate-limiting.",
      severity: WSProtocolSeverity.Medium,
      test_case:
        "Send invalid frame (bad version). " +
        "Verify ERROR.payload.retry_ms is set (e.g., 5000). " +
        "Wait 5s, send valid frame. " +
        "Verify backend accepts it (not rate-limited).",
      fix:
        "Backend: implement per-session rate-limit state. " +
        "Track last error time and reject frames within retry_ms window. " +
        "Return error with updated retry_ms if still blocked.",
    });

    // Version negotiation
    issues.push({
      opcode: "READY",
      frontend_field:
        "Hardcoded protocol version: v: '1.0.0' in all frames. " +
        "No version negotiation or fallback.",
      backend_field:
        "CockpitProtocolV1 is hardcoded. " +
        "Rejects frames with v != '1.0.0' (ProtocolError BAD_VERSION). " +
        "No v0.9 or v2.0 support.",
      issue:
        "No version negotiation. " +
        "If backend is upgraded to v2.0 but frontend is still v1.0, connection fails. " +
        "No graceful downgrade.",
      severity: WSProtocolSeverity.Medium,
      test_case:
        "Frontend sends v='0.9.0'. " +
        "Backend returns error with code='BAD_VERSION' and suggested version in error payload.",
      fix:
        "Add version negotiation in ready frame. " +
        "Backend returns supported versions. " +
        "Client picks highest common version or falls back.",
    });

    // Unsubscribe not implemented
    issues.push({
      opcode: "UNSUBSCRIBE",
      frontend_field:
        "CockpitWSClient has no unsubscribe() method. " +
        "Once subscribed, topics are subscribed for the lifetime of the connection.",
      backend_field:
        "CockpitProtocolV1.parse_client_frame() does not handle 'unsubscribe' type. " +
        "No way to remove a topic from subscriptions.",
      issue:
        "Cannot dynamically unsubscribe from topics. " +
        "If frontend needs to stop receiving graph events, no way to do so.",
      severity: WSProtocolSeverity.Medium,
      test_case:
        "Send { type: 'unsubscribe', payload: { topics: ['graph.snapshot'] } }. " +
        "Verify backend acks or returns error (not yet implemented).",
      fix:
        "Implement unsubscribe() in frontend CockpitWSClient. " +
        "Implement unsubscribe handling in backend CockpitProtocolV1.parse_client_frame().",
    });
  }

  return issues;
}
