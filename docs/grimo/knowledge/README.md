> Current Carol checkpoint (2026-09-17): v006 is paused at the user request, geometry FAIL / Human Gate PENDING. B is retired. The v005 A/B selection described below is historical. Follow [the v006 evidence and handoff](/docs/production/carol/evidence/reconstruction-v006/README.md) and /prompt.md for the current state. Single agent only; resume modeling only when requested.

# Grimo knowledge authority index

This directory is the stable Project Knowledge layer. Active production state and Human Gate evidence are kept separately under `docs/production/`, while canonical/source assets live under `assets/grimo/source/`.

Start new Grimo work by reading:

1. `CURRENT_PROJECT_MEMORY.md` — compact latest project memory and routing
2. the domain authority below that matches the task
3. `docs/production/carol/CAROL_PRODUCTION_STATE.md` when the task touches current Carol production

## 1. Stable product authority

| Domain | Current authority |
|---|---|
| Product behavior / reward / Collection | `product/GRIMO_PRODUCT_FEATURE_SPEC.md` |
| Logical data model | `product/GRIMO_DATA_MODEL_SPEC.md` |
| Living-companion motion / interaction philosophy | `character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md` |
| Generic Full-3D / Blender production | `character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md` |
| Carol-specific motion implementation | `character-production/carol/CAROL_MVP_MOTION_SPEC.md` |

The current character architecture is Full 3D + Blender-centered production + GLB/glTF + PlayCanvas. The archived PixiJS / 2D / 2.5D direction is obsolete.

## 2. Carol visual and geometry authority

### Visible identity

`assets/grimo/source/carol/carol-Identity-canonical.png`

This remains the authority for Carol's character identity, palette, motifs, appeal, perceived softness/age and recognizable sacred presentation.

### Concrete 3D geometry

`assets/grimo/source/carol/approved-3d/authority.json`

The following **six approved individual views are the highest concrete authority for geometry, volume, proportion, depth and part placement**:

- `carol-front-ortho-transparent.png`
- `carol-side-ortho-transparent.png`
- `carol-back-ortho-transparent.png`
- `carol-top-plan-transparent.png`
- `carol-front-3q-left.png`
- `carol-front-3q-right.png`

Use Side and both 3/4 views together with Front. Never flatten the face by deriving depth from Front alone. The 3/4 views formally constrain facial depth, muzzle/cheek/forehead volume, eye-to-face depth, ear roots, fleece-to-face ordering, body depth, limb fore/aft placement and overall fleece volume.

`carol-3d-production-canonical-sheet.png` is supplementary and yields to conflicting approved individual views for concrete geometry.

The identity image must not overwrite concrete depth/thickness/volume/part placement established by the six approved views. The geometry references likewise do not authorize redesign of Carol's identity, palette, motifs or appeal.

## 3. Active production memory and gate truth

Operational truth is intentionally outside this stable knowledge directory:

- Current Carol state: `docs/production/carol/CAROL_PRODUCTION_STATE.md`
- Geometry decision record: `docs/production/carol/CAROL_GEOMETRY_DECISION.md`
- Modeling contract: `docs/production/carol/CAROL_MODELING_CONTRACT.md`
- Camera contract: `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- Review history: `docs/production/carol/CAROL_REVIEW_LOG.md`
- Current v005 A/B evidence: `docs/production/carol/evidence/hero-geometry-v005/`

As of 2026-09-16, v005 A and B are **not approved hero geometry**. Human construction-direction comparison is pending. Do not infer rigging/export/runtime authorization from the presence of `.blend` files or successful automated checks.

## 4. Research / evidence layer

`research/` contains evidence and architecture research, not automatic production authority:

- `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md`
- `Grimo Character Production Architecture — Zero-Based Deep Research.md`
- `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md`
- `GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md`
- `motion-masters/PIKACHU_MOTION_MASTER_INVENTORY.md`
- `motion-masters/EEVEE_MOTION_MASTER_INVENTORY.md`
- `camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_BENCHMARK.md`

Research informs production choices, but a newer explicit Human decision, current production contract, or approved source authority wins when they conflict. Motion/reference footage supplies principles and evidence; copyrighted Pokémon assets or exact performances are not production assets.

## 5. Authority separation rule

Keep these layers distinct:

```text
stable specs / Project Knowledge
        ↓ informs
active production contracts + Human Gates
        ↓ consume
canonical / approved source assets
        ↓ produce
Blender / runtime artifacts + review evidence
```

A generated model, old recovered model, review screenshot, automated metric or research report cannot promote itself into authority.

## 6. Historical material

`docs/archive/obsolete-2_5d/` is non-authoritative historical material. Historical Carol source under `assets/grimo/source/carol/historical/` is evidence/reference only unless a specific experiment explicitly authorizes reuse; v005 B is currently such a limited exception.
