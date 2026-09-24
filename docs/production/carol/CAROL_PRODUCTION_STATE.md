# Carol production state

This file is the single mutable Carol execution truth.

## Hero ear, hoof and eye/socket v003 — 2026-09-24

- Local execution branch: `codex/carol-hero-modules-v003`, from v002 HEAD
  `c85b9ab202c5a9a9c663f246300b225ca47b617a`. The locally supplied
  `CAROL_HERO_MODULES_AND_EYE_PARAMETERS.md` was preserved and included.
- Starting asset: `carol-hero-modules-v002.blend`; diagnostic candidate:
  `assets/grimo/production/carol/blender/carol-hero-modules-v003.blend`.
  Changed scope: both ears, all four hooves, both eyes, both eyelids. The
  chassis and all other 31 objects are frozen and verified after save/reload.
- **Disposition: STALLED_PARAMETERIZATION. Executor visual precheck: REJECTED.
  Human Geometry Gate: NOT SUBMITTED.** The approved Ear Side/Top and Hoof Top
  contours remain visibly different. The review page at
  `docs/production/carol/evidence/hero-modules-v003/review.html` is diagnostic,
  not a candidate for Human geometry approval.
- Final normalized Ear Front/Side/Top/3Q IoU:
  `0.8297 / 0.7553 / 0.7424 / 0.6970`; Front centerline angle `18.0°`.
  Hoof: `0.9376 / 0.9037 / 0.6083 / 0.7929`; actual width `.219 H`,
  nominal visible crown `.111 H`.
- Eye/socket correction: visible Front aperture measured after occlusion
  `.1370 × .1485 H`, centered at `±.16175 H`; central optical relief `.013 H`;
  neutral Side eye does not extend beyond the anterior head silhouette.
  This repairs the measured Front-size regression in an intermediate local
  trial, but Human eye/identity acceptance remains unevaluated.
- Next handoff: **CHATGPT_PLANNER — review the v003 diagnostic and choose a
  new ear/hoof spatial section basis or another bounded probe before another
  Human Geometry Gate.** Do not treat v003 as production geometry acceptance.

## Hero ear and hoof modules v002 — 2026-09-24

- Execution branch: `codex/carol-hero-modules-v002`; source is the exact
  `carol-v011.blend`, preserving its face, eyes, torso, support, tail, cameras,
  and authority registration. Candidate:
  `assets/grimo/production/carol/blender/carol-hero-modules-v002.blend`.
- Approved localized sheets:
  `assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png`
  and
  `assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.png`.
  They are ear/hoof module authority, not whole-character authority. The 3Q
  panels validate one Front/Side/Top spatial form; pale helper stubs indicate
  orientation, not final visible cut lines.
- The Human Geometry Gate remains **PENDING HUMAN REVIEW**. Review evidence is
  at `docs/production/carol/evidence/hero-modules-v002/review.html`.
- Technical Module Gate and Executor Visual Precheck are **ATTENTION**: source
  freeze and module topology checks pass, but the bounded three-cycle fit did
  not reach the stated multi-view silhouette targets. The localized module
  decision now routes to Human review with the measured mismatch visible.
- The body-attached stylized cloud fleece motion decision below remains in
  force; this static module task does not revise it.


## Current state — Full-Spatial architecture review, 2026-09-24

- Current repository line for this doctrine update: `chore/full-spatial-3d-production-system`, branched from pushed Hero Probe Attempt-2 HEAD `d373b50c14e5febff791ff506942f52e97abdc50`.
- Human review of Hero Experience Probe v001 Attempt 2 is complete. **Disposition: PROBE_INVALID.** It does **not** establish a v011 geometry FAIL or PASS.
- Human-observed validity failures:
  - transferred fleece/motion read like sticky/mochi-like material attached to the character rather than one naturally owned body system;
  - ears visibly appeared/disappeared through the fleece during motion;
  - the review artifact was video/images only, so it could not support a claim about actual touch-interaction feel;
  - overall visible form/fleece quality was too low for a fair judgment of cuteness, naturalness, or whether v011 should continue.
