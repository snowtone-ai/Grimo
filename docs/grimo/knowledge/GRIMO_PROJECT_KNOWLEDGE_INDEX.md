# Grimo — Project Knowledge Index

**Status:** Active routing authority  
**Updated:** 2026-09-23

## 0. Three-layer information model

1. **ChatGPT Project Memory** — how to reason: Product Goal, first principles,
   Planner/Codex/Human roles, Goal-Backward Spiral, stop rules.
2. **Project Knowledge** — durable authority/evidence: product feeling,
   canonical identity, production architecture, character-specific authority,
   reference evidence.
3. **GitHub** — mutable execution truth: branch, HEAD, current candidate,
   blockers, implementation, evidence, tests, current handoff.

Never use Project Knowledge to infer mutable repository state.

## 1. Authority order

Resolve durable-production conflicts in this order:

1. Current explicit user decision
2. `GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md`
3. Canonical identity images
4. `GRIMO_CHARACTER_EXPERIENCE_SPEC.md`
5. `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`
6. Character-specific approved authority such as Carol references/parameters
7. `GRIMO_PRODUCT_FEATURE_SPEC.md` / `GRIMO_DATA_MODEL_SPEC.md` in their domains
8. Reference evidence

Final perceptual acceptance remains Human authority. Automated technical
evidence cannot override a user-visible failure.

## 2. Planner read routing

| Question | Read first |
|---|---|
| What is Grimo trying to achieve? | `GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md` |
| What makes the companion feel alive? | `GRIMO_CHARACTER_EXPERIENCE_SPEC.md` |
| What production architecture are we using? | `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md` |
| How do Planner/Codex/Human work? | `GRIMO_PRODUCTION_OPERATING_SYSTEM.md` |
| What is Carol's approved geometry target? | `CAROL_GEOMETRY_PARAMETERS.md` + four locked Carol refs |
| Highest visual identity authority? | character identity canonical |
| What did Partner Eevee/Pikachu actually do? | motion masters; then detailed analyses as needed |
| Front-camera benchmark? | `GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS.md` |
| Product/data contracts? | product/data specs |
| Current branch/candidate/blocker? | **Latest GitHub only** |

Do not read every knowledge file by default.

## 3. Active Project Knowledge

### Product / identity
- `GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md`
- canonical identity images for Carol / Jill / Pino / Shushu

### Experience
- `GRIMO_CHARACTER_EXPERIENCE_SPEC.md`

### Production architecture / workflow
- `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`
- `GRIMO_PRODUCTION_OPERATING_SYSTEM.md`

### Carol geometry authority
- `CAROL_GEOMETRY_PARAMETERS.md`
- `carol_front.png`
- `carol_side.png`
- `carol_skin_front.png`
- `carol_skin_side.png`

Skin references/parameters are supporting underbody authority; canonical identity
and approved visible Hero appearance outrank hidden-surface polish.

### Product system
- `GRIMO_PRODUCT_FEATURE_SPEC.md`
- `GRIMO_DATA_MODEL_SPEC.md`

### Reference evidence
- `EEVEE_MOTION_MASTER_INVENTORY.md`
- `PIKACHU_MOTION_MASTER_INVENTORY.md`
- `GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md`
- `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md`
- `GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS.md`

## 4. Superseded active documents

These old documents must not be treated as current workflow/architecture
authority:

- old `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md`
- old `GRIMO_EXPERIENCE_MOTION_BIBLE.md`
- old `GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`
- old `GRIMO_PARTNER_EXPERIENCE_PRODUCTION_REQUIREMENTS.md`, if encountered
- old `Grimo Character Production Architecture — Zero-Based Deep Research.md`
- repository-local `CURRENT_PROJECT_MEMORY.md`

Historical provenance belongs under `docs/archive/`.
