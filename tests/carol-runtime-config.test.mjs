import assert from "node:assert/strict";
import test from "node:test";
import { CAROL_IDLE_VARIANTS, getCarolIdlePose, parseCarolIdleVariant } from "../src/grimo/motion/carol-motion.ts";
import { hitTestCarolZone } from "../src/grimo/interaction/carol-semantic-zones.ts";
import { FrameTimeMonitor } from "../src/grimo/runtime/frame-time-monitor.ts";

test("Carol Phase 2 candidates remain ordered from grounded to expressive", () => {
  assert.ok(CAROL_IDLE_VARIANTS.A.baselineBodyLiftPx < CAROL_IDLE_VARIANTS.B.baselineBodyLiftPx);
  assert.ok(CAROL_IDLE_VARIANTS.B.baselineBodyLiftPx < CAROL_IDLE_VARIANTS.C.baselineBodyLiftPx);
  assert.ok(CAROL_IDLE_VARIANTS.A.attentionTiltDeg < CAROL_IDLE_VARIANTS.B.attentionTiltDeg);
  assert.ok(CAROL_IDLE_VARIANTS.B.attentionTiltDeg < CAROL_IDLE_VARIANTS.C.attentionTiltDeg);
  for (const candidate of Object.values(CAROL_IDLE_VARIANTS)) {
    assert.ok(candidate.fleeceLagMs >= 120);
    assert.ok(candidate.fleeceLagMs <= 250);
  }
});

test("Carol Phase 2 idle sequence is deterministic and reduced motion preserves state", () => {
  const balanced = CAROL_IDLE_VARIANTS.B;
  assert.deepEqual(getCarolIdlePose(4_800, balanced), getCarolIdlePose(4_800, balanced));
  assert.equal(getCarolIdlePose(5_300, balanced).activeAction, "glance");
  assert.equal(getCarolIdlePose(12_100, balanced).activeAction, "ear-settle");
  assert.equal(getCarolIdlePose(19_400, balanced).activeAction, "attention");
  const regular = getCarolIdlePose(19_400, balanced);
  const reduced = getCarolIdlePose(19_400, balanced, true);
  assert.equal(reduced.activeAction, regular.activeAction);
  assert.ok(Math.abs(reduced.headTiltDeg) < Math.abs(regular.headTiltDeg));
  assert.equal(parseCarolIdleVariant("C"), "C");
  assert.equal(parseCarolIdleVariant("unexpected"), "B");
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
