type FluxUniforms = {
  throughput: number;
  phase: number;
  coherence: number;
  noiseFloor: number;
  alert: number;
};

export class FluxRenderer {
  private gl: WebGL2RenderingContext;
  private program: WebGLProgram;
  private vao: WebGLVertexArrayObject;
  private start = performance.now();

  private uTime!: WebGLUniformLocation;
  private uResolution!: WebGLUniformLocation;
  private uThroughput!: WebGLUniformLocation;
  private uPhase!: WebGLUniformLocation;
  private uCoherence!: WebGLUniformLocation;
  private uNoiseFloor!: WebGLUniformLocation;
  private uAlert!: WebGLUniformLocation;
  private uPaletteA!: WebGLUniformLocation;
  private uPaletteB!: WebGLUniformLocation;
  private uPaletteC!: WebGLUniformLocation;

  private state: FluxUniforms = {
    throughput: 0.4,
    phase: 0.0,
    coherence: 0.8,
    noiseFloor: 0.12,
    alert: 0.0,
  };

  constructor(private canvas: HTMLCanvasElement, fragmentSource: string) {
    const gl = canvas.getContext("webgl2");
    if (!gl) throw new Error("WebGL2 unavailable");
    this.gl = gl;

    const vert = `#version 300 es
      precision highp float;
      out vec2 v_uv;
      const vec2 POS[3] = vec2[3](
        vec2(-1.0, -1.0),
        vec2( 3.0, -1.0),
        vec2(-1.0,  3.0)
      );
      void main() {
        vec2 p = POS[gl_VertexID];
        v_uv = p * 0.5 + 0.5;
        gl_Position = vec4(p, 0.0, 1.0);
      }
    `;

    this.program = this.createProgram(vert, fragmentSource);
    this.vao = gl.createVertexArray()!;

    this.cacheUniforms();
  }

  setState(partial: Partial<FluxUniforms>): void {
    this.state = { ...this.state, ...partial };
  }

  frame = (): void => {
    const gl = this.gl;
    this.resize();

    gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    gl.useProgram(this.program);
    gl.bindVertexArray(this.vao);

    const t = (performance.now() - this.start) / 1000;

    gl.uniform1f(this.uTime, t);
    gl.uniform2f(this.uResolution, this.canvas.width, this.canvas.height);
    gl.uniform1f(this.uThroughput, this.state.throughput);
    gl.uniform1f(this.uPhase, this.state.phase);
    gl.uniform1f(this.uCoherence, this.state.coherence);
    gl.uniform1f(this.uNoiseFloor, this.state.noiseFloor);
    gl.uniform1f(this.uAlert, this.state.alert);

    gl.uniform3f(this.uPaletteA, 0.08, 0.23, 0.55);
    gl.uniform3f(this.uPaletteB, 0.18, 0.74, 0.92);
    gl.uniform3f(this.uPaletteC, 0.95, 0.36, 0.30);

    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(this.frame);
  };

  startLoop(): void {
    requestAnimationFrame(this.frame);
  }

  private cacheUniforms(): void {
    const gl = this.gl;
    const p = this.program;
    const get = (n: string) => {
      const u = gl.getUniformLocation(p, n);
      if (!u) throw new Error(`Missing uniform: ${n}`);
      return u;
    };

    this.uTime = get("u_time");
    this.uResolution = get("u_resolution");
    this.uThroughput = get("u_throughput");
    this.uPhase = get("u_phase");
    this.uCoherence = get("u_coherence");
    this.uNoiseFloor = get("u_noiseFloor");
    this.uAlert = get("u_alert");
    this.uPaletteA = get("u_paletteA");
    this.uPaletteB = get("u_paletteB");
    this.uPaletteC = get("u_paletteC");
  }

  private resize(): void {
    const dpr = window.devicePixelRatio || 1;
    const w = Math.floor(this.canvas.clientWidth * dpr);
    const h = Math.floor(this.canvas.clientHeight * dpr);
    if (this.canvas.width !== w || this.canvas.height !== h) {
      this.canvas.width = w;
      this.canvas.height = h;
    }
  }

  private createProgram(vs: string, fs: string): WebGLProgram {
    const gl = this.gl;
    const v = this.compile(gl.VERTEX_SHADER, vs);
    const f = this.compile(gl.FRAGMENT_SHADER, fs);

    const p = gl.createProgram();
    if (!p) throw new Error("Failed to create program");
    gl.attachShader(p, v);
    gl.attachShader(p, f);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      throw new Error(`Program link failed: ${gl.getProgramInfoLog(p)}`);
    }
    return p;
  }

  private compile(type: number, source: string): WebGLShader {
    const gl = this.gl;
    const s = gl.createShader(type);
    if (!s) throw new Error("Failed to create shader");
    gl.shaderSource(s, source);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error(`Shader compile failed: ${gl.getShaderInfoLog(s)}`);
    }
    return s;
  }
}
