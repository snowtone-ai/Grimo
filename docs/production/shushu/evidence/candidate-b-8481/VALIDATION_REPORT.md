# Shushu Candidate B 8481 — production feasibility validation

**Decision: B / defined structural repair required. GO for targeted Blender repair; HOLD for final production acceptance.**

Remaining Tripo opportunities: **1, UNTOUCHED**. No generation, Mesh Edit, Auto Rig, credit use, paid operation, subscription change or external publication occurred. Human identity/cuteness/naturalness approval remains pending.

## A. Executive verdict

B is a useful **volume and silhouette donor**, not a finished deformable character. Keep its large head, rounded torso, short separate forelimbs, ears and independent feet. The tests do not justify discarding those volumes or consuming the last generation. The most reliable route is **partial targeted reconstruction/retopology** around eyes/lids, mouth interface, neck/shoulder overlaps and lower-body deformation regions, while preserving the approved proportions.

This is stronger work than a topology review: Blender actually evaluated 24 body/raw-face states, 10 localized facial reconstruction states, local support smoothing, 81 bounded contact combinations, concurrent head touch while holding, and a skeletal/morph GLB export/reimport. Successful transformation is not declared natural animation readiness.

## B. Input integrity and provenance

- Working branch: `codex/grimo-motion-zero-based-design-20261011`.
- Input HEAD: `65dcab996f0963ae2054d8474f07cf0fafaca608`.
- Upstream: `origin/codex/grimo-motion-zero-based-design-20261011`.
- Initial working tree: exactly the six supplied files, all untracked; no staged or tracked modifications.
- Blender: **5.2.1 LTS**. Git LFS: **3.7.1**. Existing `*.glb` and `*.blend` LFS rules were followed. Historical JSONs have narrowly scoped `-text` attributes to preserve supplied bytes across Windows/Linux checkouts.
- All six originals were moved without renaming into the paths in [input-manifest.json](input-manifest.json). Before/after SHA-256 equality was asserted. No original was resaved.
- FBX binary signature/version 7400, GLB v2 chunk/length/JSON structure, both JSON documents and both PNG decodes were verified. Historical PNGs are 2050×1960 and 1800×1860. Historical JSONs have no formal schema and cover A/B/C/D.
- Original FBX: **361,520 bytes**, SHA-256 `6420ce386c0dc1a19dc0a9b5dc827a3d247f91c6cc4f83cd883e79f5ff3fe06d`.
- Original GLB: **366,032 bytes**, SHA-256 `803937cd10bd48d5b15be9f6dca43a38183ec730ed0b62eb2820fd160d14d448`.
- Both hashes match historical B, independently establishing candidate identity. **A/C/D were not freshly validated**; their raw meshes were unavailable in this intake.
- Canonical and all four approved body-only PNGs were actually viewed and inventoried without changes. Left/right names follow the register's **image-facing** convention.

Authority consulted: Knowledge Index, Production Operating System, Character Production Architecture, Blender Implementation Guide, Motion-to-Anatomy contract §D and Shushu requirements, Four-Character Motion Architecture §H and relevant holding/Wear rules, and the Body-only Register. Historical task-specific prohibitions in draft design documents do not override this explicit experimental-validation request. Project Memory was not retrieved or invented. No personal-wiki context was used.

## C. Measured geometry

Full reproducible details and localized edge coordinates: [independent-audit.json](independent-audit.json).

| Measurement | Independently measured B |
|---|---:|
| FBX vertices / polygons | 8,259 / 8,481 |
| FBX quads / triangles / ngons | 5,373 / 3,108 / 0 |
| GLB vertices / triangles / edges | 8,259 / 13,854 / 22,039 |
| Boundary edges / >2-face non-manifold edges | 2,546 / 28 |
| Inconsistent winding on two-face shared edges | 11 |
| Boundary graph loops / chains / branched components | 88 / 9 / 16 |
| Exact duplicate positions / duplicate faces / unused vertices | 0 / 0 / 0 |
| Triangle area below 1e-12 | 0 |
| Edge-connected face components | **123** |
| Vertex-connected face components | **90** |
| Tiny edge components (<10 faces) / total area fraction | 22 / 0.2408% |
| Triangle area sum | 2.94124237 normalized units² |
| Longest edge / altitude, p95 / maximum | 3.7851 / 107.4398 |
| Triangles with that ratio >10 | 43 |
| Strict transverse intersection pairs, original GLB | 1,373 |

