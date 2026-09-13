import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";

const baseUrl = process.env.GRIMO_QA_BASE_URL ?? "http://127.0.0.1:3000";
const sampleDurationMs = Number(process.env.GRIMO_QA_SAMPLE_MS ?? 30_000);
const stabilityDurationMs = Number(process.env.GRIMO_QA_STABILITY_MS ?? 300_000);
const outputDir = resolve(process.env.GRIMO_QA_OUTPUT ?? "artifacts/grimo-qa/gate-1");

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: process.env.GRIMO_QA_BROWSER_CHANNEL ?? "chrome" });
const errors = [];
const failedRequests = [];

async function makePage(viewport, options = {}) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: options.deviceScaleFactor ?? 1,
    reducedMotion: options.reducedMotion ?? "no-preference",
  });
  const page = await context.newPage();
  page.on("console", (message) => {
    if (message.type() === "error") errors.push({ viewport, text: message.text() });
  });
  page.on("pageerror", (error) => errors.push({ viewport, text: error.message }));
  page.on("requestfailed", (request) => failedRequests.push({ url: request.url(), error: request.failure()?.errorText ?? "unknown" }));
  page.on("response", (response) => {
    if (response.status() >= 400) failedRequests.push({ url: response.url(), error: `HTTP ${response.status()}` });
  });
  return { context, page };
}

async function openRuntime(page, query = "") {
  await page.goto(`${baseUrl}/grimo${query}`, { waitUntil: "networkidle" });
  await page.waitForFunction(() => Boolean(window.__GRIMO_QA__));
  await page.waitForTimeout(250);
}

async function capture(name, viewport, query, options = {}) {
  const { context, page } = await makePage(viewport, options);
  await openRuntime(page, query);
  await page.screenshot({ path: resolve(outputDir, `${name}.png`), fullPage: true });
  const evidence = await page.evaluate(() => {
    const viewport = document.querySelector(".carol-viewport")?.getBoundingClientRect();
    const nav = document.querySelector(".bottom-nav__inner")?.getBoundingClientRect();
    const canvas = document.querySelector("canvas");
    return {
      qa: window.__GRIMO_QA__.snapshot(),
      viewportBox: viewport ? { x: viewport.x, y: viewport.y, width: viewport.width, height: viewport.height } : null,
      navBox: nav ? { x: nav.x, y: nav.y, width: nav.width, height: nav.height } : null,
      canvasBackingSize: canvas ? { width: canvas.width, height: canvas.height } : null,
      documentOverflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    };
  });
  await context.close();
  return evidence;
}

const captures = {};
captures.pixel7aNeutral = await capture("pixel-7a-neutral", { width: 412, height: 915 }, "?motion=still", { deviceScaleFactor: 2.625 });
captures.pixel7aDeformed = await capture("pixel-7a-light-deformation", { width: 412, height: 915 }, "?motion=deformed", { deviceScaleFactor: 2.625 });
captures.narrow = await capture("narrow-360", { width: 360, height: 740 }, "?motion=still", { deviceScaleFactor: 2 });
captures.desktop = await capture("desktop-1280", { width: 1280, height: 900 }, "?motion=still", { deviceScaleFactor: 1 });
captures.reducedMotion = await capture("pixel-7a-reduced-motion", { width: 412, height: 915 }, "", { deviceScaleFactor: 2.625, reducedMotion: "reduce" });

const sampled = await makePage({ width: 412, height: 915 }, { deviceScaleFactor: 2.625 });
await openRuntime(sampled.page);
await sampled.page.waitForTimeout(sampleDurationMs);
captures.pixel7aIdleSample = await sampled.page.evaluate(() => window.__GRIMO_QA__.snapshot());

await sampled.page.evaluate(() => {
  const canvas = document.querySelector("canvas");
  canvas?.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, pointerId: 41, clientX: 206, clientY: 430 }));
  canvas?.dispatchEvent(new PointerEvent("pointercancel", { bubbles: true, pointerId: 41, clientX: 206, clientY: 430 }));
});
captures.pointerCancel = await sampled.page.evaluate(() => window.__GRIMO_QA__.snapshot());

const stabilityStartedAt = Date.now();
let remountCycles = 0;
while (Date.now() - stabilityStartedAt < stabilityDurationMs) {
  await sampled.page.getByRole("link", { name: "タスク" }).click();
  await sampled.page.waitForURL(`${baseUrl}/tasks`);
  await sampled.page.getByRole("link", { name: "グリモ" }).click();
  await sampled.page.waitForURL(`${baseUrl}/grimo`);
  await sampled.page.waitForFunction(() => Boolean(window.__GRIMO_QA__));
  remountCycles += 1;
  await sampled.page.waitForTimeout(1_000);
}
captures.stability = {
  requestedDurationMs: stabilityDurationMs,
  actualDurationMs: Date.now() - stabilityStartedAt,
  remountCycles,
  final: await sampled.page.evaluate(() => window.__GRIMO_QA__.snapshot()),
};
await sampled.context.close();

const report = {
  generatedAt: new Date().toISOString(),
  baseUrl,
  sampleDurationMs,
  captures,
  consoleErrors: errors,
  failedRequests,
};
await writeFile(resolve(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();

const final = captures.stability.final;
if (errors.length || failedRequests.length || final.activeApplications !== 1 || final.mounts - final.destroys !== 1 || captures.pointerCancel.activePointers !== 0) {
  console.error(JSON.stringify({ errors, failedRequests, stability: captures.stability, pointerCancel: captures.pointerCancel }, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ outputDir, frameTime: captures.pixel7aIdleSample.frameTime, stability: captures.stability }, null, 2));
}
