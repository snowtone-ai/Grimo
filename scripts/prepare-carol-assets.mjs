import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { dirname, resolve } from "node:path";

const source = resolve("assets/grimo/source/carol/canonical.png");
const derivedManifest = resolve("assets/grimo/derived/carol/runtime-manifest.json");
const runtimeImage = resolve("public/grimo/carol/canonical.png");

const sourceBytes = await readFile(source);
const sha256 = createHash("sha256").update(sourceBytes).digest("hex");

await mkdir(dirname(derivedManifest), { recursive: true });
await mkdir(dirname(runtimeImage), { recursive: true });
await copyFile(source, runtimeImage);

const manifest = {
  schemaVersion: 1,
  character: "carol",
  identityAuthority: "assets/grimo/source/carol/canonical.png",
  sourceSha256: sha256,
  sourceSize: { width: 768, height: 493 },
  alphaBounds: { x: 97, y: 7, width: 640, height: 485 },
  runtimeTexture: "/grimo/carol/canonical.png",
  runtimeLayers: [
    "environment-back",
    "ground-shadow",
    "canonical-mesh",
    "semantic-hit-overlay-dev",
  ],
  note: "The canonical pixels remain unchanged. PixiJS derives mesh and semantic layers at runtime; generated references are not runtime identity sources.",
};

await writeFile(derivedManifest, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(`Carol runtime asset prepared (${sha256.slice(0, 12)}…).`);
