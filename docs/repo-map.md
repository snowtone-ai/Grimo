# Repository map

| Path | Responsibility |
|---|---|
| `src/app/` | Next.js routes, launch gate, manifest, service worker, server routes |
| `src/components/app-shell/` | Mobile shell and bottom navigation |
| `src/domain/task/` | Pure task date/recurrence/streak logic |
| `src/domain/calendar/` | Pure Calendar import validation/dedup planning |
| `src/domain/preferences/` | Startup-page preference contract |
| `src/data/db/` | Dexie schema and data types, including compatibility stores |
| `src/data/repositories/` | Persistence operations |
| `src/data/backup/` | Legacy import and future backup boundaries |
| `src/integrations/google/` | GIS token flow, Gmail and Calendar API clients |
| `src/integrations/gemini/` | Prompt and Gemini server client boundaries |
| `assets/grimo/source/` | Immutable character identity canonicals and app-icon source |
| `public/icons/` | Browser-ready icon derivatives; preserve byte-for-byte |
| `docs/archive/obsolete-2_5d/` | Historical 2D/2.5D source material, not current authority |
| `docs/setup/` | Local, Google Cloud, Vercel, and contributor setup notes |
| `tests/` | Pure-domain and compatibility tests |

The future Full 3D foundation may add a focused character/runtime structure in a later phase. Do not create empty runtime skeletons during Phase 0. Do not place generated QA captures or build output in tracked source paths.
