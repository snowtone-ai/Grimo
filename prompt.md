# Handoff — Carol v006 Geometry Final-Convergence Task

Target model: **CODEX_Astra_XHIGH**  
Execution mode: **single agent only / no subagents**  
Repository: `snowtone-ai/Grimo`  
Working branch: **`codex/carol-zero-based-hero-geometry-v005`**

---

## 0. Mission

You are not doing planning-only work. You are doing **actual geometry correction work**.

Your task is to take the current Carol v006 checkpoint and **push the geometry substantially closer to true acceptance quality**, with the explicit priority of fixing the currently visible shape failures in the Human Review page.

This is a **shape task**, not a lookdev task.

The goal is:

> **Carol must stop looking like one continuous clay blob and instead read as a correctly constructed character whose major anatomical/structural parts are clearly and correctly separated, while still matching the approved reference images extremely tightly from all six review views.**

You must work with **millimeter-level seriousness**.  
Do not tolerate “close enough”, “roughly similar”, or “good from one angle” thinking.

---

## 1. Current repository state you must respect

Read and understand the latest repo state before changing anything.

Start by reading these files in this order:

1. `docs/production/carol/CAROL_PRODUCTION_STATE.md`
2. `docs/production/carol/evidence/reconstruction-v006/README.md`
3. `docs/production/carol/CAROL_REVIEW_LOG.md`
4. `docs/production/carol/CAROL_GEOMETRY_DECISION.md`

Current known state:

- Current working asset:
  - `assets/grimo/production/carol/blender/carol-a-v006.blend`
- Current generator:
  - `scripts/blender/build-carol-v006.py`
- Current latest valid checkpoint:
  - **pass 05 / iteration 16**
- Current status:
  - **NOT ACCEPTED / geometry FAIL / Human Gate PENDING**
- Current review page:
  - `http://127.0.0.1:3017/`

Important current conclusion already established in repo state:

- camera-only 3Q adjustments were tested and rejected
- a shared rear/ear candidate was tested and rejected
- iteration 16 is a clean restore checkpoint
- unresolved problems remain real geometry problems, especially in:
  - ear / face correspondence
  - fleece hierarchy
  - lower contour / hoof shaping
  - 3Q identity
  - silhouette coherence

Do **not** waste time rediscovering what the current docs already say.

---

## 2. Geometry authority / source authority

### 2.1 Absolute geometry authority

The shape authority is the approved 3D reference image set under:

`assets/grimo/source/carol/approved-3d/`

Use these as the **formal geometry authority**:

- `carol-front-ortho-transparent.png`
- `carol-side-ortho-transparent.png`
- `carol-back-ortho-transparent.png`
- `carol-top-plan-transparent.png`
- `carol-front-3q-left.png`
- `carol-front-3q-right.png`

### 2.2 Additional authority

Also use:

- `assets/grimo/source/carol/carol-Identity-canonical.png`

Use Identity-canonical for:
- identity preservation
- motif placement sanity
- overall character feel
- face feeling / charm guardrail

But for body construction and six-view shape matching, the **approved 3D set has priority**.

### 2.3 Explicit non-authorities

Do **not** treat the following as geometry authority:

- old B route
- retired B geometry
- old historical source GLB
- fixed historical front screenshot
- material appearance
- flattering single-view resemblance

Old assets are **look-only reference at most**, not geometry authority.

---

## 3. Hard rules

### 3.1 Single-agent rule
Use **one agent only**. No subagents.

### 3.2 No cheating with cameras
Do **not** “solve” geometry by only changing 3Q camera correspondence.  
Camera-only 3Q candidates were already tested and rejected.

### 3.3 No view-dependent hacks
Do not create geometry that only works from one view and collapses elsewhere.

### 3.4 No fake acceptance
Do not claim acceptance just because numbers improve a bit.
The goal is not cosmetic metric gaming; it is **actual six-view structural convergence**.

### 3.5 Scope discipline
This task is primarily:
- geometry
- proportions
- part separation
- silhouette
- structural read

Do **not** spend the session on:
- final material rendering
- texture polish
- runtime integration
- rigging
- export
- animation
unless absolutely required for geometry validation.

---

## 4. Core diagnosis you must internalize before editing

