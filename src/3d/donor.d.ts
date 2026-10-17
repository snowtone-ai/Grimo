declare module "*.mjs" {
  import type * as pc from "playcanvas";
  export function loadShushuCandidate(options: {
    pc: typeof pc; app: pc.Application; url: string; signal: AbortSignal;
    readAsset: (url: string) => Promise<ArrayBuffer>;
    equipmentOptions: { flowerUrl: string; padsUrl: string; signal: AbortSignal; readAsset: (url: string) => Promise<ArrayBuffer> };
  }): Promise<{
    entity: pc.Entity; equipment: { enabled: boolean; flower: pc.Entity };
    dispose(): void;
  }>;
}
