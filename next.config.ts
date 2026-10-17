import type { NextConfig } from "next";
import withSerwistInit from "@serwist/next";

const withSerwist = withSerwistInit({
  swSrc: "src/app/sw.ts",
  swDest: "public/sw.js",
  disable: process.env.NODE_ENV === "development",
  // Route entry owns 3D downloads, including when the PWA installs on Task.
  exclude: [({ asset, compilation }) => {
    for (const chunk of compilation.chunks) {
      if (!chunk.files.has(asset.name)) continue;
      for (const chunkModule of compilation.chunkGraph.getChunkModulesIterable(chunk)) {
        const resource = (chunkModule as { resource?: string }).resource ?? chunkModule.identifier();
        if (/[\\/]playcanvas[\\/]|[\\/]src[\\/]3d[\\/]|[\\/]shushu[\\/]runtime[\\/]/.test(resource)) return true;
      }
    }
    return false;
  }],
});

const nextConfig: NextConfig = {
  reactStrictMode: true,
};

export default withSerwist(nextConfig);