- Attempt 1 was likewise not decision-valid because its low-fidelity sphere fleece dominated the presentation. **No Attempt 3 is authorized.** Two invalid probe cycles trigger Architecture Review rather than another cosmetic probe.
- v011-A3 therefore remains **NOT EVALUATED BY HERO PROBE v001**. Its historical static evidence remains unchanged.
- Human observation on the retained v011 source: the current **front face is sufficiently high quality to serve as a meaningful visual-quality anchor**, but this is not full-model or multi-view acceptance.
- v011 ears, limbs, and hooves remain separate/frozen predecessor modules; their historical temporary quality defects remain. They can be replaced as bounded modules without requiring a whole-character rebuild.
- Fleece motion decision (2026-09-24): Carol's fleece is a **body-attached stylized cloud mass**, not loose fur. Macro fleece position follows its owning head/torso region with effectively zero perceptible transform lag. Do not use sliding-shell follow-through, independent cloud-ball jiggle, or physics-led broad motion. Use low-amplitude local compression/opening/recovery only when causally useful; a very small authored broad shape settle is optional. Mesh separation may remain for production control and does not imply independent motion ownership.
- Historical full-3D fleece recovery: the pre-Skin-separation v006 line on `codex/carol-zero-based-hero-geometry-v005` contains `assets/grimo/production/carol/blender/carol-a-v006.blend`, generator `scripts/blender/build-carol-v006.py`, and six-view evidence under `evidence/reconstruction-v006/`. Pass 05 / iteration 27 recorded Front/Side/Back/Top/3Q silhouette alignment from one model (Front 0.936253, Side 0.944835, Back 0.934204, Top 0.965988, 3Q-L 0.842496, 3Q-R 0.889279 IoU under its historical metric). This is a **donor/benchmark candidate, not current authority or Human-approved production fleece**.
- Architecture decision: adopt **Full-Spatial 3D Living Character Architecture with View-Weighted Polish**. Exterior geometry must remain coherent through practical Front/3Q/Side/Rear/derived-Top exposure so later Motion does not create view-debt; Front remains the highest-polish Hero view.
- Human-facing perceptual probes now require a declared **Human-Evaluable Fidelity Floor**. If unrelated visible proxy quality dominates judgment, record `PROBE_INVALID`; do not infer candidate FAIL.
- Visible asset production is **reuse-first**: inspect stronger existing/current/historical assets before generating a lower-quality replacement.
- No geometry, fleece, rig, animation, GLB, runtime, or canonical/reference asset was promoted by this doctrine update.
- **Next handoff: CHATGPT_PLANNER — choose the first production Decision Question under the Full-Spatial 3D architecture; do not resume Hero Experience Probe v001.**

## Historical Hero experience probe — Attempt 2, 2026-09-24

