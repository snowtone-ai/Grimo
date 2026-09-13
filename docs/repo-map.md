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
| `src/grimo/` | PixiJS runtime/interaction/motion/rendering modules; implementation follows vertical slice |
| `assets/grimo/source/` | Canonical identity sources; never auto-overwrite |
| `docs/product/source-pack/` | Current Grimo product source documents |
| `tests/` | Pure-domain and compatibility tests |

Do not place generated QA captures or build output in tracked source paths.
