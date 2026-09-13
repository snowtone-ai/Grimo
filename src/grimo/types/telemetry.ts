import type { CarolSemanticZoneId } from "../interaction/carol-semantic-zones";
import type { CarolIdleVariant } from "../motion/carol-motion";

export type CarolRuntimeMode = "idle" | "still" | "deformed";

export type FrameTimeSummary = {
  sampleCount: number;
  windowMs: number;
  averageFps: number;
  p95Ms: number;
  p99Ms: number;
  framesOver50Ms: number;
  framesOver50Percent: number;
};

export type InteractionTrace = {
  inputTimestamp: number;
  zone: CarolSemanticZoneId | null;
  reactionId: null;
  firstVisibleAcknowledgmentTimestamp: null;
  primaryMotionStartTimestamp: null;
  primaryMotionPeakTimestamp: null;
  secondaryMotionStartTimestamp: null;
  settleStartTimestamp: null;
  settleEndTimestamp: null;
  interruptState: "none" | "pointercancel" | "lostpointercapture";
};

export type CarolQaSnapshot = {
  mode: CarolRuntimeMode;
  idleVariant: CarolIdleVariant;
  idleAction: "quiet" | "glance" | "ear-settle" | "attention";
  reducedMotion: boolean;
  resolution: number;
  viewportCss: { width: number; height: number };
  activeApplications: number;
  mounts: number;
  destroys: number;
  pointerListeners: number;
  activePointers: number;
  reactionQueueLength: 0;
  accidentalActionsAfterCancel: 0;
  frameTime: FrameTimeSummary;
  latestInteraction: InteractionTrace | null;
  neutralFidelity: {
    derivation: "same-canonical-texture-and-neutral-transform";
    centerDriftPercent: 0;
    scaleDriftPercent: 0;
    faceCenterDriftPercentOfHeadWidth: 0;
    eyeLineRotationDeg: 0;
    hoofBaselineDriftCssPx: 0;
  };
};
