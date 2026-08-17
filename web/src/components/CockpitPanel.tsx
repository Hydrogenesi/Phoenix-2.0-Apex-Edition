import { useEffect, useRef, useState } from "react";
import type { FluxStatePayload, AgentHealthPayload } from "../ws/protocol";
import { GraphCanvas } from "./GraphCanvas";
import { FluxView } from "./FluxView";
import type { GraphLayout } from "../viz/layoutRenderer";

interface CockpitPanelProps {
  runId?: string;
  initialLayout?: GraphLayout | null;
}

/**
 * Full cockpit panel: bootstraps a session via the HTTP handshake endpoint
 * (`/api/cockpit/handshake`) and polls `/api/cockpit/frame` for updates.
 * Using HTTP transport because the backend exposes only HTTP endpoints under
 * `/api/*` — there is no `/ws/cockpit` WebSocket handler.
 */
export function CockpitPanel({ runId = "dev", initialLayout = null }: CockpitPanelProps) {
  const [layout, setLayout] = useState<GraphLayout | null>(initialLayout);
  const [fluxState, setFluxState] = useState<Partial<FluxStatePayload>>({
    throughput: 0.4,
    phase: 0.0,
    coherence: 0.8,
    noise_floor: 0.12,
  });
  const [health, setHealth] = useState<Record<string, AgentHealthPayload>>({});
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const ctrl = new AbortController();
    abortRef.current = ctrl;

    async function bootstrap() {
      try {
        // Establish session via HTTP handshake (no WebSocket backend available).
        const hsRes = await fetch(
          `/api/cockpit/handshake?run_id=${encodeURIComponent(runId)}`,
          { signal: ctrl.signal }
        );
        if (!hsRes.ok) throw new Error(`handshake failed: ${hsRes.status}`);
        const frame = (await hsRes.json()) as { type: string; payload: { session_id: string } };
        if (frame.type === "ready") {
          setSessionId(frame.payload.session_id);
        }

        // Fetch initial layout and flux state over HTTP.
        const [layoutRes, fluxRes] = await Promise.all([
          fetch(`/api/graph/layout?run_id=${encodeURIComponent(runId)}`, { signal: ctrl.signal }),
          fetch(`/api/flux/state?run_id=${encodeURIComponent(runId)}`, { signal: ctrl.signal }),
        ]);
        if (layoutRes.ok) {
          const layoutData = (await layoutRes.json()) as GraphLayout;
          setLayout(layoutData);
        }
        if (fluxRes.ok) {
          const fluxData = (await fluxRes.json()) as FluxStatePayload;
          setFluxState(fluxData);
        }
      } catch (err) {
        if ((err as { name?: string }).name !== "AbortError") {
          setSessionError(err instanceof Error ? err.message : String(err));
        }
      }
    }

    bootstrap();
    return () => {
      ctrl.abort();
      abortRef.current = null;
    };
  }, [runId]);

  return (
    <div style={{ padding: 16 }}>
      <header style={{ marginBottom: 12 }}>
        <h2 style={{ margin: 0 }}>PhoenixEngine Cockpit</h2>
        <small style={{ color: "#888" }}>
          run_id: <code>{runId}</code>
          {sessionId && (
            <>
              {" · "}session: <code>{sessionId}</code>
            </>
          )}
          {sessionError && (
            <span style={{ color: "#f88", marginLeft: 8 }}>⚠ {sessionError}</span>
          )}
        </small>
      </header>

      <section>
        <h3>Agent Graph</h3>
        <GraphCanvas layout={layout} />
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>Quantum Flux</h3>
        <FluxView fluxState={fluxState} />
      </section>

      {Object.keys(health).length > 0 && (
        <section style={{ marginTop: 24 }}>
          <h3>Agent Health</h3>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr>
                {["Agent", "Status", "CPU", "Mem MB", "Queue", "Latency p95"].map((h) => (
                  <th key={h} style={{ textAlign: "left", padding: "4px 8px", borderBottom: "1px solid #333" }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.values(health).map((a) => (
                <tr key={a.agent_id}>
                  <td style={{ padding: "4px 8px" }}>{a.agent_id}</td>
                  <td style={{ padding: "4px 8px", color: a.status === "healthy" ? "#73f0a8" : a.status === "degraded" ? "#ffb74d" : "#ff5a5a" }}>
                    {a.status}
                  </td>
                  <td style={{ padding: "4px 8px" }}>{(a.cpu * 100).toFixed(1)}%</td>
                  <td style={{ padding: "4px 8px" }}>{a.mem_mb}</td>
                  <td style={{ padding: "4px 8px" }}>{a.queue_depth}</td>
                  <td style={{ padding: "4px 8px" }}>{a.latency_ms_p95} ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}
