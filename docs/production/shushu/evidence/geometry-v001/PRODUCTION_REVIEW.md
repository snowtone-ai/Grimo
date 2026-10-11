# Shushu — Candidate B geometry convergence v001

**GO for this bounded editable geometry/deformation candidate. HOLD for production acceptance. Human Gate: PENDING.**

Production branch: `codex/grimo-motion-zero-based-design-20261011`. Verified input remote HEAD: `749675cac5ebdb07587e715eb2cb59bfcae2768f`. The commit containing this report supplies its final revision; no merge to main. Live routing is on `coord/grimo-ai-handoff`, not the production branch's handoff copy.

## Review entry points

- [Before / after and approved authority](before-after-review.png)
- [Face: open, half, closed, reopen, independent sides, gaze, mouth](face-review.png)
- [Support, paws, contact, head and local pressure](support-contact-review.png)
- [Actual sampled face timeline](face-timeline.gif)
- [Actual sampled settle / rest / recovery timeline](support-timeline.gif)

The source and repaired comparisons use the same studio lights, camera directions, orthographic framing and provisional colors. Full-body cameras are slightly elevated so the marked ground plane and feet remain visible; an upward-looking orthographic floor view was discarded because it occluded the legs. Canonical/reference images are unchanged. Raw full-resolution renders remain in `renders/`; there is no flattering-camera-only acceptance claim.

## Saved assets and editing

- [Editable production-owned Blender candidate](../../../../../assets/grimo/production/shushu/blender/shushu-geometry-v001.blend)
- [Focused skin + morph + animation GLB](../../../../../assets/grimo/production/shushu/runtime-probes/shushu-geometry-v001.glb)
- [Separate neutral geometry-only GLB](../../../../../assets/grimo/production/shushu/runtime-probes/shushu-geometry-v001-static.glb)

Blender 5.2.1. The original FBX/GLB bytes and five authority/reference PNG hashes are verified unchanged in [focused-validation.json](focused-validation.json). A hidden `SOURCE_B_REFERENCE_ONLY` collection also retains the complete normalized source topology for editing/provenance. It is not rendered or exported as the repaired character.

The eight useful source volumes remain semantic modules: head, torso, two ears, two short forelimbs, and two short hind limbs with feet. Their surfaces were repaired independently; exterior continuity does not depend on combining every source island. Generated eye caps were replaced; overlapping superficial source strips/details are classified and retained in the hidden donor. This does not promote the earlier eight-component scratch to approved truth.

Edit `Shushu_Head` shape keys `Blink.L` / `Blink.R`, `MouthOpen`, `CheekPressure.L`; the blink arc corrective follows each blink through a driver. Iris/highlight gaze keys are separate. `SupportedRest` and `WeightShift` exist on their owned modules. The short forepaws use independent `Paw.L` / `Paw.R` bones; sole ownership includes separate foot bones. `Shushu_DeformationRig` is a development rig, explicitly not the final production Rig. The scene contains a 1–120 frame capability proof at 24 fps.

## What materially changed

**Face:** damaged orbital and mouth relief was replaced locally. Eyelid skin is connected to the donor head through radial transition rows; it is not an added floating spherical lid. Recessed convex eye surfaces, separate bounded gaze, conforming highlights, a curved lid margin, and an intermediate blink corrective prevent pupil/highlight exposure through closing skin. The small curved closed mouth opens into a minimal recessed bowl and shallow floor. Large head, cheeks and ears were retained; no human fingers or enlarged mouth were introduced.

**Lower body:** source sole surfaces were flattened locally and protected. A broad continuous plush shank/thigh deformation distributes settling across the actual short leg, with restrained local expansion, instead of driving a thin human-style knee into a fold. The candidate's low rest lowers the body by **0.065 character-height units** and is supported by both feet. It is **not a deep seat or belly-supported sitting pose**. No Game Neutral choice is made.

**Head/paws/plush:** head-base ownership blends into the neck, and head/paw pose pivots account for the support morph. Forepaws rotate without stretching their source volume. A large sphere proved unreachable after removing the earlier shoulder stretch; it was replaced by a small test handle fitted to the real paw surfaces. Local cheek/body pressure uses protected spatial fields, followed by exact recovery; it never scales the whole character.

## Actual capability verdicts

