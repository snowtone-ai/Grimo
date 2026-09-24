# Codex Task — Carol Hero Ear + Hoof v001

## Executor configuration

**Recommended model:** GPT-6 Astra  
**Reasoning effort:** High  
**Subagents:** PROHIBITED  
**Mode:** one cohesive bounded production task; do not delegate visual/geometry decisions to subagents.

Read this file completely before changing anything.

---

# 0. Mission

Produce and integrate **production-quality Full-Spatial Hero ears and hooves for Carol** using the Human-approved localized module authorities already in the repository.

This is a precision geometry task, not a redesign task.

The user requirement is intentionally strict:

> Match the approved ear and hoof module images as closely as a coherent 3D model physically allows. Do not accept “close enough” when a visible difference can still be removed without violating higher authority.

The task ends at a **Human-review-ready neutral Carol** with high-quality ear/hoof geometry and compact evidence.

Do NOT start fleece reconstruction, rig production, animation production, GLB export, PlayCanvas integration, app work, or unrelated cleanup in this task.

---

# 1. Repository / branch boundary

Repository:

`snowtone-ai/Grimo`

Source branch:

`chore/full-spatial-3d-production-system`

At planner handoff, the execution state immediately before this task was:

`ef1fc4602f0a481fbd1a2d095a30a073796434bb`

The branch may contain a later commit that only adds/updates this `prompt.md`. Treat the **latest pushed remote HEAD containing this prompt** as the task base unless another execution commit appeared after it.

Required startup:

1. `git fetch origin`
2. confirm remote source branch HEAD
3. read `AGENTS.md`
4. read the task-relevant authority listed below
5. verify the worktree is clean
6. create a new branch from the current remote source-branch HEAD:

`codex/carol-hero-modules-v001`

Do not continue on an older reconstruction branch.

Do not overwrite or mutate the source branch.

If unrelated user work is present locally, do not discard/stash/reset it silently. Stop and report the blocker.

---

# 2. Mutable truth and authority

Current mutable routing truth:

`docs/production/carol/CAROL_PRODUCTION_STATE.md`

Task-relevant durable authority:

- `AGENTS.md`
- `docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`
- `docs/grimo/knowledge/character-production/GRIMO_BLENDER_IMPLEMENTATION_GUIDE.md`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `assets/grimo/source/carol/approved-3d/modules/README.md`

Visual authority:

1. `assets/grimo/source/carol/carol-Identity-canonical.png`
2. `assets/grimo/source/carol/approved-3d/carol_front.png`
3. `assets/grimo/source/carol/approved-3d/carol_side.png`
4. `assets/grimo/source/carol/approved-3d/carol_skin_front.png`
5. `assets/grimo/source/carol/approved-3d/carol_skin_side.png`
6. localized ear/hoof module helpers:
   - `assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.webp`
   - `assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.webp`

Important authority rule:

- The four locked Normal/Skin references and Carol canonical identity remain above the module sheets.
- The module sheets constrain only ear/hoof construction.
- Their Front/Side/Top panels constrain one coherent module.
- Their 3/4 panels are **validation**, not an independent per-view fitting target.
- The cream attachment/pastern stubs in the sheets are orientation helpers only. They must NOT appear as visible cut cylinders in final Carol.
- Historical whole-character AI Back/Top/3Q images are not fitting authority for this task.

Do not modify any approved source image.

---

# 3. Source Carol that must be preserved

Use:

`assets/grimo/production/carol/blender/carol-v011.blend`

as the source Carol.

The current production state explicitly says the retained v011 **front face is a high-quality visual anchor** and that ears/limbs/hooves are predecessor modules that can be replaced as bounded modules.

If the LFS object is not materialized, retrieve **only the required LFS asset**. Do not rebuild v011 from another generator as a substitute.

Do NOT overwrite `carol-v011.blend`.

New output asset:

`assets/grimo/production/carol/blender/carol-hero-modules-v001.blend`

Expected old module names from the retained architecture include:

- `EAR_L`
- `EAR_R`
- `HOOF_FORE_L`
- `HOOF_FORE_R`
- `HOOF_HIND_L`
- `HOOF_HIND_R`

Verify the actual source scene before assuming names.

Freeze every unrelated object.

Record source hashes / frozen-object geometry digests before modification and prove they are unchanged afterward.

The task may replace the ear/hoof meshes and may add narrowly scoped module helper objects/metadata/evidence. It must not redesign:

