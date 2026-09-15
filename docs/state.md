# Production state

As of 2026-09-15, `snowtone-ai/Grimo` has a clean main foundation for Task, Calendar, Google read-only access, server-only Gemini requests, and the Serwist PWA shell. The active Phase 0 branch is preparing that foundation for a future Full 3D character rebuild.

The authoritative character direction is Blender-authored Full 3D shipped as GLB/glTF and rendered by a future PlayCanvas runtime. No 3D runtime, model, motion system, or touch interaction is implemented in Phase 0. `/grimo` is intentionally a neutral placeholder.

Carol, Jill, Pino, and Shushu canonical identity images and the current Grimo app icon are preserved. Old 2D/2.5D implementation references and QA material are not active production assets; historical source documents are isolated under `docs/archive/obsolete-2_5d/`.

## 3D environment state

The reproducible environment bootstrap is recorded in `docs/setup/3D_TOOLCHAIN.md`. Blender 5.2.1 LTS and the official Blender Lab MCP bridge are installed; the localhost MCP bridge was live-tested with a disposable object. PlayCanvas Engine/React, `sync-ammo`, GLB Transform/Validator, Lighthouse CI, Sentry (disabled without DSN), and Playwright are exact-pinned in `package.json`. Official PlayCanvas Skills and Editor MCP are registered.

The repository currently contains no production GLB, glTF, or Blender source asset, by design. GLB CI validation skips cleanly until an asset is added. Android Platform Tools are installed and Xiaomi 14T Pro is connected as the real-device QA target; Pixel 7a-class remains the minimum device acceptance baseline. KTX-Software 4.4.2 is installed, on PATH, and its `ktx`, `toktx`, and `ktx2check` executables report v4.4.2. PlayCanvas Editor MCP is registered and the Grimo / Untitled Editor session has been connected and read-only verified.

Carol production infrastructure and partial authoritative source ingestion are staged under `docs/production/carol/`, `docs/grimo/knowledge/`, and `assets/grimo/source/carol/approved-3d/`; no modeling has started. The existing canonical Carol image remains the visible-identity authority, and the approved 3D packet is recorded by `assets/grimo/source/carol/approved-3d/authority.json`. One pre-existing Eevee Motion Master destination conflict remains unresolved, so source ingestion and the next geometry interpretation are not yet ready to start.

Lighthouse CI direct collection completed an audit successfully. On this Windows host, the full local autorun may exit during `chrome-launcher` temporary-profile cleanup with `EPERM`; this is recorded as a tooling limitation, not an application audit failure.

## Frontend production and QA state

The repository now has an exact-pinned Storybook 10.6.0 / `@storybook/nextjs-vite` 10.6.0 environment for isolated component preview, Storybook MCP discovery, Vitest browser interaction tests, and addon-a11y checks. Motion 13.3.0 is the only new production UI runtime dependency and is reserved for DOM/React animation; PlayCanvas remains responsible for 3D animation. Radix is policy-only until a concrete accessible behavior primitive is needed.

The Playwright foundation covers `/`, `/tasks`, `/calendar`, `/grimo`, and `/settings` with Pixel 7a-like and Xiaomi 14T Pro-like viewport profiles. Screenshot baselines are intentionally opt-in until product UI stabilizes. A viewport profile is not physical-device verification; Xiaomi 14T Pro is the available real-device QA target and Pixel 7a is a performance/viewport target only. See `docs/setup/FRONTEND_TOOLCHAIN.md` for commands and upgrade policy.
