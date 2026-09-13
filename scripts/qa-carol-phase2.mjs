import { mkdir, rename, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";

const baseUrl = process.env.GRIMO_QA_BASE_URL ?? "http://127.0.0.1:3000";
const captureDurationMs = Number(process.env.GRIMO_QA_SAMPLE_MS ?? 30_000);
const outputDir = resolve(process.env.GRIMO_QA_OUTPUT ?? "artifacts/grimo-qa/gate-2");
const viewport = { width: 412, height: 915 };

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  args: ["--enable-precise-memory-info"],
  ...(process.env.GRIMO_QA_BROWSER_CHANNEL ? { channel: process.env.GRIMO_QA_BROWSER_CHANNEL } : {}),
});
const consoleErrors = [];
const failedRequests = [];

async function captureCandidate(id) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 2.625,
    recordVideo: { dir: outputDir, size: viewport },
    reducedMotion: "no-preference",
  });
  const page = await context.newPage();
  const video = page.video();
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push({ id, text: message.text(), url: message.location().url });
  });
  page.on("pageerror", (error) => consoleErrors.push({ id, text: error.message }));
  page.on("requestfailed", (request) => failedRequests.push({ id, url: request.url(), error: request.failure()?.errorText ?? "unknown" }));
  await page.goto(`${baseUrl}/grimo/human-gate-2?idleVariant=${id}&seed=eevee-recovery-20260913`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => Boolean(window.__GRIMO_QA__));
  const memorySamplesBytes = [await page.evaluate(() => performance.memory?.usedJSHeapSize ?? null)];
  for (let sample = 0; sample < 3; sample += 1) {
    await page.waitForTimeout(captureDurationMs / 3);
    memorySamplesBytes.push(await page.evaluate(() => performance.memory?.usedJSHeapSize ?? null));
  }
  await page.screenshot({ path: resolve(outputDir, `pixel-7a-${id}.png`), fullPage: true });
  const qa = await page.evaluate(() => window.__GRIMO_QA__.snapshot());
  await context.close();
  const artifact = resolve(outputDir, `pixel-7a-${id}-30s.webm`);
  await rm(artifact, { force: true });
  await rename(await video.path(), artifact);
  return { qa, artifact, memorySamplesBytes };
}

async function checkRuntimeEdges() {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 2.625, reducedMotion: "reduce" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/grimo/human-gate-2?idleVariant=B&seed=eevee-recovery-20260913`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => Boolean(window.__GRIMO_QA__));
  await page.waitForTimeout(3_000);
  const reducedMotion = await page.evaluate(() => window.__GRIMO_QA__.snapshot());

  await page.setViewportSize({ width: 360, height: 740 });
  await page.waitForTimeout(250);
  const narrow = await page.evaluate(() => window.__GRIMO_QA__.snapshot());
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.waitForTimeout(250);
  const desktop = await page.evaluate(() => window.__GRIMO_QA__.snapshot());

  for (const id of ["C", "A", "B", "C", "A", "B"]) {
    await page.getByRole("link", { name: id, exact: true }).click();
    await page.waitForFunction((expected) => window.__GRIMO_QA__?.snapshot().idleVariant === expected, id);
  }
  const remount = await page.evaluate(() => window.__GRIMO_QA__.snapshot());

  await page.bringToFront();
  const visibilityBefore = await page.evaluate(() => ({ hidden: document.hidden, snapshot: window.__GRIMO_QA__.snapshot() }));
  await page.evaluate(() => {
    Object.defineProperty(document, "hidden", { configurable: true, value: true });
    document.dispatchEvent(new Event("visibilitychange"));
  });
  await page.waitForTimeout(500);
  const visibilityHidden = await page.evaluate(() => ({ hidden: document.hidden, snapshot: window.__GRIMO_QA__.snapshot() }));
  await page.evaluate(() => {
    Object.defineProperty(document, "hidden", { configurable: true, value: false });
    document.dispatchEvent(new Event("visibilitychange"));
  });
  await page.waitForTimeout(500);
  const visibilityResumed = await page.evaluate(() => ({ hidden: document.hidden, snapshot: window.__GRIMO_QA__.snapshot() }));

  await context.close();
  return { reducedMotion, narrow, desktop, remount, visibilityBefore, visibilityHidden, visibilityResumed };
}

const candidates = {};
const videos = {};
const memory = {};
for (const id of ["A", "B", "C"]) {
  const captured = await captureCandidate(id);
  candidates[id] = captured.qa;
  videos[id] = captured.artifact;
  memory[id] = {
    samplesBytes: captured.memorySamplesBytes,
    deltaBytes: captured.memorySamplesBytes[0] === null || captured.memorySamplesBytes.at(-1) === null
      ? null
      : captured.memorySamplesBytes.at(-1) - captured.memorySamplesBytes[0],
  };
}
const runtimeEdges = await checkRuntimeEdges();
const report = { generatedAt: new Date().toISOString(), baseUrl, viewport, captureDurationMs, candidates, memory, runtimeEdges, consoleErrors, failedRequests };
await writeFile(resolve(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();

const runtimeFailed = !runtimeEdges.reducedMotion.reducedMotion
  || runtimeEdges.narrow.viewportCss.width >= runtimeEdges.reducedMotion.viewportCss.width
  || runtimeEdges.narrow.viewportCss.height >= runtimeEdges.reducedMotion.viewportCss.height
  || runtimeEdges.desktop.viewportCss.width <= runtimeEdges.narrow.viewportCss.width
  || runtimeEdges.desktop.viewportCss.height <= runtimeEdges.narrow.viewportCss.height
  || runtimeEdges.remount.activeApplications !== 1
  || runtimeEdges.remount.mounts !== runtimeEdges.remount.destroys + 1
  || runtimeEdges.remount.pointerListeners !== 4
  || !runtimeEdges.visibilityHidden.hidden
  || runtimeEdges.visibilityHidden.snapshot.frameTime.sampleCount !== runtimeEdges.visibilityBefore.snapshot.frameTime.sampleCount
  || runtimeEdges.visibilityResumed.hidden
  || runtimeEdges.visibilityResumed.snapshot.frameTime.sampleCount <= runtimeEdges.visibilityHidden.snapshot.frameTime.sampleCount;
if (consoleErrors.length || failedRequests.length || runtimeFailed || Object.values(candidates).some((candidate) => candidate.activeApplications !== 1)) {
  console.error(JSON.stringify(report, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ outputDir, videos, candidates, memory, runtimeEdges }, null, 2));
}
