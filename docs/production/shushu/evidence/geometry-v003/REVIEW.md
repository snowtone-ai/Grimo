# Shushu geometry v003 — review candidate

2026-10-13 (resumed from 2026-10-12). **Human Geometry Gate: PENDING. Downstream Tripo work: HOLD.**

**Current Human Gate revision:** see [the focused eye / seating / full-mouth comparison](human-gate-revision/REVIEW.md). It locally edits the saved v003 at `93869a8771045d7ed79ab036bd61d66ed97bd437`, preserving topology, original controls, contact mechanisms and the 285-frame timeline. Current editable/static assets and machine checks below were updated. The original review boards and GIFs below show the preceding geometry and are retained as history; use the new Clay + diagnostic-colour boards for the current visual decision.

The current candidate restores the **visible** eye width/height to donor measurements while preserving the eye/lid mechanism, softens only the intermediate lid annulus, tucks the proximal seated thigh into the pelvis without moving the foot/standing Basis, and adds `MouthDonorOpen` without replacing the small-mouth/smile controls. Actual donor eye-component size, visible aperture, eyelid/orbital regions and the temporary pink mask are recorded separately. The old whole-eye "20–30% enlargement" estimate remains withdrawn. Human acceptance remains PENDING.

This continues the interrupted v003 work. It does not restart from v001/v002 geometry and does not supersede any Human rejection or approved art. The current purpose is a recognizable, appealing Shushu that can blink, sit with believable support, and participate in gentle contact. Mesh counts and export success only support that purpose.

## Authority and continuity

- Resumption authority: `main@2fcb1b8198e5ffdab9cc2face3a7dda347870db2`, specifically `AGENTS.md`, `docs/grimo/knowledge/Goal√map.md`, and `docs/production/Handoff.md`. The three documents were brought into this older production branch without merging/rebasing main's production history.
- Final remote refresh observed `main@526a1b33c59529eadf58fec2fa010a9049f02764`; the same three authority documents are unchanged from the resumption revision. The intervening specification and context-configuration changes were not bulk-merged into production.
- Execution branch: `codex/grimo-motion-zero-based-design-20261011`. The intervening remote commit `2812a9a` changed only AGENTS.md and was fast-forwarded before the focused continuation. The interrupted v003 files and pre-existing user changes were preserved.
- Geometry donor: original Candidate B FBX, **8,259 vertices / 8,481 polygons** on import. The original FBX and GLB remain byte-identical to the intake manifest. No v001/v002 mesh is imported by the builder.
- Visual authority: Canonical identity, approved body-only four views, approved references #01–17, and revised #18–26. #25's accepted rear-side view informs the additional seated inspection angle. Its camera acceptance is not approval of this mesh.
- Corrected #27 remains **UNKNOWN**. The existing root #27 is not treated as a revised approved reference. Work does not wait for it.
- No new visual authority was created by the anatomy research. See [the applied research notes](ANATOMY_AND_DEFORMATION_NOTES.md).

## Deliverables

| Artifact | Purpose |
| --- | --- |
| [Editable geometry](../../../../../assets/grimo/production/shushu/blender/shushu-geometry-v003.blend) | Source-derived neutral geometry, editable face/body shapes, hidden untouched source reference, inspection stage. |
| [Editable proof](../../../../../assets/grimo/production/shushu/blender/shushu-geometry-v003-proof.blend) | 285 frames at 24 fps, named timeline markers, independent face controls, seating, reach, bounded hold, release, and self-contact. This is a disposable deformation proof, not a production rig or final performance. |
| [Static FBX](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/shushu-geometry-v003-tripo.fbx) | Neutral upload candidate, no rig, shape keys, animation, UVs or texture work. |
| [Static GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/shushu-geometry-v003-tripo.glb) | Same neutral geometry; no materials, textures, images, skins, animations, cameras or inspection props. |
| [Identity comparison](review-01-identity.png) | Original donor and v003, identical front, both exact sides, three-quarter and rear cameras. |
| [Face proof](review-02-face.png) | Neutral, half, closed, reopen, unilateral blink, gaze geometry, small mouth, smile, surprise and side depth. |
| [Support/contact proof](review-03-support-contact.png) | Rump seating from four angles, offer, actual inspection prop between both paws, self-contact and release. |
| [Transition proof](review-04-transition.png) | Standing, three intermediate seating poses, full seated and resting pose. |
| [Seating preview](seat-proof.gif), [blink preview](blink-proof.gif) | Renders from the saved proof timeline; study timing only. |

