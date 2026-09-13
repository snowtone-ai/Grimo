export const CAROL_MOTION_IDS = [
  "quiet-hold",
  "gaze-release-right",
  "soft-close-settle",
  "head-sweep-settle",
  "ear-sweep-settle",
  "surprise-ear-open",
  "bow-afterglow",
  "partner-invite",
  "present-invitation",
] as const;

export type CarolMotionId = (typeof CAROL_MOTION_IDS)[number];
export type CarolIdleAction = "quiet" | CarolMotionId;

export type CarolMotionPose = {
  bodyShiftXPx: number;
  bodyLiftPx: number;
  bodyCompressionPx: number;
  headShiftXPx: number;
  headLiftPx: number;
  headTiltDeg: number;
  gazeShiftPx: number;
  leftEarTiltDeg: number;
  rightEarTiltDeg: number;
  fleeceShiftXPx: number;
  fleeceFollowPx: number;
  attention: number;
};

type MotionPhase = "initial" | "anticipation" | "primary" | "peak" | "hold" | "follow-through" | "settle" | "afterglow";
type MotionEase = "hold" | "linear" | "ease-in" | "ease-out" | "ease-in-out";

export type CarolMotionKeyframe = {
  atMs: number;
  phase: MotionPhase;
  ease?: MotionEase;
  pose?: Partial<CarolMotionPose>;
};

export type EeveeMotionClip = {
  id: CarolMotionId;
  semanticName: string;
  sourceClipId: string;
  sourceVideoId: string;
  sourceTimestamp: string;
  sourceDurationMs: number;
  durationMs: number;
  confidence: "high" | "medium";
  settleState: "neutral";
  phaseOrder: readonly MotionPhase[];
  adaptationNotes: string;
  keyframes: readonly CarolMotionKeyframe[];
};

export const NEUTRAL_CAROL_POSE: CarolMotionPose = {
  bodyShiftXPx: 0,
  bodyLiftPx: 0,
  bodyCompressionPx: 0,
  headShiftXPx: 0,
  headLiftPx: 0,
  headTiltDeg: 0,
  gazeShiftPx: 0,
  leftEarTiltDeg: 0,
  rightEarTiltDeg: 0,
  fleeceShiftXPx: 0,
  fleeceFollowPx: 0,
  attention: 0,
};

const clip = (value: EeveeMotionClip) => value;

