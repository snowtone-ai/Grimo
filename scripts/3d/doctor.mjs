import fs from "node:fs";
import net from "node:net";
import path from "node:path";
import { spawnSync } from "node:child_process";

const root = process.cwd();
const blenderCandidates = [
  process.env.BLENDER_PATH,
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\Blender.exe",
].filter(Boolean);
const adbCandidates = [
  process.env.ADB_PATH,
  "C:\\Users\\chidj\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\\platform-tools\\adb.exe",
].filter(Boolean);
const ktxCandidates = [
  process.env.KTX_PATH,
  "C:\\Users\\chidj\\AppData\\Local\\GrimoToolchain\\ktx-4.4.2\\bin\\ktx.exe",
  "C:\\Program Files\\KTX-Software\\bin\\ktx.exe",
].filter(Boolean);
const results = [];

function run(executable, args = []) {
  const isWindowsPnpm = process.platform === "win32" && executable === "pnpm";
  const command = isWindowsPnpm ? "pnpm" : executable;
  const spawnArgs = isWindowsPnpm
    ? ["/d", "/s", "/c", [command, ...args].map((arg) => /[\s&]/.test(arg) ? `"${arg.replaceAll('"', '\\"')}"` : arg).join(" ")]
    : args;
  const result = spawnSync(isWindowsPnpm ? "cmd.exe" : command, spawnArgs, { cwd: root, encoding: "utf8", timeout: 30_000, windowsHide: true });
  return {
    ok: result.status === 0,
    output: `${result.stdout ?? ""}${result.stderr ?? ""}`.trim() || (result.error ? result.error.message : ""),
    status: result.status,
  };
}

function runPowerShell(command) {
  return run("powershell.exe", ["-NoProfile", "-NonInteractive", "-Command", command]);
}

function firstLine(value) {
  return value.split(/\r?\n/).find(Boolean) ?? "";
}

function findFile(candidates) {
  return candidates.find((candidate) => fs.existsSync(candidate));
}

function record(label, ok, detail, critical = false) {
  results.push({ label, ok, detail, critical });
  console.log(`${ok ? "[PASS]" : critical ? "[FAIL]" : "[WARN]"} ${label}: ${detail}`);
}

function packageVersion(packageName) {
  const file = path.join(root, "node_modules", ...packageName.split("/"), "package.json");
  if (!fs.existsSync(file)) return null;
  try {
    return JSON.parse(fs.readFileSync(file, "utf8")).version ?? null;
  } catch {
    return null;
  }
}

function packageSpec(packageName) {
  const packageJson = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
  return packageJson.dependencies?.[packageName] ?? packageJson.devDependencies?.[packageName] ?? null;
}

function probeTcp(host, port, timeoutMs = 800) {
  return new Promise((resolve) => {
    const socket = net.createConnection({ host, port });
    const finish = (connected) => {
      socket.destroy();
      resolve(connected);
    };
    socket.setTimeout(timeoutMs, () => finish(false));
    socket.once("connect", () => finish(true));
    socket.once("error", () => finish(false));
  });
}

function listAssets() {
  const assets = [];
  const ignored = new Set([".git", "node_modules", ".next", "coverage"]);
  function walk(directory) {
    if (!fs.existsSync(directory)) return;
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.name.startsWith(".") && entry.name !== ".well-known") continue;
      if (entry.isDirectory()) {
        if (!ignored.has(entry.name)) walk(path.join(directory, entry.name));
      } else if (/\.(blend|glb|gltf|ktx2|exr|mp4|mov)$/i.test(entry.name)) {
        assets.push(path.relative(root, path.join(directory, entry.name)));
      }
    }
  }
  walk(root);
  return assets;
}

record("Node", Number(process.versions.node.split(".")[0]) >= 24, process.version, true);
const pnpm = run("pnpm", ["--version"]);
record("pnpm", pnpm.ok, firstLine(pnpm.output), true);
const git = run("git", ["--version"]);
record("Git", git.ok, firstLine(git.output), true);
const lfs = run("git", ["lfs", "version"]);
record("Git LFS", lfs.ok, firstLine(lfs.output));
const python = run("python", ["--version"]);
record("Python", python.ok, firstLine(python.output));
const uv = run("uv", ["--version"]);
record("uv", uv.ok, firstLine(uv.output));
const ffmpeg = run("ffmpeg", ["-version"]);
record("FFmpeg", ffmpeg.ok, firstLine(ffmpeg.output));

