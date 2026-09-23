# Grimo 3D Toolchain

Status: bootstrap baseline verified 2026-09-15 (Asia/Tokyo)

This document records the reproducible toolchain for Grimo's current Full-Spatial 3D implementation hypothesis. It is an implementation/tooling guide, not architecture or production-order authority.

## Source of truth and non-negotiables

The source of truth is Git repository content, Blender source assets, exported GLB/glTF, and TypeScript runtime code. PlayCanvas Editor is an authoring, inspection, preview, and QA surface; it is not the repository's new source of truth.

The current implementation hypothesis is:

`Blender -> GLB/glTF -> PlayCanvas -> Next.js/React smartphone-first PWA`

It remains subordinate to the Product North Star and may change only through evidence-driven Architecture Review.

Carol is the first vertical slice. This bootstrap does not create a Carol mesh, rig, animation, or runtime fixture. It preserves the existing Task/Calendar semantics, Dexie compatibility, PWA/service worker, Google read-only boundary, server-only Gemini secret handling, app icon, and canonical character identities.

Physics is reserved for props, collision, joints, environment interaction, bounded residual secondary motion, and Secret Motion. It must not decide Carol's hero acting, facial acting, primary touch reaction, main body acting, or primary fleece performance.

## Verified versions

| Tool | Version / pin | Status | Purpose | Verification |
| --- | --- | --- | --- | --- |
| Node.js | 24.14.0 (`24.x`) | Existing | Next.js and scripts | `node --version` |
| pnpm | 12.3.4 | Existing | Package manager | `pnpm --version` |
| Git | 2.54.0.windows.1 | Existing | Repository source control | `git --version` |
| Git LFS | 3.7.1 | Existing | Large source/runtime asset storage | `git lfs version` |
| Python | 3.13.14 | Existing | Blender/utility scripting | `python --version` |
| uv | 0.11.15 | Existing | Official Blender MCP server runner | `uv --version` |
| FFmpeg | N-125875-g5d4d3bdc61-win64-gpl | Existing | Future media/QA utilities | `ffmpeg -version` |
| Blender | 5.2.1 LTS | Existing and verified | Blender-centered production and headless automation | `blender --version` |
| Blender Lab MCP add-on | 1.0.3 | Installed and enabled | Local Blender TCP bridge | `blender --command extension list` |
| Blender Lab MCP server | Official repository commit `ff54e4d8f6b09502f2f466189cca0e52b4a91643` | Codex-registered | MCP stdio server; launched with `uvx` | `codex mcp get blender` |
| CloudRig | 2.2.29 | Installed and enabled | `Carol Rig Prototype A` comparison path | `blender --command extension list` |
| EasyWeight | 1.1.3 | Installed and enabled | Weight painting and cleanup | `blender --command extension list` |
| Pose Shape Keys | 1.1.1 | Installed and enabled | Corrective/facial/fleece deformation | `blender --command extension list` |
| PlayCanvas Engine | 2.22.2 | Exact project dependency | Runtime renderer/animation/camera | `pnpm 3d:playcanvas` |
| `@playcanvas/react` | 0.11.5 | Exact project dependency | React integration surface | `pnpm 3d:playcanvas` |
| `sync-ammo` | 0.1.2 | Exact project dependency | PlayCanvas Ammo/Bullet integration helper | package resolution in `pnpm 3d:playcanvas` |
| `@gltf-transform/cli` | 4.5.0 | Exact dev dependency | GLB/glTF optimization/inspection foundation | `pnpm exec gltf-transform --version` |
| `@gltf-transform/core` | 4.5.0 | Exact dev dependency | Deterministic GLB metrics reader | `pnpm 3d:inspect -- <file.glb>` |
| Khronos `gltf-validator` | 2.0.0-dev.3.10 | Official current package; no stable release is published for this validator | Structural/accessor/animation validation | `pnpm 3d:validate -- <file.glb>` |
| KTX-Software | 4.4.2 stable | Installed, on PATH, and verified (`ktx`, `toktx`, `ktx2check`) | Future Basis/KTX2/ASTC/ETC2 texture pipeline | `ktx --version` |
| Playwright | 1.63.0 | Existing project dependency and browser cache verified | Mobile user-flow smoke | `pnpm qa:browser:smoke` |
| Lighthouse CI | 0.15.1 | Exact dev dependency | PWA shell/startup/network/Core Web Vitals | `pnpm exec lhci --help` |
| Sentry Next.js | 10.74.0 | Exact dev dependency; disabled by default | Env-driven future monitoring | `SENTRY_DSN` / `NEXT_PUBLIC_SENTRY_DSN` |
| Android Platform Tools | 37.0.1 | Existing and verified | Xiaomi 14T Pro real-device QA; Pixel 7a-class compatibility target | `adb version` |
| PlayCanvas Editor MCP | 0.7.1 | Codex-registered | Editor inspection/preview/QA bridge | `codex mcp get playcanvas` |
| PlayCanvas official Skills | marketplace `playcanvas`, plugin `engine` 0.3.0 | Installed and enabled | Official agent guidance for PlayCanvas workflows | `codex plugin list` |

