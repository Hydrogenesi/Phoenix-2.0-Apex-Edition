from __future__ import annotations

from typing import Dict, Any, List
import math


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


class Plate71SVGBuilder:
    def __init__(self, viewbox: str = "-512 -512 1024 1024"):
        self.viewbox = viewbox

    def render(self, layout: Dict[str, Any], telemetry: Dict[str, Any] | None = None) -> str:
        telemetry = telemetry or {}
        nodes = layout.get("nodes", [])
        edges = layout.get("edges", [])

        node_map = {n["id"]: n for n in nodes}

        parts: List[str] = []
        parts.append(f'<svg viewBox="{self.viewbox}" xmlns="http://www.w3.org/2000/svg" data-spec="plate71@1.0.0">')
        parts.append('<defs>')
        parts.append('<radialGradient id="bgGrad" cx="50%" cy="50%" r="60%">')
        parts.append('<stop offset="0%" stop-color="#0a1020"/>')
        parts.append('<stop offset="100%" stop-color="#03050c"/>')
        parts.append('</radialGradient>')
        parts.append('</defs>')

        parts.append('<g id="plate71-background_field">')
        parts.append('<rect x="-512" y="-512" width="1024" height="1024" fill="url(#bgGrad)"/>')
        parts.append('</g>')

        parts.append('<g id="plate71-radial_grid" stroke="#23304d" stroke-opacity="0.35" fill="none">')
        for r in range(64, 64 + 52 * 7, 52):
            parts.append(f'<circle cx="0" cy="0" r="{r}" stroke-width="1"/>')
        for i in range(12):
            a = (2 * math.pi / 12) * i
            x = math.cos(a) * 420
            y = math.sin(a) * 420
            parts.append(f'<line x1="0" y1="0" x2="{x:.2f}" y2="{y:.2f}"/>')
        parts.append('</g>')

        parts.append('<g id="plate71-primary_rings" stroke="#5b7cff" stroke-opacity="0.45" fill="none">')
        for i in range(7):
            r = 64 + i * 52
            w = max(1.5, 4.0 - i * 0.35)
            parts.append(f'<circle cx="0" cy="0" r="{r}" stroke-width="{w:.2f}"/>')
        parts.append('</g>')

        parts.append('<g id="plate71-edge_arcs" fill="none">')
        for e in edges:
            s = node_map.get(e.get("from"))
            t = node_map.get(e.get("to"))
            if not s or not t:
                continue
            x1, y1 = self._to_view_coords(s["x"], s["y"])
            x2, y2 = self._to_view_coords(t["x"], t["y"])
            mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            dx, dy = x2 - x1, y2 - y1
            dist = max(1.0, math.sqrt(dx * dx + dy * dy))
            nx, ny = -dy / dist, dx / dist
            kappa = 0.14
            cx, cy = mx + nx * kappa * dist, my + ny * kappa * dist
            weight = float(e.get("weight", 1.0))
            sw = max(1.0, min(4.0, 1.0 + weight * 1.8))
            op = max(0.25, min(0.9, 0.25 + weight * 0.35))
            parts.append(
                f'<path data-edge-id="{_esc(str(e.get("id", "")))}" data-from="{_esc(str(e.get("from", "")))}" data-to="{_esc(str(e.get("to", "")))}" data-throughput="{weight:.3f}" '
                f'd="M {x1:.2f} {y1:.2f} Q {cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}" '
                f'stroke="#6dc7ff" stroke-opacity="{op:.3f}" stroke-width="{sw:.2f}"/>'
            )
        parts.append('</g>')

        parts.append('<g id="plate71-agent_nodes">')
        for n in nodes:
            x, y = self._to_view_coords(n["x"], n["y"])
            health = self._health_for_node(n["id"], telemetry)
            queue_depth = self._queue_for_node(n["id"], telemetry)
            color, dash, glow = self._health_style(health)
            parts.append(
                f'<g data-node-id="{_esc(n["id"])}" data-agent-kind="{_esc(n.get("kind", "agent"))}" '
                f'data-health="{_esc(health)}" data-queue-depth="{queue_depth}">'
            )
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="19" fill="#0f1a33" stroke="{color}" stroke-width="2.4" stroke-dasharray="{dash}"/>')
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="24" fill="none" stroke="{color}" stroke-opacity="0.25" stroke-width="{glow}"/>')
            parts.append('</g>')
        parts.append('</g>')

        parts.append('<g id="plate71-glyph_overlays" fill="none" stroke="#d2b6ff" stroke-opacity="0.65">')
        for n in nodes:
            x, y = self._to_view_coords(n["x"], n["y"])
            r = 30
            parts.append(self._triad_glyph(x, y, r))
        parts.append('</g>')

        parts.append('<g id="plate71-labels" fill="#e7ecff" font-family="Inter,Segoe UI,sans-serif" font-size="12">')
        for n in nodes:
            x, y = self._to_view_coords(n["x"], n["y"])
            parts.append(f'<text x="{x + 10:.2f}" y="{y - 10:.2f}">{_esc(n["id"])}</text>')
        parts.append('</g>')

        parts.append('<g id="plate71-fx_highlights" fill="none" stroke="#ffe082" stroke-opacity="0.35">')
        active = telemetry.get("active_rings", [1, 3, 5])
        for i in active:
            r = 64 + int(i) * 52
            parts.append(f'<circle cx="0" cy="0" r="{r}" stroke-width="2"/>')
        parts.append('</g>')

        parts.append('</svg>')
        return "\n".join(parts)

    @staticmethod
    def _to_view_coords(u: float, v: float) -> tuple[float, float]:
        x = (float(u) - 0.5) * 860.0
        y = (float(v) - 0.5) * 860.0
        return x, y

    @staticmethod
    def _triad_glyph(x: float, y: float, r: float) -> str:
        pts = []
        for i in range(3):
            a = (2 * math.pi / 3) * i - math.pi / 2
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        return (
            f'<path d="M {pts[0][0]:.2f} {pts[0][1]:.2f} '
            f'L {pts[1][0]:.2f} {pts[1][1]:.2f} '
            f'L {pts[2][0]:.2f} {pts[2][1]:.2f} Z"/>'
        )

    @staticmethod
    def _health_for_node(node_id: str, telemetry: Dict[str, Any]) -> str:
        by_node = telemetry.get("health", {})
        return str(by_node.get(node_id, "healthy"))

    @staticmethod
    def _queue_for_node(node_id: str, telemetry: Dict[str, Any]) -> int:
        q = telemetry.get("queue_depth", {})
        return int(q.get(node_id, 0))

    @staticmethod
    def _health_style(health: str) -> tuple[str, str, float]:
        if health == "critical":
            return ("#ff5a5a", "2 2", 3.2)
        if health == "degraded":
            return ("#ffb74d", "5 3", 2.8)
        return ("#73f0a8", "", 2.2)
