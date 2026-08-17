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
      <h2>⚡ Quantum Flux</h2>
      <FluxView fluxState={fluxState} />
      <pre style={{ fontSize: 11, marginTop: 12 }}>{JSON.stringify(fluxState, null, 2)}</pre>
    </div>
  );
}
