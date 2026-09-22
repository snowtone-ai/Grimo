# Carol production state

This is the single mutable source of detailed current Carol production truth.
Do not duplicate its candidate, gate, branch, evidence, blocker, or next-step
facts in durable memory, maps, contracts, prompts, or skills.

## Current state — 2026-09-22

- Candidate/version: **Carol v007**
- Candidate asset: `assets/grimo/production/carol/blender/carol-v007.blend`
- Generator: `scripts/blender/build-carol-v007.py`
- Evidence: `docs/production/carol/evidence/reconstruction-v007/README.md`
- Human Geometry Gate: **FAIL**
- Technical checks: supporting evidence only; they cannot override Human FAIL.

The production method remains correct:

```text
4 FINAL / LOCKED references
+ CAROL_GEOMETRY_PARAMETERS.md
        ↓
one single 3D model
        ↓
derived Back / Top / 3Q
```

Formal references are `carol_front.png`, `carol_side.png`,
`carol_skin_front.png`, and `carol_skin_side.png`. Older six-view references,
v005, and v006 geometry are historical/superseded and are not current fitting
targets.

## Human failure reasons

### Skin Side

- body too long
- head/body transition incorrect
- front/rear leg placement incorrect
- tail root too long

### Normal Side

- helmet-like fleece
- ear recess incorrect
- flank massing incorrect

## Next allowed production step

`v008 Geometry revision → Human Geometry Gate re-review`

Do not begin v008 in a documentation/tool-routing task. Until a new Human
Geometry Gate passes, do not advance to rigging, retopo lock, animation, final
materials/lookdev, GLB export, or PlayCanvas integration.

Historical gate chronology remains in `CAROL_REVIEW_LOG.md`; it is not current
execution state.
