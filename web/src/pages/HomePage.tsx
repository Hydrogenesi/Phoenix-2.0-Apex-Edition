import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <div>
      <h1>🔥 PhoenixEngine Cockpit</h1>
      <p>Select a view to begin:</p>
      <ul style={{ listStyle: "none", padding: 0, display: "flex", gap: 16 }}>
        <li>
          <Link to="/cockpit" style={{ display: "block", padding: "12px 20px", background: "#111a32", borderRadius: 8, color: "#aabbff", textDecoration: "none" }}>
            🖥 Full Cockpit<br /><small>Graph + Flux + WS</small>
          </Link>
        </li>
        <li>
          <Link to="/graph" style={{ display: "block", padding: "12px 20px", background: "#111a32", borderRadius: 8, color: "#aabbff", textDecoration: "none" }}>
            🕸 Graph Layout<br /><small>Agent topology</small>
          </Link>
        </li>
        <li>
          <Link to="/flux" style={{ display: "block", padding: "12px 20px", background: "#111a32", borderRadius: 8, color: "#aabbff", textDecoration: "none" }}>
            ⚡ Quantum Flux<br /><small>Real-time shader</small>
          </Link>
        </li>
      </ul>
    </div>
  );
}