- `CENTRAL_CHASSIS`
- eyes
- eyelids
- nose
- mouth
- face
- head
- torso
- tail
- cameras
- locked reference registration
- unrelated materials
- support centers
- current limb architecture, except that a hidden overlap with the new hoof is allowed.

---

# 4. Toolchain

Use the repository-pinned toolchain.

- Blender: **5.2.1 LTS**
- Official Blender Lab MCP may be used for inspection.
- Reproducible final work must live in version-controlled Blender/Python code and a saved `.blend`.
- Prefer deterministic headless Blender execution for final generation/evidence.
- Do not upgrade Blender or add a new modeling dependency.

Recommended implementation file:

`scripts/blender/build-carol-hero-modules-v001.py`

You may create one small helper script only if it materially simplifies deterministic reference-mask comparison. Do not create a framework.

---

# 5. Research-derived modeling decision — ADOPT THIS

The production method has already been architecture-reviewed.

## 5.1 General

Use **structured parametric quad-friendly modeling + evaluated multi-view silhouette fitting**, not freehand sculpt guessing.

Use the reference images as technical orthographic constraints, while preserving one coherent 3D object.

Use low-dimensional control parameters and smooth continuous surfaces. Do NOT fit hundreds of individual vertices independently to pixels.

Use Subdivision Surface only where it improves smooth organic form while preserving editability. All image/error measurements must evaluate the **final evaluated surface**, not only the control cage.

Do not use Voxel Remesh as final production topology for these modules. It is acceptable only as a disposable diagnostic proxy if absolutely necessary; it must not become the production ear. Avoid it entirely for the ear if possible.

No final Boolean-union workflow.

No metaball construction.

No collection of overlapping spheres.

No per-camera geometry.

No camera-dependent shape keys.

No final geometry generated by global warp/squash.

## 5.2 Why

Official Blender documentation describes orthographic projection as useful for technical proportion judgment and image empties as suitable blueprint/reference displays. Subdivision Surface is intended to produce smooth organic forms from simpler editable control geometry. Blender's remeshing documentation explicitly warns that voxel topology should not be used as the final topology for a mesh that will deform in animation. Blender Studio's asset workflow likewise treats multi-angle reference, shape development, retopology, and downstream rig/deformation needs as connected production concerns.

The task therefore uses deterministic structured surfaces and quantitative multi-view checks rather than freehand “looks about right” modeling.

---

# 6. Reference-sheet extraction and fit space

Both module authorities are 2×2 sheets.

Treat each sheet as four equal quadrants:

- top-left = Front Orthographic
- top-right = Side Orthographic
- bottom-left = Top Orthographic
- bottom-right = 3/4 Validation

Do not use sheet margins as physical scale.

For geometry fitting:

1. isolate the colored module from the near-white background;
2. exclude the cream helper stub from the geometry target;
3. normalize the module mask by its own bounding box for silhouette-shape comparison;
4. get absolute physical scale from `CAROL_GEOMETRY_PARAMETERS.md`, not from sheet margins.

Use the highest fidelity repository module files, not screenshots.

Do not introduce new external image generation.

The sheet is a shaded design reference, so geometry scoring must prefer:
- silhouette
- section/profile
- inner-ear patch boundary
- thickness/depth
- curvature continuity

over literal RGB pixel equality caused by lighting.

Generate flat diagnostic/material-ID renders for objective comparison. Beauty shading is secondary evidence.

---

# 7. EAR — production method

## 7.1 Required architecture

Build **one coherent closed ear mesh family** and mirror it spatially for the opposite side without leaving negative object scale.

The ear must not be:
- a flat card
- a solid ellipsoid
- a thin realistic sheep ear
- multiple floating shells
- a pink decal hovering above a brown shell.

Preferred topology architecture:

- a smooth resampled outer perimeter;
- a structured sequence of nested shell/bowl loops similar in spirit to the successful part of the old v008 ear approach, but completely refit to the new approved module;
- sufficient radial/perimeter resolution for smooth tip and rim;
- explicit thickness/camber;
- an integrated recessed inner bowl;
- pink material assigned to faces of the same coherent ear mesh, not a coplanar floating card.

Suggested conceptual loop stack:

```text
buried/back root cap
→ back shell
→ outer back rim
→ outer front rim
→ inner lip
→ recessed bowl transition
→ inner bowl
```

