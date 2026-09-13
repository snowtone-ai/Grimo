# Repository map

| Path | Responsibility |
|---|---|
| `src/app/` | Next.js routes, launch gate, manifest, service worker, server routes |
| `src/components/app-shell/` | Mobile shell and bottom navigation |
| `src/domain/task/` | Pure task date/recurrence/streak logic |
| `src/domain/calendar/` | Pure Calendar import validation/dedup planning |
| `src/domain/preferences/` | Startup-page preference contract |
| `src/data/db/` | Dexie schema and data types |
| `src/data/repositories/` | Persistence operations |
| `src/data/backup/` | Legacy import and future backup boundaries |
| `src/integrations/google/` | GIS token flow, Gmail and Calendar API clients |
| `src/integrations/gemini/` | Prompt and Gemini server client boundaries |
| `src/components/grimo/` | React-owned Grimo viewport hosts and accessible surrounding UI |
| `src/grimo/runtime/` | PixiJS application lifecycle, renderer loop, and local QA instrumentation |
| `src/grimo/interaction/` | Renderer-independent semantic zones and future gesture/state contracts |
| `src/grimo/motion/` | Typed character motion parameters and pure motion helpers |
| `assets/grimo/source/` | Canonical identity sources; never auto-overwrite |
| `assets/grimo/source/app-icon.png` | User-provided immutable PWA icon source; derived public sizes live under `public/icons/` |
| `assets/grimo/derived/` | Reproducible runtime manifests/derived working assets; never identity authority |
| `public/grimo/` | Browser-ready runtime copies generated from immutable source assets |
| `public/icons/` | Browser-ready PWA and Apple Touch icon sizes derived from the immutable app-icon source |
| `scripts/prepare-carol-assets.mjs` | Reproduces Carol Phase 1 runtime asset/manifest from canonical source |
| `docs/grimo/asset-generation-workflow.md` | On-demand, human-in-the-loop image-generation runbook |
| `docs/product/source-pack/` | Current Grimo product source documents |
| `tests/` | Pure-domain and compatibility tests |

Do not place generated QA captures or build output in tracked source paths.
