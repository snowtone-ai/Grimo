# Carol v007 — structural and motion-capability review candidate

**TECHNICAL GEOMETRY CHECK: CONDITIONAL**

**HUMAN GEOMETRY GATE: AWAITING REVIEW**

**NOT ACCEPTED FOR PRODUCTION. Next handoff: HUMAN.**

This is a zero-based, editable Blender reconstruction, not a production rig or
an approved replacement for Carol. It provides a concrete geometry proposal
and exposes remaining reference and deformation risks. The four authority
views have not been certified as a faithful final match.

## Source and reproducibility

- Branch: `codex/carol-final-reconstruction-v007`.
- Base: `10ce89a619bbf6c766d8812c21fed56292502f57`, fetched and verified against
  `origin/codex/carol-zero-based-hero-geometry-v005` before construction.
- Asset: `assets/grimo/production/carol/blender/carol-v007.blend`.
- Generator: `scripts/blender/build-carol-v007.py`.
- Registration/contact-sheet utility: `scripts/blender/carol-v007-evidence.py`.
- Blender: **5.2.1 LTS**, build `9e2066aef7ef`; Python image utility uses Pillow.
- Single agent, no web research, no old Carol meshes, fitted arrays or old
  geometry generators reused. The session's exact model/effort was not
  verifiable; the requested model label is not recorded as an actual runtime fact.

Formal authority is `CAROL_GEOMETRY_PARAMETERS.md` together with the locked
`carol_front.png`, `carol_side.png`, `carol_skin_front.png`, and
`carol_skin_side.png`. Their observed SHA-256 hashes are in `measurements.json`.
Identity canonical was inspected as secondary identity support. No reference
was modified or regenerated. Old Back/Top/3Q images were not used as targets.

Commands, from repository root:

```powershell
# These stages rebuild the candidate; do not rerun completed stages for review.
blender -b --python scripts/blender/build-carol-v007.py -- --stage skin
python scripts/blender/carol-v007-evidence.py skin
# Inspect Skin Front/Side before proceeding.
blender -b --python scripts/blender/build-carol-v007.py -- --stage skin-stress --resolution 480
python scripts/blender/carol-v007-evidence.py skin-stress
# Supplemental disposable closure/gaze checks, without fleece:
blender -b --python scripts/blender/build-carol-v007.py -- --stage skin-stress --diagnostics blink,gaze
# Inspect the diagnostic renders before adding fleece.
blender -b --python scripts/blender/build-carol-v007.py -- --stage normal
python scripts/blender/carol-v007-evidence.py normal
# Final output after the structural review checkpoints:
blender -b --python scripts/blender/build-carol-v007.py -- --stage final --resolution 1254
python scripts/blender/carol-v007-evidence.py final
```

Each Blender invocation starts from an empty scene and writes the same candidate
asset. Earlier stages intentionally omit fleece. Final recreates both modes
and saves the neutral Normal model after resetting diagnostic poses. Disposable
renders go to `tmp-carol-v007/` and are not part of this committed packet.
There are no production bones, animation clips, final retopology/skinning,
final materials, runtime GLB or PlayCanvas changes.

## One model and registration

X increases front to rear, Y is bilateral, Z is up; ground is Z=0 and H=1.
Skin and Normal renders share the identical head, eyes, ears, torso, four
limbs, four hooves and tail. Only `FLEECE_MASTER`, moon and stars change
visibility. Front and Side cameras are orthographic with the same 1.52 H
span. Derived views use the same neutral geometry; diagnostic poses are the
only deliberate pose changes. There are no view-dependent meshes or shape keys.

The `.blend` retains registered image empties in the disabled
`REFERENCES locked, H-registered` collection. Enable that collection for
inspection. Image paths are relative to the asset. Registration parameters
and their observational basis are recorded in `measurements.json`; the PNG
canvas dimensions were never used as a common geometry scale.

Skin Side registration uses the near-hoof footprint centers at approximately
x=461 and x=1001 on row 1030: 540 px / 0.530 H gives 1019 px/H. Its X origin is
approximately 64 px so the fore-support maps to X=0.390. This refinement of
the initial visual estimate is a reference registration change, not a
camera/model scale change. It implies a skull top near 0.728 H, compared with
the numerical 0.690 H chassis-height guidance and the Skin Front reading.
The numerical construction is retained; this residual reference difference
is visible in the overlay. These observations are not replacement lock values.

## Construction and deformation evidence

