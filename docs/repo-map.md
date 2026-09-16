# Repository map

This map reflects the current Full-3D project structure. It separates stable Project Knowledge, active production memory/evidence, source authority, generated production assets, and application/runtime code.

## Project authority and production map

| Path | Responsibility / authority |
|---|---|
| `docs/grimo/knowledge/CURRENT_PROJECT_MEMORY.md` | Compact latest durable project memory; first read for a new session/agent |
| `docs/grimo/knowledge/README.md` | Project Knowledge authority index and routing rules |
| `docs/grimo/knowledge/product/` | Authoritative product feature and logical data specifications |
| `docs/grimo/knowledge/character-experience/` | Authoritative living-companion experience / motion principles |
| `docs/grimo/knowledge/character-production/` | Generic Full-3D/Blender production authority and character-specific production specs |
| `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md` | Current Carol-specific motion implementation authority |
| `docs/grimo/knowledge/research/` | Research/evidence layer; does not silently override current production decisions |
| `docs/grimo/knowledge/research/motion-masters/` | Consolidated Pikachu/Eevee motion inventories used as evidence, not motions to copy |
| `docs/grimo/knowledge/research/camera-framing/` | Partner Eevee framing/camera benchmark for later presentation decisions |
| `docs/production/carol/` | Active Carol production contracts, state, Human Gate history and review records |
| `docs/production/carol/evidence/` | Versioned review packets and QA evidence; evidence is not approval |
| `assets/grimo/source/carol/carol-Identity-canonical.png` | Carol visible identity/color/motif/appeal authority |
| `assets/grimo/source/carol/approved-3d/authority.json` | Machine-readable Carol approved 3D geometry authority contract |
| `assets/grimo/source/carol/approved-3d/` | Approved geometry reference views; six individual views are highest concrete geometry authority |
| `assets/grimo/source/carol/historical/` | Recovered historical Carol source evidence; non-authoritative except where a specific experiment explicitly permits reuse |
| `assets/grimo/source/{jill,pino,shushu}/` | Current identity canonicals for the remaining Grimo characters |
| `assets/grimo/production/carol/blender/` | Carol Blender production/review assets; presence here does not imply Human approval |
| `assets/grimo/production/carol/manifests/` | Carol production manifests/metadata when created |
| `scripts/blender/` | Blender generation, review, render and inspection automation |
| `scripts/3d/` | GLB metrics, validation, review-packet and PlayCanvas verification utilities |
| `docs/archive/obsolete-2_5d/` | Historical PixiJS / 2D / 2.5D material; explicitly non-authoritative |

## Current Carol geometry sources

The six approved individual reference views under `assets/grimo/source/carol/approved-3d/` are:

```text
carol-front-ortho-transparent.png
carol-side-ortho-transparent.png
carol-back-ortho-transparent.png
carol-top-plan-transparent.png
carol-front-3q-left.png
carol-front-3q-right.png
```

They govern concrete volume/depth/proportion/part placement. `carol-3d-production-canonical-sheet.png` is supplementary. `carol-Identity-canonical.png` remains the identity/appeal authority and must not be used to flatten or otherwise overwrite depth established by the approved geometry views.

## Current Carol production branch

`codex/carol-zero-based-hero-geometry-v005`

Current comparison assets:

```text
assets/grimo/production/carol/blender/carol-a-v005.blend
assets/grimo/production/carol/blender/carol-b-v005.blend
assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb
docs/production/carol/evidence/hero-geometry-v005/
```

A and B are comparison experiments, **not approved hero geometry**. Human construction-direction review is pending.

## Application / web architecture

| Path | Responsibility |
|---|---|
| `src/app/` | Next.js routes, manifest, service worker and server routes |
| `src/components/app-shell/` | Mobile application shell and navigation |
| `src/domain/task/` | Pure task/date behavior |
| `src/domain/calendar/` | Calendar import validation/dedup planning |
| `src/domain/preferences/` | Startup-page preference contract |
| `src/data/db/` | Local persistence schema/types and compatibility stores |
| `src/data/repositories/` | Persistence operations |
| `src/data/backup/` | Legacy import / backup boundaries |
| `src/integrations/google/` | Google authorization, Gmail and Calendar integration |
| `src/integrations/gemini/` | Gemini prompt/server-client boundaries |
| `public/icons/` | Browser/PWA icon derivatives |
| `docs/setup/` | Local, frontend, 3D, Google Cloud, Vercel and model-policy setup |
| `tests/` | Domain / compatibility / visual tests |

## Separation rules

1. **Stable knowledge is not execution state.** Specs belong under `docs/grimo/knowledge/`; rapidly changing Carol gate truth belongs under `docs/production/carol/`.
2. **Evidence is not authority.** Screenshots, metrics, old binaries and generated models cannot self-promote into an approved canonical.
3. **Source authority is separate from outputs.** Canonical/approved references live under `assets/grimo/source/`; generated/working Blender assets live under `assets/grimo/production/`.
4. **Historical assets remain historical.** The recovered Carol source can be used only when an explicit current production experiment authorizes it; v005 B is such a limited exception.
5. **Do not infer current state from `main` alone.** Current Carol production work is ahead on the active v005 branch until an explicit Human-approved merge occurs.
