import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { CAROL_IDLE_VARIANTS, EEVEE_MOTION_CORPUS, getCarolIdlePose, parseCarolIdleVariant } from "../src/grimo/motion/carol-motion.ts";
import { NEUTRAL_CAROL_POSE, sampleEeveeMotion } from "../src/grimo/motion/eevee-motion-corpus.ts";
import { hitTestCarolZone } from "../src/grimo/interaction/carol-semantic-zones.ts";
import { FrameTimeMonitor } from "../src/grimo/runtime/frame-time-monitor.ts";

test("Carol Phase 2 candidates compose source clips without overlap", () => {
  for (const candidate of Object.values(CAROL_IDLE_VARIANTS)) {
    assert.equal(candidate.cycleDurationMs, 30_000);
    for (let index = 0; index < candidate.schedule.length; index += 1) {
      const event = candidate.schedule[index];
      const end = event.atMs + EEVEE_MOTION_CORPUS[event.motionId].durationMs;
      assert.ok(end <= candidate.cycleDurationMs);
      if (index + 1 < candidate.schedule.length) assert.ok(end <= candidate.schedule[index + 1].atMs);
    }
  }
});

test("Carol Phase 2 schedules are deterministic and differ by selection rather than amplitude", () => {
  const balanced = CAROL_IDLE_VARIANTS.B;
  assert.deepEqual(getCarolIdlePose(9_000, balanced), getCarolIdlePose(9_000, balanced));
  assert.equal(getCarolIdlePose(0, balanced).activeAction, "quiet");
  assert.equal(getCarolIdlePose(3_000, balanced).activeAction, "gaze-release-right");
  assert.equal(getCarolIdlePose(9_000, balanced).activeAction, "head-sweep-settle");
  assert.equal(getCarolIdlePose(17_000, balanced).activeAction, "surprise-ear-open");
  assert.equal(getCarolIdlePose(23_000, balanced).activeAction, "bow-afterglow");
  assert.equal(getCarolIdlePose(2_000, CAROL_IDLE_VARIANTS.C).activeAction, "partner-invite");
  assert.equal(getCarolIdlePose(19_000, CAROL_IDLE_VARIANTS.C).activeAction, "present-invitation");
  const regular = getCarolIdlePose(9_000, balanced);
  const reduced = getCarolIdlePose(9_000, balanced, true);
  assert.equal(reduced.activeAction, regular.activeAction);
  assert.equal(reduced.gazeShiftPx, regular.gazeShiftPx);
  assert.ok(Math.abs(reduced.headTiltDeg) < Math.abs(regular.headTiltDeg));
  assert.equal(parseCarolIdleVariant("C"), "C");
  assert.equal(parseCarolIdleVariant("unexpected"), "B");
});

test("every authored motion starts and settles at Carol neutral", () => {
  for (const motion of Object.values(EEVEE_MOTION_CORPUS)) {
    assert.deepEqual(sampleEeveeMotion(motion.id, 0), NEUTRAL_CAROL_POSE);
    assert.deepEqual(sampleEeveeMotion(motion.id, motion.durationMs), NEUTRAL_CAROL_POSE);
    assert.ok(motion.sourceClipId.startsWith("E"));
    assert.ok(motion.sourceTimestamp.length > 0);
  }
});

test("primary idle motion contains no global sine-wave generator", async () => {
  const [scheduler, corpus] = await Promise.all([
    readFile(new URL("../src/grimo/motion/carol-motion.ts", import.meta.url), "utf8"),
    readFile(new URL("../src/grimo/motion/eevee-motion-corpus.ts", import.meta.url), "utf8"),
  ]);
  assert.doesNotMatch(`${scheduler}\n${corpus}`, /Math\.sin|\bsin\s*\(/);
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
