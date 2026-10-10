# GRIMO — Tripo Generation Pose Contract (Jill / Pino / Shushu)

**Status:** DRAFT — requires Human visual approval; not a new canonical image or geometry authority  
**Date:** 2026-10-11  
**Goal:** Create high-fidelity base bodies for Tripo reconstruction with later Blender rigging, Pikachu/Eevee-inspired contact, and PlayCanvas GLB motion.

## 0. Authority and limitations

1. Existing original character identity image remains the appearance authority. A newly generated pose image is only a derivative production input after Human approval; it never replaces the original identity.
2. Source: `/mnt/data/{jill,pino,shushu}-identity-canonical(2).png` and Grimo's `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md` and `GRIMO_CHARACTER_EXPERIENCE_SPEC.md`.
3. Tripo generation pose, Blender armature rest pose, and in-game interaction neutral are three **distinct concepts**. The latter two may be related but must not be treated as automatically identical.
4. This document specifies **proposed angular/clearance starting values, not measurements extracted from a 3D asset**, validated physics, or Tripo-specific guaranteed tolerances. All proposed values must be visually re-evaluated after producing 2D multi-view reference candidates and actual 3D geometry.
5. No Tripo generations, rigging, collision simulations, or physical balance tests have occurred in preparation of this contract.

## 1. Common generation-pose contract

Coordinate conventions for 3D drafting: the character looks toward **+Y**, its right is **+X** (define consistently in export pipeline), up **+Z**; floor `Z=0`. Front camera looks toward -Y; rear toward +Y. X-side cameras are true orthographic profiles. Establish these conventions in Blender before export. Image labels must be unambiguous; never mirror a side image and silently use it as the opposite side.

- **H:** height of retained solid anatomy in generation pose (feet to highest retained body/head appendage), excluding independent wearables, scene VFX, petals, detached blossoms, bubbles and loose ornaments.
- **W:** outer width of the main torso at the widest point, excluding wing, arms and tail.
- Body centered; head facing forward; head yaw/roll target 0° and natural small pitch ≤5°; no forced expression symmetry.
- Body axial pitch ≤10° unless a character-specific exception is approved. No strong 3/4 pose, perspective foreshortening, tilt, cropped silhouette, or ground shadow that hides feet.
- Relaxed **creature-specific open pose**; **never stretch short limbs just to imitate an adult human T-pose**.
- Each forelimb's non-shoulder portions must have a visible contour at least in Front and a distinguishable contour in Side. Prefer **~0.025–0.05H** projected clearance wherever there would otherwise be ambiguous limb/torso overlap. Natural shoulder/hip attachment stays continuous.
- Two hind feet are identifiable, with inner contours not fused; preferred front-projection gap between neighboring distal feet ≥~0.02–0.04H. A small failure of one image-space threshold is not by itself a reason to distort a canonical body.
- Tail root visibly joins the pelvis, but the free tail must not fuse to a leg/flank. At least one profile clearly describes base, curvature and tip. The tail is never chopped off or shortened to fit a frame.
- Ear/head, wing/back and tail/root anatomical joins **stay joined**. Artificially separated 'floating body parts' are prohibited.
- All images of a given character depict **the same 3D pose**; no different paw locations, head yaw, wing deployment, or tail route in different views. All views use matched orthographic framing and diffuse studio lighting.
- Use a plain neutral background; normal anatomical details, colors, facial markings, eye highlights, pads, scales and clover marks retained. No scenery, contact shadows that resemble feet, or carried props.
- **Independent-decoration separation:** Maintain identity-essential natural anatomy (including biological ears, wings and tail). Detach clearly accessory-like flowers, crown, bouquet, water/bubbles, floating petals/butterflies/stars. On Jill, head fronds/leaf mane and tail spikes require an explicit **anatomy vs decoration** classification before erasure, not wholesale removal.
- Numerical values are **starting hypotheses for a pose illustrator**; visual checks and approved anatomical shapes supersede them. The user must approve the production Front before progressing to other views.

## 2. Jill — J-GEN-01: low, grounded creature A-stance

### Proposed posture

- Support: **two hind feet**, flat and grounded, knees lightly bent (**~15–30°** from full extension); pelvis remains low, torso rounded and belly prominent. Keep head-to-torso proportion consistent with canonical source. Do not lengthen legs or forearms.
- Torso: near-vertical or mild anterior inclination **~0–6°**. Head looks directly at camera (yaw/roll 0°), while preserving face shape, green-eyed appeal, ear shape and friendly expression anatomy.
- Hind feet: mildly outward (**~5–15°** toe-out) and laterally spaced sufficiently to expose each foot and its base. Thighs remain massive and short; no humanoid waist.
- Arms: short, arms move laterally apart **~25–40° from relaxed downward direction**, relaxed elbows **~10–20°**; forepaws point down and slightly forward, hands do **not** rest against belly or thigh. Ensure contours around lower forearms from front and side.
- Wings: attached symmetrically at the back; modestly open in a way that reveals wing roots and membrane in front and an actual thickness/attachment in side. Target **~20–35°** more open than their naturally folded pose, only insofar as this doesn't change canonical span/outline. Do not make a straight human T-wing. Front silhouette separated from both arms and head leaves. Keep wing joint recoverable for flapping.
- Tail: thick continuous root at rear pelvis; curve to **one side and behind** to expose the full root, central section and tip without touching either hind leg or wing membrane. Preserve the canonical tail's *thick, sweeping and upward-curled* visual language. Do not copy a front-of-body decorative curve as an implausible 3D intersection.
- Preserve: eye shape / colors; short fangs and mouth design; ear shape; natural head/neck leaf mantle; belly plates; clover body marking; tail ridges; anatomical wings.
- Independently authored: floating leaves and particles, detached blossoms, butterflies, ground vegetation/flowers. Individual flowers worn on the body require an explicit attachment classification before removal.

