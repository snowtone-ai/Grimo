# Grimo — Blender Implementation Guide

**Status:** Active implementation guide  
**Updated:** 2026-10-10  
**Scope:** Blender / rig / deformation / glTF implementation technique only

This guide does **not** decide architecture, production order, gates, or the next
task. Those belong to the Production Architecture, Production Operating System,
and current production state.

## Implementation rules

- Author one coherent spatial character, not geometry that is only valid from a
  single camera.
- Preserve exterior validity through practical Front / 3/4 / Side / Rear /
  derived Top exposure and the articulation range relevant to current or
  reasonably anticipated companion motion.
- Apply view-weighted polish: **HERO_PRIORITY** gets the highest aesthetic
  investment; **GENERAL_EXTERIOR** must remain coherent; **MOTION_CRITICAL**
  regions need the deformation/attachment quality demanded by behavior;
  **FUNCTIONAL_HIDDEN** needs functional correctness rather than beauty.
- Modular/separate meshes are valid. One continuous watertight Hero body and
  all-quads everywhere are not product requirements.
- Quad-friendly authoring is useful where deformation/editability benefits, but
  GLB runtime topology is triangulated; inspect exported behavior when relevant.
- Rig semantic controls needed by the experience: head/gaze/face, ears,
  forelimbs/hooves, support/COM, tail, and Carol fleece regions.
- Give appendages and fleece real ownership hierarchies. Avoid a face sliding
  inside stationary fleece, ears appearing/disappearing because of bad
  attachment, or secondary motion that reads as separate sticky material.
- Prefer authored primary acting plus bounded corrective deformation and
  restrained secondary follow-through. Physics must not define Hero acting,
  facial meaning, touch causality, or the main fleece silhouette.
- Corrective morphs, bones, material states, local shader controls, and local
  compositing may be combined when they preserve identity and export reliably.
- Bake/evaluate Blender-only constraints or drivers when GLB/glTF cannot carry
  their runtime behavior directly.
- Validate the exported GLB, not only the Blender scene, when export/runtime is
  part of the Decision Question.

## Asset selection and historical evidence

Current and historical assets can provide donor geometry, fleece, rig/control
patterns, generator scripts, or benchmark evidence. Inspect those that are
**relevant to the current decision**, rather than mandating an exhaustive
historical review or always preferring reuse. Codex chooses whether to reuse,
reshape, rebuild, or replace based on observed quality and downstream risk,
as defined by the active Production Operating System.

Do not discard a demonstrably stronger asset for an easier but weaker
approximation; likewise, do not preserve a weak donor solely because it exists.
Current canonical identity and approved visual references take precedence.

## Character modeling craft — sourced principles and Grimo application

This section is **implementation advice**, not a prescribed pipeline or a new
quality authority. Project canonical references, Human decisions, architecture,
and current production state remain authoritative. A technique is not
"Grimo-validated" merely because a professional tutorial recommends it.

### Shape design before detail (professional production evidence)

Blender Studio's *Sprite Fright: Sculpting Advice* and *Sculpting Pets* describe
design exploration that iterates between 2D art and 3D sculpting. An initial
drawing is not proof that its forms work in 3D; early sculpts can expose
proportion, expression, attachment, and acting problems. They also recommend
avoiding detailed polish before the underlying design stabilizes.

**Grimo application (inference; validate on assets):**

- Compare large/medium/small volumes and negative spaces against the approved
  identity before spending effort on fine surface detail. Prioritize silhouette,
  facial appeal, depth/profile, weight, and coherent anatomical connections.
- Inspect the model in a readable shaded Hero view *and* diagnostic views.
  Attractive material/lighting must not hide a wrong silhouette or volume.
- A gentle characterful pose/expression can make an appeal review more legible,
  but do not confuse temporary presentation posing with a tested production rig.
- Revisit 2D references or use draw-over comparisons when a mathematically
  good overlay still looks wrong. Never silently revise canonical identity.

### Choose tools for the failure, not for their reputation