Version policy: the Blender/PlayCanvas/physics/MCP/rig versions above are pinned. Automatic upgrades are prohibited. Upgrade on a branch, run repository checks, run GLB validation, perform Carol visual regression once Carol exists, pass the Human Gate, then merge deliberately.

## Blender and official Blender Lab MCP

The only Blender MCP used by this repository is the official Blender Lab server and add-on:

- Add-on source/release: [Blender Lab MCP server](https://www.blender.org/lab/mcp-server/), extension repository `https://lab.blender.org/`, add-on 1.0.3.
- Server source: `https://projects.blender.org/lab/blender_mcp.git`, pinned to commit `ff54e4d8f6b09502f2f466189cca0e52b4a91643`, `mcp` subdirectory, package `blender-mcp` 1.0.2.
- Codex registration: `blender` -> `cmd /c uvx --from git+https://projects.blender.org/lab/blender_mcp.git@ff54e4d8f6b09502f2f466189cca0e52b4a91643#subdirectory=mcp blender-mcp`.
- Environment: `BLENDER_MCP_HOST=localhost`, `BLENDER_MCP_PORT=9876`, and the verified Blender executable path.
- Blender user online access was enabled only so the official extension repository could synchronize. The add-on is configured for localhost and the default port 9876.

The server can execute Python in the connected Blender instance. Treat this as privileged local actuation:

- Keep it localhost-only.
- Inspect before modifying; use temporary, named objects for probes.
- Do not read `.env` files, credentials, browser profiles, or unrelated files.
- Do not download external assets or call external generation services.
- Do not overwrite or delete canonical assets.
- Keep repeatable work in version-controlled `scripts/blender/` and background CLI runs.

The verified probe read the default scene, executed `import bpy`, created `GRIMO_MCP_TEMP`, and deleted it. No `.blend` file was opened or saved.

## PlayCanvas

The runtime dependencies are exact-pinned in `package.json`. Do not introduce or switch a primary renderer/physics backend opportunistically inside a bounded implementation task. The current runtime hypothesis is PlayCanvas with the existing physics boundary; an alternative renderer/runtime may be considered only through Architecture Review when final-use evidence justifies it.

The official PlayCanvas Skills are installed from the current [PlayCanvas Skills repository](https://github.com/playcanvas/skills) using the current Codex plugin path:

```powershell
codex plugin marketplace add playcanvas/skills
codex plugin add engine@playcanvas
```

This provides the official `build-app`, `apply-conventions`, `find-examples`, `reuse-scripts`, `inspect-glb`, `calibrate-model`, `configure-animation`, `assemble-scene`, `manage-game-state`, `light-scene`, `add-effects`, and `build-hud` skills. The older `npx skills add playcanvas/skills` path is not used because the official repository now documents the Codex plugin marketplace integration.

The Editor MCP is registered as `playcanvas` with the official `@playcanvas/editor-mcp-server` package. The Editor-side connection is intentionally separate from code-first runtime source control. It requires a user-opened PlayCanvas Editor project and the Editor MCP connection control; see Human action below.

## GLB export and manifest contract

Future Carol exports are separate artifacts:

```text
carol.raw.glb
carol.runtime.glb
carol.manifest.json
```

The manifest foundation reserves these fields:

```json
{
  "sourceBlend": "...",
  "sourceBlendHash": "sha256:...",
  "exportHash": "sha256:...",
  "blenderVersion": "5.2.1",
  "exportPresetVersion": "...",
  "triangleCount": 0,
  "vertexCount": 0,
  "materialCount": 0,
  "textureCount": 0,
  "deformBoneCount": 0,
  "morphTargetCount": 0,
  "animationClips": [],
  "semanticBoneMapVersion": "...",
  "touchZoneMapVersion": "...",
  "generatedAt": "..."
}
```

`pnpm 3d:validate -- path/to/model.glb` reports validator errors/warnings plus file size, triangles, vertices, materials, textures, bones, morph targets, and animation names. `pnpm 3d:inspect -- path/to/model.glb` reports only metrics. CI uses `pnpm 3d:validate:ci`; it skips cleanly while the repository has no GLB/glTF asset and validates every asset once one is added.

## Texture pipeline

The source texture remains lossless. KTX-Software 4.4.2 is the selected stable Windows x64 baseline for a future Basis/KTX2 pipeline and ASTC/ETC2 target packaging. No texture was converted during bootstrap. Runtime conversion must be a separate reproducible step with platform targets, source hashes, quality settings, and visual regression evidence.

## Git LFS policy

`.gitattributes` tracks `*.blend`, `*.glb`, `*.gltf`, `*.ktx2`, `*.exr`, `*.mp4`, and `*.mov` through Git LFS. Existing canonical PNG files were not moved to LFS. Add binary assets deliberately and keep source/runtime variants separate.

## Sentry policy

`src/instrumentation-client.ts` initializes Sentry only when `NEXT_PUBLIC_SENTRY_DSN` exists. `src/instrumentation.ts` initializes server-side Sentry only when `SENTRY_DSN` exists. With neither environment variable present, the application is disabled-by-default and no account login or DSN was created.

## Reproduction and diagnostics

The diagnostic and QA commands below are available tools, not a checklist to
run in every task. For a changed/exported GLB, use targeted validation once;
reserve inspection, PlayCanvas, browser/mobile, and full scans for an explicit
milestone, release/Human Gate, or concrete regression risk.

```powershell
pnpm install --frozen-lockfile
pnpm 3d:doctor
pnpm 3d:playcanvas
pnpm 3d:blender:doctor
pnpm 3d:validate:ci
pnpm qa:browser:smoke
pnpm exec lhci --help
```

Run `pnpm qa:lighthouse` against a running production server on port 3000. For another local port, set `LHCI_URL`; set `CHROME_PATH` only when Lighthouse needs an explicit Chrome executable.

`pnpm 3d:doctor` distinguishes installed/registered checks from runtime connections. Blender MCP runtime is `localhost:9876`; PlayCanvas Editor runtime is the Editor connection port `localhost:52000`. A missing adb device, KTX executable, Context7 registration, or Editor login is a warning rather than a reason to change the repository's source-of-truth architecture.

## Human action

The previously required one-time external actions are complete: KTX-Software 4.4.2 is installed and verified, the Xiaomi 14T Pro is connected over adb, and the Grimo PlayCanvas Editor session is connected and read-only verified. No texture conversion is required yet. Xiaomi 14T Pro is the currently available real-device QA source. Pixel 7a-class is the lower-performance compatibility/design target and remains `UNVERIFIED_TARGET`; do not require or claim Pixel 7a real-device PASS without actual target-class validation.
