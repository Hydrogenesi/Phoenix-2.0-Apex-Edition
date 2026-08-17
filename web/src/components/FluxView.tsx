import { useEffect, useRef } from "react";
import { FluxRenderer } from "../viz/fluxRenderer";
import type { FluxStatePayload } from "../ws/protocol";

// Inline the fragment shader source. In production this would be
// imported via ?raw in Vite: `import fragSrc from '../../../phoenixengine/modules/quantum_flux/shader/flux.frag.glsl?raw'`
// For the scaffold we embed a minimal passthrough so the component mounts
// without Vite's asset pipeline being required at dev time.
const FALLBACK_FRAG = `#version 300 es
precision highp float;
out vec4 outColor;
uniform float u_time;
uniform vec2  u_resolution;
uniform float u_throughput;
uniform float u_phase;
uniform float u_coherence;
uniform float u_noiseFloor;
uniform float u_alert;
uniform vec3  u_paletteA;
uniform vec3  u_paletteB;
uniform vec3  u_paletteC;
void main() {
  vec2 uv = gl_FragCoord.xy / u_resolution;
  float t = u_throughput;
  vec3 col = mix(u_paletteA, u_paletteB, uv.x * t + sin(u_time + u_phase) * 0.3);
  col = mix(col, u_paletteC, u_alert * 0.6);
  outColor = vec4(col, 1.0);
}`;

interface FluxViewProps {
  fluxState?: Partial<FluxStatePayload>;
  fragmentSource?: string;
  width?: number;
  height?: number;
}

/**
 * Renders the Quantum Flux animation using WebGL2 + FluxRenderer.
 * Accepts live flux state updates from the cockpit WebSocket.
 */
export function FluxView({
  fluxState,
  fragmentSource = FALLBACK_FRAG,
  width = 800,
  height = 220,
}: FluxViewProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<FluxRenderer | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    let renderer: FluxRenderer | null = null;
    try {
      renderer = new FluxRenderer(canvas, fragmentSource);
      rendererRef.current = renderer;
      renderer.startLoop();
    } catch (e) {
      console.warn("FluxRenderer init failed (WebGL2 may be unavailable):", e);
    }
    return () => {
      renderer?.stopLoop();
      rendererRef.current = null;
    };
  }, [fragmentSource]);

  useEffect(() => {
    if (!rendererRef.current || !fluxState) return;
    rendererRef.current.setState({
      throughput: fluxState.throughput,
      phase: fluxState.phase,
      coherence: fluxState.coherence,
      noiseFloor: fluxState.noise_floor,
    });
  }, [fluxState]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ width: "100%", height: "auto", borderRadius: 8 }}
      aria-label="Quantum flux animation"
    />
  );
}