| Technique | Useful when | Failure to watch |
| --- | --- | --- |
| Direct mesh/edit-mode operations or `bmesh` | Explicit control of measured forms, attachment and local mesh edits | Faceted or mechanical contours; brittle local vertex patches |
| Sculpting/remesh/proportional deformation | Exploring organic transitions, appealing volumes and asymmetry | Lost approved proportions; uncontrolled topology/detail |
| Procedural `bpy` geometry, curves or modifiers | Repeatable construction, parametrized variation and inexpensive iterations | Formula-fitting a view while the 3D form becomes awkward |
| Retopology plus deformation tests | A selected form needs stable bend, facial controls, or export | Early topology work that preserves a weak design |

These are complementary options, not mutually exclusive required stages.
Codex may use GUI-authored, scripted or hybrid approaches as justified by the
actual problem. A Python-generated mesh is not inherently lower quality than
a hand-sculpted mesh; evaluate the artifact and its future behavior.

### Carol-focused diagnostic examples

Use these only when a corresponding visible issue or credible motion risk exists:

- **Face / eyes / muzzle:** verify pleasing eye-to-socket mass and muzzle depth
  in Front, 3/4 and Side; measure without mistaking numerical fit for appeal.
- **Crown fleece / cheek / neck:** check perceived volume, recesses, continuity
  of head/body mass, and whether fleece follows the face/neck during movement.
- **Ears / tail / legs / hooves:** check root placement and thickness, support
  and ground contact, and how exposed seams/clearance behave with local turns,
  weight shifts, or bends.

When a comparison could change the production decision, compare against the
**strongest relevant baseline** (not automatically the newest checkpoint), with
consistent camera, scale, lighting and source attribution. Do not normalize away
a requested size change. Human-facing identity and cuteness remain Human-owned;
silhouette overlap, closed meshes and topology diagnostics cannot award them.

### Semantic 2D-to-3D translation — Carol's current high-risk craft problem