The current main failure is not merely “some spheres are wrong”.

The deeper failure is:

> **major body parts are not sufficiently articulated as independent structural masses.**

Right now, several regions still read like:
- one blob of clay
- inflated bead packing
- stretched fleece
- face inserted into a generic round volume
- ears / tail / legs emerging as vague lumps instead of true parts

This must change.

Carol must read as a coherent character with clear structural differentiation among:

- head / facial mass
- cheek / muzzle zone
- ear base and ear bowl
- torso / main fleece body
- rear / butt mass
- tail tuft as an independent rear organ
- four leg/hoof structures as independent supports

---

## 5. Highest-priority correction goals from the user

You must center the work on the following corrections.

---

## 6. View-by-view correction brief

### 6.1 Front view — highest issues

Fix these specifically:

1. **Ear attachment position**
   - Ear roots are wrong.
   - Their vertical placement and lateral emergence must match the approved front view much more precisely.
   - They must feel attached to the correct head/body transition zone, not arbitrarily stuck into fleece.

2. **Cheek fullness**
   - The cheeks need correct soft puffiness.
   - The face should feel cute and volumetric, not flat, not generic, not overly circular.

3. **Ear shape**
   - Ear silhouette must be corrected.
   - Thickness, taper, bowl shape, and outer contour must match the approved reference more faithfully.

### 6.2 Side view — highest issues

Fix these specifically:

1. **Ear shape and root placement**
   - Side view currently reveals incorrect ear construction and attachment.
   - Correct root depth, angle, thickness, and silhouette.

2. **Face construction**
   - The face is currently too much “just a circle”.
   - This is wrong.
   - Build the face as actual form:
     - cheek volume
     - muzzle/nose zone relief
     - mouth recess / facial opening logic
     - proper front-face projection vs surrounding fleece

3. **Tail independence**
   - The tail region currently reads like an extension of the butt mass.
   - This is wrong.
   - The tail must read as an **independent organ**, attached to the rear, not merely a continuation of the fleece body.

4. **Leg construction**
   - Legs are currently too much like round blobs.
   - This is wrong.
   - Build them as believable independent support structures with clearer hoof/leg distinction.

### 6.3 Back view — highest issues

Fix these specifically:

1. **Rear / butt / tail region**
   - The rear area currently looks badly broken / stripped / poorly resolved.
   - Tail and rear mass need clearer structure and better correspondence.

2. **Ear position**
   - Rear ear placement is off and must be corrected.

3. **Leg construction**
   - Back view still exposes overly spherical / generic legs.
   - Rear support structures must read more intentionally.

### 6.4 Top view — highest issues

What is currently good:
- the overall silhouette direction is already closer than some other views

What is still wrong:
1. **Ear separation**
   - Ears do not read as clearly separate parts.
2. **Tail separation**
   - Tail does not read as an independent rear structure.
3. **“Single stretched clay” problem**
   - From top view, the model still feels too much like one continuous mass stretched outward.

You must preserve what is already relatively successful in top silhouette **while increasing part separation clarity**.

### 6.5 3Q left / right — highest issues

This is extremely important.

The current major problem is:

> **The fluffy head mass reads too large, making the head/skull feel like the dominant volume.**

This is wrong.

The correct read is:

- head
- body / back / main torso fleece
- rear / butt

And among these:

> **the largest overall mass should read as the body / torso zone, not the head.**

Additional critical instruction:

- In the two 3Q views, the **left 3Q reference is the more correct mental guide** for mass separation.
- The left 3Q view more clearly reads:
  - head
  - back/body
  - rear
- The right 3Q view currently needs to be pushed toward that same clearer structural separation.

Therefore:
- reduce the feeling that the head canopy dominates everything
- improve the read of torso as the largest main mass
- make rear mass legible behind/after torso
- keep face embedded correctly rather than swallowed by generic fleece

---

## 7. Global structural principles you must enforce

These are not optional.

### 7.1 Independent-part principle
Ears, tail, and legs must be modeled as **independent structural organs**, not vague bumps in a unified blob.

### 7.2 Main-mass hierarchy
The mass hierarchy must read approximately as:

- **largest**: torso / main body fleece
- secondary: rear / butt mass
- smaller but distinct: head / facial mass
- attached independent organs: ears / tail / four legs

