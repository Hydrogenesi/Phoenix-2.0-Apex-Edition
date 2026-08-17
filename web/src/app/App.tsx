import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router-dom";

/**
 * Root application shell.
 * Mounts a minimal nav bar and renders the active route via <Outlet />.
 */
export default function App() {
  const [health, setHealth] = useState<"ok" | "error" | "pending">("pending");

  useEffect(() => {
    fetch("/health")
      .then((r) => (r.ok ? setHealth("ok") : setHealth("error")))
      .catch(() => setHealth("error"));
  }, []);

  return (
    <div style={{ fontFamily: "Inter, Segoe UI, sans-serif", background: "#07091a", color: "#e8eeff", minHeight: "100vh" }}>
      <nav style={{ display: "flex", gap: 20, padding: "12px 20px", borderBottom: "1px solid #1a2040" }}>
        <strong style={{ color: "#5b7cff" }}>PhoenixEngine</strong>
        <Link to="/" style={{ color: "#aabbff", textDecoration: "none" }}>Home</Link>
        <Link to="/cockpit" style={{ color: "#aabbff", textDecoration: "none" }}>Cockpit</Link>
        <Link to="/graph" style={{ color: "#aabbff", textDecoration: "none" }}>Graph</Link>
        <Link to="/flux" style={{ color: "#aabbff", textDecoration: "none" }}>Flux</Link>
        <span style={{ marginLeft: "auto", color: health === "ok" ? "#73f0a8" : health === "error" ? "#ff5a5a" : "#888", fontSize: 12 }}>
          {health === "ok" ? "● backend online" : health === "error" ? "● backend offline" : "● …"}
        </span>
      </nav>
      <main style={{ padding: 20 }}>
        <Outlet />
      </main>
    </div>
  );
}
