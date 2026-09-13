export type CarolIdleVariant = "A" | "B" | "C";

export type CarolIdleConfig = {
  id: CarolIdleVariant;
  label: string;
  description: string;
  baselineBodyLiftPx: number;
  baselineHeadTiltDeg: number;
  attentionTiltDeg: number;
  earTiltDeg: number;
  fleeceLagMs: number;
  fleeceFollowPx: number;
  actionOffsetsMs: readonly number[];
  reducedMotionMultiplier: number;
};

export type CarolIdlePose = {
  bodyLiftPx: number;
  headTiltDeg: number;
  gazeShiftPx: number;
  leftEarTiltDeg: number;
  rightEarTiltDeg: number;
  fleeceFollowPx: number;
  activeAction: "quiet" | "glance" | "ear-settle" | "attention";
};

const IDLE_CYCLE_MS = 24_700;

export const CAROL_IDLE_VARIANTS = {
  A: { id: "A", label: "A — restrained / grounded", description: "最小限の呼吸と、長い静けさ。重さを最優先。", baselineBodyLiftPx: 0.72, baselineHeadTiltDeg: 0.55, attentionTiltDeg: 1.25, earTiltDeg: 0.8, fleeceLagMs: 190, fleeceFollowPx: 1.15, actionOffsetsMs: [5_600, 13_900, 20_900], reducedMotionMultiplier: 0.18 },
  B: { id: "B", label: "B — balanced", description: "静かな視線、耳、遅れて追うフリースが読める基準案。", baselineBodyLiftPx: 0.92, baselineHeadTiltDeg: 0.72, attentionTiltDeg: 1.75, earTiltDeg: 1.15, fleeceLagMs: 160, fleeceFollowPx: 1.65, actionOffsetsMs: [4_800, 11_600, 18_900], reducedMotionMultiplier: 0.18 },
  C: { id: "C", label: "C — expressive", description: "少しだけこちらを意識する、やわらかく明瞭な注意の移動。", baselineBodyLiftPx: 1.12, baselineHeadTiltDeg: 0.9, attentionTiltDeg: 2.35, earTiltDeg: 1.55, fleeceLagMs: 125, fleeceFollowPx: 2.05, actionOffsetsMs: [3_900, 10_200, 16_800], reducedMotionMultiplier: 0.18 },
} as const satisfies Record<CarolIdleVariant, CarolIdleConfig>;

export const CAROL_PHASE_ONE_MOTION = CAROL_IDLE_VARIANTS.B;

export function parseCarolIdleVariant(value: string | null): CarolIdleVariant {
  return value === "A" || value === "B" || value === "C" ? value : "B";
}

export function smoothstep(edge0: number, edge1: number, value: number): number {
  const t = Math.max(0, Math.min(1, (value - edge0) / (edge1 - edge0)));
  return t * t * (3 - 2 * t);
}

function pulse(elapsedMs: number, startMs: number, durationMs: number) {
  const progress = (elapsedMs - startMs) / durationMs;
  return progress <= 0 || progress >= 1 ? 0 : Math.sin(progress * Math.PI);
}

export function getCarolIdlePose(elapsedMs: number, config: CarolIdleConfig, reducedMotion = false): CarolIdlePose {
  const amplitude = reducedMotion ? config.reducedMotionMultiplier : 1;
  const cycleTime = ((elapsedMs % IDLE_CYCLE_MS) + IDLE_CYCLE_MS) % IDLE_CYCLE_MS;
  const breath = Math.sin((elapsedMs / 8_900) * Math.PI * 2);
  const glance = pulse(cycleTime, config.actionOffsetsMs[0], 1_250);
  const ear = pulse(cycleTime, config.actionOffsetsMs[1], 1_250);
  const attention = pulse(cycleTime, config.actionOffsetsMs[2], 1_750);
  const activeAction = attention ? "attention" : ear ? "ear-settle" : glance ? "glance" : "quiet";

  return {
    bodyLiftPx: (breath * config.baselineBodyLiftPx + attention * 0.52) * amplitude,
    headTiltDeg: (breath * config.baselineHeadTiltDeg + glance * config.attentionTiltDeg - attention * config.attentionTiltDeg * 0.65) * amplitude,
    gazeShiftPx: (glance * 0.8 - attention * 0.45) * amplitude,
    leftEarTiltDeg: (ear * config.earTiltDeg + attention * config.earTiltDeg * 0.35) * amplitude,
    rightEarTiltDeg: (-ear * config.earTiltDeg * 0.7 + glance * config.earTiltDeg * 0.25) * amplitude,
    fleeceFollowPx: (breath * config.fleeceFollowPx + attention * config.fleeceFollowPx * 0.6) * amplitude,
    activeAction,
  };
}