This is guidance, not a requirement to preserve old v008 coordinates.

Use the approved new numerical contract in `CAROL_GEOMETRY_PARAMETERS.md`.

Primary targets include:

- root-to-tip length ≈ `0.305 H`
- maximum planform breadth ≈ `0.124 H`
- root breadth ≈ `0.091 H`
- tip breadth ≈ `0.042 H`
- root thickness ≈ `0.058 H`
- mid thickness ≈ `0.043 H`
- tip thickness ≈ `0.021 H`
- front outward projection ≈ `0.235 H`
- front downward drop ≈ `0.094 H`
- side visible length ≈ `0.266 H`
- side visible height ≈ `0.218 H`
- side pitch down ≈ `31°`
- top sweep back ≈ `10°`
- tip twist out ≈ `8°`
- inner patch length ≈ `0.205 H`
- inner patch max breadth ≈ `0.073 H`

These are construction constraints. The approved visible identity remains the final visual judge.

## 7.2 Ear root integration

Preserve the current Carol ear-root location/relationship unless a tiny adjustment is necessary to satisfy the current locked Normal/Skin refs.

The final root must:

- overlap the head sufficiently inside hidden geometry so no crack can open in neutral;
- read as a soft attached saddle, not a glued-on cylinder;
- preserve a clean future ear-root pivot region;
- avoid visible penetration into the eye/cheek;
- remain compatible with future independent ear motion;
- remain partially coverable by future fleece without disappearing through it.

Do not Boolean-union the ear to the head.

Keep it as a modular object with hidden overlap.

If a root pivot helper is added, make it explicitly non-rendering and semantically named. Do not create a production armature in this task.

## 7.3 Mirroring

Author one side to Hero quality, then create the opposite side from the same geometry family.

Do not leave a negative scale on the final object.

Mirror vertex coordinates / apply a mirror cleanly and recalculate normals so both final ear objects have positive transforms and correct winding.

---

# 8. HOOF — production method

## 8.1 Required architecture

Build **one continuous stylized hoof mass** with:

- exactly 3 rounded toe lobes;
- exactly 2 shallow clefts;
- one coherent surface;
- no detached toe objects;
- no Boolean-cut realistic splits.

Prefer a structured closed loft / section cage.

A useful starting architecture is the historical v008 ring/section idea, but replace the old generic sinusoidal result with a new fitted profile that explicitly controls:

- top footprint;
- side depth;
- front lobe widths;
- center-toe dominance;
- cleft depth/width;
- heel roundness;
- toe-forward projection;
- sole/contact profile;
- upper pastern transition.

The production hoof must not be built as three spheres fused together.

Do not use Voxel Remesh as the final result.

## 8.2 Numerical targets

Use the current locked contract:

- front width ≈ `0.219 H`
- front height ≈ `0.111 H`
- depth ≈ `0.150 H`
- top width ≈ `0.184 H`
- sole width ≈ `0.196 H`
- sole depth ≈ `0.112 H`
- center toe width ≈ `0.073 H`
- left/right outer toe ≈ `0.066 H` each
- each cleft width ≈ `0.007 H`
- cleft depth ≈ `0.023 H`
- toe forward projection ≈ `0.014 H`
- heel back projection ≈ `0.009 H`
- front-face roundness ≈ `0.019 H`
- upper-edge softness ≈ `0.016 H`
- lower contact corner ≈ `0.010 H`
- pastern insert width ≈ `0.148 H`
- pastern insert depth ≈ `0.106 H`
- pastern-to-hoof transition height ≈ `0.031 H`

## 8.3 Body integration

Preserve the current support centers and current short-limb architecture.

Do not move the body/support system to make the new hoof fit.

Fit the hoof to Carol.

Use a short hidden overlap between distal limb and hoof so:

- no visible gap exists;
- no hard artificial cut line exists;
- the cream helper cylinder shown in the module sheet is not reproduced;
- the hoof retains a clear brown mass;
- future hoof/support control remains possible.

Ground contact must remain planted.

Neutral hoof ground error should be effectively zero in world-space inspection.

Create one master hoof geometry family and reuse it consistently for all four hooves. Separate objects are allowed/expected; shared mesh data is preferred when it does not conflict with transform/orientation needs.

Do not “improve” rear hooves by inventing a different design.

---

# 9. Precision fitting loop

The user explicitly wants tiny visible discrepancies removed.

