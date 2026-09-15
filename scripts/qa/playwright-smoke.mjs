import http from "node:http";
import { spawn, spawnSync } from "node:child_process";
import { chromium } from "@playwright/test";

const port = Number(process.env.PORT ?? 3187);
const baseUrl = process.env.BASE_URL ?? `http://127.0.0.1:${port}`;
let devServer;

function request(url) {
  return new Promise((resolve, reject) => {
    const request = http.get(url, (response) => {
      response.resume();
      resolve(response.statusCode ?? 0);
    });
    request.once("error", reject);
  });
}

async function waitForServer(url, timeoutMs = 60_000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const status = await request(url);
      if (status >= 200 && status < 500) return;
    } catch {
      // The dev server is still starting.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

function stopServer() {
  if (!devServer) return;
  if (process.platform === "win32" && devServer.pid) {
    spawnSync("taskkill", ["/pid", String(devServer.pid), "/t", "/f"], { stdio: "ignore", windowsHide: true });
  } else {
    devServer.kill();
  }
}

try {
  if (!process.env.BASE_URL) {
    const command = `pnpm dev --hostname 127.0.0.1 --port ${port}`;
    const executable = process.platform === "win32" ? "cmd.exe" : "pnpm";
    const args = process.platform === "win32"
      ? ["/d", "/s", "/c", command]
      : ["dev", "--hostname", "127.0.0.1", "--port", String(port)];
    devServer = spawn(executable, args, {
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });
    devServer.stderr.on("data", () => {});
    await waitForServer(`${baseUrl}/manifest.webmanifest`);
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 412, height: 915 },
    isMobile: true,
    hasTouch: true,
    deviceScaleFactor: 2,
    reducedMotion: "no-preference",
  });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("requestfailed", (request) => failedRequests.push(`${request.method()} ${request.url()}: ${request.failure()?.errorText ?? "failed"}`));

  for (const route of ["/", "/tasks", "/calendar", "/grimo", "/settings"]) {
    const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded", timeout: 60_000 });
    if (!response || response.status() >= 400) throw new Error(`${route} returned ${response?.status() ?? "no response"}`);
    await page.waitForTimeout(150);
  }
  const manifest = await page.request.get(`${baseUrl}/manifest.webmanifest`);
  if (!manifest.ok()) throw new Error(`manifest.webmanifest returned ${manifest.status()}`);

  await browser.close();
  if (consoleErrors.length || pageErrors.length || failedRequests.length) {
    console.error(JSON.stringify({ consoleErrors, pageErrors, failedRequests }, null, 2));
    process.exitCode = 1;
  } else {
    console.log(`Playwright mobile smoke: PASS (${baseUrl}; routes, manifest, no console/runtime/network errors)`);
  }
} finally {
  stopServer();
}
