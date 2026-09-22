# Carol production state

This is the single mutable source of detailed current Carol production truth.
Do not duplicate its candidate, gate, branch, evidence, blocker, or next-step
facts in durable memory, maps, contracts, prompts, or skills.

## Current state — 2026-09-22

- Candidate/version: **Carol v008 — partial Skin cage prototype**
- Candidate asset: `assets/grimo/production/carol/blender/carol-v008.blend`
- Generator: `scripts/blender/build-carol-v008.py`
- Evidence: `docs/production/carol/evidence/reconstruction-v008/README.md`
- Branch: `codex/carol-final-reconstruction-v008`
- Execution status: **BLOCKED_AT_V008_SKIN_INTERNAL_GATE**
- Human Geometry Gate: **PENDING; not ready for Human submission**
- Technical checks: supporting evidence only; they do not approve geometry.

Three Skin edit/render cycles were inspected in both locked primary views.
Cycle 2 is retained; cycle 3 worsened the ear outline and obscured the mouth.
The selected candidate was rebuilt in a clean Blender process. No fleece,
Normal evidence, derived views or motion diagnostics were produced.

## Current blockers

- The short reference-fitted rump and contract-positioned tail attachment
  remain visibly separated: evaluated longitudinal gap approximately
  **0.14031 H**. No long renderable root was added to bridge it.
- Ear Side volume/root relationship remains incorrect.
- Head/chest overlap and limb-root shape still need fitting in both views.
- Skin Front and support-registered Skin Side imply different skull heights;
  this discrepancy is recorded without changing the locked contract.

The new architecture uses explicit quad head/torso/socket/limb cages with
non-destructive subdivision, fixed support centers, heavy hoof cages, a
non-rendered internal tail pivot, short attachment and independent tuft.
The coherent fleece cage and regional fields remain unimplemented because
the Skin internal gate was not satisfied.

## Formal authority

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

## Previous candidate — v007 historical Human FAIL

v007 scripts, asset and evidence remain unchanged. Its Human failures were:

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

**CHATGPT_PLANNER: review blocked Skin evidence, reconcile tail/rump
attachment intent under fixed support registration, then specify the next
Skin cage revision.** v008 is not ready for Human Geometry Gate review.

Do not proceed to fleece while Skin is blocked. Until a new Human Geometry
Gate approves a complete candidate, do not advance to rigging, retopo lock,
animation, final materials/lookdev, GLB export, or PlayCanvas integration.

Historical gate chronology remains in `CAROL_REVIEW_LOG.md`; it is not current
execution state.
