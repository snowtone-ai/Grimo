import type { FrameTimeSummary } from "../types/telemetry";

export class FrameTimeMonitor {
  readonly #windowMs: number;
  #samples: { timestamp: number; duration: number }[] = [];

  constructor(windowMs = 30_000) {
    this.#windowMs = windowMs;
  }

  record(timestamp: number, duration: number): void {
    if (duration <= 0 || duration > 500) return;
    this.#samples.push({ timestamp, duration });
    const cutoff = timestamp - this.#windowMs;
    while (this.#samples[0]?.timestamp < cutoff) this.#samples.shift();
  }

  summary(): FrameTimeSummary {
    const durations = this.#samples.map((sample) => sample.duration).sort((a, b) => a - b);
    const percentile = (p: number) => durations.length
      ? durations[Math.min(durations.length - 1, Math.ceil(durations.length * p) - 1)]
      : 0;
    const total = durations.reduce((sum, duration) => sum + duration, 0);
    const framesOver50Ms = durations.filter((duration) => duration > 50).length;
    return {
      sampleCount: durations.length,
      windowMs: this.#windowMs,
      averageFps: total ? 1000 / (total / durations.length) : 0,
      p95Ms: percentile(0.95),
      p99Ms: percentile(0.99),
      framesOver50Ms,
      framesOver50Percent: durations.length ? (framesOver50Ms / durations.length) * 100 : 0,
    };
  }
}
