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

For the cheapest useful probe, compare one specific change to the current
candidate using a consistent reference, camera and lighting setup. Keep
evaluation snapshots attributable to the actual candidate. Human-facing
identity and cuteness still require Human perceptual acceptance; automated
overlap, intersections and topology diagnostics cannot award it.

### Topology, motion and delivery boundary

Professional blocking material (e.g. Dikko's *Modeling for Animation 02*)
demonstrates planning articulation and checking rough motion early. It is an
example from humanoid animation, **not** proof of Carol-specific joint layout.
Use a small relevant articulation or attachment probe to expose design limits
when a plausible motion depends on them. Do not require final retopology or a
full animation library before such a probe.

Blender's glTF exporter documents object transforms, pose-bone animation and
shape-key values as exportable animation channels; arbitrary Blender property
animation is not universally exported. The export mode also affects how
Actions/NLA tracks become clips. PlayCanvas documents GLB import support for
skeletons/skinning and morph targets. Therefore validate any required motion
or deformation behavior on **the exported GLB in PlayCanvas**, not from the
Blender viewport alone. These checks become mandatory only when relevant to
the current Decision Question or production lock.

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
- [Blender — Stylized Character Workflow with Blender (Julien Kaspar, YouTube)](https://www.youtube.com/watch?v=f-mx-Jfx9lA) — public video metadata/description verified; not a claim to have watched the full video.
- [Dikko — Modeling for Animation 02 (YouTube)](https://www.youtube.com/watch?v=4vAqPaFv8QA) — public video metadata/description verified; broad articulation-planning reference, not Carol-specific proof.
- [Blender 4.5 LTS Manual — glTF 2.0 export and animation](https://docs.blender.org/manual/ja/4.5/addons/import_export/scene_gltf2.html) — direct technical documentation.
- [PlayCanvas — Building Models](https://developer.playcanvas.com/user-manual/assets/models/building/) and [Exporting Assets](https://developer.playcanvas.com/user-manual/assets/models/exporting/) — direct engine documentation.

All Grimo-specific examples above are **engineering inferences**, not
reported successful experiments. The guide does not assert that any tutorial
has been reproduced or any new Carol quality gate has been passed.

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

Unknown consequence should be tested with the cheapest **valid** probe before
another polish cycle.

## Export / runtime boundary

Current hypothesis is Blender → GLB/glTF → PlayCanvas. Keep runtime-facing assets
deterministic, bounded, and inspectable; preserve semantic controls/anchors
required by interaction.

Available real-device QA is **Xiaomi 14T Pro**. Pixel 7a-class remains
**UNVERIFIED_TARGET** until actual target-class validation exists.