| Capability | Technical verdict | Observed outcome / boundary |
|---|---|---|
| Independent open → half → closed → reopen | **GO, bounded** | Actual head surfaces cover both eyes. Each side has 513 exposed samples open, 312 half, **0 closed**. Closing one side leaves the opposite side's 513 samples exposed. Intermediate skin follows the eye surface. Human naturalness/cuteness is pending. |
| Gaze + representative blink | **GO, bounded** | Independent surface-projected iris/highlight movement, lateral ±0.006 and vertical ±0.004 height units. Combined left blink/right gaze evaluated. Not unrestricted eye rotation. |
| Small mouth open/closed | **GO, bounded** | Connected surrounding skin changes the actual aperture, with a small interior about 0.013 units deep. No completed Food animation, teeth or large tongue system. |
| Standing → settle → low rest → recovery | **GO, bounded** | 142/144 sole samples stay fixed; no leg vertex goes below ground. Rest leg edge ratios approximately **0.471–1.141**, instead of the prior folding/penetration. Head/torso primary volume survives. Recovery error **0**. |
| Deep sitting / seated daily Neutral | **UNKNOWN / HOLD** | The earlier failed deep seat is not repaired or relabeled as passing. This candidate demonstrates a shallow foot-supported rest only. Daily Neutral remains Human-owned. |
| Head turn/tilt, single low paw offer | **GO, bounded / HOLD for perceptual acceptance** | Head yaw 18°, pitch 8°, roll 7° example; separate low forepaw offering. Short paw length and shape are preserved. These are tested amplitudes, not approved final limits. |
| Reachable two-paw holding | **GO for the test handle** | Both paw/handle surface gaps are below **0.000063** units. Torso clearance is about **0.0274**, head clearance about **0.0329**. No arm lengthening or prop-through-belly solution. This is tangent support of a small handle, not a complete grasp/bouquet system. |
| Holding + cheek touch response | **GO, bounded** | The held pose persists during a 5° pitch / 7° roll head response and local cheek pressure. Head/handle clearance remains about **0.0289**. An external touching hand and a self-paw-to-head grooming action are not supplied. |
| Local plush pressure/release | **GO, bounded** | Cheek and belly change locally. Eye, iris, lid margin, nose and mouth modules move **0** under the isolated pressure probe; reset error **0**. Human softness/weight acceptance remains pending. |
| GLB interchange | **GO, focused** | One combined animation, one skin, eight joints, two maximum bone influences, normalized weight sums. Morphs include sampled blink corrections. Sixteen actual source/import frame comparisons pass; worst bidirectional nearest-vertex error **1.73×10⁻⁶**, tolerance 2×10⁻⁵. Skin uses standard linear blending, not Blender-only dual quaternion deformation. |
| Human identity / naturalness / final production | **HOLD** | Technical success does not grant Human approval. Review the visual package before committing to final UV, texture or rig services. |

Detailed reproducible numbers: [measurements.json](measurements.json), [focused-validation.json](focused-validation.json). The head's intentional open boundaries are the two moving eye apertures and mouth; core modules have no edges with more than two incident faces. Export/import testing checks actual animated surfaces, and includes meaningful source motion guards rather than accepting an entirely static clip.

## Remaining visible and technical limitations

- The donor's lower-head outline still reads more squared than the painted Canonical. Side/back head banding and mild orbital transition relief remain visible under the neutral studio; final facial color/eye ornament, fur, pads and material polish are absent. The review images expose these differences.
- Low rest visibly compresses the short upper leg, but deeper sitting and broader pose combinations remain unproven. Feet are the actual support; the abdomen is above ground.
- Forepaws currently preserve volume through mostly rigid articulation. Extreme shoulder motion, large props, unilateral bouquet holding, grip compression and self-grooming are not certified. The tested handle is a reach/contact fixture.
- This is editable candidate geometry with local control loops, not a claim of finished all-quad production topology. Spatial coherence at the demonstrated views/poses is assessed; comprehensive collision certification and mobile runtime performance are unknown.
- Units are normalization units, with height approximately one and scene scale one. A physical character size has not been approved. Export changes Blender Z-up/front −Y to glTF Y-up/front +Z; reimport equivalence verifies the actual orientation and rest/animation data.
- Final Rig, Motion library, Texture, Wear, crown/bouquet, complete Food animation and smartphone runtime are not completed.

## Tripo: verified facts and next operations

No Tripo generation, API endpoint, key creation, upload, credit spending or free attempt was executed. The read-only browser inventory timed out; authenticated Studio import and available UV/Texture/Rig operations for **this repaired asset remain UNKNOWN**. Geometry work was not blocked on authentication.

The [current official upload/animation help](https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation) documents GLB/OBJ/STL/FBX upload and Auto Rig, with T-pose humanoid / standard standing quadruped limitations. The [official import documentation](https://docs.tripo3d.ai/model-generation/import-model.html) documents downstream processing of imported assets. This establishes documented features, not this user's session entitlement or successful handling of Shushu.

1. **Skip** global regeneration, Mesh Edit, Segmentation and global Retopology by default. They have no demonstrated benefit over these regional repairs and may replace identity/control topology.
2. **Delay** Smart UV / Texture until Human accepts the geometry/face and the actual Studio import screen confirms the desired imported-model operation and cost. Use the separate static GLB for a no-processing compatibility check if the UI explicitly permits that without credits/trials. Keep the editable/animated derivative out of topology-changing processing.
3. **Test before spending** whether imported modules and topology survive, whether UV/Texture results can transfer back to the same geometry, and whether a non-finger short-animal skeleton is available. Do not default to Humanoid/Mixamo, stretch limbs, invent fingers or force a T-pose. Auto Rig suitability for this A-pose remains UNKNOWN.
4. Remesh before final rigging when necessary; preserve the proven Blender facial morphs/correctives and revalidate any service result rather than assuming they survive.

**Next Human decision:** accept or reject this candidate's identity, integrated open/half/closed eyelids, small mouth and bounded low rest using the compact evidence. Standing versus seated Game Neutral is still a separate unresolved decision; nothing here settles it.

## Reproduction

From repository root, with Blender 5.2 and the existing source feasibility asset available:

```powershell
blender -b -t 6 --python scripts/blender/build-shushu-geometry-v001.py
blender -b -t 6 --python scripts/blender/validate-shushu-geometry-v001.py
blender -b -t 6 --python scripts/blender/review-shushu-geometry-v001.py
python scripts/blender/shushu-geometry-v001-boards.py
```

The last command uses the existing Pillow workflow to arrange images and make short GIF previews. Review-only temporary frame PNGs stay outside the repository. No external service is needed.