export const EEVEE_MOTION_CORPUS = {
  "quiet-hold": clip({
    id: "quiet-hold", semanticName: "Intentional near-still hold", sourceClipId: "E22", sourceVideoId: "MUykqFWL7R4", sourceTimestamp: "00:20-00:26", sourceDurationMs: 6_000, durationMs: 6_000, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "hold", "settle"],
    adaptationNotes: "The source proves that a weighted pose and genuine stillness read as life. Carol stays awake and exactly neutral.",
    keyframes: [{ atMs: 0, phase: "initial", ease: "hold" }, { atMs: 5_500, phase: "hold", ease: "hold" }, { atMs: 6_000, phase: "settle", ease: "hold" }],
  }),
  "gaze-release-right": clip({
    id: "gaze-release-right", semanticName: "Eyes lead a small rightward attention release", sourceClipId: "E06", sourceVideoId: "0KSZwNZ5m1E", sourceTimestamp: "01:20-01:23.6", sourceDurationMs: 3_600, durationMs: 3_600, confidence: "medium", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "hold", "settle"], adaptationNotes: "Gaze moves before the head. The root and hooves remain still.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 360, phase: "anticipation", ease: "ease-out", pose: { gazeShiftPx: 1.4, attention: 0.55 } },
      { atMs: 920, phase: "primary", ease: "ease-out", pose: { gazeShiftPx: 2.2, headShiftXPx: 0.8, headTiltDeg: 0.65, attention: 0.8 } },
      { atMs: 2_150, phase: "hold", ease: "hold", pose: { gazeShiftPx: 2.2, headShiftXPx: 0.8, headTiltDeg: 0.65, attention: 0.8 } },
      { atMs: 3_600, phase: "settle", ease: "ease-in-out" },
    ],
  }),
  "soft-close-settle": clip({
    id: "soft-close-settle", semanticName: "Soft centered dip and ear release", sourceClipId: "E33", sourceVideoId: "KLYnGhsu8AI", sourceTimestamp: "02:34-02:40", sourceDurationMs: 6_000, durationMs: 6_000, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "hold", "follow-through", "settle"], adaptationNotes: "Carol has no eyelid layer, so the source eye-close is carried by a shallow head dip and later ear broadening.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 650, phase: "anticipation", ease: "ease-in", pose: { headLiftPx: 0.8, attention: 0.25 } },
      { atMs: 1_550, phase: "primary", ease: "ease-out", pose: { headLiftPx: 2.6, bodyCompressionPx: 0.8, attention: 0.7 } },
      { atMs: 2_250, phase: "hold", ease: "ease-out", pose: { headLiftPx: 2.9, bodyCompressionPx: 1.0, leftEarTiltDeg: 3.5, rightEarTiltDeg: -3.5, attention: 0.8 } },
      { atMs: 3_500, phase: "follow-through", ease: "hold", pose: { headLiftPx: 2.5, bodyCompressionPx: 0.8, leftEarTiltDeg: 3.5, rightEarTiltDeg: -3.5, fleeceFollowPx: 0.8, attention: 0.7 } },
      { atMs: 6_000, phase: "settle", ease: "ease-in-out" },
    ],
  }),
  "head-sweep-settle": clip({
    id: "head-sweep-settle", semanticName: "Downbeat, two-direction head sweep, and attentive recovery", sourceClipId: "E03", sourceVideoId: "6tJzupfNSN8", sourceTimestamp: "02:29.8-02:35", sourceDurationMs: 5_200, durationMs: 5_200, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "peak", "follow-through", "settle", "afterglow"], adaptationNotes: "Preserves the down → right → left → center order. Fleece follows after each reversal; hooves remain locked.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 900, phase: "anticipation", ease: "ease-in", pose: { headLiftPx: 4.2, bodyCompressionPx: 1.4, attention: 0.35 } },
      { atMs: 1_700, phase: "primary", ease: "ease-out", pose: { headShiftXPx: 2.2, headLiftPx: 3.4, headTiltDeg: 3.6, leftEarTiltDeg: 1.6, rightEarTiltDeg: -4.2, attention: 0.65 } },
      { atMs: 2_850, phase: "peak", ease: "ease-in-out", pose: { headShiftXPx: -2.8, headLiftPx: 2.6, headTiltDeg: -4.4, gazeShiftPx: -0.6, leftEarTiltDeg: 4.8, rightEarTiltDeg: -1.4, bodyShiftXPx: -0.8, fleeceShiftXPx: 0.6, attention: 0.9 } },
      { atMs: 3_650, phase: "follow-through", ease: "ease-out", pose: { headShiftXPx: 0.8, headLiftPx: 1.1, headTiltDeg: 1.3, gazeShiftPx: 0.5, leftEarTiltDeg: 1.0, rightEarTiltDeg: -1.8, fleeceShiftXPx: -0.9, fleeceFollowPx: 0.9, attention: 0.8 } },
      { atMs: 4_700, phase: "settle", ease: "ease-in-out", pose: { headTiltDeg: -0.35, fleeceShiftXPx: 0.35, fleeceFollowPx: 0.25, attention: 0.35 } },
      { atMs: 5_200, phase: "afterglow", ease: "ease-out" },
    ],
  }),
  "ear-sweep-settle": clip({
    id: "ear-sweep-settle", semanticName: "Asymmetric ear relax and soft recovery", sourceClipId: "E18", sourceVideoId: "8Z8UUm5wYms", sourceTimestamp: "01:43.5-01:48", sourceDurationMs: 4_500, durationMs: 4_500, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "peak", "follow-through", "settle"], adaptationNotes: "One ear moves strongly while the opposite ear remains attentive; recovery passes through a broad-ear pose.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 760, phase: "anticipation", ease: "ease-in", pose: { headLiftPx: 1.0, headTiltDeg: -0.55, attention: 0.4 } },
      { atMs: 1_650, phase: "primary", ease: "ease-out", pose: { headLiftPx: 1.9, headTiltDeg: -1.2, leftEarTiltDeg: 8.2, rightEarTiltDeg: -1.0, attention: 0.8 } },
      { atMs: 2_250, phase: "peak", ease: "ease-out", pose: { headLiftPx: 2.1, headTiltDeg: -1.45, leftEarTiltDeg: 10.4, rightEarTiltDeg: -1.4, fleeceFollowPx: 0.45, attention: 0.9 } },
      { atMs: 3_250, phase: "follow-through", ease: "ease-in-out", pose: { headLiftPx: 1.0, leftEarTiltDeg: 3.6, rightEarTiltDeg: -3.6, fleeceFollowPx: 0.9, attention: 0.6 } },
      { atMs: 4_500, phase: "settle", ease: "ease-in-out" },
    ],
  }),
  "surprise-ear-open": clip({
    id: "surprise-ear-open", semanticName: "Open attention followed by a late joyful ear spread", sourceClipId: "E12", sourceVideoId: "I3aGhd8KKB8", sourceTimestamp: "00:27.2-00:30.2", sourceDurationMs: 3_000, durationMs: 3_000, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "peak", "hold", "settle"], adaptationNotes: "Head/gaze anticipation leads; both ears move late and quickly into the widest silhouette.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 620, phase: "anticipation", ease: "ease-out", pose: { headLiftPx: -1.8, gazeShiftPx: 0.35, attention: 1 } },
      { atMs: 1_080, phase: "primary", ease: "ease-in", pose: { headLiftPx: -1.0, bodyLiftPx: -0.8, attention: 1 } },
      { atMs: 1_620, phase: "peak", ease: "ease-out", pose: { headLiftPx: 0.6, bodyCompressionPx: 0.9, leftEarTiltDeg: 9.2, rightEarTiltDeg: -9.2, attention: 1 } },
      { atMs: 2_260, phase: "hold", ease: "hold", pose: { headLiftPx: 0.7, bodyCompressionPx: 0.8, leftEarTiltDeg: 9.2, rightEarTiltDeg: -9.2, fleeceFollowPx: 0.7, attention: 0.9 } },
      { atMs: 3_000, phase: "settle", ease: "ease-in-out" },
    ],
  }),
  "bow-afterglow": clip({
    id: "bow-afterglow", semanticName: "Centered weighted bow, held compression, and happy lift", sourceClipId: "E30", sourceVideoId: "Zp5UqOMfXds", sourceTimestamp: "03:18.5-03:25.3", sourceDurationMs: 6_800, durationMs: 6_800, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "hold", "peak", "follow-through", "settle", "afterglow"], adaptationNotes: "Uses the clean bow/lift portion rather than the repeated touch interval. Feet remain fixed while upper mass compresses.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 700, phase: "anticipation", ease: "ease-in", pose: { headLiftPx: 1.4, bodyCompressionPx: 0.6, attention: 0.45 } },
      { atMs: 1_850, phase: "primary", ease: "ease-out", pose: { headLiftPx: 7.2, bodyCompressionPx: 3.4, leftEarTiltDeg: 2.4, rightEarTiltDeg: -5.8, attention: 0.85 } },
      { atMs: 3_250, phase: "hold", ease: "hold", pose: { headLiftPx: 7.2, bodyCompressionPx: 3.4, leftEarTiltDeg: 2.4, rightEarTiltDeg: -5.8, fleeceFollowPx: 1.2, attention: 0.85 } },
      { atMs: 4_150, phase: "peak", ease: "ease-out", pose: { headLiftPx: -1.2, bodyLiftPx: -1.1, bodyCompressionPx: 0.2, leftEarTiltDeg: 5.6, rightEarTiltDeg: -5.6, fleeceFollowPx: 1.6, attention: 1 } },
      { atMs: 5_050, phase: "follow-through", ease: "ease-in-out", pose: { headLiftPx: 0.5, bodyLiftPx: 0.2, leftEarTiltDeg: 2.2, rightEarTiltDeg: -2.2, fleeceFollowPx: -0.55, attention: 0.75 } },
      { atMs: 6_050, phase: "settle", ease: "ease-in-out", pose: { fleeceFollowPx: 0.25, attention: 0.3 } },
      { atMs: 6_800, phase: "afterglow", ease: "ease-out" },
    ],
  }),
  "partner-invite": clip({
    id: "partner-invite", semanticName: "Self-initiated forward attention and held invitation", sourceClipId: "E05", sourceVideoId: "0KSZwNZ5m1E", sourceTimestamp: "00:30-00:39", sourceDurationMs: 9_000, durationMs: 9_000, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "hold", "follow-through", "settle", "afterglow"], adaptationNotes: "Maps the initial invitation and held partner focus. The source paw is omitted because Carol has no independent forelimb layer.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 900, phase: "anticipation", ease: "ease-out", pose: { gazeShiftPx: 0.7, headLiftPx: -1.2, attention: 0.75 } },
      { atMs: 2_100, phase: "primary", ease: "ease-out", pose: { headShiftXPx: 1.5, headLiftPx: -2.2, headTiltDeg: 1.8, bodyShiftXPx: 0.6, bodyLiftPx: -0.6, gazeShiftPx: 1.1, attention: 1 } },
      { atMs: 5_200, phase: "hold", ease: "hold", pose: { headShiftXPx: 1.5, headLiftPx: -2.2, headTiltDeg: 1.8, bodyShiftXPx: 0.6, bodyLiftPx: -0.6, gazeShiftPx: 1.1, attention: 1 } },
      { atMs: 6_250, phase: "follow-through", ease: "ease-in-out", pose: { headShiftXPx: -0.5, headLiftPx: 0.8, headTiltDeg: -0.7, bodyShiftXPx: -0.2, leftEarTiltDeg: 4.4, rightEarTiltDeg: -4.4, fleeceShiftXPx: 0.7, attention: 0.9 } },
      { atMs: 7_650, phase: "settle", ease: "ease-in-out", pose: { fleeceShiftXPx: -0.25, fleeceFollowPx: 0.45, attention: 0.5 } },
      { atMs: 9_000, phase: "afterglow", ease: "ease-out" },
    ],
  }),
  "present-invitation": clip({
    id: "present-invitation", semanticName: "Centered proud reveal, broad-ear afterglow, and quiet return", sourceClipId: "E32", sourceVideoId: "KLYnGhsu8AI", sourceTimestamp: "02:06-02:18", sourceDurationMs: 12_000, durationMs: 12_000, confidence: "high", settleState: "neutral",
    phaseOrder: ["initial", "anticipation", "primary", "hold", "peak", "follow-through", "settle", "afterglow"], adaptationNotes: "The Pokémon item is omitted. Carol keeps the centered forward offer, proud hold, late ear breadth, and player-facing return.",
    keyframes: [
      { atMs: 0, phase: "initial" },
      { atMs: 1_500, phase: "anticipation", ease: "ease-in", pose: { headLiftPx: 1.0, bodyCompressionPx: 0.5, attention: 0.65 } },
      { atMs: 3_100, phase: "primary", ease: "ease-out", pose: { headLiftPx: -1.8, bodyLiftPx: -0.8, bodyCompressionPx: 0.3, attention: 1 } },
      { atMs: 5_300, phase: "hold", ease: "hold", pose: { headLiftPx: -1.8, bodyLiftPx: -0.8, bodyCompressionPx: 0.3, attention: 1 } },
      { atMs: 7_200, phase: "peak", ease: "ease-out", pose: { headLiftPx: 1.0, bodyCompressionPx: 1.1, leftEarTiltDeg: 7.2, rightEarTiltDeg: -7.2, fleeceFollowPx: 0.8, attention: 1 } },
      { atMs: 8_650, phase: "follow-through", ease: "hold", pose: { headLiftPx: 0.8, leftEarTiltDeg: 7.2, rightEarTiltDeg: -7.2, fleeceFollowPx: 1.1, attention: 0.9 } },
      { atMs: 10_500, phase: "settle", ease: "ease-in-out", pose: { leftEarTiltDeg: 1.2, rightEarTiltDeg: -1.2, fleeceFollowPx: -0.35, attention: 0.45 } },
      { atMs: 12_000, phase: "afterglow", ease: "ease-out" },
    ],
  }),
} as const satisfies Record<CarolMotionId, EeveeMotionClip>;