- Branch: `codex/carol-hero-experience-probe-v001`; execution started at exact pushed HEAD `c6f3df031adb72dd3e1697c9da91f6d56471fa3d`.
- **Attempt 1 = UNKNOWN**: its newly generated sphere proxy fleece and loose head/fleece ownership confounded Human review. It is preserved in commit `c6f3df0`, not a v011 geometry or architecture failure.
- **Attempt 2 = final allowed attempt**. Source geometry: unchanged **v011-A3** at `assets/grimo/production/carol/blender/carol-v011.blend` (SHA-256 `568fb4378b6ca3093ba5134d8d082f37a6723c9d5b5cf0b491a7c8e5f757aed3`). Selected probe: `assets/grimo/production/carol/blender/carol-hero-experience-probe-v001.blend`.
- Full-3D fleece donor: `Carol_Fleece_Continuous` from `codex/carol-structural-blockout-v004` commit `041868310df584ae5efa4d05fb9f77877b00d0f7`, asset `carol-blockout-v004.blend` (unchanged SHA-256 `8f6f0b64bf81ce591856d46359b7d827c6a9f6403b70884c8677d461023f6c19`). Only its continuous fleece, crescent, and four major stars were copied; the v004 face, ears, hooves, supports, cameras and chassis were not transferred. Attempt-1 visible sphere proxy is absent from the selected probe.
- Registration: donor front `-Y` maps to v011 front `-X`; donor lateral `X` maps to v011 lateral `Y`; both use `Z` up. One uniform scale `.30` maps donor world `(x,y,z)` to v011 `(.48 + .30y, .30x, .30z - .0075)`. This aligns donor hoof-ground `.025` to v011 ground `0`, puts donor front relief beside the v011 face, and gives the fleece an approximately `.82` high envelope. No v011 source edit or per-axis scale was used.
- Donor-only adaptation: a smooth, low-order front facial clearance pushes copied fleece locally back by at most `.235` around the larger v011 face/eye region. The copied crescent is shifted `(-.08,+.50,+.12)` in v011 XYZ to sit on the upper left cloud without covering the eye. Copied crown, top, wool and chest stars remain attached to the transferred spatial fleece presentation. All transferred components retain their donor meshes; the fleece keeps its 164,272 vertices.
- Provisional motion ownership: v011 eyes, eyelids, nose, mouth and both ear bases use a head owner; the near ear adds a delayed secondary owner. The v011 chassis has one localized cranial lean key. The donor fleece has local cheek ACK, head-owned lean and upper-body delay shape keys. Head-owned motifs follow the head control. Root and four hooves remain fixed. One 120-frame fixed-camera phrase covers cheek contact, acknowledgement, attention, contact-seeking lean, delayed nearby response, settle and afterglow.
- Human evidence: [neutral](evidence/hero-experience-probe-v001/hero-neutral.png), [unwarped authority comparison](evidence/hero-experience-probe-v001/hero-neutral-comparison.png), [motion](evidence/hero-experience-probe-v001/hero-motion.mp4), [contact sheet](evidence/hero-experience-probe-v001/hero-contact-sheet.png), [review page](evidence/hero-experience-probe-v001/human-review.html).
- Executor-observed limitations: the donor's relief remains pale and materially simple compared with the approved painted fleece; its large front face opening and partly embedded crescent visibly differ from Normal Front. The local ACK and head lean are small in the fixed Hero view. Known v011 Side under-jaw/head-to-chest and Side eye limitations were not repaired or evaluated by this front probe. This is one authored phrase, not extended behavior.
- Targeted checks: saved probe reopened; donor fleece and motif objects exist; shape-key controls animate; hoof transforms are unchanged at peak; six beats rendered; H.264 540×540/5.04 s MP4 encodes and decodes; all seven HTML media references resolve; source and donor hashes remain unchanged. Canonical identity and approved Front/Side files are unmodified.
- Browser review status: localhost delivery and playback verification are scheduled after push. **Human Experience Review = PENDING HUMAN REVIEW**. No production geometry or fleece promotion, production rig, production animation approval, GLB/runtime integration or Human PASS is claimed.
- Handoff: **CHATGPT_PLANNER — evaluate Carol Hero Experience Probe v001 Attempt 2 with Human review**.

## Current state — 2026-09-23

