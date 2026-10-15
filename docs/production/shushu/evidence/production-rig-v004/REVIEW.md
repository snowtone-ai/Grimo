# Shushu Production Rig v004 — true-seat candidate

**Appearance HOLD / Human PENDING.** v004 replaces v003's crouched Seat with a forward-foot, lowered-rump sitting design. Both short legs advance independently of the hips; the heels roll while support transfers toward the rump. The accepted v003 face and standing Neutral side are locked. The side leg/abdomen junction and resting/return appeal remain unapproved. This candidate does not replace v003 or an approved static asset.

## Open first

- [Pose refs 23/24, old crouch and new seat](references-before-after.png)
- [All eight views of the full seat](view-seat.png)
- [Standing, forward-leg stage and seated side comparison](comparison-left.png)
- [Seated face, five angles](face-seat.png) / [half](face-seat-half.png) / [closed](face-seat-closed.png) / [joy](face-seat-joy.png)
- [Actual image observations and remaining HOLD](VISUAL-OBSERVATIONS.md)
- [Authority and reference provenance](AUTHORITY.md), [exact supplied reference hashes](reference-provenance.json)
- [Controls, reproduction, camera/light conditions](README.md)

## Separate editable assets

In `assets/grimo/production/shushu/tripo/geometry-v003/rigging/`:

- `shushu-v006-production-rig-v004.blend`: editable controls, original bone lengths/rest matrices and local corrections.
- `shushu-v006-production-rig-v004-proof.blend`: editable 24fps diagnostic action, 821 frames, with the seat/return sequence first and 81 inherited capability witnesses after it.
- `shushu-v006-production-rig-v004.glb`: saved Skin/Morph/Anchor animation.
- `shushu-v006-production-rig-v004-proof.glb`: separate diagnostic held-sphere fixture.

The final asset hashes are in [delivery-manifest.json](delivery-manifest.json). Diagnostic timing is not an adopted production Motion specification.

## Construction and preservation

The old fixed-foot premise is removed for Seat. Both targets travel 0.180 forward and 0.018 outward, with 65° sole pitch; the hips lower independently with a forward anticipation before settlement. Whole-foot rotation is supported by a sampled rigid-foot envelope. There is no per-vertex floor clamp, foot thinning, rest-bone lengthening or new body mesh.

Torso weights below the ankle blend are locally reassigned to retain the approved full foot. v003's `Corrective.SupportVolume.*` keys are replaced by 48 lower-body pose corrections. UV-seam-equivalent vertices receive coherent volume/crease relaxation. Original retained shape coordinates are exact. A new additive paw/contact correction on a 4×9 Seat/WeightShift grid repairs the inherited two-hand span after the support path changed; it activates only while both hands hold. It does not edit the original paw keys or single-hand poses. Maximum distal adjustment is 0.0154081 scene units; arbitrary item spans/regrasp remain unverified.

[Inheritance](inheritance.json): 14 mesh Basis coordinates, polygons, UV and packed texture bytes match v003; all original bone rest matrices/lengths and control names remain. The removed Torso support keys are explicitly listed. All face shape keys are unchanged. [90 inherited/composed face witnesses](v003-face-regression.json) differ by at most 1.238e-7 after registering the intended head transform; head translation caused by sitting is not mistaken for a face edit. Neutral return error is at most 2.910e-8.

## Focused evidence

- [505 support samples](support-regression.json): Seat 0–1 at 0.01 increments × five WeightShift values; finite coordinates, no vertices below −0.001, no invalid drivers. Overall minimum −1.143e-5. Whole-foot pair-distance error ≤9.537e-7; original foot thickness/length is preserved under its rigid transform.
- At full Seat / zero shift, the rump subset minimum is 0.0017515 and 11 vertices enter the `<0.004` near-floor band; the left sole center has moved to Y=−0.194322. At extreme shifts, rump minima range 0.0013545–0.0022741. The review floor is at −0.002. Thus the rump's smallest geometric clearance is about 0.00335–0.00427, not a simulated finite-area loaded contact patch. These bounded near-contact measurements and shadows do not establish physical mass/COM or a complete dynamic support solution.
- [Holding](grip-audit.json): 15 standing/mid/full-seat and lateral witnesses; span 0.3365623–0.3366792, within the inherited 0.001 tolerance after correction.
- [Composition/independence](capability-regression.json): occupied-paw arbitration, four stroke zones, independent foot lift/side/forward and free target rotation pass the focused assertions. [Composed face visibility](composed-face-occlusion.json) also passes the inherited audit.
- [Baking](bake-verification.json) and [all-frame floor](proof-floor.json): 821 frames; evaluated-to-baked maximum 7.207e-7, floor minimum −1.119e-5. This is a bounded rig proof, not a physics solver.

