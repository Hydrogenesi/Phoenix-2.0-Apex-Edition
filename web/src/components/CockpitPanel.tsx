import { useEffect, useRef, useState } from "react";
import type { FluxStatePayload } from "../ws/protocol";
import { GraphCanvas } from "./GraphCanvas";
import { FluxView } from "./FluxView";
import { Plate71View } from "./Plate71View";
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
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    const ctrl = new AbortController();
    abortRef.current = ctrl;

    async function bootstrap() {
      try {
        const hsRes = await fetch(
          `/api/cockpit/handshake?run_id=${encodeURIComponent(runId)}`,
          { signal: ctrl.signal }
        );
        if (!hsRes.ok) throw new Error(`handshake failed: ${hsRes.status}`);
        const frame = (await hsRes.json()) as { type: string; payload: { session_id: string } };
        if (frame.type === "ready") {
          setSessionId(frame.payload.session_id);
        }

        const [layoutRes, fluxRes] = await Promise.all([
          fetch(`/api/graph/layout?run_id=${encodeURIComponent(runId)}`, { signal: ctrl.signal }),
          fetch(`/api/flux/state?run_id=${encodeURIComponent(runId)}`, { signal: ctrl.signal }),
        ]);
        if (layoutRes.ok) setLayout((await layoutRes.json()) as GraphLayout);
        if (fluxRes.ok)   setFluxState((await fluxRes.json()) as FluxStatePayload);
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
    <div className="cockpit">
      {/* ── Header ────────────────────────────────────────────── */}
      <div className="cockpit__header">
        <h2 className="cockpit__title">🔥 PhoenixEngine Cockpit</h2>
        <div className="cockpit__meta">
          <span>run: <code>{runId}</code></span>
          {sessionId && <span>session: <code>{sessionId}</code></span>}
          {sessionError && (
            <span className="badge badge--error">⚠ {sessionError}</span>
          )}
        </div>
      </div>

      {/* ── Agent Graph ───────────────────────────────────────── */}
      <div className="panel">
        <div className="panel__header">
          <h3 className="panel__title">🕸 Agent Graph</h3>
          <span className="panel__subtitle">tri-layer deterministic layout</span>
        </div>
        <GraphCanvas layout={layout} />
      </div>

      {/* ── Quantum Flux ──────────────────────────────────────── */}
      <div className="panel">
        <div className="panel__header">
          <h3 className="panel__title">⚡ Quantum Flux</h3>
          <span className="panel__subtitle">WebGL2 shader · real-time</span>
        </div>
        <FluxView fluxState={fluxState} />
      </div>

      {/* ── Plate71 ───────────────────────────────────────────── */}
      <div className="panel">
        <div className="panel__header">
          <h3 className="panel__title">△ Plate 71</h3>
          <span className="panel__subtitle">symbolic layer · plate71@1.0.0</span>
        </div>
        <Plate71View layout={layout as Record<string, unknown> | null} />
      </div>

    </div>
  );
}