### Risks

1. Wing membranes and leafy mane may merge -> isolate root vs membrane boundaries; no loose floating leaves in base reconstruction.
2. Tail curls across the side camera's foot -> reroute the *pose* rearward, not shrink the tail.
3. Character becomes a tall humanoid dragon -> reject; use original head/hip/leg proportions.
4. Arms touch belly after restoration to neutral -> test shoulder bend before accepting generated geometry.

## 3. Pino — P-GEN-01: round upright soft biped, no held bubble

### Proposed posture

- Canonical image is a dynamic, reclined 'bubble-play' pose, not an ideal generation/rest posture. Preserve the body design, not that momentary limb arrangement.
- Support: **short hind feet on floor**, mild knee flex **~15–30°**, low center of mass; preserve short legs, plump torso and large round head. Do not lengthen the torso or make the waist thin to achieve standing.
- Torso: up, with slight natural forward incline **~0–8°**; head upright yaw/roll 0°. Ensure both ears and head tuft remain intact.
- Arms: no bubble held; short forelimbs symmetrically **~30–45° out from relaxed downward direction** and **~5–15° forward** so both hands can be segmented from chest. Wrists/forepaws visible from front and side. Do not change them into human hands.
- Feet: inner contours remain independent; soles generally face **floor**, not camera, in this production pose. Pink pad geometry is still an authority from the canonical illustration, but may require separate underside reference/Blender material work because it will be naturally occluded in a standing Front view. Never relocate pads onto the front of the shins.
- Tail: preserve broad, thick otter-like tail; root exits pelvis/back, runs behind then to one side, smoothly curled upward as far as feasible, with its complete path visible from an appropriate side view. No tail/foot fusion and no floating isolated tail.
- Face: canonical wink is an **expression**, not missing eye anatomy. Keep anatomical capacity for **both fully modeled eyes**, and reserve the wink as an authored expression; original eye design must remain visually consistent.
- Independently authored: held bubble, external bubbles, water sheets/splash VFX, droplets. Retain paws, ears, head tuft, tail as anatomy.

### Risks

1. Pose transfer from recline to standing invents long hidden legs -> require a distinct Body-only Front Human Gate before generating Side.
2. Foot pads disappear from model because soles face floor -> underside detail/reference and mesh validation.
3. Tail mistaken for fin or separate bubble -> require side/profile clarity, classify attached tail.
4. Both hands become fused to chest -> reject and adjust arm distance before spending another generation credit.

## 4. Shushu — S-GEN-01: very low biped squat, pre-sit neutral

### Proposed posture

- Canonical image is deeply seated with feet directed at camera and both arms holding a bouquet. This is *not* the Tripo mesh-generation pose.
- Support: two short, wide hind feet on floor, knees **~30–50°** bent, pelvis *very low* without the entire hip/butt underside settling into the ground. Forebody remains a rounded continuous plush volume, not a slim standing panda.
- Torso: soft almost-vertical pose, inclination **~0–5°**; head level and facing front, ears large and spatially separated from head outer silhouette.
- Arms: no bouquet; move short pink forepaws outward **~25–40° from relaxed downward direction** and **~5–15° forward**, giving each forearm a clearly distinguishable boundary. Keep rounded paw shapes, with natural shoulder attachment.
- Legs: keep short thick thigh stubs and feet independently readable from front and profile. Foot-pad surfaces naturally face down/diagonally forward in production pose; record original full pads from canonical for seat-pose reconstruction. No added long visible shins to imitate a standing bear.
- Abdomen: near legs but not fused to front paws or the ground plane; large cream belly stays round and recognizable.
- Expression: eyes, pink eye patches, round ears, gentle face and paw-pad design preserved. Two independently poseable forelimbs remain available for offering and touching.
- Independently authored: worn flower crown, held bouquet, petals/butterflies and ground flowers. Reattach with head/hand anchors after rigging; never paint the bouquet permanently into the belly mesh.

### Risks

1. Short hidden hind legs may be hallucinated -> low squat, human visual review of leg length and foot anatomy, reject elongated/shrunken results.
2. Seated pads lost in forward-facing render -> make supplementary sole diagnostics, not fake foot-pad placement.
3. Rounded hands fuse with belly -> expose actual lower arm contour, and test reach deformation.
4. Squat-to-sit causes belly/thigh collapse -> validate in Blender with proper weights and possibly corrective shapes; if collapse is unfixable and canonical pose changes too much, *alternate S-GEN-02* is an **arms-open, legs-separated seated geometry pose** with Blender manual rigging. Test this alternate with low-cost geometry preview before switching, not on assumption.

