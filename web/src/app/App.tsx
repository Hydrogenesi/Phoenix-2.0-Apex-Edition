import { useEffect, useState } from "react";
import { Link, NavLink, Outlet } from "react-router-dom";

/**
 * Root application shell.
 * Mounts a sticky nav bar and renders the active route via <Outlet />.
 */
export default function App() {
  const [health, setHealth] = useState<"ok" | "error" | "pending">("pending");

  useEffect(() => {
    fetch("/health")
      .then((r) => (r.ok ? setHealth("ok") : setHealth("error")))
      .catch(() => setHealth("error"));
  }, []);

  return (
    <div className="app-shell">
      <nav className="app-nav">
        <Link to="/" className="app-nav__brand">PhoenixEngine</Link>
        {(
          [
            ["/cockpit", "Cockpit"],
            ["/graph",   "Graph"],
            ["/flux",    "Flux"],
            ["/plate71", "Plate71"],
          ] as [string, string][]
        ).map(([path, label]) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              "app-nav__link" + (isActive ? " app-nav__link--active" : "")
            }
          >
            {label}
          </NavLink>
        ))}

        <div className="app-nav__status">
          <span
            className={`app-nav__status-dot app-nav__status-dot--${health}`}
            aria-hidden="true"
          />
          <span>
            {health === "ok" ? "backend online" : health === "error" ? "backend offline" : "connecting…"}
          </span>
        </div>
      </nav>

      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