Raw GLB bounds: X ±0.379150390625, Y 0…0.99951171875, Z ±0.291748046875. Height is approximately one **normalization unit**, not a declared physical panda size. Blender uses X/right, Y/back, Z/up; original GLB uses Y/up and Z/front. Original object hierarchy/transforms are recorded in the audit.

FBX↔GLB normalization yielded a unique one-to-one match for **all 8,259 vertices**, maximum distance **6.0643e-8**, RMS **3.1411e-8**. Every FBX polygon boundary edge exists in GLB; GLB adds 5,373 quad diagonals. Every source triangle/quad has a matching GLB triangulation. Thus these are the same geometry, with the expected triangle conversion, not two competing candidates.

Quantized-position diagnostic welds at 1e-7, 1e-5 and 1e-4 did not change counts. They were performed on arrays only. Bin boundaries can miss nearby pairs and larger tolerances could falsely merge nearby layers; the original was never welded. Vertex separation here is **not explained by UV seams or duplicate normal-split positions**: source GLB has POSITION/NORMAL only, no UV, textures, skins, morphs or animation. FBX also has no UV layers or shape keys. One plain material is present. Export normals are near unit length; two triangles have average vertex normals opposing geometric face normals.

The large edge-connected parts are anatomically informative: head 2,432 GLB triangles, torso 1,526, legs/feet 1,081 and 1,078, ears 916 and 907, forelimbs 692 and 691. Separation is not automatically a defect; their overlapping attachment interfaces become consequential under articulation. Many remaining parts are thin surface strips or local details, including eye caps. They must be classified before production cleanup.

**Historical reproducibility:** the principal counts, boundary/winding graph, areas and hashes reproduce. The supplied claim of 96 edge-connected components with a 13,706-face largest component does **not** reproduce under either explicit edge or vertex adjacency. The original diagnostic algorithm was not supplied, so its exact error cannot be established. This discrepancy cannot be attributed to a different input file. Historical `aspect_ratio_p95=0.79` has no stated formula and is not comparable to the standard edge/altitude ratio above.

Intersection detection uses BVH candidates plus strict interior segment/triangle crossings, excluding shared-index neighbors. Coplanar overlaps and contacts at endpoints remain UNKNOWN. Counts include designed modular overlaps and thin surface detail; they are **not** a count of visible defects. Examples and locations are recorded, and stressed-vs-neutral comparisons are interpreted together with renders.

## D. Canonical visual comparison

See [canonical-comparison.png](canonical-comparison.png), plus eight controlled source views and front/front-threequarter wire renders under `renders/`. Orthographic scale 1.2, fixed target (0,0,0.5), consistent Workbench lighting, framing and source generation pose were used. Wireframe is added only for its corresponding view; artwork was scaled into evidence panels without modifying reference files.

**Visual observations:** the large cranium, full lower cheeks, circular ears, rounded torso, short independent forelimbs and distinct hind feet provide useful source volumes. B's face is comparatively box-like at its lower outline, with simplified eye caps, small hard orbital borders and angular mouth detail. Head/body and limb/body interfaces contain visible surface strips and overlapping seams. The feet are distinguishable but lack final sole/pad appearance. Side and rear volume are present rather than a front-only shell. Crown/bouquet meshes are absent.

**Predicted risks:** socket/lid seams, lower-face edge flow, attachment-interface exposure and thigh/knee/ankle folding need work. These observations do not certify final identity or material cuteness. The asset has no final textures/materials; the deliberately plain eye reconstruction proof is mechanically informative and aesthetically unfinished. Its protruding interfaces must be fitted and blended before perceptual review. Canonical infant-like proportions must be preserved, rather than changing head size, limb length, torso thickness or ear size for rig convenience.

Generation Pose, Rig Rest Pose and Game Neutral remain distinct. “Neutral” in evidence means the imported pose or its diagnostic reset. **Standing/sitting Game Neutral has not been selected.**

## E. Anatomy and motion test matrix

Measurements: [deformation-measurements.json](deformation-measurements.json), [facial-repair-and-roundtrip.json](facial-repair-and-roundtrip.json), [contact-feasibility.json](contact-feasibility.json). Boards: [deformation](deformation-contact-sheet.png), [raw face](raw-face-probes.png), [local face repair](local-face-repair-proof.png), [support/seams](support-and-seams.png), [contact/handoff](contact-and-handoff.png).