## 5. Virtual failure scenarios — reasoning-based preflight, NOT computed model validation

| Scenario | Jill | Pino | Shushu | Required gate |
|---|---|---|---|---|
| Distal forelimbs fuse to torso | Medium | High | High | Front + Side contour + actual wireframe after Tripo |
| Tail fuses to body/leg | High | High | Low/not salient | Side + rear and topology inspection |
| Wing/leaf geometry confusion | High | N/A | N/A | Clear wing and mane boundaries |
| Anatomy/ornament accidental merge | High | High (bubbles) | High (bouquet/crown) | Body-only classification and compare to original |
| Unnatural anatomical proportions | High (overlong limbs) | High (recline-to-stand) | High (sit-to-stand) | Human approval against identity |
| Bad rig/pose transition | Medium | Medium/High | High (deep sit) | Blender prototype deformations |
| Loss of paw sole detail | Moderate | High | High | Sole diagnostics + material review |

These rankings are expert hypotheses and do **not** represent experimental failure rates.

## 6. Pre-Tripo 2D review gate

For each character, create and Human-approve a new **Body-only Generation Pose Front**, using original canonical as *style/identity* reference (not direct orthographic authority). Then use the approved pose Front to derive true Side + Back and Opposite Side when necessary, all **same posture**, with separate human checks. Any view containing new anatomy invented to solve projection conflicts must be reviewed.

Check:

1. Identity: recognizable eyes, face, head/torso/limb ratios, signature geometry, colors, motif placement.
2. Front: limbs and wings separated at the intended movable sections; no forced humanoid articulation.
3. Side: head and muzzle volume, belly/front profile, appendage roots, hind limb/foot thickness, tail trajectory.
4. Back: roots and appendages anatomically attach; body taper/legs and pelvis plausible; no cylinder or fused leg silhouette.
5. Same pose from view to view; no mismatched feet, joints, head tilt, wings or tail.
6. Decoration removal did not erase natural body/fronds/material markings.
7. An image failing an essential criterion stays a **candidate**; never promote to formal authority.

## 7. Tripo test + Blender motion smoke gate

- Official Tripo pages currently differ on '1–3' vs '2–4' multi-view images. Verify **actual available Studio slots, model mode, credit costs** before submission; do not assume an API capability equals Studio capability. Favor consistent Front/Side/Back when only three can be submitted; retain Opposite for audit/selection or fourth slot if supported.
- Generate **one economical mesh preview per character**, not bulk runs. Read geometric result before pursuing textures, auto-rigging or higher quality.
- Inspect the mesh in flat shading, front, side, back, 3/4, and low/bottom angle. Confirm projected clearances correspond to actual geometry rather than painted lines.
- Tripo official Help Center says Auto Rig for uploaded existing models supports T-pose humanoids and standard standing quadrupeds and warns non-standard poses/creatures may fail; do **not** assume a stylized winged or seated companion auto-rigs successfully. Test only where justified; **Blender custom rig + weight painting is the fallback**, not a change in character anatomy.
- In Blender, treat generated pose as the starting mesh configuration; select/set the actual armature Rest Position intentionally. Derive each in-game **Interaction Neutral** after rigging.
- Rig smoke checks per character (working motion, no clipping, preserving identity): (a) head yaw ±20–25°; (b) unilateral cheek/head touch response; (c) each forepaw reaches forward ~25–40° without torso fusion; (d) settle from rest into target Interaction Neutral (Jill low grounded stance, Pino sitting, Shushu plush deep sitting); (e) tail yaw ±15–20° if present; (f) Jill wing small flap 10–20°.
- Joint-angle test values are **motion smoke-test initial estimates**, not new Grimo final-motion specs. Fix actual mesh/weights or pose before further paid generations.

## 8. Decision and immediate next step

**Working candidates:** `J-GEN-01` low creature A-stance; `P-GEN-01` soft upright neutral; `S-GEN-01` squat-to-sit convertible low standing. For Shushu, `S-GEN-02` modified seated remains a contingency only if low standing causes excessive identity or rig damage.

**Next action, BEFORE Tripo or completing all sheets:** Create **Jill Body-only Generation Pose Front candidate**, then Human review, then build same-pose side/back views. Pino and Shushu follow their own Human gates.

## 9. Source links (external context)

- Tripo official Help Center: https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation
- Tripo multi-view preparation: https://www.tripo3d.ai/blog/multi-view-reference-images-3d
- Tripo additional multi-view discussion: https://www.tripo3d.ai/blog/multi-view-to-3d
- Tripo AI rigging limits: https://www.tripo3d.ai/blog/prepare-creature-mesh-before-auto-rigging
- Tripo source-image artifacts: https://www.tripo3d.ai/blog/tripo-pix-anime-3d-characters
- Blender Armature Rest/Pose: https://docs.blender.org/manual/en/5.3/animation/armatures/posing/introduction.html

**Do not lock this draft until Human pose reference approval and first 3D-generation result.**
