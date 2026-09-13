import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";

const baseUrl = process.env.GRIMO_QA_BASE_URL ?? "http://127.0.0.1:3000";
const captureDurationMs = Number(process.env.GRIMO_QA_SAMPLE_MS ?? 20_000);
const outputDir = resolve(process.env.GRIMO_QA_OUTPUT ?? "artifacts/grimo-qa/gate-2");
const viewport = { width: 412, height: 915 };

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true, ...(process.env.GRIMO_QA_BROWSER_CHANNEL ? { channel: process.env.GRIMO_QA_BROWSER_CHANNEL } : {}) });
const consoleErrors = [];
const failedRequests = [];

async function captureCandidate(id) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 2.625 });
  const page = await context.newPage();
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push({ id, text: message.text() });
  });
  page.on("pageerror", (error) => consoleErrors.push({ id, text: error.message }));
  page.on("requestfailed", (request) => failedRequests.push({ id, url: request.url(), error: request.failure()?.errorText ?? "unknown" }));
  await page.goto(`${baseUrl}/grimo/human-gate-2?idleVariant=${id}`, { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => Boolean(window.__GRIMO_QA__));
  await page.waitForTimeout(captureDurationMs);
  await page.screenshot({ path: resolve(outputDir, `pixel-7a-${id}.png`), fullPage: true });
  const qa = await page.evaluate(() => window.__GRIMO_QA__.snapshot());
  await context.close();
  return qa;
}

const candidates = {};
for (const id of ["A", "B", "C"]) candidates[id] = await captureCandidate(id);
const report = { generatedAt: new Date().toISOString(), baseUrl, viewport, captureDurationMs, candidates, consoleErrors, failedRequests };
await writeFile(resolve(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
await browser.close();

if (consoleErrors.length || failedRequests.length || Object.values(candidates).some((candidate) => candidate.activeApplications !== 1)) {
  console.error(JSON.stringify(report, null, 2));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ outputDir, candidates }, null, 2));
}
