import { useEffect, useState } from "react";
import { GraphCanvas } from "../components/GraphCanvas";
import type { GraphLayout } from "../viz/layoutRenderer";

export function GraphPage() {
  const [layout, setLayout] = useState<GraphLayout | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/graph/layout")
      .then((r) => r.json())
      .then((data: GraphLayout) => setLayout(data))
      .catch((e: unknown) => setError(String(e)));
  }, []);

  return (
    <div>
      <div style={{ marginBottom: "var(--sp-6)" }}>
        <h2>🕸 Agent Graph Layout</h2>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--fs-sm)", marginTop: "var(--sp-2)" }}>
          Tri-layer deterministic layout of the agent graph.
        </p>
      </div>

      {error && <p className="state-error">Error: {error}</p>}
      {!layout && !error && <p className="state-loading">Loading layout…</p>}

      {layout && (
        <>
          <GraphCanvas layout={layout} />
          <details style={{ marginTop: "var(--sp-4)" }}>
            <summary style={{ cursor: "pointer", color: "var(--text-muted)", fontSize: "var(--fs-sm)" }}>
              Raw layout JSON
            </summary>
            <pre style={{ marginTop: "var(--sp-2)" }}>
              {JSON.stringify(layout, null, 2)}
            </pre>
          </details>
        </>
      )}
    </div>
  );
}
