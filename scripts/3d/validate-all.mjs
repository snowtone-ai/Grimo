import fs from "node:fs/promises";
import path from "node:path";
import { inspectGlb } from "./glb-metrics.mjs";

const root = process.cwd();
const ignored = new Set([".git", "node_modules", ".next", "coverage"]);

async function findAssets(directory) {
  const entries = await fs.readdir(directory, { withFileTypes: true });
  const assets = [];
  for (const entry of entries) {
    if (entry.name.startsWith(".") && entry.name !== ".well-known") continue;
    if (entry.isDirectory()) {
      if (ignored.has(entry.name)) continue;
      assets.push(...await findAssets(path.join(directory, entry.name)));
    } else if (/\.(glb|gltf)$/i.test(entry.name)) {
      assets.push(path.join(directory, entry.name));
    }
  }
  return assets;
}

const assets = await findAssets(root);
if (assets.length === 0) {
  console.log("GLB validation skipped: no .glb or .gltf assets are present.");
  process.exit(0);
}

let failures = 0;
for (const asset of assets) {
  try {
    const report = await inspectGlb(asset);
    console.log(`${path.relative(root, asset)}: ${report.validator.errors} errors, ${report.validator.warnings} warnings`);
    if (report.validator.errors > 0) failures += 1;
  } catch (error) {
    failures += 1;
    console.error(`${path.relative(root, asset)}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

if (failures > 0) process.exitCode = 1;
