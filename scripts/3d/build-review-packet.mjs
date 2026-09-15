import { mkdir, readdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const outputDir = path.join(root, "artifacts", "carol-review");
const required = [
  "assets/grimo/source/carol/carol-Identity-canonical.png",
  "docs/production/carol/CAROL_PRODUCTION_STATE.md",
  "docs/production/carol/CAROL_CAMERA_CONTRACT.md",
  "docs/production/carol/CAROL_MODELING_CONTRACT.md",
  "docs/production/carol/CAROL_GEOMETRY_DECISION.md",
  "docs/setup/CODEX_MODEL_POLICY.md",
];

async function exists(relativePath) {
  try { await stat(path.join(root, relativePath)); return true; } catch { return false; }
}

async function approvedReferences() {
  const directory = path.join(root, "assets/grimo/source/carol/approved-3d");
  const entries = await readdir(directory, { withFileTypes: true });
  return entries.filter((entry) => entry.isFile() && !entry.name.startsWith(".") && !entry.name.endsWith(".md"))
    .map((entry) => path.posix.join("assets/grimo/source/carol/approved-3d", entry.name)).sort();
}

const missing = [];
for (const relativePath of required) if (!(await exists(relativePath))) missing.push(relativePath);
if (!(await exists("assets/grimo/source/carol/approved-3d"))) missing.push("assets/grimo/source/carol/approved-3d/");
if (missing.length) {
  console.error(`Carol review packet cannot be built; missing required inputs:\n- ${missing.join("\n- ")}`);
  process.exit(1);
}

const files = [...required, ...(await approvedReferences())].sort();
const manifest = { schemaVersion: 1, purpose: "carol-geometry-review", files };
await mkdir(outputDir, { recursive: true });
await writeFile(path.join(outputDir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
await writeFile(path.join(outputDir, "README.md"), [
  "# Carol review packet",
  "",
  "Generated deterministically from the manifest below. Review inputs remain in their repository source paths.",
  "",
  ...files.map((file) => `- ${file}`),
  "",
].join("\n"), "utf8");
console.log(`Carol review packet manifest written: ${files.length} input(s)`);
