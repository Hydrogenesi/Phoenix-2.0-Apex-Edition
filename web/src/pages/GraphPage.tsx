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
      <h2>Agent Graph Layout</h2>
      {error && <p style={{ color: "#f88" }}>Error: {error}</p>}
      {!layout && !error && <p>Loading layout…</p>}
      {layout && (
        <>
          <GraphCanvas layout={layout} />
          <details style={{ marginTop: 12 }}>
            <summary style={{ cursor: "pointer", color: "#888" }}>Raw layout JSON</summary>
            <pre style={{ fontSize: 11, overflow: "auto", maxHeight: 300 }}>
              {JSON.stringify(layout, null, 2)}
            </pre>
          </details>
        </>
      )}
    </div>
  );
}