## What changed and why

The eight main donor modules retain the original head, cheek, muzzle, torso and short-limb proportions. Disconnected source strips and small fan defects are excluded or repaired. Source subdivision removes coarse facets; there is no whole-head voxel remesh, broad relaxation, or replacement analytic face surface.

The eye regions and small mouth have bounded replacement topology. Eye surfaces sample the **front envelope** of the original eye components; fitting front and back together made the eyes too recessed during development and was corrected. Upper/lower lids meet over the eye, with a separate half-blink correction and independent left/right control. The half-blink keeps the opening's corners in their original positions and moves the upper lid more than the lower one, avoiding the corner gaps observed with a translated, shrunken ellipse. Its angled lid contour still needs Human judgment for softness and expression. The nose and muzzle outside the local mouth edit remain source-derived. The mouth is small in neutral and can open, smile or form a small surprised shape.

Three-quarter inspection exposed an additional parallax gap during partial closure. The eye now continues beneath the lids as a closed volume, the lid follows the eye envelope, and local inner lid walls block views into the rear of the head. Left/right wall thickness reduces independently at final closure so it does not protrude at the corners. Eye retraction is limited to the final part of closure. Facial displacements also rotate with the head through driven composition corrections; adding a facial delta in its original frame left gaps during tilted closure. These are bounded geometry corrections, not an anatomical simulation. The resulting lid thickness and closed-eye volume remain part of the visual gate.

Seating separates the foot frame, curved leg centerline and pelvis motion. The upper leg changes orientation while preserving its radial thickness; it is not one rigid leg swung forward. Local abdomen clearance and rump volume accompany the pelvis descent. Foot support moves the support frame rather than clamping individual vertices to a floor. Four sampled poses keep intermediate articulation editable. Seat025 provides the shallow feet-supported stage; Seat100 is the rump-supported seat. The timeline's named Rest pose is a head-lowered variation of Seat100, not a claim that these support states are interchangeable.

The self-contact proof includes a head lean toward the raised paw. This lets a short arm reach the cheek without requiring the arm alone to bridge the whole distance. Two-paw holding uses a sphere sized and positioned against both evaluated paw surfaces, with clearance from the torso. Release returns the hands and moves/hides the inspection prop.

## Verification and limits

Machine-readable evidence: [saved artifact checks](saved-artifact-checks.json), [static roundtrip](static-roundtrip.json), [geometry checks](geometry-checks.json), [hold contacts](hold-contact.json), [source hashes](source-integrity.json), and [camera settings](review-cameras.json).

