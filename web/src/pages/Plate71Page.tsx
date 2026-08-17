import { Plate71View } from "../components/Plate71View";

/**
 * Standalone Plate71 symbolic-layer page.
 * Fetches the SVG from /api/plate71/svg and renders it full-width.
 */
export function Plate71Page() {
  return (
    <div>
      <div style={{ marginBottom: "var(--sp-6)" }}>
        <h2>△ Plate 71</h2>
        <p style={{ color: "var(--text-muted)", fontSize: "var(--fs-sm)", marginTop: "var(--sp-2)" }}>
          Symbolic layer — agent topology rendered as a Plate71 glyph diagram.
          <span className="badge badge--muted" style={{ marginLeft: "var(--sp-3)" }}>plate71@1.0.0</span>
        </p>
      </div>
      <Plate71View />
    </div>
  );
}
