// Immutable donor revision; no build-time LFS download or credentials required.
export const donorRevision = "c5bed8b7cf0e7963388f9d20699fedd2c08c2c44";
const base = `https://media.githubusercontent.com/media/snowtone-ai/Grimo/${donorRevision}/assets/grimo/production/shushu/`;
export const shushuAssets = {
  body: { url: base + "tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004.glb", bytes: 62567088, sha256: "a082195104713c21b9a219ff19bd9d37702486aaa4cdf2bbf2e9f0ad58b5c91f", glb: true },
  flower: { url: base + "equipment/standard-v002/shushu-head-flower-v002.glb", bytes: 1279984, sha256: "ed474a714105d9a8a853d5caf1db0268acb86890589d3354e322bd9351490e41", glb: true },
  pads: { url: base.replace("media.githubusercontent.com/media/", "raw.githubusercontent.com/") + "equipment/standard-v001/shushu-hind-sole-pads-v001.png", bytes: 2582567, sha256: "f5c4aa2969b9b4971e3926dfede7c56cc8211091b9c074a9c67bb0738a2f21fe", glb: false },
} as const;

export async function readShushuAsset(url: string, signal: AbortSignal, report: (text: string) => void) {
  const asset = Object.values(shushuAssets).find(asset => asset.url === url);
  if (!asset) throw new Error("Unknown Shushu asset");
  const start = performance.now();
  report("シュシュを読み込んでいます…");
  const response = await fetch(url, { signal });
  if (!response.ok) throw new Error(`Asset HTTP ${response.status}`);
  const bytes = await response.arrayBuffer();
  const downloaded = performance.now();
  if (bytes.byteLength !== asset.bytes) throw new Error("Incomplete Shushu asset / LFS pointer");
  if (asset.glb) {
    const header = new DataView(bytes);
    if (header.getUint32(0, true) !== 0x46546c67 || header.getUint32(4, true) !== 2 || header.getUint32(8, true) !== bytes.byteLength) throw new Error("Invalid GLB");
  }
  const digest = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)), value => value.toString(16).padStart(2, "0")).join("");
  signal.throwIfAborted();
  if (digest !== asset.sha256) throw new Error("Shushu SHA256 mismatch");
  performance.measure(`shushu:download:${asset.sha256.slice(0, 8)}`, { start, end: downloaded });
  performance.measure(`shushu:verify:${asset.sha256.slice(0, 8)}`, { start: downloaded, end: performance.now() });
  report("シュシュの表示を準備しています…");
  return bytes;
}