function applyEase(progress: number, ease: MotionEase): number {
  if (ease === "hold") return 0;
  if (ease === "linear") return progress;
  if (ease === "ease-in") return progress * progress;
  if (ease === "ease-out") return 1 - (1 - progress) * (1 - progress);
  return progress * progress * (3 - 2 * progress);
}

function completePose(partial?: Partial<CarolMotionPose>): CarolMotionPose {
  return { ...NEUTRAL_CAROL_POSE, ...partial };
}

export function sampleEeveeMotion(id: CarolMotionId, elapsedMs: number, reducedMotion = false): CarolMotionPose {
  const motion = EEVEE_MOTION_CORPUS[id];
  const localMs = Math.max(0, Math.min(motion.durationMs, elapsedMs));
  let left = motion.keyframes[0];
  let right = motion.keyframes[motion.keyframes.length - 1];
  for (let index = 1; index < motion.keyframes.length; index += 1) {
    if (motion.keyframes[index].atMs >= localMs) {
      right = motion.keyframes[index];
      left = motion.keyframes[index - 1];
      break;
    }
  }
  const span = Math.max(1, right.atMs - left.atMs);
  const rawProgress = Math.max(0, Math.min(1, (localMs - left.atMs) / span));
  const progress = applyEase(rawProgress, right.ease ?? "ease-in-out");
  const from = completePose(left.pose);
  const to = completePose(right.pose);
  const travelScale = reducedMotion ? 0.28 : 1;
  const angleScale = reducedMotion ? 0.42 : 1;
  const result = { ...NEUTRAL_CAROL_POSE };
  for (const key of Object.keys(result) as Array<keyof CarolMotionPose>) {
    const value = from[key] + (to[key] - from[key]) * progress;
    if (key === "attention" || key === "gazeShiftPx") result[key] = value;
    else if (key === "headTiltDeg" || key === "leftEarTiltDeg" || key === "rightEarTiltDeg") result[key] = value * angleScale;
    else result[key] = value * travelScale;
  }
  return result;
}
