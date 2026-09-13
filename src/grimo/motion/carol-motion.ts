export type CarolMotionConfig = {
  idleCycleMs: number;
  bodyTranslationRatio: number;
  headRotationDeg: number;
  fleeceLagMs: number;
  fleeceFollowPx: number;
  groundLockStart: number;
  reducedMotionMultiplier: number;
};

export const CAROL_PHASE_ONE_MOTION = {
  idleCycleMs: 5_600,
  bodyTranslationRatio: 0.012,
  headRotationDeg: 2.4,
  fleeceLagMs: 180,
  fleeceFollowPx: 2.2,
  groundLockStart: 0.78,
  reducedMotionMultiplier: 0.18,
} as const satisfies CarolMotionConfig;

export function smoothstep(edge0: number, edge1: number, value: number): number {
  const t = Math.max(0, Math.min(1, (value - edge0) / (edge1 - edge0)));
  return t * t * (3 - 2 * t);
}
