import fs from "node:fs";
import { spawnSync } from "node:child_process";

const candidates = [
  process.env.BLENDER_PATH,
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\Blender.exe",
  "C:\\Program Files\\Blender Foundation\\Blender\\Blender.exe",
].filter(Boolean);

const executable = candidates.find((candidate) => fs.existsSync(candidate)) ?? "blender";
const result = spawnSync(executable, ["--background", "--python", "scripts/blender/doctor_scene.py"], {
  cwd: process.cwd(),
  stdio: "inherit",
  windowsHide: true,
});

if (result.error) {
  console.error(`Unable to execute Blender: ${result.error.message}`);
  process.exitCode = 1;
} else {
  process.exitCode = result.status ?? 1;
}
