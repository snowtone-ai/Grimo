# Repository map

This map is durable routing. Mutable branch/HEAD/candidate/attempt/blocker/
Human-Gate/next-handoff facts belong only to
`docs/production/carol/CAROL_PRODUCTION_STATE.md`.

## Authority / production routing

| Path | Responsibility |
|---|---|
| `AGENTS.md` | Minimum repository operating rules |
| `.codex/config.toml` | Repository invariant only; task tooling is selected per Decision Question |
| `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md` | Durable authority routing |
| `docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md` | Highest durable product/quality authority |
| `docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md` | What the companion must feel like |
| `docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md` | Current falsifiable production architecture |
| `docs/grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md` | Planner / Codex / Human + Goal-Backward Spiral |
| `docs/grimo/knowledge/product/` | Product feature and data contracts |
| `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md` | Carol motion/behavior vocabulary |
| `docs/grimo/knowledge/character-production/GRIMO_BLENDER_IMPLEMENTATION_GUIDE.md` | Blender technique only |
| `docs/grimo/knowledge/research/` | Reference evidence / superseded pointers, not automatic authority |
| `docs/production/carol/CAROL_PRODUCTION_STATE.md` | Single mutable current Carol truth |
| `docs/production/carol/evidence/` | Versioned evidence/history; evidence is not approval |
| `assets/grimo/source/carol/approved-3d/authority.json` | Machine-readable Carol authority roles |
| `assets/grimo/production/carol/blender/` | Working/generated assets; presence is not approval |
| `scripts/blender/` | Production and historical version-specific Blender utilities |
| `scripts/3d/` | Opt-in GLB/runtime diagnostic utilities |
| `docs/archive/` | Historical/non-authoritative material |
| `src/` | Next.js application/runtime code |

## Carol routing

```text
canonical identity
↓
Normal Front / Normal Side
↓
full-spatial Carol exterior
├─ HERO_PRIORITY
├─ GENERAL_EXTERIOR
└─ MOTION_CRITICAL
↓
Skin Front / Skin Side / CAROL_GEOMETRY_PARAMETERS.md
↓
FUNCTIONAL_HIDDEN implementation
```

One coherent full-spatial Carol is required; one continuous mesh is not. Front
receives the highest polish, but practical 3/4 / Side / Rear / derived Top
exposure must remain structurally coherent. Back/Top/3Q remain derived
diagnostics rather than independent fitting authorities.

## Application map

- `src/app/` — Next.js routes, manifest, service worker, server routes
- `src/components/app-shell/` — mobile shell/navigation
- `src/domain/` — task/calendar/preference behavior
- `src/data/` — local persistence/backup boundaries
- `src/integrations/` — Google/Gemini boundaries
- `public/` — PWA assets
- `tests/` — domain/compatibility/visual tests
