import { useEffect, useState } from "react";
import { FluxView } from "../components/FluxView";
import type { FluxStatePayload } from "../ws/protocol";

export function FluxPage() {
  const [fluxState, setFluxState] = useState<Partial<FluxStatePayload>>({
    throughput: 0.6,
    phase: 1.2,
    coherence: 0.85,
    noise_floor: 0.12,
  });

  // Poll the flux state endpoint every 2 seconds.
  useEffect(() => {
    const tick = () =>
      fetch("/api/flux/state")
        .then((r) => r.json())
        .then((d: FluxStatePayload) => setFluxState(d))
        .catch(() => undefined);

    tick();
    const id = setInterval(tick, 2000);
    return () => clearInterval(id);
  }, []);

  return (
    <div>
      <div style={{ marginBottom: "var(--sp-6)" }}>
        <h2>⚡ Quantum Flux</h2>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--fs-sm)", marginTop: "var(--sp-2)" }}>
          Real-time WebGL2 flux renderer — polling every 2 s.
        </p>
      </div>
      <FluxView fluxState={fluxState} />
    </div>
  );
}
