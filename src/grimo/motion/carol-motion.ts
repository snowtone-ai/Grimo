import {
  EEVEE_MOTION_CORPUS,
  NEUTRAL_CAROL_POSE,
  sampleEeveeMotion,
  type CarolIdleAction,
  type CarolMotionId,
  type CarolMotionPose,
} from "./eevee-motion-corpus.ts";

export type CarolIdleVariant = "A" | "B" | "C";

export type ScheduledCarolMotion = { atMs: number; motionId: CarolMotionId };

export type CarolIdleConfig = {
  id: CarolIdleVariant;
  label: string;
  description: string;
  cycleDurationMs: number;
  schedule: readonly ScheduledCarolMotion[];
};

export type CarolIdlePose = CarolMotionPose & {
  activeAction: CarolIdleAction;
  actionElapsedMs: number;
};

const CYCLE_DURATION_MS = 30_000;

export const CAROL_IDLE_VARIANTS = {
  A: {
    id: "A",
    label: "A — Eevee Calm",
    description: "長い静止を主役に、視線と片耳の小さな気配だけを置く落ち着いた構成。",
    cycleDurationMs: CYCLE_DURATION_MS,
    schedule: [
      { atMs: 0, motionId: "quiet-hold" },
      { atMs: 8_400, motionId: "gaze-release-right" },
      { atMs: 15_200, motionId: "soft-close-settle" },
      { atMs: 24_600, motionId: "ear-sweep-settle" },
    ],
  },
  B: {
    id: "B",
    label: "B — Eevee Balanced",
    description: "静けさの間に、首振り、耳開き、重いお辞儀を一度ずつ見せる基準案。",
    cycleDurationMs: CYCLE_DURATION_MS,
    schedule: [
      { atMs: 2_400, motionId: "gaze-release-right" },
      { atMs: 8_000, motionId: "head-sweep-settle" },
      { atMs: 16_000, motionId: "surprise-ear-open" },
      { atMs: 22_400, motionId: "bow-afterglow" },
    ],
  },
  C: {
    id: "C",
    label: "C — Eevee Attention-Seeking",
    description: "こちらを意識する長い誘いと誇らしい提示を中心にした、密度の高い構成。",
    cycleDurationMs: CYCLE_DURATION_MS,
    schedule: [
      { atMs: 1_000, motionId: "partner-invite" },
      { atMs: 12_000, motionId: "surprise-ear-open" },
      { atMs: 18_000, motionId: "present-invitation" },
    ],
  },
} as const satisfies Record<CarolIdleVariant, CarolIdleConfig>;

export const CAROL_PHASE_ONE_MOTION = CAROL_IDLE_VARIANTS.B;

export function parseCarolIdleVariant(value: string | null): CarolIdleVariant {
  return value === "A" || value === "B" || value === "C" ? value : "B";
}

export function smoothstep(edge0: number, edge1: number, value: number): number {
  const t = Math.max(0, Math.min(1, (value - edge0) / (edge1 - edge0)));
  return t * t * (3 - 2 * t);
}

export function getCarolIdlePose(elapsedMs: number, config: CarolIdleConfig, reducedMotion = false): CarolIdlePose {
  const cycleTime = ((elapsedMs % config.cycleDurationMs) + config.cycleDurationMs) % config.cycleDurationMs;
  const active = config.schedule.find(({ atMs, motionId }) => {
    const duration = EEVEE_MOTION_CORPUS[motionId].durationMs;
    return cycleTime >= atMs && cycleTime < atMs + duration;
  });
  if (!active) return { ...NEUTRAL_CAROL_POSE, activeAction: "quiet", actionElapsedMs: 0 };
  const actionElapsedMs = cycleTime - active.atMs;
  return { ...sampleEeveeMotion(active.motionId, actionElapsedMs, reducedMotion), activeAction: active.motionId, actionElapsedMs };
}

export { EEVEE_MOTION_CORPUS } from "./eevee-motion-corpus.ts";
export type { CarolIdleAction, CarolMotionId, CarolMotionPose } from "./eevee-motion-corpus.ts";