The saved GLB reimport passes [vertex/Morph comparison](glb-roundtrip.json) for all 91 witnesses: maximum positional error 1.052e-6. [Seven Anchor matrices × 821 frames](anchor-roundtrip.json) and the [diagnostic held-sphere fixture](fixture-roundtrip.json) pass their inherited tolerances. [Numeric accessor invariance](numeric-repack-invariance.json) confirms restoring the original 12 embedded texture byte streams did not change Skin/Morph/animation accessors. [Schema validation](schema-validation.json): zero errors in each GLB, with 14 inherited `NODE_SKINNED_MESH_NON_ROOT` warnings per file; unused-UV informational messages are not visual approval.

[Saved GLB and editable Blender, five poses](saved-glb-comparison.png) was opened: the forward-foot posture, eyelids, body contour and return match visually at the shown 3/4 angle; no missing Skin/Morph or material reset is visible there. The same residual thigh junction and underbelly crease remain in the saved asset. Texture/UV/material details are in [glb-attributes.json](glb-attributes.json) and [texture-material-restoration.json](texture-material-restoration.json). The new two-hand correction was followed by a fresh proof export, reimport audit and affected full-body/face renders. Other render states activate none of those additive two-hand corrections.

The five `saved-view-{neutral,legs-forward,seat,seat-rest,standing-return}.png` eight-angle boards were also opened: both sides and rear views retain the same support silhouette and limitations as the editable asset. No additional missing part or saved-only shape failure was observed in those views.

## Continuous excerpts

- [Seat → rest → return video](seat-return.mp4), 29 actual saved-proof frames; [1–31](sequence-00.png), [37–67](sequence-01.png), [73–103](sequence-02.png), [109–139](sequence-03.png), [145–169](sequence-04.png).
- [Seated composition video](seated-compositions.mp4), nine consecutive saved-action samples; [589–609](composition-sequence-00.png), [613–621](composition-sequence-01.png).
- [Full video frame provenance](video-provenance.json).

All these frame boards were actually opened. Legs move forward before settlement and the silhouette returns to Neutral; smooth samples do not establish believable effort or loaded contact. The return remains a simple reversed trajectory. Occupied paw poses reveal pointed shoulder/armpit folds from side/rear 3/4. They are explicitly **appearance HOLD**, despite the numerical holding/Anchor PASS. These findings are included in [visual observations](VISUAL-OBSERVATIONS.md).

## Limits and next owner

Codex owns technical corrections and reporting; Human owns cuteness, comfort, identity and naturalness approval. Resolve the harder side thigh/abdomen contour and return effort before appearance adoption. Exact zero-gap rump contact and physical support under dynamic motion remain HOLD. Smartphone/PlayCanvas Skin normals, performance, arbitrary FK/expressions/items and production interaction integration are unverified. No PWA, original/v001–v003, other-character or user image edits are part of this delivery.

Work began on `codex/grimo-motion-zero-based-design-20261011` at `d21689b8a2c094674e0ed230313610b26800c304`. The requested remote Character appearance lock at `2abea76fad578281f74b9fa628987a80b56ad6dc` was inspected and safely fast-forward integrated with the current work retained. Its rule that technical equality/contact cannot overrule posed appearance is applied to this HOLD.

[Final protection audit](protected-input-verification.json): 4,002 recorded inputs, no missing files; only the authorized remote AGENTS update and consequential Handoff update differ. Original/v001–v003 assets, other characters, the three pre-existing edited geometry review images and supplied untracked reference/model files retain their starting hashes. Only v004 assets, scripts/evidence and the Handoff change are included in the delivery commit. No force push or destructive reset is used.
