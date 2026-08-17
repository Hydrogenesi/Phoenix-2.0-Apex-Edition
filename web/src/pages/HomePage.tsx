import { Link } from "react-router-dom";

const CARDS = [
  {
    to:    "/cockpit",
    icon:  "🖥",
    label: "Full Cockpit",
    desc:  "Graph + Flux + Plate71",
  },
  {
    to:    "/graph",
    icon:  "🕸",
    label: "Graph Layout",
    desc:  "Agent topology",
  },
  {
    to:    "/flux",
    icon:  "⚡",
    label: "Quantum Flux",
    desc:  "Real-time shader",
  },
  {
    to:    "/plate71",
    icon:  "△",
    label: "Plate 71",
    desc:  "Symbolic layer SVG",
  },
] as const;

export function HomePage() {
  return (
    <div>
      <h1>🔥 PhoenixEngine Cockpit</h1>
      <p style={{ color: "var(--text-muted)", marginTop: "var(--sp-2)" }}>
        Select a view to begin.
      </p>
      <div className="home-grid">
        {CARDS.map((c) => (
          <Link key={c.to} to={c.to} className="home-card">
            <span className="home-card__icon">{c.icon}</span>
            <span className="home-card__label">{c.label}</span>
            <span className="home-card__desc">{c.desc}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
