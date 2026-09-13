import assert from "node:assert/strict";
import test from "node:test";
import { CAROL_PHASE_ONE_MOTION } from "../src/grimo/motion/carol-motion.ts";
import { hitTestCarolZone } from "../src/grimo/interaction/carol-semantic-zones.ts";
import { FrameTimeMonitor } from "../src/grimo/runtime/frame-time-monitor.ts";

test("Carol motion stays inside the Gate 1 tuning envelope", () => {
  assert.ok(CAROL_PHASE_ONE_MOTION.bodyTranslationRatio >= 0.01);
  assert.ok(CAROL_PHASE_ONE_MOTION.bodyTranslationRatio <= 0.025);
  assert.ok(CAROL_PHASE_ONE_MOTION.headRotationDeg >= 2);
  assert.ok(CAROL_PHASE_ONE_MOTION.headRotationDeg <= 5);
  assert.ok(CAROL_PHASE_ONE_MOTION.fleeceLagMs >= 120);
  assert.ok(CAROL_PHASE_ONE_MOTION.fleeceLagMs <= 250);
  assert.ok(CAROL_PHASE_ONE_MOTION.groundLockStart < 0.85);
});

test("Carol semantic zones preserve the back=normal revision lock", () => {
  assert.equal(hitTestCarolZone(170, 300)?.id, "body-fleece-back");
  assert.equal(hitTestCarolZone(170, 300)?.meaning, "normal");
  assert.equal(hitTestCarolZone(310, 455)?.meaning, "mild-dislike");
  assert.equal(hitTestCarolZone(268, 220)?.meaning, "special");
  assert.equal(hitTestCarolZone(458, 294)?.meaning, "excluded");
});

test("frame summary reports percentiles and long-frame rate", () => {
  const monitor = new FrameTimeMonitor();
  [16, 17, 18, 20, 60].forEach((duration, index) => monitor.record(index * 20, duration));
  const summary = monitor.summary();
  assert.equal(summary.sampleCount, 5);
  assert.equal(summary.p95Ms, 60);
  assert.equal(summary.framesOver50Ms, 1);
  assert.equal(summary.framesOver50Percent, 20);
});
