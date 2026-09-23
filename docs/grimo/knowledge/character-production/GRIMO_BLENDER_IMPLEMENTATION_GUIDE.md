# Grimo — Blender Implementation Guide

**Status:** Active implementation guide  
**Updated:** 2026-09-23  
**Scope:** Blender / rig / deformation / glTF implementation technique only

This guide does **not** decide architecture, production order, gates, or the
next task. Those belong to the Production Architecture, Production Operating
System, and current production state.

## Implementation rules

- Author geometry for the approved Hero camera and required motion envelope, not
  uniform free-orbit beauty.
- Use **HERO_VISIBLE / MOTION_EXPOSED / FUNCTIONAL_HIDDEN** to decide investment.
- Modular/separate meshes are valid. One continuous watertight Hero body and
  all-quads everywhere are not product requirements.
- Quad-friendly authoring is useful where deformation/editability benefits, but
  GLB runtime topology is triangulated; inspect exported behavior when relevant.
- Rig semantic controls needed by the experience: head/gaze/face, ears,
  forelimbs/hooves, support/COM, tail, and Carol fleece regions.
- Prefer authored primary acting plus bounded corrective deformation and
  restrained secondary follow-through. Physics must not define Hero acting,
  facial meaning, touch causality, or the main fleece silhouette.
- Corrective morphs, bones, material states, local shader controls, and local
  compositing may be combined when they preserve identity and export reliably.
- Bake/evaluate Blender-only constraints or drivers when GLB/glTF cannot carry
  their runtime behavior directly.
- Validate the exported GLB, not only the Blender scene, when export/runtime is
  part of the Decision Question.

## Prototype rule

Production topology, final weights, final fleece, final shader, and a complete
animation library are not prerequisites for an architecture-relevant probe.
Use provisional geometry/rig/fleece and representative motion when that is the
cheapest falsifiable way to answer a final-use question.

## Technical diagnostics

Topology checks, self-intersection checks, edge-flow inspection, naming rules,
and mesh diagnostics are evidence. They become blockers when tied to a material
visible, deformation, attachment, interaction, export, or runtime failure.
Unknown final-use consequence should be tested before another polish cycle.

## Export / runtime boundary

Current hypothesis is Blender → GLB/glTF → PlayCanvas. Keep runtime-facing
assets deterministic, bounded, and inspectable; preserve semantic controls/
anchors required by interaction.

Available real-device QA is **Xiaomi 14T Pro**. Pixel 7a-class remains
**UNVERIFIED_TARGET** until actual target-class validation exists.