PASS means only the named measured condition passed. It never confers Human or final rig approval.

| Capability / executed experiment | Verdict | Evidence and remaining work |
|---|---|---|
| A — bilateral raw eye structure; upper orbital skin moved for half/closed L/R | **FAIL for tested raw blink** | Surface folds while eye cap remains exposed; no meaningful lid coverage. Not a whole-eye scale test. Does not prove every possible morph design impossible. |
| A — additive eye/lid reconstruction: open, L half/closed, R closed, both closed | **PASS mechanically / CONDITIONAL production** | Central closed-lid apertures 0; eye geometry unchanged (0 displacement). Separate covering skin moves over fixed eye volume. Socket fit, lid/cheek blending and canonical appearance unfinished. |
| A — left/right/down gaze on reconstructed iris, independent of lids | **CONDITIONAL** | Actual iris surface morphs at bounded 8° lateral/6° downward probe amplitudes; original eye caps had no separate gaze control. Final texture/eye expression still required. |
| A/B — small smile, lower mouth displacement, pocket open/chew | **CONDITIONAL** | Raw mouth is a shallow modeled recess, not merely a painted mark. Added small pocket changes aperture and supplies internal depth. Original surrounding lip closure/interface was not rebuilt; full small-mouth open/close remains unaccepted. |
| B — bounded food approach | **CONDITIONAL** | Small proxy tested in front of mouth; face remains visible. Contact envelope and room for a minimal interior exist. Actual bite lip contact, tongue and five eating styles were NOT TESTED because final mouth and food assets are absent. |
| C — head yaw ±20°, pitch 15°, roll 12°, low presentation | **CONDITIONAL** | Actual weighted mesh evaluated front/threequarter/side. Broad head volume survives modest probes; neck/upper-torso overlapping interfaces still require ownership/weight/corrective work. These are diagnostic amplitudes, not approved production limits. |
| D — independent L/R low paw offer; hold and return | **CONDITIONAL** | Both limbs actually exercised without extension; soles stay fixed. Shoulder edge length ratios reach about 0.57…1.72 in simple offers; smoothing/weights/interface work remains. |
| D/H — initial both-paw/gift proxy placement | **FAIL for that placement** | Sphere intersects torso (vertex-sample signed distance -0.04367). It is not represented as successful holding. |
| D/H — bounded reachable both-paw hold after contact search | **CONDITIONAL** | 1/81 searched combinations gives near-symmetric tangent paw contact, torso clearance 0.00414 and head clearance 0.01888. Shoulder ratios reach 0.162…2.739, so contact is feasible but natural grasp/deformation is unfinished. |
| E — source standing support and fixed sole samples | **PASS narrowly** | 98 sole-region vertices per side remain fixed through these probes (floating-point errors approximately 1e-8 or less). Dynamic balance, contact-area pressure and final foot design are UNKNOWN. |
| E — small shift and low squat (0.012 / 0.035 height-unit lowering) | **CONDITIONAL** | Feet remain planted, but lower-joint creasing and increasing internal intersections appear. Low squat edge ratios reach 0.122…4.247. Requires better weighting/correctives and likely joint-region retopology. |
| E — toward sitting (0.095 lowering) and local smoothing repair trial | **FAIL for tested setup** | Some leg surface reaches Z=-0.04563 despite fixed soles; visible leg collapse. Ten local smoothing steps improve minimum Z to -0.01504 but do not resolve penetration. Final sitting capability remains UNKNOWN pending structural deformation repair. |
| F — local cheek/belly/support pressure, release | **PASS locality/recovery / CONDITIONAL appearance** | Actual bounded local fields, no whole-body scale. Belly max 0.02381 and support max 0.01654; neighboring eyes/distal paws unchanged. Cheek max 0.00421, nearby eye region moves 0.00277; requires a protective eye mask/corrective. Opposite cheek and paws unchanged. Release error 0. |
| G — independent ear-root probes ±10°, crown/chest/bouquet envelopes | **CONDITIONAL** | Ear mesh exercised with root falloff; bounded temporary attachments rendered. Crown centre follows head, but final crown orientation/mesh contact and all Wear combinations are NOT TESTED; actual accessory assets are absent. |
| H — head touch while paws hold selected bounded object | **CONDITIONAL** | Actual combined mesh state: paws move 0 from held pose; head/object clearance shrinks to 0.00193. Indicates a narrow conflict envelope needing controls, rather than unrestricted coexistence. |
| H — safe neutral return / release of diagnostic controls | **PASS geometric reset** | Body and contact trials return with 0 maximum vertex error. This does not implement transfer/reward logic or real user interaction. |
| GLB — skin/morph/animation export, reimport, actual evaluated samples | **PASS focused handoff** | One Scene animation, 44 channels, 1 skin, 10 meshes; source frames 1/12/24 agree within 5.65e-7 nearest-vertex distance. Device/runtime performance and final animation quality remain UNKNOWN. |

