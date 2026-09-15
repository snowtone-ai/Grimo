import fs from "node:fs/promises";
import { inspectGlb, isMain } from "./glb-metrics.mjs";

if (isMain(import.meta.url)) {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error("Usage: pnpm 3d:inspect -- path/to/model.glb");
    process.exitCode = 2;
  } else {
    try {
      await fs.access(inputPath);
      const report = await inspectGlb(inputPath);
      console.log(JSON.stringify({ file: report.file, metrics: report.metrics }, null, 2));
    } catch (error) {
      console.error(`GLB inspection failed: ${error instanceof Error ? error.message : String(error)}`);
      process.exitCode = 1;
    }
  }
}
