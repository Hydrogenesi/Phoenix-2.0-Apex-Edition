#version 300 es
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

#define TAU 6.28318530718

float hash21(vec2 p) {
  p = fract(p * vec2(123.34, 345.45));
  p += dot(p, p + 34.345);
  return fract(p.x * p.y);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  float a = hash21(i);
  float b = hash21(i + vec2(1.0, 0.0));
  float c = hash21(i + vec2(0.0, 1.0));
  float d = hash21(i + vec2(1.0, 1.0));
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(a, b, u.x) +
         (c - a) * u.y * (1.0 - u.x) +
         (d - b) * u.x * u.y;
}

mat2 rot(float a) {
  float s = sin(a), c = cos(a);
  return mat2(c, -s, s, c);
}

void main() {
  vec2 fragCoord = gl_FragCoord.xy;
  vec2 p = (2.0 * fragCoord - u_resolution) / min(u_resolution.x, u_resolution.y);

  float t = u_time;
  float throughput = clamp(u_throughput, 0.0, 1.0);
  float coherence = clamp(u_coherence, 0.0, 1.0);
  float noiseFloor = clamp(u_noiseFloor, 0.0, 1.0);
  float alert = clamp(u_alert, 0.0, 1.0);

  vec2 q = p;
  q += 0.08 * vec2(
    noise(q * 1.6 + vec2(t * 0.12, -t * 0.10)) - 0.5,
    noise(q * 1.9 + vec2(-t * 0.09, t * 0.13)) - 0.5
  );

  float r = length(q);
  float a = atan(q.y, q.x);

  float phaseField = sin(8.0 * a + u_phase + t * 0.8);
  float freq = mix(18.0, 48.0, throughput);
  float band = sin(freq * r - t * 2.2 + phaseField * 0.7);

  float sharpen = mix(0.65, 2.6, coherence);
  float signal = pow(abs(band), sharpen);

  float stream = sin((a + t * 0.35 + phaseField * 0.2) * 14.0) * 0.5 + 0.5;
  signal = mix(signal, signal * stream, 0.35 + 0.25 * throughput);

  float grain = (noise(q * 7.0 + t * 0.5) - 0.5) * mix(0.01, 0.18, noiseFloor);

  float pulse = sin(t * (4.0 + 4.0 * alert)) * 0.5 + 0.5;
  float ring = smoothstep(0.05, 0.0, abs(r - 0.62));
  float alertMask = smoothstep(0.35, 0.9, alert) * ring * pulse;

  vec3 base = mix(u_paletteA, u_paletteB, signal);
  vec3 flux = mix(base, u_paletteC, alertMask);

  float vignette = smoothstep(1.05, 0.25, r);
  flux *= vignette;
  flux += grain;

  outColor = vec4(clamp(flux, 0.0, 1.0), 1.0);
}
