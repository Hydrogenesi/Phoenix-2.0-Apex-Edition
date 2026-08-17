/**
 * Type definitions for phoenix.cockpit.v1 WebSocket frames.
 * These mirror the backend protocol defined in
 * phoenixengine/modules/cockpit_ws/protocol.py.
 */

export const PROTOCOL_VERSION = "1.0.0";
export const SUBPROTOCOL = "phoenix.cockpit.v1";

export interface Envelope<T = Record<string, unknown>> {
  v: string;
  type: string;
  ts: string;
  seq: number;
  run_id: string;
  payload: T;
}

// ── Server → Client frames ──────────────────────────────────────────────────

export interface ReadyPayload {
  session_id: string;
  heartbeat_ms: number;
  protocol: string;
}

export interface GraphSnapshotPayload {
  nodes: Array<{ id: string; x: number; y: number; r: number; kind: string }>;
  edges: Array<{ id: string; from: string; to: string; weight: number }>;
  bbox: { x: number; y: number; w: number; h: number };
  rev: number;
}

export interface GraphDiffPayload {
  from_rev: number;
  to_rev: number;
  ops: Array<Record<string, unknown>>;
}

export interface AgentHealthPayload {
  agent_id: string;
  status: "healthy" | "degraded" | "critical";
  cpu: number;
  mem_mb: number;
  queue_depth: number;
  latency_ms_p95: number;
}

export interface FluxStatePayload {
  throughput: number;
  phase: number;
  coherence: number;
  noise_floor: number;
}

export interface Plate71StatePayload {
  glyph_mode: string;
  intensity: number;
  active_rings: number[];
}

export interface ErrorPayload {
  code: string;
  message: string;
  retry_ms?: number;
}

// ── Client → Server frames ──────────────────────────────────────────────────

export function helloFrame(clientId: string): Record<string, unknown> {
  return {
    v: PROTOCOL_VERSION,
    type: "hello",
    payload: {
      client_id: clientId,
      capabilities: ["graph.diff", "telemetry.stream", "plate71.layer", "flux.layer"],
    },
  };
}

export function subscribeFrame(topics: string[]): Record<string, unknown> {
  return { v: PROTOCOL_VERSION, type: "subscribe", payload: { topics } };
}

export function ackFrame(seq: number): Record<string, unknown> {
  return { v: PROTOCOL_VERSION, type: "ack", payload: { seq } };
}

export function pongFrame(): Record<string, unknown> {
  return { v: PROTOCOL_VERSION, type: "pong", payload: {} };
}
