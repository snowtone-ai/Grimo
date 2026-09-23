# Carol v013-A-REPAIR — technical failure after two bounded passes

**Executor status: TECHNICAL_FAIL. Human Geometry Gate: NOT_REVIEW_READY.**
The Option D semantic anterior chassis has still not reached a legitimate
Front/Side visual test. The selected R2 blend is **DIAGNOSTIC ONLY — NOT
PROMOTED**. Phase B/C remain **NOT STARTED**.

- Repair starting HEAD: `94761dfdcca7475480a173effe783993146fc484`.
- Original source v012: `9d39680389b20677b6627491fd79bd6acbc51658`.
- Working branch: `codex/carol-final-reconstruction-v013`.
- Repair passes: **R1 and R2; selected R2 — DIAGNOSTIC ONLY; NOT PROMOTED**.
- Asset: `assets/grimo/production/carol/blender/carol-v013.blend`.
- v012 source SHA-256: `c2aa573baa3dc5723d6b20b80ba5355fb464606f2e0814a1ee81747c532a2055`, unchanged.
- All four locked image hashes and inherited reference registration verified.

## Implemented architecture

A deterministic BMesh-authored anterior cage replaces the old head and direct
head-to-portal strip. Named face fields feed each 24-segment R3/R2/R1/R0 orbital
grid. R0–R2 have only valence 4 vertices. The lid rim is part of the central
facial mesh, with inherited material separation. A recessed closed basin lies
behind each oversized shallow optical lens; the old separate lid shells were
removed. The neutral mouth/nose are seated on the new facial field. Materials
are reused without look-development changes. Optical relief is `.030 H`.
The `.137 × .149 H`, `±.162 H` aperture is authored on the control ring;
evaluated visible aperture and edge occlusion have **not** been accepted.

The section-based cranial cage feeds distinct J0 jaw, J1 sub-jaw flex, C0 chest
crest and C1 chest blend rows. J0/J1/C0 are pole-free. C0 comes forward relative
to J1; there is no assumption that all longitudinal rows increase in X.
Quad density transitions occur after the chest blend, ahead of the retained
nonplanar `.575 H` station. No old head connectivity, remesh, Boolean, UV-sphere
primitive, camera-specific mesh or hidden corrective shell is used.

## Repair and gate result

Stored witnesses from original A support the suspected first-bridge angular
remapping problem: facial quads crossed the first cranial loft on both sides.
The face perimeter is also locally inset past neighboring cheek/forehead
columns. A local extrusion can still sweep through those adjacent faces, and
regularization farther back lets seat/transition bands overlap later cranial
bands. The diagnosis was **partially confirmed**, not fully resolved.

R1 added a 48-vertex `CRANIUM_SEAT` built from each matched face-boundary
vertex, then a 48-vertex progressive `CRANIUM_TRANSITION`. It removed some
original crossings but had **52** control intersections. R2 made one
coordinated seat/transition curvature adjustment and had **51**. There was no
R3. No facial/orbital, J0/J1/C0/C1, density-transition, rear, support or
frozen-object redesign was made.

| Check | Result |
| --- | --- |
| R2 chassis vertices / edges / faces | 921 / 1,838 / 919 |
| Face type | All quads |
| Components / nonmanifold edges / Euler | 1 / 0 / 2 |
| Degenerate / duplicate faces | 0 / 0 |
| Consistent edge winding | Pass |
| Disjoint control-face intersections | **51 pairs — FAIL** |
| Source rear coordinates, edges, faces | Exact match, including `.575` interface |
| Save/reload geometry and frozen objects | Match |
| Full evaluated intersection / adjacency audit | Not run after cheap-gate failure |
| Skin Front / Skin Side / eye/socket visual result | Not run after technical failure |
| Derived 3Q / Top | Not run |
| Motion probe | Not run |

The remaining crossings include face-field to seat and seat/transition to
Front/Dorsal cranial bands. This is still an anterior assembly failure.
Closedness and all-quad counts do not make it a clean exterior.

A-REPAIR is not structurally correct after its two allowed passes. No B/C or
further parameter rescue was attempted. The jaw/chest silhouette, integrated eye read,
rounded posterior cranium and accepted ear-root fit remain unproven. No visual
PASS/FAIL is inferred from wires or numerical projection bounds.

The rear fingerprint uses exact floating-point coordinate keys and the faces
and edges induced by source ABDOMEN/RUMP groups, rather than vertex indices or
an X threshold that would accidentally include posterior head vertices.
All 96 rear vertices match after save/reload. Ears, four limbs, four hooves,
tail, cameras, lights and reference objects retain their source records.
Ear seating delta is zero. Support centers remain `.390` / `.920 H`.

## Evidence and reproduction

The original `diagnostic-sheet.png` explicitly marks candidate, overlay and
derived-view cells **NOT RUN**. Its old 825-vertex annotation is historical A
data, not R2. It shows locked source thumbnails, not registered comparison
renders. The updated `structure-sheet.png` contains six R2 wire-only panels,
including the control/evaluated subdivision comparison and highlighted stored
intersection witnesses. Neither sheet is a visual-acceptance render. This
limited evidence respects the required technical-before-render ordering.
`measurements.json` and `validation.json` preserve the checks and omissions.

Run from the repository root:

```text
blender --background --python scripts/blender/build-carol-v013.py
blender --background --python scripts/blender/build-carol-v013.py -- --finalize-failure
python scripts/blender/carol-v013-evidence.py --structure-only
```

The first command saves R2 and stops at the failed control gate. The second
records disposition and exports temporary wire coordinates without changing
geometry. The last updates only the structure sheet.

Toolset: installed Blender 5.2 background Python, BMesh/mathutils, existing
targeted validators, installed Python/Pillow, and Git/LFS. Existing project
configuration retains `multi_agent = false`; no dependency or plugin change
was needed. Repository-local skill routing was not used. No subagent, web
research, frontend tests, browser, GLB, fleece, production rig or animation ran.

At the user's explicit request, the pre-existing `tmp-carol-v012/` files are
also committed intact as historical v012 trials. They are not v013 authority.
The A-REPAIR budget is exhausted. Further geometry work requires a new bounded
planner handoff.
