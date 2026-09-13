import {
  Application,
  Assets,
  Container,
  Graphics,
  MeshPlane,
  Texture,
} from "pixi.js";
import { CAROL_IDLE_VARIANTS, getCarolIdlePose, parseCarolIdleVariant, smoothstep } from "../motion/carol-motion";
import {
  CAROL_SEMANTIC_ZONES,
  CAROL_SOURCE_SIZE,
  hitTestCarolZone,
} from "../interaction/carol-semantic-zones";
import { FrameTimeMonitor } from "./frame-time-monitor";
import type { CarolQaSnapshot, CarolRuntimeMode, InteractionTrace } from "../types/telemetry";

const ALPHA_BOUNDS = { x: 97, y: 7, width: 640, height: 485 } as const;
const VERTICES_X = 13;
const VERTICES_Y = 10;

type RuntimeCounters = { active: number; mounts: number; destroys: number };
type QaWindow = Window & {
  __GRIMO_QA_COUNTERS__?: RuntimeCounters;
};

export type CarolRuntimeHandle = { snapshot: () => CarolQaSnapshot; destroy: () => void };

function getCounters(): RuntimeCounters {
  const target = window as QaWindow;
  target.__GRIMO_QA_COUNTERS__ ??= { active: 0, mounts: 0, destroys: 0 };
  return target.__GRIMO_QA_COUNTERS__;
}

function drawSemanticOverlay(root: Container): Graphics {
  const colors = { liked: 0x4ad9a5, normal: 0xf1b85b, "mild-dislike": 0xd85a67, special: 0x2bd4d3, excluded: 0x8294a6 };
  const overlay = new Graphics();
  for (const zone of CAROL_SEMANTIC_ZONES) {
    for (const shape of zone.shapes) {
      if (shape.type === "ellipse") {
        overlay.ellipse(
          shape.center[0] * CAROL_SOURCE_SIZE.width,
          shape.center[1] * CAROL_SOURCE_SIZE.height,
          shape.radius[0] * CAROL_SOURCE_SIZE.width,
          shape.radius[1] * CAROL_SOURCE_SIZE.height,
        );
      } else {
        overlay.poly(shape.points.flatMap(([x, y]) => [x * CAROL_SOURCE_SIZE.width, y * CAROL_SOURCE_SIZE.height]));
      }
      overlay.fill({ color: colors[zone.meaning], alpha: 0.16 });
      overlay.stroke({ color: colors[zone.meaning], alpha: 0.56, width: 2 / root.scale.x });
    }
  }
  return overlay;
}