const blender = findFile(blenderCandidates);
if (blender) {
  const version = run(blender, ["--version"]);
  record("Blender", version.ok, firstLine(version.output), true);
  const extensionList = run(blender, ["--command", "extension", "list"]);
  for (const extension of ["mcp", "cloudrig", "easyweight", "pose_shape_keys"]) {
    record(`Blender extension ${extension}`, extensionList.output.includes(`${extension} [installed]`), extensionList.output.includes(`${extension} [installed]`) ? "installed" : "not installed");
  }
  const background = run(blender, ["--background", "--python", "scripts/blender/doctor_scene.py"]);
  record("Blender background bpy", background.ok && background.output.includes("GRIMO_BLENDER_DOCTOR="), firstLine(background.output), true);
} else {
  record("Blender", false, "not found; set BLENDER_PATH or install Blender 5.2.1 LTS", true);
}

const adb = findFile(adbCandidates);
if (adb) {
  const version = run(adb, ["version"]);
  record("Android Platform Tools / adb", version.ok, firstLine(version.output));
  const devices = run(adb, ["devices", "-l"]);
  const connected = devices.output.split(/\r?\n/).some((line) => /^[^\s]+\s+device\b/.test(line));
  record("adb device", connected, connected ? "device connected" : "tool ready; no device attached");
} else {
  record("Android Platform Tools / adb", false, "not found; install official platform-tools", false);
}

const ktx = findFile(ktxCandidates);
if (ktx) {
  const version = run(ktx, ["--version"]);
  record("KTX-Software", version.ok, firstLine(version.output));
} else {
  record("KTX-Software", false, "stable 4.4.2 download is documented; executable is not installed on PATH", false);
}

for (const [name, critical] of [["playcanvas", true], ["@playcanvas/react", true], ["sync-ammo", true], ["@gltf-transform/cli", true], ["@gltf-transform/core", true], ["gltf-validator", true], ["@lhci/cli", false], ["@sentry/nextjs", false], ["@playwright/test", true]]) {
  const version = packageVersion(name);
  record(`Package ${name}`, Boolean(version), version ? `${version} (spec ${packageSpec(name)})` : "not installed", critical);
}

const playcanvasCheck = run(process.execPath, ["scripts/3d/verify-playcanvas.mjs"]);
record("PlayCanvas module import", playcanvasCheck.ok, firstLine(playcanvasCheck.output), true);
const gltfHelp = run("pnpm", ["exec", "gltf-transform", "--version"]);
record("glTF Transform CLI", gltfHelp.ok, firstLine(gltfHelp.output), true);
const playwrightBrowser = fs.existsSync(path.join(process.env.LOCALAPPDATA ?? "", "ms-playwright"));
record("Playwright Chromium cache", playwrightBrowser, playwrightBrowser ? "browser cache present" : "run pnpm exec playwright install chromium", true);

const pluginRoot = "C:\\Users\\chidj\\.codex\\plugins\\cache\\playcanvas\\engine\\0.3.0";
const skillRoot = path.join(pluginRoot, "skills");
const requiredSkills = ["build-app", "apply-conventions", "find-examples", "reuse-scripts", "inspect-glb", "calibrate-model", "configure-animation", "assemble-scene", "manage-game-state", "light-scene", "add-effects", "build-hud"];
const missingSkills = requiredSkills.filter((skill) => !fs.existsSync(path.join(skillRoot, skill)));
record("PlayCanvas official Skills", missingSkills.length === 0, missingSkills.length === 0 ? `${requiredSkills.length} required skills available` : `missing ${missingSkills.join(", ")}`);

const mcpNames = {};
for (const name of ["blender", "playcanvas", "chrome-devtools", "context7"]) {
  const result = runPowerShell(`codex mcp get ${name}`);
  mcpNames[name] = result.ok;
  record(`${name} MCP registration`, result.ok, result.ok ? "registered" : "not registered");
}
record("Blender MCP runtime", await probeTcp("localhost", 9876), "localhost:9876");
record("PlayCanvas Editor MCP runtime", await probeTcp("localhost", 52000), "Editor connection port localhost:52000; open Editor project and connect if unavailable");

const attributes = fs.existsSync(path.join(root, ".gitattributes"));
record("Git LFS policy", attributes, attributes ? ".gitattributes present" : "missing .gitattributes");
const assets = listAssets();
record("3D asset inventory", true, assets.length ? assets.join(", ") : "no production 3D assets; CI GLB validation will skip");

const criticalFailures = results.filter((result) => result.critical && !result.ok);
if (criticalFailures.length > 0) {
  console.error(`3D doctor failed: ${criticalFailures.length} critical check(s)`);
  process.exitCode = 1;
} else {
  console.log("3D doctor completed: core checks passed; warnings identify optional or externally connected surfaces.");
}
