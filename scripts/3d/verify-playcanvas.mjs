import fs from "node:fs";
import path from "node:path";
function readPackage(packageName) {
  const packageJson = path.join(process.cwd(), "node_modules", ...packageName.split("/"), "package.json");
  if (!fs.existsSync(packageJson)) throw new Error(`Cannot locate package metadata for ${packageName}`);
  return JSON.parse(fs.readFileSync(packageJson, "utf8"));
}

const packages = ["playcanvas", "@playcanvas/react", "sync-ammo"];

for (const packageName of packages) {
  console.log(`${packageName}@${readPackage(packageName).version}`);
}

const engine = await import("playcanvas");
await import("@playcanvas/react");
await import("sync-ammo");
console.log(`playcanvas import: PASS (${Object.keys(engine).length} exports)`);
console.log("PlayCanvas React and sync-ammo imports: PASS");