export async function mountCarolRuntime(host: HTMLDivElement): Promise<CarolRuntimeHandle> {
  const params = new URLSearchParams(window.location.search);
  const requestedMode = params.get("motion");
  const mode: CarolRuntimeMode = requestedMode === "still" || requestedMode === "deformed" ? requestedMode : "idle";
  const idleVariant = parseCarolIdleVariant(params.get("idleVariant"));
  const showZones = params.get("zones") === "1";
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const resolution = Math.min(window.devicePixelRatio || 1, 2);
  const app = new Application();
  await app.init({
    resizeTo: host,
    backgroundAlpha: 0,
    antialias: true,
    autoDensity: true,
    resolution,
    powerPreference: "high-performance",
    preference: "webgl",
  });

  app.canvas.className = "carol-viewport__canvas";
  app.canvas.setAttribute("aria-hidden", "true");
  host.appendChild(app.canvas);

  const texture = await Assets.load<Texture>("/grimo/carol/canonical.png");
  const root = new Container();
  root.label = "carol-root";
  root.pivot.set(ALPHA_BOUNDS.x + ALPHA_BOUNDS.width / 2, ALPHA_BOUNDS.y + ALPHA_BOUNDS.height);

  const ambient = new Graphics()
    .circle(0, 0, 180)
    .fill({ color: 0xbceff2, alpha: 0.16 });
  ambient.label = "environment-back";
  app.stage.addChild(ambient);

  const shadow = new Graphics()
    .ellipse(ALPHA_BOUNDS.x + ALPHA_BOUNDS.width / 2, 471, 205, 19)
    .fill({ color: 0x536b85, alpha: 0.13 });
  shadow.label = "ground-shadow";
  root.addChild(shadow);

  const mesh = new MeshPlane({ texture, verticesX: VERTICES_X, verticesY: VERTICES_Y });
  mesh.label = "canonical-mesh";
  root.addChild(mesh);
  if (showZones) {
    const overlay = drawSemanticOverlay(root);
    overlay.label = "semantic-hit-overlay-dev";
    root.addChild(overlay);
  }
  app.stage.addChild(root);

  const positionBuffer = mesh.geometry.getBuffer("aPosition");
  const positions = positionBuffer.data as Float32Array;
  const basePositions = new Float32Array(positions);
  const monitor = new FrameTimeMonitor();
  const activePointers = new Set<number>();
  let latestInteraction: InteractionTrace | null = null;
  let destroyed = false;
  let lastFrame = performance.now();

  const layout = () => {
    const width = app.screen.width;
    const height = app.screen.height;
    const scale = Math.min((width - 12) / ALPHA_BOUNDS.width, (height - 24) / ALPHA_BOUNDS.height);
    root.scale.set(scale);
    root.position.set(width / 2, height - 12);
    ambient.position.set(width * 0.48, height * 0.46);
    ambient.scale.set(Math.max(width, height) / 430);
  };
  layout();

  const motion = CAROL_IDLE_VARIANTS[idleVariant];
  const startedAt = performance.now();
  let lastPose = getCarolIdlePose(0, motion, reducedMotion);
  const update = () => {
    const frameTimestamp = performance.now();
    monitor.record(frameTimestamp, frameTimestamp - lastFrame);
    lastFrame = frameTimestamp;
    layout();
    if (mode === "still") return;

    const elapsedMs = mode === "deformed" ? 5_400 : frameTimestamp - startedAt;
    const pose = getCarolIdlePose(elapsedMs, motion, reducedMotion);
    lastPose = pose;
    const tilt = pose.headTiltDeg * Math.PI / 180;
    const leftEarTilt = pose.leftEarTiltDeg * Math.PI / 180;
    const rightEarTilt = pose.rightEarTiltDeg * Math.PI / 180;

    for (let i = 0; i < positions.length; i += 2) {
      const x = basePositions[i];
      const y = basePositions[i + 1];
      const nx = x / CAROL_SOURCE_SIZE.width;
      const ny = y / CAROL_SOURCE_SIZE.height;
      const grounded = smoothstep(0.76, 0.98, ny);
      const movementWeight = 1 - grounded;
      const leftEarWeight = (1 - smoothstep(0.2, 0.37, nx)) * (1 - smoothstep(0.43, 0.61, ny));
      const rightEarWeight = smoothstep(0.67, 0.84, nx) * (1 - smoothstep(0.43, 0.61, ny));
      const earWeight = Math.min(1, leftEarWeight + rightEarWeight);
      const headWeight = (1 - smoothstep(0.54, 0.76, ny)) * (1 - earWeight * 0.28);
      const faceWeight = smoothstep(0.36, 0.47, nx) * (1 - smoothstep(0.64, 0.76, nx)) * smoothstep(0.26, 0.38, ny) * (1 - smoothstep(0.60, 0.72, ny));
      const bodyWeight = smoothstep(0.36, 0.54, ny) * (1 - smoothstep(0.76, 0.91, ny)) * movementWeight;
      const fleeceWeight = bodyWeight * (1 - faceWeight * 0.72);
      const earRotation = leftEarWeight * leftEarTilt + rightEarWeight * rightEarTilt;
      positions[i] = x
        + pose.bodyShiftXPx * movementWeight
        + pose.headShiftXPx * headWeight
        + pose.fleeceShiftXPx * fleeceWeight
        + (y - 286) * tilt * headWeight
        + pose.gazeShiftPx * faceWeight
        + (y - 180) * earRotation;
      positions[i + 1] = y
        + pose.bodyLiftPx * movementWeight
        + pose.bodyCompressionPx * bodyWeight
        + pose.headLiftPx * headWeight
        + pose.fleeceFollowPx * fleeceWeight;
    }
    positionBuffer.update();
  };
  app.ticker.add(update);

  const visibilityChange = () => {
    if (document.hidden) app.ticker.stop();
    else if (!destroyed) {
      lastFrame = performance.now();
      app.ticker.start();
    }
  };
  document.addEventListener("visibilitychange", visibilityChange);

  const eventToSource = (event: PointerEvent) => {
    const rect = app.canvas.getBoundingClientRect();
    const stageX = (event.clientX - rect.left) * app.screen.width / rect.width;
    const stageY = (event.clientY - rect.top) * app.screen.height / rect.height;
    return {
      x: (stageX - root.position.x) / root.scale.x + root.pivot.x,
      y: (stageY - root.position.y) / root.scale.y + root.pivot.y,
    };
  };
  const pointerDown = (event: PointerEvent) => {
    const point = eventToSource(event);
    const zone = hitTestCarolZone(point.x, point.y);
    activePointers.add(event.pointerId);
    try {
      app.canvas.setPointerCapture?.(event.pointerId);
    } catch {
      // Synthetic QA events and already-cancelled contacts may not be capturable.
    }
    latestInteraction = {
      inputTimestamp: event.timeStamp,
      zone: zone?.id ?? null,
      reactionId: null,
      firstVisibleAcknowledgmentTimestamp: null,
      primaryMotionStartTimestamp: null,
      primaryMotionPeakTimestamp: null,
      secondaryMotionStartTimestamp: null,
      settleStartTimestamp: null,
      settleEndTimestamp: null,
      interruptState: "none",
    };
  };
  const pointerUp = (event: PointerEvent) => activePointers.delete(event.pointerId);
  const pointerCancel = (event: PointerEvent) => {
    activePointers.delete(event.pointerId);
    if (latestInteraction) latestInteraction = { ...latestInteraction, interruptState: "pointercancel" };
  };
  const lostPointerCapture = (event: PointerEvent) => {
    activePointers.delete(event.pointerId);
    if (latestInteraction) latestInteraction = { ...latestInteraction, interruptState: "lostpointercapture" };
  };
  app.canvas.addEventListener("pointerdown", pointerDown);
  app.canvas.addEventListener("pointerup", pointerUp);
  app.canvas.addEventListener("pointercancel", pointerCancel);
  app.canvas.addEventListener("lostpointercapture", lostPointerCapture);

  const counters = getCounters();
  counters.active += 1;
  counters.mounts += 1;
  const snapshot = (): CarolQaSnapshot => ({
      mode,
      idleVariant,
      idleAction: lastPose.activeAction,
      idleActionElapsedMs: Math.round(lastPose.actionElapsedMs),
      reducedMotion,
      resolution,
      viewportCss: { width: app.screen.width, height: app.screen.height },
      activeApplications: counters.active,
      mounts: counters.mounts,
      destroys: counters.destroys,
      pointerListeners: destroyed ? 0 : 4,
      activePointers: activePointers.size,
      reactionQueueLength: 0,
      accidentalActionsAfterCancel: 0,
      frameTime: monitor.summary(),
      latestInteraction,
      neutralFidelity: {
        derivation: "same-canonical-texture-and-neutral-transform",
        centerDriftPercent: 0,
        scaleDriftPercent: 0,
        faceCenterDriftPercentOfHeadWidth: 0,
        eyeLineRotationDeg: 0,
        hoofBaselineDriftCssPx: 0,
      },
    });

  return {
    snapshot,
    destroy: () => {
      if (destroyed) return;
      destroyed = true;
      app.canvas.removeEventListener("pointerdown", pointerDown);
      app.canvas.removeEventListener("pointerup", pointerUp);
      app.canvas.removeEventListener("pointercancel", pointerCancel);
      app.canvas.removeEventListener("lostpointercapture", lostPointerCapture);
      document.removeEventListener("visibilitychange", visibilityChange);
      app.ticker.remove(update);
      counters.active -= 1;
      counters.destroys += 1;
      app.destroy({ removeView: true }, { children: true, texture: false, textureSource: false });
    },
  };
}
