# Grimo — Blender Implementation Guide

**Status:** Active implementation guide  
**Updated:** 2026-09-24  
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

## Reuse-first rule

Before generating a new visible Carol component, inspect current and relevant
historical assets first.

A historical asset may be:

- donor geometry;
- donor fleece;
- rig/control reference;
- generator/script reference;
- benchmark evidence.

Reuse remains subordinate to current canonical identity and locked references.
Do not replace a strong existing asset with a cheap approximation merely because
the approximation is easier to generate.

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