- Production-doctrine routing (2026-09-23): the same anterior/static blocker survived at least two bounded local repair cycles. Under the Two-Cycle Stop Rule, no third local repair is authorized by default. This repository migration deliberately does **not** select the next production probe; the next ChatGPT Planner must choose the first Decision Question under the new production system before authorizing further production work.
- Branch: `codex/carol-final-reconstruction-v013`. Bounded **v013-A-REPAIR** started from exact pushed HEAD `94761dfdcca7475480a173effe783993146fc484`; no new branch or v014.
- Execution status: **TECHNICAL_FAIL** after two structural repair passes. Selected asset: `assets/grimo/production/carol/blender/carol-v013.blend`, **A-REPAIR-R2, diagnostic only; not promoted**.
- Root cause: the original first facial-to-cranial bridge changed circumferential parameterization before spatial separation. Stored witnesses support this, but it was not the only defect. The rounded face perimeter is locally inset relative to adjacent cheek/forehead columns, and the gradual regularization bands still cross later cranial bands. R1 added a matched 48-vertex `CRANIUM_SEAT` and progressive 48-vertex `CRANIUM_TRANSITION`; control intersections were **52**. One allowed R2 seat/transition curvature adjustment left **51**. No R3.
- R2 chassis: **921 vertices / 1,838 edges / 919 quads**, 1 component, nonmanifold edges `0`, Euler `2`, degenerate/duplicate faces `0`, consistent winding. Control disjoint intersections **51 — FAIL**. Evaluated intersections and adjacent improper contacts: **NOT_RUN_CONTROL_GATE_FAILED**.
- `.575 H` interface and all **96** retained ABDOMEN/RUMP vertices, coordinate-keyed edges and faces match source after save/reload. Frozen objects, four reference hashes/registration and source v012 blend are unchanged. No eye/face-field, J0/J1/C0/C1, support or rear redesign.
- Skin Front / Skin Side / eye/socket visual precheck: **NOT_RUN_TECHNICAL_GATE_FAILED**. Derived 3Q/Top and motion probe: **NOT RUN**. Human Geometry Gate: **NOT_REVIEW_READY**. No Human pass claimed.
- Evidence: [v013 repair diagnostic](evidence/reconstruction-v013/README.md), [R2 structure wire](evidence/reconstruction-v013/structure-sheet.png), [measurements](evidence/reconstruction-v013/measurements.json), [validation](evidence/reconstruction-v013/validation.json). The original diagnostic sheet remains an explicit NOT RUN template, with historical A counts.
- Phase B/C, fleece, production rig, animation, GLB and runtime integration: **NOT STARTED**.

## Historical retained v013-A state

- Branch: `codex/carol-final-reconstruction-v013`, from exact source HEAD `9d39680389b20677b6627491fd79bd6acbc51658`.
- Execution status: **TECHNICAL_FAIL**. Selected attempt: **v013-A, DIAGNOSTIC ONLY — NOT PROMOTED**. Historical asset is preserved in commit `94761dfdcca7475480a173effe783993146fc484`; the working `carol-v013.blend` path now holds A-REPAIR-R2.
- Architecture: **Option D — semantic anterior chassis replacement**. New BMesh-authored face fields, integrated 24-segment orbital R0–R3 grids and recessed basins, shallow optical lenses, section-based cranium, J0 jaw / J1 flex / C0 chest crest / C1 blend, connected to the retained `.575 H` interface. Old head connectivity and separate structural eyelid shells are replaced.
- Topology: **825 vertices / 1,646 edges / 823 quads**, one component, zero nonmanifold edges, Euler `2`, no degenerate or duplicate faces, consistent edge winding. R0–R2 and J0/J1/C0 are pole-free with valence `4`.
- Cheap technical gate: **FAIL — 36 disjoint control-face intersection pairs**. The lateral face boundary overlaps the initial cranial loft bands. Closedness and all-quad status do not make this a valid exterior. Full evaluated intersection/adjacent-contact validation was not run after this failure.
- All **96** source ABDOMEN/RUMP vertices and their coordinate-keyed edges/faces, including the nonplanar `.575 H` interface, match exactly after save/reload. Frozen ears, limbs, hooves, tail, cameras, lights and references match source records; materials are reused unchanged. Ear seating delta is `0`. Source v012 blend and four locked reference files remain unchanged.
- Skin Front / Skin Side / eye/socket / derived 3Q/Top: **NOT_RUN_TECHNICAL_GATE_FAILED**. Aperture control rings author `.137 × .149 H` at `±.162 H`; evaluated visible aperture, eye containment, jaw/chest read, cranial shape and ear-root fit remain unproven. No visual pass is claimed.
- Motion probe: **NOT_RUN_TECHNICAL_GATE_FAILED**. Human Geometry Gate: **NOT_REVIEW_READY**. No Human decision or pass is claimed.
- Attempts: **A only**. B/C not eligible because A is not structurally correct; no parameter rescue or architecture restart performed.
- Evidence: [v013 technical diagnostic](evidence/reconstruction-v013/README.md), [gate sheet](evidence/reconstruction-v013/diagnostic-sheet.png), [wire structure sheet](evidence/reconstruction-v013/structure-sheet.png). Candidate/overlay/derived render cells explicitly say NOT RUN; wire diagnostics are not visual-acceptance renders.
- At the user's explicit request, pre-existing `tmp-carol-v012/` trial data are retained unchanged and included with this handoff as historical diagnostics, not current authority.
- Phase B/C: **NOT STARTED**. Fleece, production rig, animation, GLB and runtime integration: **NOT STARTED**.

