# Carol v010 — Phase A visual reconstruction failed

**TECHNICAL_STATIC_GATE = PASS. EXECUTOR_VISUAL_PRECHECK = FAIL.**
`v010-A3` is retained as a **diagnostic asset only**, not a promoted production
candidate. Human Geometry Gate was **not reached**. Motion clearance was not
run because the executor visual prerequisite failed. The three-attempt budget
is exhausted; there is no A4.

Source: `codex/carol-final-reconstruction-v009` at
`5de182d5eab04f84e3fa46926a953efa3527d679`. Fetch confirmed that exact remote
HEAD, a clean worktree, and no newer remote Carol production branch. The four
locked source hashes were verified before construction. The source v009 blend
is unchanged (`94b3b38122343024f76107dd69d3fec7cf3e66f91aa290a91287c809524c58fe`).
The current user handoff records v009-A2 as **Human-reviewed FAIL**; its older
pending label is historical, not a request to reconsider that decision.

## Architecture and causal finding

Selected: cube-derived cranial patches with an anterior ventral jaw, a matched
short posterior-ventral neck strip, an open chest patch, and retained rear
longitudinal stations. The chassis is one authored exterior, with no buried
head/body owners, Boolean, remesh, or camera-dependent geometry. The defective
`.575` dorsal seam is reconstructed; all `.730` and rearward control stations
are retained to float32 precision (comparison tolerance `1e-7 H`). A3 has
533 vertices / 1,062 edges / 531 quad faces.

The architecture comparison also considered a separate ventral-jaw multipatch
atlas and a single sagittal-profile extrusion. The former added more patch
boundaries near deformation zones; the latter constrained depth shaping around
the under-chin concavity and ocular housing. The cube-derived option provided
the simplest explicit jaw ownership and correspondence to the chest. Only that
family was implemented; this is not a continuation of the v009 A3/A4 repair.

Actual v009 control and evaluated meshes show a reversal of the posterior
section order, lateral jaw/transition crossings, and another reversal at the
upper-chest seam. The 64-sector head/torso turn compounds these placements and
makes a long anterior sheet. Subdivision spreads the folds; it is not their
sole cause. Dense rings restrict local jaw shaping. Orbital seating and the
over-tall head interpretation are additional visual problems, not explanations
for the self-intersections.

`source-intersection-audit.json` records triangle/segment crossing witnesses in
all three regions. Independent strict interior tests confirmed 112 of the 116
control pairs and 452 of the 455 evaluated pairs. The remaining pairs were not
discarded or declared false positives. The original detector and adjacency
exclusion were not loosened to obtain zero.

## Bounded results

| Attempt | Control / evaluated disjoint pairs | Components / nonmanifold / quads / Euler | Disposition |
| --- | --- | --- | --- |
| A1 | 0 / 0 | 1 / 0 / all / 2 | Rejected: outward chest rim, pointed crown, diamond-like head |
| A2 | 0 / 0 | 1 / 0 / all / 2 | Rejected: small anterior chest lip and weak Side eye visibility |
| A3 | 0 / 0 | 1 / 0 / all / 2 | Rejected: 3Q eye stretching, angular Top shoulders, dominant oblique under-jaw plane |

A3 additionally checks adjacent tessellated faces, excluding only their shared
vertex/edge contact: **5,904 control and 93,515 evaluated triangle pairs; zero
improper contacts**. Coplanar overlap is checked by clipped triangle area.
Segment predicates use double arithmetic to avoid cancellation near shared
edges; the geometric contact tolerance is `5e-7 H`. This supplements the
unchanged disjoint-pair check. No structural intersection blocker remains in
the retained A3. The blocker is visual reconstruction.

The locked `.137 H × .149 H` Front eye apertures and `±.162 H` lateral centers
remain intact. Caps and lids are seated using local facial normals and tangent
frames; their relief is `.023 H` along the surface normal. The larger Side
projection in A3 produces a horizontally stretched 3Q aperture. The source
views require both huge-eye identity and a soft, compact face; improving Side
visibility cannot compensate for that 3Q failure. The lower-cheek shelf is
removed, but the under-jaw plane and angular cranial shoulders still prevent a
visual pass. No formal constraint was relaxed; a new geometry handoff is
required to reconsider cranial cross-sections and eye/socket curvature.

## Retained evidence and boundaries

- `diagnostic-rejection.png`: one compact rejection sheet containing registered
  Skin Front/Side comparisons, 50% overlays, and derived 3Q/Top. These are
  480-square, 16-sample Cycles diagnostics from one unchanged neutral model.
- `measurements.json` and `validation.json`: A3 topology, adjacency audit,
  dimensions, frozen-module fingerprints, hashes, and failed visual disposition.
- `attempt-1.json`, `attempt-2.json`: minimal rejected-attempt numerical records.
- `source-intersection-audit.json`: v009 crossing localization and witnesses.
- `assets/grimo/production/carol/blender/carol-v010.blend`: rejected A3 diagnostic
  with failure status stored in the scene. v009 remains byte-identical.

Ears, hooves, limbs, tail, supports, cameras, lights, reference registration,
reference images and material assignments remain unchanged. The temporary v008
ear and hoof defects were not repaired. No production rig, animation, fleece,
GLB, runtime changes, or Phase B/C work exists. There is no full Human review
packet because no candidate passed the executor's visual precheck.

The existing project configuration remains sufficient: `multi_agent = false`,
Blender MCP disabled, no repository-local skills present. This Phase A task used
Blender 5.2.1 in background mode, local image inspection/compositing, shell and
Git; it needed no configuration change or additional plugin.

Reconstruct with `blender --background --python scripts/blender/build-carol-v010.py
-- --attempt N --render` for N = 1, 2, 3. `--finalize-failure` archives A3 with
its factual failed disposition and performs the supplemental adjacency audit.
No further geometry iteration is authorized by this attempt budget.

Next handoff: **CHATGPT_PLANNER**. No accepted v010 candidate is claimed.