The head and torso use editable section-based construction. Separate thick
ears, eyes, limbs, hooves and a rooted tail permit independent channels.
The fleece is a voxel-unioned master with overlapping regional vertex groups:
crown, face frame, chest/front, central back, lower belly and rear rump.
Ear recesses are actual cut volumes. Tiny boolean crumbs are removed; this is
an authoring mesh, not final topology or a runtime polygon budget.

Named anchors bind to their owning surface, with a vertex-relative offset
for local diagnostic deformation. Head/ear anchors inherit their owner's
transform. Fleece/motif markers follow the master surface, and motifs follow
their markers in compression diagnostics. These bindings are a geometric
prototype; they need production retopology-aware transfer later.

`motion-readiness-sheet.png` contains neutral, 10-degree head yaw, L/R cheek
lean, asymmetric ears, small torso transfer, one-forehoof adjustment, local
fleece compression, shallow face nestling, and a subtle tail pose. Amplitudes
and observed hoof contact coordinates are in `measurements.json`.
The three supporting hooves remain fixed when one forehoof is raised.
These are static analytical diagnostic poses, not authored animation or a
dynamic center-of-mass simulation.

A separate closure-envelope diagnostic was inspected. An initially exposed
iris edge was corrected by reducing iris depth and aligning it with the eye;
the revised lid envelope covered it. This proves available covering space,
not an appealing blink, approved facial acting or final eyelid topology.
Small gaze offset was also inspected. Neither constitutes a full expression
stress test across all future presets.

## Review disposition

| Area | Result | Remaining limitation |
| --- | --- | --- |
| Skin Front | CONDITIONAL | Broad support and shared head exist; ear bowl shape and cheek/forehead character differ from the locked illustration. |
| Skin Side | CONDITIONAL | Support spacing follows the contract; head/reference registration and the exposed long tail root differ from the illustration. |
| Normal Front | CONDITIONAL | Crown/face-frame/hoof hierarchy is present; fleece is still coarser and more helmet-like than the reference. |
| Normal Side | CONDITIONAL | Face and ear remain visible; ear recess, fleece profile and motif visibility need review. |
| Derived 3D coherence | CONDITIONAL | All views use one model; off-axis eye exposure, ear recesses and rear fleece massing remain art-direction risks. |
| Motion readiness | CONDITIONAL | Independent small diagnostic poses exist; combined extremes, deep face-in-fleece, expressive lids and production attachment behavior are not proven. |

Largest geometry deviation: **coarse crown/face-frame and flank fleece massing,
especially the side ear recess, still diverge from the locked references.**

Largest motion risk: **a deeper face-in-fleece movement combined with head yaw
and an asymmetric ear may require revised local geometry; the shallow separate
diagnostics do not establish the full clearance envelope.**

The single moon is retained on the front-left surface. Its visibility from the
opposite-side camera does not reproduce the Side illustration. It was not
duplicated or moved per view to manufacture agreement. Debug clay deliberately
avoids final shading/texture work; color matching is not a claimed result.

Regional fields provide a future means of local, regional and broad fleece
deformation. Temporal delay, causal ordering, afterglow, physics and complete
layer combinations are outside this static-geometry task and remain untested.
No collision-solver proof or automatic visual-identity approval is claimed.

## Evidence index

- `final-four-view-sheet.png`: four authority pairs, reference then render.
- `skin-front.png`, `skin-side.png`, `normal-front.png`, `normal-side.png`:
  1254-square neutral renders.
- Matching `*-overlay.png`: registered 50/50 reference/render comparisons.
- `derived-3q-left.png`, `derived-3q-right.png`, `derived-back.png`,
  `derived-top.png`: neutral views derived only from this 3D model.
- `motion-readiness-sheet.png`: ten compact static diagnostic views.
- `measurements.json`: actual mesh measurements, source/generator hashes,
  registration, support-contact observations and anchor bindings.

Numerical checks cover the explicitly listed dimensions, not every clause of
the production contract. A passing measurement cannot override the conditional
visual disposition above. Human approval remains required before production
topology, rigging, skinning, animation, final look development or export.

Final observed checks: all eight recorded dimensions are within 2% of their
listed targets. H=0.999568, fleece width=1.153409, eye width/height=0.136850 /
0.149000, forehoof width/height=0.218949 / 0.111000, chassis width=0.610000,
and head maximum Z=0.689843. The fleece has one connected component
(208,312 authoring vertices). In the forehoof diagnostic the moved hoof is
at Z=0.022; the other three minimum contact heights remain exactly Z=0.