Use an objective, bounded fitting loop.

## 9.1 Fit order

For each module:

1. satisfy absolute numeric dimensions;
2. fit Front silhouette;
3. fit Side silhouette/depth;
4. fit Top silhouette;
5. re-check all three together;
6. freeze parameters;
7. render 3/4 validation **without adding new per-view degrees of freedom**;
8. only if 3/4 exposes a real full-spatial defect, change the shared 3D parameters and re-run all views.

Never solve a 3/4 mismatch with a 3/4-only deformation.

## 9.2 Quantitative targets

These are **task targets stricter than the broad construction tolerances**, not replacements for repository authority.

Aim for:

### Ear
- locked primary dimension error: target ≤ `0.003 H`
- locked angle error: target ≤ `1°`
- Front/Side/Top normalized silhouette IoU: target ≥ `0.990`
- do not call executor visual precheck PASS below `0.985` in any of Front/Side/Top unless a documented reference inconsistency makes that mathematically impossible
- 3/4 validation silhouette IoU: target ≥ `0.975`
- inner pink patch contour should visually/quantitatively align; target patch IoU ≥ `0.965` when segmentation is reliable

### Hoof
- locked primary dimension error: target ≤ `0.003 H`
- Front/Side/Top normalized silhouette IoU: target ≥ `0.990`
- do not call executor visual precheck PASS below `0.985` in any of Front/Side/Top unless a documented reference inconsistency makes that mathematically impossible
- 3/4 validation silhouette IoU: target ≥ `0.975`
- three-toe / two-cleft count must be visually unambiguous in Front and coherent in Top/3Q

Also record a normalized contour-distance metric if practical. Use it to find local mismatch, not as a substitute for visual inspection.

## 9.3 Important limitation

The approved sheet was image-generated and may contain tiny cross-view inconsistencies or antialiasing/shading ambiguity.

Do NOT create physically incoherent geometry to obtain a fake perfect pixel score.

If all coherent low-dimensional solutions plateau below the target:

- preserve the locked numeric contract;
- preserve one coherent 3D module;
- report the exact residual view/region and metric;
- do not hide it with per-view geometry.

A coherent 3D residual is preferable to camera cheating.

---

# 10. Automated fitting implementation

Do not add external dependencies.

You may use Blender's bundled Python / `numpy` if available.

For module masks:

- load the WebP directly in Blender/Python;
- work from the exact 2×2 quadrants;
- remove near-white background;
- exclude the low-saturation cream helper stub;
- retain the main brown/pink module component;
- compare shape in a normalized module-local bounding box.

Use flat emission/material-ID renders to avoid lighting contaminating the geometry metric.

Do not run full Cycles beauty renders during every parameter evaluation.

A low-resolution diagnostic render is enough during fitting; render final evidence at higher resolution only after convergence.

Use a low-dimensional parameter search / coordinate descent / bounded search. Do not add SciPy just for optimization.

Compute work is cheap; repository complexity is not. Prefer one deterministic script over many manual intermediate files.

---

# 11. Subdivision / topology rules

The final source asset should remain editable.

### Ear
- structured deformation-friendly topology;
- continuous closed surface;
- no nonmanifold edges;
- no zero-area/duplicate faces;
- no self-intersection in the visible shell;
- smooth normals;
- Subdivision Surface may remain non-destructive if it is part of the evaluated final shape;
- judge the evaluated result.

### Hoof
- continuous closed surface;
- no detached toes;
- no nonmanifold edges;
- no zero-area/duplicate faces;
- no self-intersection;
- clean smooth shading;
- topology may be denser than the ear because independent toe articulation is not required, but do not create wasteful sculpt density.

Do not force “all quads” as an aesthetic religion if a tiny hidden cap requires a harmless triangle, but the main surfaces should be structured and predictable.

No final voxel-remesh topology.

---

# 12. Preserve v011 — hard freeze gate

Before modification record frozen data for every object outside the allowed module set.

After module integration prove that unrelated source geometry did not change.

At minimum verify:

- object name
- object transform
- mesh vertex count
- mesh face count
- vertex-coordinate digest
- face-connectivity digest
- material slots

for all frozen mesh objects.

The high-quality v011 face must remain bit-for-bit geometrically unchanged.

Do not “fix” the known v011 Side/head issues in this task.

This task is ear + hoof only.

---

# 13. Integration visual gate

