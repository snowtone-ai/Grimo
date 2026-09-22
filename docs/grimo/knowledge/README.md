# Grimo knowledge authority index

This directory contains durable product, architecture, and routing knowledge.
Mutable Carol execution truth is kept under `docs/production/carol/`.

Start new work with:

1. `CURRENT_PROJECT_MEMORY.md` — durable decisions and mandatory routing
2. the task-specific authority below
3. `docs/production/carol/CAROL_PRODUCTION_STATE.md` for current Carol state

## Stable product authority

| Domain | Authority |
|---|---|
| Product behavior / reward / Collection | `product/GRIMO_PRODUCT_FEATURE_SPEC.md` |
| Logical data model | `product/GRIMO_DATA_MODEL_SPEC.md` |
| Living-companion motion / interaction | `character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md` |
| Generic Full-3D / Blender production | `character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md` |
| Carol-specific motion | `character-production/carol/CAROL_MVP_MOTION_SPEC.md` |

## Carol geometry authority

Use these as the formal authority:

- `assets/grimo/source/carol/approved-3d/authority.json`
- `docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`

The authority is **4 FINAL / LOCKED Front/Side + Skin Front/Side → one model →
derived Back/Top/3Q**. Derived views are validation evidence, not independent
fitting targets. The identity canonical remains a secondary identity/appeal
reference and cannot override the formal geometry package.

## Production routing

- Current mutable Carol state: `docs/production/carol/CAROL_PRODUCTION_STATE.md`
- Current-version evidence: follow the evidence path named by that state file.
- Stable geometry rules: `CAROL_MODELING_CONTRACT.md` and
  `CAROL_GEOMETRY_DECISION.md`.
- Review history: `CAROL_REVIEW_LOG.md`.
- Research and archive material are non-authoritative unless a current task
  explicitly makes them relevant.

Do not infer candidate, branch, HEAD, or Human Gate status from this index.