### 7.3 Face is not a circle
The face must stop reading as a simple inserted disc or sphere.
It must have:
- cheek fullness
- muzzle / nose relief
- mouth recess logic
- stronger facial spatial organization

### 7.4 Four-support readability
All four legs/hooves must read as distinct supports.
No “pebble supports”.
No “merged underbody bumps”.

### 7.5 Rear clarity
Rear structure must be understandable.
The tail must emerge from the rear, not dissolve into it.

### 7.6 Cloud/fleece hierarchy
Do not let fleece devolve into repetitive equal-sphere packing.
Major clusters must support the body structure and silhouette logic.

---

## 8. Recommended execution strategy

Follow this workflow.

### Step 1 — Re-open and inspect current state
- Read the docs listed above.
- Re-open or regenerate the current review state.
- Confirm the current visible failures yourself in all six views.

### Step 2 — Diagnose shared root causes
Before editing, explicitly determine which failures are shared by multiple views, especially:
- ear root placement
- overgrown head canopy
- weak torso-vs-head hierarchy
- fused rear/tail construction
- blob-like leg construction
- insufficient cheek/muzzle structure

### Step 3 — Make geometry edits, not cosmetic excuses
You may modify:
- generator logic
- section/chassis logic
- cluster placement
- local sculpted form
- part transitions
- ear construction
- leg / hoof shaping
- rear / tail attachment logic

If the current construction method blocks correct shape, **change the construction method**.

### Step 4 — Validate repeatedly
After major passes, regenerate the review outputs and inspect:
- front
- side
- back
- top
- 3q-left
- 3q-right

Do not continue blind.

### Step 5 — Converge, then package evidence
When you have meaningfully improved geometry:
- regenerate review assets
- confirm browser review works
- save evidence
- commit
- push
- stop at the Human review stage

---

## 9. What “success” means in this session

You are not allowed to interpret success lazily.

Success means the updated model clearly improves the user’s cited failure modes:

### Must visibly improve
- correct ear root placement
- more correct ear shapes
- puffier / better-constructed cheeks
- side face no longer just a circle
- tail clearly independent from rear mass
- legs no longer simple round blobs
- back view rear/tail/ears less broken
- top view shows clearer ear/tail separation
- 3Q head no longer dominates incorrectly
- torso clearly reads as the largest main mass

### Must not regress
- overall six-view coherence
- previously improved silhouette logic
- top-view macro silhouette
- global body identity
- approved reference alignment discipline

### Forbidden outcome
Do **not** produce a result that improves one view while obviously worsening several others.

---

## 10. Quantitative metrics vs visual truth

Use the existing metrics pipeline and diagnostics, but do **not** become a metric-only optimizer.

Your hierarchy is:

1. obvious visual structural correctness in all six views
2. cross-view coherence
3. metrics support
4. documentation / evidence packaging

If metrics improve but the character still reads like fused clay, that is not success.

---

## 11. Files and tooling

Primary editable targets likely include:

- `assets/grimo/production/carol/blender/carol-a-v006.blend`
- `scripts/blender/build-carol-v006.py`

Use the existing repo tooling and saved review workflow documented in:

- `docs/production/carol/evidence/reconstruction-v006/README.md`

Do not invent a parallel workflow if the repo already has the needed one.

---

## 12. End-of-task deliverables

By the end, you must provide a clean handoff state with:

1. updated geometry source
2. updated generator/script if changed
3. regenerated review/evidence outputs
4. local review page working
5. commit created
6. push completed
7. final report

### Final report must include:
- branch name
- commit hash
- what was changed
- what user-priority issues were addressed
- what still remains if anything
- exact files touched
- exact command(s) used to re-open the review page
- confirmation that the browser review page was opened and left ready for HUMAN inspection

---

## 13. Final behavioral instruction

Be bold enough to restructure local geometry where necessary, but disciplined enough to preserve cross-view coherence.

Do not be timid.  
Do not be sloppy.  
Do not hide behind camera excuses.  
Do not stop at “somewhat better”.

Your job is to make Carol’s geometry **materially more correct** according to the approved six-view references and the explicit user corrections above, then package the result cleanly for immediate HUMAN review.

Begin now.