- Both originals and the five primary art references pass SHA-256 preservation checks. v001/v002 assets and the user's modified v002 review PNGs are not changed by this work.
- The neutral static export has **11 meshes / 123,270 triangles**. Zero-area faces from zero-weight rim regions are removed on static export. This is an upload/editing candidate, not an optimized smartphone runtime asset.
- FBX and GLB are imported again locally and compared in both directions against the exported surface. Maximum FBX error is below `0.000001` scene units; GLB is exact within the recorded surface comparison. This establishes local roundtrip fidelity only.
- Saved proof neutral-return frames reproduce the editable neutral geometry within the asserted `0.000002` tolerance. Reset checks also cover left/right face controls.
- At full closure, all 128 interior eye-cap probes per side are occluded by the head. Half-blink probe coverage is recorded, but does not establish a natural half-blink expression.
- A bounded three-quarter parallax regression checks seven symmetric blink values and two asymmetric left/right combinations in upright and resting configurations. Each combination uses 1,728 upright and 588 rest-region rays; none falls through to the rear head or empty space. This covers the observed gap and those sampled regions, not every possible view or facial combination.
- A 41-sample seating sweep checks the two feet and torso against the support plane. Full seated foot minimum is about `0.001`; rump minimum about `0.0036`; the largest foot gap during interpolation is about `0.0031` in a character approximately one unit tall. These small positive offsets are retained and reported, not called exact physical contact.
- The hold sphere's two surface gaps are within `0.0001` and torso clearance exceeds `0.002`. This is a bounded geometry check, not a grasp-force or collision simulation.
- Self-contact reports only distal-paw proximity, excluding the shoulder attachment. Its signed nearest-surface diagnostic is a local normal proxy, not a general inside/outside solver.
- Ear, limb, torso and head parts use intentional overlapping articulation. Eyes, eyelids and mouth use separate interacting surfaces; this is not a single watertight solid. No claim of universal collision-free deformation is made.

## Pending acceptance and downstream readiness

| Gate | Status | What is still required |
| --- | --- | --- |
| Neutral identity / cuteness | **Human PENDING** | Judge eye surround, tiny mouth, nose/muzzle depth, cheeks and whole-body proportions against Canonical and the original donor. |
| Facial deformation | **Local mechanism checked; appearance PENDING** | Half/closed eyelid contour and mouth transitions need perceptual acceptance. Untextured eye surfaces do not establish the final gaze impression. |
| Seating / contact | **Local support/contact checks passed; appearance PENDING** | Judge the thigh-to-foot shape, abdomen/rump weight, intermediate poses, and the gentle head/paw relationship. |
| Static interchange | **Local PASS** | FBX/GLB contain the intended neutral meshes and pass the local roundtrip. |
| Tripo Studio texturing | **UNKNOWN / HOLD** | No upload or paid/free trial was executed. Format support is not proof that this particular mesh is accepted. |
| Tripo Studio Auto Rig | **UNKNOWN / HOLD** | The original short-limbed standing pose is preserved. It has not been proven to match Studio's supported rigging assumptions. |
| Final rig / Motion / smartphone runtime | **Not produced in this scope** | Production skeleton, motion interruption/state behavior, final timing, runtime export and device validation follow accepted geometry. |

The [official Tripo upload-for-animation guidance](https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation) distinguishes supported humanoid T poses and standard standing quadrupeds. A stylized, short-limbed Shushu must not be assumed compatible from the API's broader category list. The [official texturing feature](https://www.tripo3d.ai/features/ai-texturing) advertises existing-model texturing, but this deliverable has not been tested there.

If a later authorized Tripo stage cannot provide the required facial, seated or contact controls, the bounded fallback is to retain the accepted geometry, obtain only the authorized texture result, and build a specialized Blender rig with localized corrective targets. That fallback is documented, not executed. Tripo credits and current account state remain UNKNOWN; this work uses no credits or trials.

## Reproduction

Run `scripts/blender/build-shushu-geometry-v003.py` with Blender 5.2 in background mode and `--python-exit-code 1` before `--python`. `--quick` produces Workbench inspection renders. The normal run creates neutral Cycles evidence and both editable `.blend` files. `--character-only` reuses the unchanged donor images and regenerates all character views; use it only after a full run. Run `scripts/blender/verify-shushu-geometry-v003.py -- --preview` in Blender to reopen the saved artifacts, check the proof, and render preview frames. Run `scripts/blender/shushu-v003-review-boards.py` with Python/Pillow to pack unchanged renders into boards/GIFs.

The proof's shape keys are explicitly derived from Basis. Seat025/050/075/100 are adjacent samples to crossfade, not four additive switches. Half-blink corrections are driven automatically from the corresponding Blink value. The inspection stage and prop are excluded from static exports. No application behavior, final material, UV, fur, or texture work is included.
