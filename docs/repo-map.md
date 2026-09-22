# Repository map

This map is durable routing. Mutable candidate, branch, HEAD, Human Gate,
blocker, and next-step facts belong only to
`docs/production/carol/CAROL_PRODUCTION_STATE.md`.

## Authority and production map

| Path | Responsibility |
|---|---|
| `AGENTS.md` | Repository guardrails and ChatGPT↔Codex handoff rules |
| `.codex/config.toml` | Repository-scoped Codex policy and current tool surface |
| `docs/grimo/knowledge/CURRENT_PROJECT_MEMORY.md` | Durable decisions and mandatory phase preflight |
| `docs/grimo/knowledge/README.md` | Knowledge authority index and routing |
| `docs/grimo/knowledge/product/` | Product and data specifications |
| `docs/grimo/knowledge/character-experience/` | Companion motion and interaction principles |
| `docs/grimo/knowledge/character-production/` | Full-3D/Blender and character production authority |
| `docs/grimo/knowledge/research/` | Research evidence, not automatic production authority |
| `docs/production/carol/CAROL_PRODUCTION_STATE.md` | Single mutable current Carol truth |
| `docs/production/carol/evidence/` | Versioned review evidence; evidence is not approval |
| `assets/grimo/source/carol/approved-3d/authority.json` | Machine-readable geometry authority |
| `assets/grimo/source/carol/approved-3d/` | Four locked references and supplementary derived-view evidence |
| `assets/grimo/production/carol/blender/` | Generated/working Blender assets; presence is not approval |
| `scripts/blender/` | Blender generation and review automation |
| `scripts/3d/` | 3D validation and review utilities |
| `src/` | Next.js application and domain/runtime code |
| `docs/archive/obsolete-2_5d/` | Historical, non-authoritative material |

## Carol geometry routing

```text
4 FINAL / LOCKED Front/Side + Skin Front/Side
+ CAROL_GEOMETRY_PARAMETERS.md
        ↓
one single 3D model
        ↓
derived Back / Top / 3Q
```

Use `authority.json` and `CAROL_GEOMETRY_PARAMETERS.md` for formal references.
Use `CAROL_PRODUCTION_STATE.md` for current execution truth. Do not infer
current status from this map, old prompts, historical branches, or generated
assets.

## Application map

- `src/app/` — Next.js routes, manifest, service worker, server routes
- `src/components/app-shell/` — mobile shell and navigation
- `src/domain/` — pure task, calendar, and preference behavior
- `src/data/` — local persistence and backup boundaries
- `src/integrations/` — Google and Gemini integration boundaries
- `public/` — PWA assets
- `tests/` — domain, compatibility, and visual tests
