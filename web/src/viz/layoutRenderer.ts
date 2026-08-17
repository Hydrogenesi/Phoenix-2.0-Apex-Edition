export type GraphNode = {
  id: string;
  kind?: string;
  x: number; // normalized 0..1
  y: number; // normalized 0..1
  layer?: number;
};

export type GraphEdge = {
  id: string;
  from: string;
  to: string;
  weight?: number;
};

export type GraphLayout = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export class LayoutRenderer {
  private ctx: CanvasRenderingContext2D;

  constructor(private canvas: HTMLCanvasElement) {
    const ctx = canvas.getContext("2d");
    if (!ctx) throw new Error("2D context unavailable");
    this.ctx = ctx;
  }

  render(layout: GraphLayout): void {
    const { width, height } = this.canvas;
    const ctx = this.ctx;

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#0a0f1f";
    ctx.fillRect(0, 0, width, height);

    const nodeMap = new Map(layout.nodes.map((n) => [n.id, n]));

    ctx.save();
    for (const e of layout.edges) {
      const s = nodeMap.get(e.from);
      const t = nodeMap.get(e.to);
      if (!s || !t) continue;

      const [x1, y1] = this.toPx(s.x, s.y, width, height);
      const [x2, y2] = this.toPx(t.x, t.y, width, height);
      const mx = (x1 + x2) / 2;
      const my = (y1 + y2) / 2;
      const dx = x2 - x1;
      const dy = y2 - y1;
      const d = Math.max(1, Math.hypot(dx, dy));
      const nx = -dy / d;
      const ny = dx / d;
      const k = 0.14;
      const cx = mx + nx * k * d;
      const cy = my + ny * k * d;

      const w = Math.max(1, Math.min(4, 1 + (e.weight ?? 1) * 1.6));
      ctx.strokeStyle = "rgba(109,199,255,0.65)";
      ctx.lineWidth = w;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.quadraticCurveTo(cx, cy, x2, y2);
      ctx.stroke();
    }
    ctx.restore();

    for (const n of layout.nodes) {
      const [x, y] = this.toPx(n.x, n.y, width, height);
      ctx.fillStyle = "#111a32";
      ctx.strokeStyle = "#73f0a8";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 14, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#e8eeff";
      ctx.font = "12px Inter, Segoe UI, sans-serif";
      ctx.fillText(n.id, x + 10, y - 10);
    }
  }

  private toPx(x: number, y: number, w: number, h: number): [number, number] {
    return [x * w, y * h];
  }
}