## Historical retained v012 state

- Branch: `codex/carol-final-reconstruction-v012`, from exact source HEAD `e95654fae3dc8434cbe651e7d6467aafe59dc667`.
- Execution status: **BLOCKED_AT_V012_PHASE_A_VISUAL_RECONSTRUCTION** after bounded T1/T2 and O1/O2 probes; no further v012 probe.
- Selected v012 attempt: **T2-O2, diagnostic only; not promoted**. Asset: `assets/grimo/production/carol/blender/carol-v012.blend`.
- The v011 topology and exact face connectivity are retained: 533 vertices / 1,062 edges / 531 quads, one component, zero nonmanifold edges, Euler `2`. Control / evaluated disjoint intersections **0 / 0**; adjacent improper contacts **0 / 0**.
- Chassis Y/Z delta **0**; `.575 H` and rearward delta **0**. T2 transition X delta at most `.050 H`; O2 local orbital seat X delta at most `.015 H`. Front eye locks remain `.137 × .149 H` at `±.162 H`.
- Eye cap Side whole-span `.1286 H`, near-eye derived 3Q width/height `1.137`; both are numerical projection metrics, not visual acceptance.
- Executor visual precheck: **FAIL**. The long oblique Side under-jaw/head-to-chest surface remains. The Side eye is wider but protrudes from the socket; Front under-chin transition is too sharp. Posterolateral Top rounding is retained; anterior taper is not clearly improved.
- Motion clearance: **NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED**. Human Geometry Gate: **NOT_REVIEW_READY**. No Human decision or pass is claimed.
- Frozen references and registration, cameras, lights, materials, ears, limbs, hooves, tail and support centers `.390` / `.920 H` remain unchanged. The v011 source blend is byte-identical.
- Phase B/C: **NOT STARTED**. Fleece, retopology lock, production rig, animation, GLB and runtime integration: **NOT STARTED**.
- Evidence: [v012 bounded reconstruction](evidence/reconstruction-v012/README.md) and [diagnostic sheet](evidence/reconstruction-v012/diagnostic-sheet.png).

## Historical retained v011 state

- Branch: `codex/carol-final-reconstruction-v011`, from exact source HEAD `9569bea8e08e0e068ed7debadf242419e9655a40`.
- Execution status: **BLOCKED_AT_V011_PHASE_A_VISUAL_RECONSTRUCTION** after three bounded attempts; **no A4**.
- Selected v011 attempt: **A3, diagnostic only; not promoted**. Asset: `assets/grimo/production/carol/blender/carol-v011.blend`.
- Topology family and exact face connectivity: **v010-A3 retained**. Cube-derived cranial patches, head-owned ventral jaw, short matched transition, open chest patch and retained rear stations; no architecture restart, Boolean or remesh.
- Technical static gate: **PASS**. 533 vertices / 1,062 edges / 531 quad faces; one component, zero nonmanifold edges, Euler `2`; control / evaluated disjoint intersections **0 / 0**. Supplemental adjacent-triangle tests: **5,903 / 93,515 pairs, zero improper contacts**.
- Executor visual precheck: **FAIL**. Front eye locks remain intact. Derived 3Q horizontal eye stretch is substantially reduced and Top posterior shoulders are rounded. Side still has a dominant oblique under-jaw surface, and the Side eye is too narrow/exposed. Slight anterior cranial taper remains; the full multi-view form gate is unresolved.
- Motion clearance: **NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED**.
- Human Geometry Gate: **NOT_REVIEW_READY**. No Human decision or pass is claimed.
- Frozen source hashes/registration, cameras, lights, materials, ears, hooves, limbs, tail and support centers `.390` / `.920 H` remain unchanged. Rear stations from `.730 H` are unchanged. The source v010 blend is byte-identical.
- Phase B/C: **NOT STARTED**. Fleece, retopology lock, production rig, animation, GLB and runtime integration: **NOT STARTED**.
- Evidence: [v011 bounded refinement](evidence/reconstruction-v011/README.md) and [diagnostic sheet](evidence/reconstruction-v011/diagnostic-sheet.png).