After standalone module fitting, integrate the modules into the v011 source copy.

Render the same neutral scene from:

- Front
- Side
- derived 3/4 left
- derived 3/4 right
- derived Top only if it materially helps ear/hoof inspection

Use current source cameras/registration where applicable.

Do not change camera to flatter the result.

Inspect:

### Ear
- root seating
- visible thickness
- broad soft tip
- no pasted-on cylinder
- no head/eye clipping
- bilateral symmetry in neutral
- full-spatial coherence in 3/4
- sufficient root clearance for future independent motion

### Hoof
- planted contact
- three-lobe read
- shallow clefts
- depth from Side
- no flat-card look
- no heel over-bulk
- no limb/hoof visible cut line
- support centers unchanged
- same design family on all four supports

Because v011 has unrelated known non-module issues, whole-image pixel difference is NOT the integration metric.

Evaluate localized ear/hoof ROIs and verify unrelated frozen geometry exactly rather than failing the task because of an old v011 Side defect.

---

# 14. Minimal motion-readiness preflight

Do not build a production rig.

Ear only: perform one disposable geometric clearance probe around the intended root/pivot sufficient to detect immediate head/fleece-clearance impossibility. Keep the amplitude small and representative. This is not a motion quality test.

Hoof: confirm neutral load-bearing/contact logic and insertion; no animation probe is required unless the geometry itself raises a clear support issue.

Do not start the Carol motion library.

---

# 15. Critical failure scenarios already simulated

Treat the following as explicit constraints.

## Failure A — fitting the four sheet cells as four independent shapes
Result: camera-specific fake geometry.

Prevention:
- one mesh;
- fit Front/Side/Top jointly;
- 3/4 validation only;
- no per-view morphs.

## Failure B — literal sheet-pixel fitting uses unknown panel margins as scale
Result: wrong real dimensions.

Prevention:
- normalized silhouette for shape;
- world scale from the numerical contract.

## Failure C — AI sheet views contain tiny inconsistencies
Result: grotesque twist/flattening in order to chase 100% IoU.

Prevention:
- coherent low-dimensional fit;
- numeric contract wins over impossible micro-conflicts;
- report residual instead of cheating.

## Failure D — ear is pretty from Front but paper-flat
Prevention:
- explicit thickness profile;
- Side + Top gates;
- 3/4 validation.

## Failure E — pink inner ear is a floating card
Prevention:
- integrated bowl/material region in the same coherent ear mesh.

## Failure F — ear root looks pasted on or opens a crack in motion
Prevention:
- hidden saddle overlap;
- stable root pivot zone;
- small clearance probe;
- no Boolean union.

## Failure G — mirrored right ear has negative scale / broken normals
Prevention:
- bake/reflection into mesh coordinates and recalc normals; final transforms positive.

## Failure H — hoof becomes three separate blobs
Prevention:
- single continuous loft;
- no detached toe meshes;
- shallow modeled clefts.

## Failure I — hoof matches Front but is flat in Side
Prevention:
- depth/top/sole numeric locks;
- Side and Top fit gates.

## Failure J — hoof leg transition copies the cream helper cylinder
Prevention:
- helper stub is orientation-only;
- integrate via hidden overlap into the real current limb.

## Failure K — Subdivision shrinks the silhouette after fitting
Prevention:
- measure the evaluated surface after modifiers, never only the cage.

## Failure L — remesh/sculpt destroys deformation-ready ear topology
Prevention:
- no production voxel remesh;
- structured cage + Subdivision.

## Failure M — silhouette metric passes while curvature/cuteness is wrong
Prevention:
- final shaded 3/4 closeups + Human Gate;
- Codex may report executor precheck, never Human PASS.

## Failure N — fixing modules accidentally changes the face/body
Prevention:
- frozen-object digests;
- source blend preserved;
- bounded allowed-object set.

## Failure O — endless polishing / token waste
Prevention:
- deterministic fitting loop is allowed;
- after numerical convergence, at most **two bounded visual/integration correction cycles**;
- if essentially the same blocker survives two cycles, stop under the Two-Cycle Rule and report it. No third cosmetic attempt.

---

# 16. Evidence package

Create:

`docs/production/carol/evidence/hero-modules-v001/`

Minimum useful evidence:

- `README.md`
- `measurements.json`
- `validation.json`
- `ear-module-fit.png`
- `hoof-module-fit.png`
- `integration-front.png`
- `integration-side.png`
- `integration-3q-left.png`
- `integration-3q-right.png`
- `human-review-sheet.png`

