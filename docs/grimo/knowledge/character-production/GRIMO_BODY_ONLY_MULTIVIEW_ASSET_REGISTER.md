# Grimo — Body-only Multiview Asset Register

**Status:** Human-reviewed 2D production inputs; repository binary registration and Tripo technical preflight are **pending** until checked by the executing agent.
**Updated:** 2026-10-11
**Scope:** Carol / Jill / Pino / Shushu, four orthographic-ish source views per character. This is a scoped production registry, **not** replacement canonical identity.

## 1. Authority and safety

1. Current explicit Human decisions and each character's **canonical identity** govern completed visible appearance.
2. Approved full-design art and established Carol geometry/support documents are preserved; body-only views are **derived image-to-3D inputs only**.
3. Retain anatomical/identity-critical fleece, leaves, horns, wings, ears, eyes, paws/hooves, tail, markings. Remove only independently authored props (Carol moon/stars; Jill loose flowers/butterflies; Pino bubbles/water; Shushu crown/bouquet/loose flowers).
4. The 2026-10-11 Human visual decisions accept Jill/Pino/Shushu **Front, left-facing Side, right-facing Opposite Side, Back** as 2D candidates. Jill's peach-colored paired head appendages are interpreted as **horn-like anatomy**, rather than conventional ears; do not perform an automatic "ear-back recolor" that would rewrite accepted appearance. Preserve head leaves, wing and tail relationships. Body markings that may have drifted (e.g. Jill's canonical clover) remain a later identity/material QA obligation.
5. Carol's body-only Front, left-facing Side and right-facing Opposite Side have been recovered from prior user images; **do not presume a particular historical Carol Back revision is final** without matching the user's selected local source. Carol Back should pass the Human-visible body taper and three-part hoof/rear-foot identity check before promotion.
6. No 2D approval implies successful Tripo reconstruction, mesh topology, rigging, motion, material, or mobile performance. No paid Tripo use without approval.

## 2. Proposed canonical *production-input* placement

Create each file below, retaining the **original PNG bytes**. These paths are distinct from completed-design/canonical image paths.

| Character | Front | Left-facing Side | Right-facing Opposite | Back |
| --- | --- | --- | --- | --- |
| Carol | `carol_bodyonly_front.png` | `carol_bodyonly_left.png` | `carol_bodyonly_right.png` | `carol_bodyonly_back.png` |
| Jill | `jill_bodyonly_front.png` | `jill_bodyonly_left.png` | `jill_bodyonly_right.png` | `jill_bodyonly_back.png` |
| Pino | `pino_bodyonly_front.png` | `pino_bodyonly_left.png` | `pino_bodyonly_right.png` | `pino_bodyonly_back.png` |
| Shushu | `shushu_bodyonly_front.png` | `shushu_bodyonly_left.png` | `shushu_bodyonly_right.png` | `shushu_bodyonly_back.png` |

Place the four files for each character in:

`assets/grimo/source/<character>/tripo-generation-pose/`

Here **left/right mean the direction the character faces *on the image***: `left` = nose facing screen left, `right` = nose facing screen right. They are **not** Tripo's left/right camera-slot labels. Establish actual camera/character coordinates and map slot names explicitly at upload.

## 3. Registration requirements for local image-placement task

- Start from actual current branch, working tree, and repository instructions; do not infer uploads exist in the remote. Locate newly added PNGs even when currently untracked.
- Inspect the 16 selected images visually or against an image contact sheet and check their original provenance. Identify Carol Back from the user's *actual* final candidate rather than filename order, modification time or the first "back" match. If ambiguous, leave it pending and report clearly; do not fabricate, overwrite or silently substitute.
- Preserve the bytes of the selected approved sources; compare SHA-256 before and after move/copy, and check simple PNG readability and dimensions. Do not regenerate, upscale, crop, normalize, or resave originals.
- Only canonicalize clear duplicates/old versions **within this import's scope**. Before archiving/removing an old file, check its references, original authority role and unique bytes. Keep historically approved art, `approved-3d/`, original Carol Normal/Skin and image evidence intact.
- If a duplicate is referenced from code/docs, update only the relevant references after verifying the intended authority. No bulk text replace across unrelated documentation.
- Store the actual SHA-256, dimensions, role and source basename of each imported PNG in a small machine-readable manifest beside these inputs (per character or one shared index). Never invent hashes.
- Preserve user edits and uncommitted state. One focused image/manifest commit and push on the actual working branch; do not force-push, merge `main`, or do unrelated repairs.
- When technical preflight is incomplete, report `BODY_ONLY_REFERENCE_ACCEPTED / TRIPO_PREFLIGHT_PENDING`, not `TRIPO_READY`.

## 4. Character-specific 3D risks

| Character | Preserve / later Blender QA |
| --- | --- |
| Carol | Dream-cloud fleece as *spatial*, expressive anatomy; ear volume; three-part hoof structure and natural rear taper; stars/moons restored as separate objects in final appearance |
| Jill | Leaf mane as anatomy; horn-like peach appendages; two wing roots; thick grounded tail with leaf ridges; distinct limb roots; inspect canonical clover/body markings after generation |
| Pino | Huge rounded *single* tail joining the rear pelvis, compact low body, short limbs, complete eye anatomy (original wink is an expression), underside paw pads |
| Shushu | Large plush head, pink ear volumes and round body, short distinguishable limbs, grounded squat/sitting motion capability, sole/pad details; floral crown/bouquet are independent props |

**Execution handoff:** Once the binaries have been registered and the manifest is populated with measured hashes, verify this registry's statuses and update local references as needed. This document records the intended interpretation; it does **not** claim any binary is already committed.
