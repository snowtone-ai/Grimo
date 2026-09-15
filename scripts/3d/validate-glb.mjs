import fs from "node:fs/promises";
import { inspectGlb, isMain } from "./glb-metrics.mjs";

if (isMain(import.meta.url)) {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error("Usage: pnpm 3d:validate -- path/to/model.glb");
    process.exitCode = 2;
  } else {
    try {
      await fs.access(inputPath);
      const report = await inspectGlb(inputPath);
      console.log(JSON.stringify(report, null, 2));
      if (report.validator.errors > 0) process.exitCode = 1;
    } catch (error) {
      console.error(`GLB validation failed: ${error instanceof Error ? error.message : String(error)}`);
      process.exitCode = 1;
    }
  }
}