## F. Observed failures and root causes

1. **Raw lid probe:** the generated cap/socket construction has no usable covering eyelid surface in this test. Folding existing upper skin distorts the orbital boundary while leaving the cap visible. Additive covering lids demonstrate localized repairability, but the visible seam/protrusion prevents final facial acceptance.
2. **Support collapse:** the actual short legs lack a resolved deformation setup around pelvis/thigh/knee/ankle. Fixed feet do not imply the rest of the leg avoids the ground. Modest lower-joint movement already produces creasing; larger lowering exposes severe fold/penetration. Simple local smoothing is insufficient. This is a failure of the tested geometry-plus-weights combination, not mathematical proof that all possible rigs fail.
3. **Holding conflict:** an arbitrary low sphere is embedded in the belly. Contact search proves a bounded alternative, with small clearance that shrinks under head touch. The product must choose reachable low presentation and resolve holding conflicts; arms must not be lengthened.
4. **Eye influence during cheek pressure:** 0.00277 displacement reaches eye-region source vertices. Protective semantic weighting/correctives are needed before facial softness is accepted.
5. **Surface/interface work:** open thin strips and modular overlaps are present at source neutral. Their existence is not fatal; exposed seam behavior and deformed ownership require repair.

**Setup errors distinguished and corrected:** an initial temporary leg orientation used a tracking quaternion that introduced axial twist; it was replaced with rest-orientation-preserving rotation. An initial baseline was captured before a clean rig reset; the final baseline asserts unchanged copied geometry and reports zero neutral error. Re-runs now remove only their prior diagnostic objects. GLB initially split bones and morphs into nine clips, so default reimport playback omitted simultaneous morphs. Merging the shared Scene timeline fixed this. The exported first time is 1/24 second, not zero; matching the preserved timestamps removed a one-frame comparison error. These superseded setup results are not used as mesh verdicts.

## G. Local repair versus final Tripo trial

| Route | Evidence-based assessment |
|---|---|
| Keep B, superficial cleanup only | **Insufficient.** Does not solve eyelids, mouth closure/interfaces or support deformation. |
| B, targeted partial reconstruction/retopology | **Recommended.** Reuse major volumes; rebuild identity-critical local facial controls and deformation interfaces, then re-test planted support and actual prop contact. |
| B, extensive reconstruction | **Not yet justified.** No decisive failure requires replacing the entire head/torso/ears/short-limb proportions. Reconsider only if regional work cannot retain identity and required support. |
| One final Tripo generation | **Preserve it.** No demonstrated global proportion/anatomy failure makes regeneration preferable. Another generated mesh is not evidenced to deliver eyelids, final weighting, sole design or clean deformation loops. |

Smallest reliable next production route:

1. Separate semantic source regions and classify thin detail/eye-cap components. Preserve source proportions; do not blanket-delete every small island. The eight-largest-component scratch (4,700 vertices / 9,323 triangles) intentionally omits eye caps and surface strips to expose core volumes; **it is not an approved cleaned production mesh**.
2. Fit canonical eye surfaces and rebuild socket/lid transition loops, bilateral closure and gaze; resolve the proof's protruding interface. Reconstruct the small mouth rim and minimal interior with actual closure; preserve nose/cheeks, no large human mouth/eyebrows/fingers.
3. Tune anatomical support pivots/weights first, then add pose correctives or targeted loops at pelvis/thigh/knee/ankle where folding persists. Preserve separate feet and original short proportions. Re-test shallow settle, toward sitting and return with all surface vertices above support except intended contact.
4. Repair neck, shoulder/armpit and ear attachment ownership only where the observed interfaces require it. Keep major cranium/torso/ear volume as the donor. Mask eyes during cheek touch.
5. Re-test low offer, bounded actual holding objects, held-paw head touch and food approach together; use attachment geometry before accepting any crown/bouquet/Wear state. Then bake supported controls and validate GLB again.
6. Present representative materials and motions for Human identity/cuteness/naturalness review before final production acceptance, followed by real Xiaomi runtime checks. Do not fix Game Neutral in this validation task.

