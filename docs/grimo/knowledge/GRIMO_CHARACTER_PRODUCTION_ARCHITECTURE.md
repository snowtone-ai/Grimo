# Grimo — Character Production Architecture

**Status:** Active durable production-architecture authority  
**Updated:** 2026-09-23  
**Scope:** Carol first vertical slice; reusable principles for Jill / Pino / Shushu

## 1. Architecture decision

Adopt **Front-Optimized 3D-First Living Character Architecture** as the current
baseline hypothesis.

Carol remains a genuine spatial 3D character, but Grimo does not pursue uniform
360-degree Hero polish. Investment follows the actual interaction envelope.

This architecture is subordinate to the Product North Star. Final-use evidence
may trigger Architecture Review, including an evidence-driven hybrid.

## 2. Core rules

1. **Front-weighted, not flat.** Primary presentation is front-weighted, but
   enough real depth must exist for self-occlusion, head/body turns, limb
   presentation, and contact-seeking motion.
2. **Hero quality is non-uniform.** Face, eyes, ears, visible hooves, fleece
   silhouette, tail, and motion-exposed transitions receive priority.
3. **360-degree beauty is not a target.**
4. **Hidden geometry is functional.** It exists for support, deformation,
   attachment, collision/clearance, and continuity.
5. **One watertight Hero body is not required.** Modular/separate meshes are
   allowed when required seams/poses remain acceptable.
6. **Rig for semantics, not anatomical purity.**
7. **Facial acting may be hybrid.** Geometry, skinning, morphs, material states,
   and local procedural controls may combine.
8. **Carol fleece is a Hero identity system.** Primary silhouette/acting is
   authored; secondary softness is restrained.
9. **Motion evidence precedes expensive Hero topology lock.**
10. **Every geometry task names the final interaction failure it fixes.**
11. **Whole-character image pseudo-life remains prohibited.**

## 3. Why real spatial 3D remains baseline

Experience-critical behavior benefits from spatial 3D: foreground limb
presentation while support stays grounded, changing overlap relationships,
profile/front reorientation, sustained contact with compression/rebound/limb
participation, off-axis holds, and reusable interaction semantics across four
different morphologies.

A reusable interruptible companion system would otherwise require large
view-specific asset/layer-order complexity. Local hybrid techniques remain
allowed.

## 4. Surface investment classes

### HERO_VISIBLE
High visible identity/appeal quality is required.

### MOTION_EXPOSED
Normally hidden/secondary surfaces revealed by approved motion. Require
sufficient visual and deformation quality for that motion envelope.

### FUNCTIONAL_HIDDEN
Permanently hidden support/deformation/attachment/collision/clearance structure.
Functional correctness is required; Hero visual polish is not.

A region may change class when approved behavior exposes it.

## 5. Carol functional degrees of freedom

Where required by approved behavior, support: stable grounded base/COM,
independent head orientation/pitch, gaze/facial controls, independent ears,
independent front limbs/hoof presentation, limited torso/chest compression and
weight shift, tail control, fleece primary regions plus restrained secondary
follow-through, left/right touch locality, recoverable transitions and
interruption.

Realistic sheep anatomy is not required.

## 6. Camera envelope

The front companion camera is primary.

- **PRIMARY_HERO_ENVELOPE:** neutral and ordinary front-weighted interactions;
  highest fidelity.
- **TRANSITION_ENVELOPE:** approved 3/4, pitch, lean, limb foreground, limited
  withdrawal; coherent motion-safe fidelity.
- **OUT_OF_SCOPE_ENVELOPE:** unused angles/poses; no Hero polish requirement.

## 7. Provisional-before-production rule

Do not require production topology, production rig, final weights, final fleece,
final shader, or complete animation library before architecture-relevant
behavior is tested.

A functional prototype may deliberately use cheap geometry, modular components,
provisional rigging/fleece, and representative motion when that is the cheapest
way to answer a final-use question.

## 8. Stress conditions before lock

Use task-specific representative states, such as neutral Hero, small attention
turn/gaze, blink/expression, ear response, left/right cheek lean, one-front-limb
presentation, small weight shift, deeper compression where approved, larger
positive phrase, and interruption/recovery.

The exact set may be smaller for a narrower Decision Question.

## 9. Technical defects: when they block

Topology/self-intersection/mesh-cleanliness defects block when they materially
cause or threaten visible artifact in the approved envelope, deformation
collapse, bad attachment/clearance, unstable rig behavior, export/runtime
failure, or demonstrated production scalability failure.

If final-use consequence is unknown, prototype final use before spending another
polish cycle.

## 10. Architecture kill criteria

Trigger Architecture Review when evidence shows the baseline cannot, at
acceptable production/runtime cost, preserve canonical identity/cuteness,
required local touch causality, grounded spatial believability, required
motion/deformation, interruptibility/variation, smartphone feasibility, or
four-character scalability.

Two bounded cycles on essentially the same blocker without answering the
Decision Question also trigger Architecture Review before attempt 3.

## 11. Device boundary

Blender-centered authoring with GLB/glTF exchange and PlayCanvas runtime is the
current implementation hypothesis.

- Xiaomi 14T Pro is the available real-device QA source.
- Pixel 7a-class is the lower-performance design/compatibility target and
  remains **UNVERIFIED_TARGET** until actual target-class validation exists.

Runtime constraints are architecture evidence, not merely final optimization.

## 12. Durable lesson from Carol v001–v013

Retain the useful work: canonical/authority system, numerical registration,
geometry parameters, camera research, topology diagnostics, eye/socket lessons,
intersection validators, bounded-attempt methodology, motion inventories, and
evidence methodology.

The failure lesson is prioritization/gate ordering: static intermediate
correctness repeatedly blocked motion/fleece/runtime evidence. Technical PASS
does not guarantee identity, and technical FAIL alone does not quantify final
companion impact.