## Historical retained v010 state

- Branch: `codex/carol-final-reconstruction-v010`, from exact source HEAD `5de182d5eab04f84e3fa46926a953efa3527d679`.
- Execution status: **BLOCKED_AT_V010_PHASE_A_VISUAL_RECONSTRUCTION** after three bounded attempts; **no A4**.
- Retained v010 attempt: **A3, diagnostic only; not promoted**. Asset: `assets/grimo/production/carol/blender/carol-v010.blend`.
- Architecture: cube-derived cranial patches, head-owned ventral jaw, matched short neck strip, open chest patch, and retained rear torso stations. One authored exterior; no Boolean or remesh.
- Technical static gate: **PASS**. 533 vertices / 1,062 edges / 531 faces; one component, zero nonmanifold edges, all quads, Euler `2`; control / evaluated disjoint intersections **0 / 0**. Supplemental checks of 5,904 / 93,515 adjacent triangle pairs found **zero improper contacts**.
- Executor visual precheck: **FAIL**. The hard jaw shelf is removed, but A3's Side ocular visibility produces horizontally stretched eyes in 3Q; Top has angular cranial shoulders and wedge-like anterior volume; the oblique under-jaw plane remains too dominant against locked Skin Side.
- Motion clearance: **NOT_RUN_EXECUTOR_VISUAL_PRECHECK_FAILED**.
- Human Geometry Gate for v010: **NOT_REVIEW_READY**. No Human decision is claimed.
- Frozen reference hashes/registration, cameras, materials, unrelated modules, support centers `.390` / `.920 H`, and Front eye dimensions/centers remain unchanged. The `.575` seam was reconstructed; `.730` and rearward control stations are retained.
- Source v009 blend remains byte-identical. The current user handoff records **v009-A2 HUMAN-REVIEWED FAIL**; the older pending label below is historical.
- Phase B/C: **NOT STARTED**. Fleece, final retopology lock, production facial/body rig, animation, GLB and runtime integration: **NOT STARTED**.
- Evidence: [v010 rejection record](evidence/reconstruction-v010/README.md) and [compact visual proof](evidence/reconstruction-v010/diagnostic-rejection.png).

## Historical retained v009 state

- Branch: `codex/carol-final-reconstruction-v009`.
- Retained asset: `assets/grimo/production/carol/blender/carol-v009.blend`.
- Retained candidate: **v009-A2**, a bounded Phase A architecture attempt; it is **not an accepted static candidate**.
- Execution status: **BLOCKED_AT_V009_PHASE_A_ARCHITECTURE**.
- Human Geometry Gate: **PENDING HUMAN REVIEW**; this state file does not self-approve or reject that gate.
- Executor-recorded static visual status: **FAIL**.
- Motion preflight: **NOT_RUN_STATIC_PREREQUISITE_FAILED**.

## Bounded Phase A recovery — A3 / A4