## H. Final GO / HOLD / FAIL

- **GO:** preserve Candidate B and proceed with targeted Blender production repair.
- **HOLD:** adopting B as Shushu's final production base without the specified structural/deformation work and Human review.
- **FAIL:** tested raw lid folding, initial embedded holding placement, deep support pose and cheap smoothing fix.
- **UNKNOWN / NOT TESTED:** full final rig and natural motion library; real crown/bouquet assets; five eating styles; final mouth closure; full product-state composition; PlayCanvas/browser-device performance. No simple existing Shushu PlayCanvas inspection fixture was used; no main app or new runtime framework was created. Xiaomi 14T Pro and Pixel-class frame rate, GPU cost, latency and thermal performance were not measured.

## I. GLB findings and reproduction

The diagnostic GLB is a temporary proof, not a public/runtime replacement. It contains 23 nodes, 10 meshes, 1 skin, a unified 44-channel Scene animation and skeletal + morph controls. Raw source remains unrigged. Normal splits increase core reimport vertices from 4,700 to 4,756 without changing its 9,323 triangles. Preserved animation time is **0.0416667…1.0 seconds at 24 fps**; frames 1, 12 and 24 are compared at those times.

Blender preserve-volume dual-quaternion skinning does not survive as glTF behavior. It was disabled for the exported reference comparison, using linear skinning on both sides. Temporary IK calculations are baked into joint transforms; Workbench lighting is diagnostic only. The exporter still emits one armature-parent warning; sample agreement verifies this focused handoff, but the production rig hierarchy must be cleaned before runtime acceptance. Nearest-vertex comparison accommodates split normals; it is not a perceptual animation score.

Run from the repository root, in order (ordinary Python needs Pillow; Blender needs its bundled NumPy):

```powershell
# The intake command is idempotent when the six inputs are already organized.
& '<ordinary-python-with-Pillow>' scripts/blender/shushu-candidate-b-intake.py
& '<blender.exe>' --background --factory-startup --python scripts/blender/shushu-candidate-b-audit.py
& '<blender.exe>' --background --factory-startup --python scripts/blender/shushu-candidate-b-deform.py
& '<blender.exe>' --background --factory-startup --python scripts/blender/shushu-candidate-b-facial-roundtrip.py
& '<blender.exe>' --background --factory-startup --python scripts/blender/shushu-candidate-b-contact.py
& '<ordinary-python-with-Pillow>' scripts/blender/shushu-candidate-b-boards.py --compact
```

The scripts operate only on original-file reads and disposable diagnostic scenes. They never connect to Tripo or the running Blender session. Rerunning recreates the diagnostic blend/evidence; preserve any later hand-edited diagnostic work before doing so. `--compact` retains the comparison boards and selected full-resolution proof/failure views; intermediate images can be regenerated.

## J. Exact evidence paths and repository handoff

- Sources: `assets/grimo/production/shushu/tripo/candidate-b-8481/` (original basenames).
- Historical diagnostics: `docs/production/shushu/evidence/candidate-b-8481/historical/`.
- Current evidence: this directory's manifest, independent audit, deformation measurements, facial/roundtrip report, contact report, six comparison boards and selected `renders/`.
- Reproducible scene: `assets/grimo/production/shushu/blender/shushu-candidate-b-feasibility.blend`.
- Temporary handoff: `assets/grimo/production/shushu/runtime-probes/shushu-candidate-b-diagnostic.glb`.
- Reproduction code: six `scripts/blender/shushu-candidate-b-*.py` files.

Changes are limited to Shushu intake/experimental assets/evidence and their reproducible scripts. No application, other-character or approved reference file changed. A focused local commit is the handoff snapshot; its SHA is supplied in the final response. **Push status: not pushed; this task explicitly requires authorization before publication.**

**Next production step:** an identity-preserving regional face and support-deformation repair of B, starting with a production-owned copy and reusing the measured source volumes. This report is a repair decision, not Human acceptance of a final Shushu.
