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
| Product North Star / minimum quality | `research/GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md` |
| Product behavior / reward / Collection | `product/GRIMO_PRODUCT_FEATURE_SPEC.md` |
| Logical data model | `product/GRIMO_DATA_MODEL_SPEC.md` |
| Living-companion motion / interaction | `character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md` |
| Current 3D-first / Blender production technique | `character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md` |
| Carol-specific motion | `character-production/carol/CAROL_MVP_MOTION_SPEC.md` |

The technology-agnostic Product North Star outranks implementation purity.
Current architecture is the **Front-Optimized 3D-First Living Character**
baseline hypothesis. It may move to an evidence-driven hybrid through
Architecture Review. The Zero-Based Deep Research document is retained as
architecture-research provenance; its old “final” Full-3D recommendation and
strict gate-order/device wording do not override current durable memory.

## Device truth

- Available real-device QA: **Xiaomi 14T Pro**.
- **Pixel 7a-class**: lower-performance compatibility/design target.
- Pixel 7a real-device status: **UNVERIFIED_TARGET** until actual or sufficiently
  trustworthy target-class validation is available.

## Carol geometry authority

Use these as the formal geometry authority:

- `assets/grimo/source/carol/approved-3d/authority.json`
- `docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`

The authority is **4 FINAL / LOCKED Front/Side + Skin Front/Side → one model →
derived Back/Top/3Q**. Derived views are validation evidence, not independent
fitting targets.

The formal package governs geometry. The identity canonical remains the highest
authority for visible identity/appeal; it does not silently rewrite locked
hidden-geometry numbers, and locked geometry numbers do not justify a visibly
off-model final companion.

## Production routing

- Current mutable Carol state: `docs/production/carol/CAROL_PRODUCTION_STATE.md`
- Current-version evidence: follow the evidence path named by that state file.
- Stable geometry rules: `CAROL_MODELING_CONTRACT.md` and
  `CAROL_GEOMETRY_DECISION.md`.
- Review history: `CAROL_REVIEW_LOG.md`.
- Research and archive material are non-authoritative unless a current task
  explicitly makes them relevant.
- Goal-backward repository rule: root `AGENTS.md`.

Do not infer candidate, branch, HEAD, or Human Gate status from this index.
