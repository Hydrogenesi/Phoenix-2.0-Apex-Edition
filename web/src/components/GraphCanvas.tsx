import { useEffect, useRef } from "react";
import { LayoutRenderer, GraphLayout } from "../viz/layoutRenderer";

interface GraphCanvasProps {
  layout: GraphLayout | null;
  width?: number;
  height?: number;
}

/**
 * Renders a PhoenixEngine graph layout on a 2-D canvas using
 * the LayoutRenderer from web/src/viz/layoutRenderer.ts.
 */
export function GraphCanvas({ layout, width = 800, height = 500 }: GraphCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<LayoutRenderer | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    if (!rendererRef.current) {
      rendererRef.current = new LayoutRenderer(canvas);
    }
    if (layout) {
      rendererRef.current.render(layout);
    }
  }, [layout]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ width: "100%", height: "auto", borderRadius: 8 }}
      aria-label="Agent graph layout"
    />
  );
}