- Starting HEAD: `01e19d27519d5731015d553cdae1acc572edf8c9`.
- A3 replaced the global transition with a head-owned jaw closure, posterior underside portal, three interior neck rows, and a local dorsal chest portal. Its existing 64 head sectors were retained to avoid reduction poles under the jaw.
- A3: one component, closed all-quads, Euler `2`; control / evaluated intersections **114 / 393**. Frozen objects passed; frozen seam coordinates failed. Rejected before visual rendering.
- A4 made the bounded jaw-curvature, portal-seating, and frozen-seam correction. One component, closed all-quads, Euler `2`; control / evaluated intersections **224 / 644**. Frozen coordinates and objects passed. Rejected for structural failure; **no A5**.
- Exact remaining blocker: the local portal/jaw/chest patch still intersects the head and upper-chest seam. A clean exterior and motion clearance are not established.
- The retained `v009-A2` blend is **byte-identical to the starting asset**. Its existing comparison images remain A2 evidence; no rejected attempt was promoted or rendered as final evidence.
- Recovery visual checks and deformation probes: **NOT RUN — technical prerequisite failed**. Human Geometry Gate remains **PENDING HUMAN REVIEW**; Phase B/C remain **not started**.
- Cheap numerical proofs: `evidence/reconstruction-v009/phase-a-attempt-3/` and `phase-a-attempt-4/`. Further geometry work requires a new planner handoff.

## Historical v009-A2 architecture

- The current v009 exterior architecture is one authored `CENTRAL_CHASSIS` mesh. The old v008 exterior-owner combination is not current v009 architecture.
- `CENTRAL_CHASSIS` is one connected, closed, all-quad surface with nonmanifold edges = `0`; these topology facts do not make it a clean production exterior.
- Evaluated disjoint face intersection pairs = `455`; this is the recorded geometric-cleanliness failure.
- The selected eye prototype is an embedded partial ellipsoid with approximately `.029 H` central relief and six surrounding lid/socket loops.
- Frozen geometry authority remains: torso evaluated width ≈ `.598571 H`; support centers `.390 H` / `.920 H` with spacing `.530 H`; Front eye width `.137 H`, height `.149 H`, centers `±.162 H`.
- The four definitive Normal/Skin Front/Side sources remain FINAL/LOCKED. One neutral model serves Front and Side; no camera-specific geometry is used.

## Historical v009 blockers

- Hard lower-cheek shelf instead of a rounded jaw.
- Over-stretched under-chin → chest transition.
- Evaluated self-intersection in the central chassis (`455` disjoint face-intersection pairs).
- Side / 3Q face-eye identity remains insufficient against the locked Skin references.

These visual blockers and the evaluated intersection failure keep Phase A blocked. Manifoldness, connectedness, and all-quad topology are recorded successes, not a Phase A pass.

## Frozen / deferred modules

- Ears remain unchanged temporary v008 modules; Ear Phase B was **not started**.
- Hooves remain unchanged temporary v008 modules; Hoof Phase C was **not started**.
- Fleece: **not started**.
- Production rig: **false / not created**.
- Animation: **false / not created**.
- GLB export: **false / not performed**.
- PlayCanvas/runtime integration: **false / not performed**.
- Motion preflight was not run because the static prerequisite failed.

## Historical predecessor context

The following is historical v008 context only and is not current v009 production truth:

- v008 revision 17 is the rejected predecessor. Its evidence records the earlier Human Review FAIL for Side face/eye identity, head/chest transition, ear-root and true 3D ear volume, and hoof 3Q form.
- v008 used separate `HEAD_CAGE`, `SHORT_NECK_SOCKET`, and `TORSO_CAGE` exterior owners. v009 replaced those owners with the single authored `CENTRAL_CHASSIS` described above.
- The v008 Boolean union / smoothing experiment was disposable and rejected; it does not describe the retained v009 architecture.
- The temporary v008 ear and hoof modules are retained only because their replacement phases were not reached. Their historical failures are preserved in the v008 evidence package.

## Next handoff

**CHATGPT_PLANNER — choose the first Decision Question under the new production system**