**Evidence:** Carol's current production-state record rejects v004-33's inflated
fleece despite strong outline fit; checkpoint 41 is an unapproved proportion
study. The canonical and approved Normal Front/Side remain visual authorities.
The following are `GRIMO_HYPOTHESIS / NOT_TESTED` decision aids, **not** a
new geometry recipe, permission to edit approved art, or a claim that v004-41
passes. The professional precedent is
[Blender Studio's *Sculpting Pets*](https://studio.blender.org/blog/pets-expression-sculpting/):
artists explored 2D/3D volumes and extreme expressions together before focused
topology work; that film workflow is evidence of *design iteration*, not a
required smartphone-game production sequence.

- **Separate painted boundaries from actual volume boundaries.** In Carol's
  moon/star/blue-white wool, a colored patch, highlight or drawn lobe edge does
  not automatically justify a full-depth swelling, mesh island or groove.
  Judge which masses carry the head, neck and torso, which smaller locks merely
  overlap those masses, and which accents can remain shallow/material-owned.
- **Check a readable head–neck–torso hierarchy.** The face projects from a
  compact head; a smaller head/neck wool surround belongs to that region; the
  larger rounded body sits behind it. Keep the lower wool rooted around the
  neck instead of reading as a padded jaw; avoid a large inflated halo,
  helmet/collar shelf or a seamless giant cloud with a pasted-on face. This
  describes the *current observed defect and user intent*, not universal
  sheep anatomy.
- **Treat negative space as a designed shape.** Inspect the face opening,
  side facial depth, ear-root pocket, neck constriction, belly-to-hoof
  clearance and silhouette breaks. Uncontrolled smoothing, voxel remesh or
  larger wool balls can erase them while improving numerical contour fit.
- **Separate shape from rendering deception.** Inspect a readable clay/
  value-neutral version to judge genuine depth and the production-like
  colored, glossy version to judge identity; neither view alone proves
  approval. In particular, painted shadows, emission and eye highlights may
  mask a weak socket, jaw, or wool transition.
- **Diagnose at the correct scale.** First distinguish a macro mass-placement
  error from a local lobe/edge problem. A repeated patch to many small locks
  should not disguise a wrong head-to-body relationship. Compare the relevant
  alternatives under equal camera **and actual scale**, then allow Codex to
  choose sculpt, scripted field, part replacement, or mixed edits.
- **Do not transfer the rule mechanically to other Grimo.** Jill's wings,
  Pino's otter torso and Shushu's floral elements have different spatial
  signatures. Transfer *the questions* (primary masses, negative space,
  silhouette/face appeal, motion ownership), not Carol's anatomy.

### Appeal and deformation — different evidence questions

A good neutral image is not a successful blink or cheek interaction. Before
locking a motion-critical region, select only the nearby behaviors that could
materially invalidate its shape: for example open/partial/closed eye and gaze
for the eye socket; small yaw/lean plus ear motion for a head/neck-wool seam;
local cheek compression for contact seeking; planted/support-shift pose for a
hoof. Temporary sculpt variants or pose proxies can reveal risk **without**
claiming a working rig. If the proxy is too crude to judge the relevant
appearance, label its result inconclusive.

Human-face retopology and the lesson's mostly-upper-eyelid closure are
**examples**, not Carol deformation laws. The correct lid path, ocular surface,
socket volume, eyelash/eye-highlight coordination and cuteness must be chosen
from Carol's own approved identity and tested through actual visible
expressions. Likewise shape-key storage requires compatible mesh topology;
independent remeshed expression sculptures can be *design probes* but are not
automatically usable as in-game morph targets. Keep attachment ownership clear
when expressive head, ear, ornaments and wool regions move.

### Topology, motion and delivery boundary

Professional blocking material (e.g. Dikko's *Modeling for Animation 02*)
demonstrates planning articulation and checking rough motion early. It is an
example from humanoid animation, **not** proof of Carol-specific joint layout.
Use a small relevant articulation or attachment probe to expose design limits
when a plausible motion depends on them. Do not require final retopology or a
full animation library before such a probe.

**Current exporter boundary (Blender 5.2; version-check before use):**
[Blender's glTF manual](https://docs.blender.org/manual/en/5.2/addons/scene_gltf2.html)
lists object transforms, pose bones and shape-key values as animation channels,
not arbitrary modifier/driver/material behavior. Since Blender 4.4, action
**slots** affect how `Actions` mode groups animation; `NLA Tracks` and
other export modes have different clip behavior. The manual documents a
specific exception for sampling shape keys driven by bone transformations:
the mesh must be a direct child of the armature. A generic instruction to
"bake drivers" is insufficient proof that every rig relationship survives.
Inspect exported clip names, channels, rest poses and coupled deformations.

**Materials are a separate high-risk boundary.** Blender-only combinations
of diffuse/emission mixes, custom nodes, procedural paint and viewport color
management must not be assumed to reproduce in glTF's supported material
model. v004 currently uses a painted-shade system; its **runtime appearance is
UNVERIFIED**. Compare a representative GLB's colors, eye gloss, wool shading
and decoration against the approved Blender presentation and adapt shader,
texture baking or PlayCanvas material behavior only if needed.

[PlayCanvas GLB import](https://developer.playcanvas.com/user-manual/assets/models/building/)
supports skinning and morph targets, but feature support is not a guarantee
that this particular rig, custom material, or blending setup looks or acts
the same. When export is relevant to the decision or production lock,
validate the **actual GLB in PlayCanvas**. For smartphone feasibility, examine
asset/texture memory, mesh/draw-call and morph costs, frame pacing and touch
responsiveness on available hardware; use
[PlayCanvas optimization guidance](https://developer.playcanvas.com/user-manual/optimization/guidelines/)
as a diagnostic, not an arbitrary per-character budget. The available
Xiaomi 14T Pro cannot certify an untested Pixel 7a-class device.

### Video-transcript field notes (2026-10-10)

**Evidence boundary.** The following notes were extracted from accessible,
complete narration transcripts: the **official Blender Studio English VTT**
where available, and YouTube transcript text for the other videos. These are
**transcript-grounded summaries**, not claims of watching/visually inspecting
every video frame or reproducing a technique inside Blender. Automatic
transcripts can mistranscribe UI commands; verify actual Blender version and
controls before use. Video advice is not automatically Grimo production law.

#### A. Design, reference and sculpting

- **Art style sets animation expectations** ([Defining Goals](https://studio.blender.org/training/stylized-character-workflow/5d3a1b3d4bc3ff1bb9513d38/), ~00:00–02:00, official subtitles): the character's design abstraction and detail level affect plausible acting. For Grimo, consult the approved identity and motion authority together; do not "improve" the face by accidentally switching visual style. `EXTERNAL_GUIDANCE`.
- **Reference has distinct jobs** ([Julien Kaspar, complete workflow overview](https://www.youtube.com/watch?v=f-mx-Jfx9lA), ~01:30–03:00, matching [free Studio subtitles](https://studio.blender.org/training/stylized-character-workflow/5df42aaf5f68a29e408d6118/)): distinguish identity/concept, visual style, implementation examples (e.g. fur) and real-world anatomy/material behavior. Grimo identity art remains authority; observed reality is evidence for plausible weight/contact, not a replacement design. `EXTERNAL_GUIDANCE`.
- **Block large forms using separate primitives before detailing** (Kaspar ~03:00–06:30; [Creating a Primitive Body](https://studio.blender.org/training/stylized-character-workflow/5d7f7cf055ccaf1a4a78102d/), ~00:00–06:00, official subtitles). Separate objects and symmetry allow fast proportion changes; sculpt/remesh can be used after mass relationships work. Preview color can conceal inaccurate volume, so periodically use clay/untextured inspection. `EXTERNAL_GUIDANCE`.
- **A scripted basemesh and a sculpt are alternative tools, not opposing doctrines**: Kaspar starts by arranging/sculpting primitive forms; [Dikko's body blocking](https://www.youtube.com/watch?v=4vAqPaFv8QA), 01:00/04:25/11:30 chapters and transcript, uses orthographic references plus a mesh/blockout with articulation loops planned early. Both approaches have credible production rationale. Choose per observed defect, not dogmatic "professional means sculpting." `EXTERNAL_GUIDANCE`.
- **Visualize a 2D concept as actual 3D masses and temporarily pose parts** ([Kaspar, Blender Conference 2023 live sculpting](https://www.youtube.com/watch?v=FDscc66fC90), transcript): independent objects, linked symmetric object data, and a side-by-side reference/camera help reveal pose and volume problems before detail. Treat 2D-to-3D interpretation as design work rather than one-camera pixel matching. A camera/lighting comparison alone is not a completed deformation test. `EXTERNAL_GUIDANCE`.

#### B. Retopology, facial expression and motion

- **Test expressions before investing in final topology** (Kaspar ~08:30–12:00): a rough, deformable head lets eyes/mouth tests expose a default design that fails during blinking/smiling. Later create efficient retopology for real articulation. For Carol, do not wait for a fully finished rig to ask whether closed eyelids, gaze or fleece attachment remain appealing. `EXTERNAL_GUIDANCE`.
- **Blink mechanics** ([Basic Expression Shapekeys](https://studio.blender.org/training/stylized-character-workflow/5da05942e2e7bac4cc81bd5a/), ~00:00–03:00, official subtitles): eyelids slide over the eye surface; the upper lid does most of the closing and the lower lid moves less. A shape-key example starts with `Basis`, `eyes closed` and `mouth open`. This is an illustrative human/stylized workflow, **not** a numerical motion contract for Carol. `EXTERNAL_GUIDANCE`.
- **Coupled visible parts must follow their parent expression** (same Studio lesson ~15:00): example drivers propagate head expression-key values to separate eyelashes. For Carol, test eye/socket, cheek fleece, ears and head ownership where applicable. Blender drivers may not survive glTF export as drivers; bake/recreate/export and test the resulting motion in PlayCanvas. `EXTERNAL_GUIDANCE` / Grimo export inference.
- **Topology should serve deformation, not topology purity** ([Planning the Facial Retopology](https://studio.blender.org/training/stylized-character-workflow/5e5407ec8faf011a381510d7/), ~01:00–07:00, official subtitles): plan loops around articulating eyes/mouth, supporting landmark boundaries and anticipated compression; strategically redirect loops rather than creating uncontrolled spirals. Several loops support curved eyelid/lip arcs, but count and arrangement vary by model and motion. `EXTERNAL_GUIDANCE`.
- **Avoid hardcoding human-face edge maps** ([Dikko, Retopologising the Face](https://www.youtube.com/watch?v=SwM19PgSdCM), full transcript): his equal upper/lower eyelid/lip span counts and deliberate edge-flow transitions make his example easier to rig; he explicitly rejects a universal required span count. Use these as *questions to test* on Carol's non-human face, not mandatory coordinates, vertex counts, or universal pole bans. `EXTERNAL_GUIDANCE`.
- **Design may need revision after expression tests** (Kaspar ~10:00–11:45; Studio course expression section): when eyelids, eye shape or face proportions cannot sustain an appealing expression, revisit the static form before hiding the problem with shader/animation tricks. Final aesthetic approval remains Human-owned. `EXTERNAL_GUIDANCE`.

#### C. Small Carol experiments that can validate these lessons

These are **GRIMO_HYPOTHESIS / NOT_TESTED**, not work performed in this
documentation update. Run only when they answer a current visible blocker or
credible near-term motion risk; reuse the current candidate as the baseline.

| Observed problem | Lowest-cost meaningful comparison | Evidence to retain |
| --- | --- | --- |
| Crown, cheek or neck fleece reads as swollen/colliding | Compare existing candidate to one separate-volume sculpt/shape variation; same Front/3/4/Side clay camera | Off-axis volume, face opening and neck continuity, approval pending |
| Eyes look unsettling or blink appears impossible | Temporary `eyes closed` expression (shape key, mesh edit or equivalent) including visible eyelid/eyelash relationships | Open/half/closed comparison, socket and silhouette integrity |
| Head turns reveal face/fleece slipping | Short yaw/pitch probe with owned attachments; no full rig required | Before/after seam/root positions, 3/4 and Side behavior |
| Hooves/legs appear thin or lose ground contact | Low-cost articulation/support pose of affected limb | Contact, thickness and perceived weight in useful views |

If a low-cost scripted solution passes the relevant comparison, **do not force
a sculpting rebuild**. If it consistently fails perceptually, a small organic
sculpting/retopology alternative can be evaluated. No test above awards a Human
Gate or proves runtime performance without the required evidence.

### Learning notes: retain only useful, auditable insights

When external material changes a real production decision, preserve a *small*
entry here rather than creating another production bible:

- **Problem / relevant region:** the observed defect or capability gap.
- **Source / access:** URL, what was actually reviewed (article, docs, video,
  description only), and date. Do not imply a video was watched if only its
  public description was inspected.
- **Principle / status:** distinguish `EXTERNAL_GUIDANCE` from
  `GRIMO_HYPOTHESIS`, `GRIMO_VERIFIED` and `REJECTED`.
- **Application / evidence:** affected asset or commit, comparison evidence,
  and perceptual/functional outcome; state `NOT_TESTED` when applicable.
- **Reuse boundary:** where the technique might transfer to other characters,
  and where it does not.

Do not transcribe entire tutorials, archive their media, or accumulate a
general-purpose Blender encyclopedia. Consult external references
selectively when they can change an execution decision. Paid training is not
required; do not assume subscriber-only videos were accessed.

### Sources reviewed (2026-10-10)

Primary professional evidence and product documentation:

- [Blender Studio — Sprite Fright: Sculpting Advice (Julien Kaspar)](https://studio.blender.org/blog/sprite-fright-sculpting-advice-for-production/) — direct article; early 2D/3D iteration, sculpt-for-design, poses, detail timing.
- [Blender Studio — Sculpting Pets (Julien Kaspar / Vivien Lulkowski)](https://studio.blender.org/blog/pets-expression-sculpting/) — direct article; parallel 2D concept and 3D character development.
- [Blender Studio — Blender Fundamentals 4.5 LTS](https://studio.blender.org/training/blender-fundamentals-45-lts/) — course overview; several individual fundamentals lessons are free, full course includes paid material.
- [Blender — Stylized Character Workflow with Blender (Julien Kaspar, YouTube)](https://www.youtube.com/watch?v=f-mx-Jfx9lA) — transcript retrieved; relevant narration and official timestamped VTT inspected; not a visual-frame review.
- [Dikko — Modeling for Animation 02 (YouTube)](https://www.youtube.com/watch?v=4vAqPaFv8QA) — transcript retrieved; relevant passages reviewed; broad articulation-planning reference, not Carol-specific proof.
- [Blender Studio — Defining Goals](https://studio.blender.org/training/stylized-character-workflow/5d3a1b3d4bc3ff1bb9513d38/), [Creating a Primitive Body](https://studio.blender.org/training/stylized-character-workflow/5d7f7cf055ccaf1a4a78102d/), [Basic Expression Shapekeys](https://studio.blender.org/training/stylized-character-workflow/5da05942e2e7bac4cc81bd5a/), [Planning the Facial Retopology](https://studio.blender.org/training/stylized-character-workflow/5e5407ec8faf011a381510d7/) — free lessons; official downloadable English VTT transcripts retrieved and relevant passages distilled, not claims of frame-by-frame inspection.
- [Dikko — Retopologising the Face](https://www.youtube.com/watch?v=SwM19PgSdCM) — transcript retrieved; relevant passages reviewed; example human topology, not a required Carol loop pattern.
- [Blender Conference 2023 — Sculpting Live Session](https://www.youtube.com/watch?v=FDscc66fC90) — transcript retrieved; relevant passages reviewed; production sculpt blocking, linked symmetry and concept comparison.
- [Blender Studio Rigging Tools](https://studio.blender.org/training/blender-studio-rigging-tools/) — free course previews/catalogue inspected; CloudRig clips and corrective shape-key addon were **not** reproduced or transcript-verified here; the CloudRig wiki warns that older video instructions can be outdated.
- [Blender 5.2 LTS Manual — glTF 2.0 animation, action slots and exporter limits](https://docs.blender.org/manual/en/5.2/addons/scene_gltf2.html) — current technical cross-check; documentation review, NOT a working Carol export test.
- [PlayCanvas Optimization — General Guidelines](https://developer.playcanvas.com/user-manual/optimization/guidelines/) — current runtime constraints, not a measured Carol cost.
- [Blender 4.5 LTS Manual — glTF 2.0 export and animation](https://docs.blender.org/manual/ja/4.5/addons/import_export/scene_gltf2.html) — direct technical documentation.
- [PlayCanvas — Building Models](https://developer.playcanvas.com/user-manual/assets/models/building/) and [Exporting Assets](https://developer.playcanvas.com/user-manual/assets/models/exporting/) — direct engine documentation.

All Grimo-specific experiments and transfer suggestions are **engineering
hypotheses**, not verified Carol fixes. Eight video transcript sources were
retrieved and their relevant passages reviewed in text form (Kaspar overview; Dikko body and face; 2023 sculpting
session; Studio Defining Goals, Primitive Body, Shape Keys, and Facial
Retopology — eight videos in total); none was visually frame-audited or
reproduced in Blender. No new Carol quality gate has been passed.

## Prototype rule

Production topology, final weights, final shader, final rig, and a complete
animation library are not prerequisites for an architecture-relevant probe.

However, a Human-facing visible prototype must meet the declared
**Human-Evaluable Fidelity Floor**. If the visible proxy itself prevents Human
from judging identity, motion ownership, weight, touch causality, or naturalness,
the result is **PROBE_INVALID** rather than candidate FAIL.

Low-detail hidden/support geometry remains acceptable when it does not dominate
the Decision Question.

## Multi-view / motion diagnostics

When a geometry task changes an exterior region, use enough derived views to
confirm that the change did not create view-specific collapse.

Typical cheap inspection set when relevant:

- Front;
- both 3/4s or the affected side;
- Side;
- Rear/Top-derived only when the region or motion can expose them.

A production lock must not depend solely on one camera view.

## Technical diagnostics

Topology checks, self-intersection checks, edge-flow inspection, naming rules,
and mesh diagnostics are evidence. They become blockers when tied to a material
visible, full-spatial, deformation, attachment, interaction, export, runtime, or
credible future-motion failure.

Where consequences are uncertain and consequential, select a
decision-useful comparison proportional to risk; cheap probes are often
valuable, but there is no mandatory cheapest-first production gate.

## Export / runtime boundary

Current hypothesis is Blender → GLB/glTF → PlayCanvas. Keep runtime-facing assets
deterministic, bounded, and inspectable; preserve semantic controls/anchors
required by interaction.

Available real-device QA is **Xiaomi 14T Pro**. Pixel 7a-class remains
**UNVERIFIED_TARGET** until actual target-class validation exists.
