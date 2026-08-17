import { useEffect, useState } from "react";
import { CockpitWSClient } from "../ws/client";
import type { WSMessage } from "../ws/client";
import type { FluxStatePayload, AgentHealthPayload } from "../ws/protocol";
import { GraphCanvas } from "./GraphCanvas";
import { FluxView } from "./FluxView";
import type { GraphLayout } from "../viz/layoutRenderer";

interface CockpitPanelProps {
  runId?: string;
  initialLayout?: GraphLayout | null;
}

/**
 * Full cockpit panel: bootstraps the WebSocket session, subscribes to all
 * relevant topics, and renders the graph + flux views with live data.
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
  const [wsError, setWsError] = useState<string | null>(null);

  useEffect(() => {
    const client = new CockpitWSClient(runId);
    const unsub = client.onMessage((msg: WSMessage) => {
      const type = msg.type as string;
      if (type === "ready") {
        const payload = msg.payload as { session_id: string };
        setSessionId(payload.session_id);
        client.subscribe([
          "graph.snapshot",
          "graph.diff",
          "agent.health",
          "flux.state",
          "plate71.state",
        ]);
      } else if (type === "graph.snapshot") {
        const p = msg.payload as GraphLayout;
        setLayout(p);
      } else if (type === "flux.state") {
        setFluxState(msg.payload as FluxStatePayload);
      } else if (type === "agent.health") {
        const p = msg.payload as AgentHealthPayload;
        setHealth((prev) => ({ ...prev, [p.agent_id]: p }));
      } else if (type === "error") {
        const p = msg.payload as { message: string };
        setWsError(p.message);
      }
    });

    client.connect();
    return () => {
      unsub();
      client.disconnect();
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
          {wsError && (
            <span style={{ color: "#f88", marginLeft: 8 }}>⚠ {wsError}</span>
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