The module-fit images should make comparison fast: reference, render, overlay/difference, and metrics for Front/Side/Top/3Q.

Do not generate dozens of redundant renders.

Evidence must state:

- source branch/commit
- source blend SHA-256
- approved module image SHA-256
- changed object names
- frozen-object verification
- exact module dimensions
- silhouette metrics
- topology/manifold diagnostics
- support centers before/after
- executor visual precheck
- Human Gate = PENDING unless the Human explicitly reviews it later
- known limitations / residuals

---

# 17. Gate definitions

## TECHNICAL_MODULE_GATE = PASS only if

- source authority hashes verified;
- unrelated geometry frozen;
- ear/hoof numeric locks within the task target or a documented unavoidable reference inconsistency;
- ear and hoof are coherent 3D objects;
- no nonmanifold/degenerate/self-intersection blocker;
- hoof support centers unchanged;
- ground contact valid;
- no negative final object scale;
- module fitting metrics recorded.

## EXECUTOR_VISUAL_PRECHECK = PASS only if

- no visible root/gap/clipping defect;
- Front/Side/Top module fit is near-authority quality;
- 3/4 does not expose a flat/fake form;
- ear retains Carol softness/roundness;
- hoof retains heavy planted 3-lobe identity;
- no new visible defect dominates Human review.

## HUMAN_GEOMETRY_GATE

Always leave as:

`PENDING HUMAN REVIEW`

Codex must not self-approve cuteness/identity/appeal.

If the visible result is too low-quality for a fair Human decision, mark `PROBE_INVALID`, not PASS/FAIL.

---

# 18. Attempt / stop policy

Automated numeric fitting iterations do not count as separate Human-facing attempts.

After automated convergence:

- Visual correction cycle 1 allowed.
- One targeted visual correction cycle 2 allowed only if cycle 1 has a concrete identified mismatch.
- If the same blocker remains after cycle 2, STOP.
- No cycle 3.
- Do not restart the whole Carol.
- Do not redesign authority.

---

# 19. Scope prohibitions

Do NOT:

- work on fleece geometry;
- implement the new fleece motion rule here;
- create an armature/production rig;
- animate Carol;
- export GLB;
- integrate PlayCanvas;
- touch Next.js;
- modify canonical/Normal/Skin/module authority images;
- fix v011 face/head/torso;
- rewrite project architecture;
- add unrelated tests;
- run full app/build/browser/device QA;
- add new packages;
- use external 3D/image generation services;
- create per-view geometry cheats;
- use subagents.

Run only the checks needed for the changed Blender geometry.

---

# 20. Production-state update

If the module task reaches a Human-review-ready candidate:

Update:

`docs/production/carol/CAROL_PRODUCTION_STATE.md`

Record:

- branch
- new asset
- source v011 hash
- ear/hoof module gate results
- silhouette metrics
- frozen-object verification
- Human Gate = PENDING
- fleece remains NOT STARTED in this task
- next handoff = Human review of Hero ear/hoof modules, then planner decision on v006 fleece donor adaptation.

Do not rewrite historical sections.

---

# 21. Commit / push

When the bounded task is complete:

1. inspect `git diff`;
2. ensure no temp files/caches are tracked;
3. commit all intended tracked outputs;
4. push branch `codex/carol-hero-modules-v001`;
5. ensure worktree is clean;
6. report branch + commit SHA + concise gate result + exact Human review artifact path.

Suggested commit subject:

`feat(carol): build hero ear and hoof modules`

---

# 22. Final response format

Return only a compact execution report:

- Branch
- HEAD
- Source v011 SHA-256
- Asset path
- Ear metrics
- Hoof metrics
- Frozen-object status
- Technical Module Gate
- Executor Visual Precheck
- Human Geometry Gate
- Evidence path
- Any unresolved blocker

Do not write a long retrospective.

---

# 23. Final decision principle

The goal is not to prove that the script ran.

The goal is:

> **A Human should be able to inspect Carol's ears and hooves from Front, Side, Top/3Q exposure and see no obvious approximation, flatness, generic placeholder quality, bad attachment, or mismatch with the approved module references.**

Preserve the v011 face. Build the best coherent ear and hoof modules the approved evidence supports. Stop rather than cheat if the references themselves become the limiting inconsistency.
