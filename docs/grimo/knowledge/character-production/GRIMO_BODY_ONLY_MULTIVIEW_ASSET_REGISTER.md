# Grimo — Body-only Multiview Asset Register

**Updated:** 2026-10-11
**Scope:** Jill, Pino, and Shushu have four selected views each. This is a scoped production registry, **not** replacement canonical identity.

## 1. Authority and safety

1. Current explicit Human decisions and each character's **canonical identity** govern completed visible appearance.
3. Retain anatomical/identity-critical fleece, leaves, horns, wings, ears, eyes, paws/hooves, tail, markings. Remove only independently authored props (Jill loose flowers/butterflies; Pino bubbles/water; Shushu crown/bouquet/loose flowers).
2. Approved full-design art is preserved; body-only views are **derived image-to-3D inputs only**.
4. The 2026-10-11 Human visual decisions accept Jill/Pino/Shushu **Front, left-facing Side, right-facing Opposite Side, Back** as 2D candidates. Jill's peach-colored paired head appendages are interpreted as **horn-like anatomy**, rather than conventional ears; do not perform an automatic "ear-back recolor" that would rewrite accepted appearance. Preserve head leaves, wing and tail relationships. Body markings that may have drifted (e.g. Jill's canonical clover) remain a later identity/material QA obligation.
6. No 2D approval implies successful Tripo reconstruction, mesh topology, rigging, motion, material, or mobile performance. No paid Tripo use without approval.

## 2. Proposed canonical *production-input* placement

Create each file below, retaining the **original PNG bytes**. These paths are distinct from completed-design/canonical image paths.

| Character | Front | Left-facing Side | Right-facing Opposite | Back |
| --- | --- | --- | --- | --- |
| Jill | `jill_bodyonly_front.png` | `jill_bodyonly_left.png` | `jill_bodyonly_right.png` | `jill_bodyonly_back.png` |
| Pino | `pino_bodyonly_front.png` | `pino_bodyonly_left.png` | `pino_bodyonly_right.png` | `pino_bodyonly_back.png` |
| Shushu | `shushu_bodyonly_front.png` | `shushu_bodyonly_left.png` | `shushu_bodyonly_right.png` | `shushu_bodyonly_back.png` |

Place the four files for each character in:

`assets/grimo/source/<character>/tripo-generation-pose/`

Here **left/right mean the direction the character faces *on the image***: `left` = nose facing screen left, `right` = nose facing screen right. They are **not** Tripo's left/right camera-slot labels. Establish actual camera/character coordinates and map slot names explicitly at upload.

## 2.1 Byte-exact source verification (12 retained originals)

| File | Dimensions (px) | SHA-256 |
| --- | --- | --- |
| `jill_bodyonly_back.png` | 1122x1402 | `503ff66c3cd5204da7351996a361f37792c7dabca384267416b078e5f4c9cfcc` |
| `jill_bodyonly_front.png` | 1122x1402 | `c6fb1709271bc476b597c040445bad7dc9e9d8ca7493bd29e22bdfa812f345a8` |
| `jill_bodyonly_left.png` | 1122x1402 | `bb1625ba8ec218a1e1a26ce70b524aa661ef94373cd7d9f5c9df37cb38cc1d31` |
| `jill_bodyonly_right.png` | 1145x1374 | `9572b69c0bbbe66eda9ef2e1011f8f0e040126b3d84cec10446da47a9233c9dc` |
| `pino_bodyonly_back.png` | 1086x1448 | `1762021a4d974fd8d9f3c3abbd43fdb31d14f5dff844b566592d7593f06ee5bf` |
| `pino_bodyonly_front.png` | 1122x1402 | `c4163765b26523849cc32a7ba22499e36a9b89432ede37559c5cd19aa2e96589` |
| `pino_bodyonly_left.png` | 1122x1402 | `787f7e58b302e6ce4288cd105192c128b7594c02ebed1a2d82d30b6dc9b02b28` |
| `pino_bodyonly_right.png` | 1122x1402 | `183bf58cda989a1a645aa8bdb045d61a0a0d3b4bc5fafc79fb97bf75d1eb8be8` |
| `shushu_bodyonly_back.png` | 1024x1536 | `a1ed01e201d6e125623d81e4289b7f17813bab354177e950b7a4836e6dda533d` |
| `shushu_bodyonly_front.png` | 1086x1448 | `e35dfc9c58324b0454dd06b1222ca8f61f23b3b605a348ecf606255b6d087a18` |
| `shushu_bodyonly_left.png` | 1122x1402 | `873fe2fbb950cbb21f2e0e64d2617650b5bac4128fb788f15dbd67e881616a61` |
| `shushu_bodyonly_right.png` | 1024x1536 | `ad754267b4d446dcce9821ceb898304e60cb4a99526b1e0fec0b6169ca25751b` |

## 3. Registration requirements for local image-placement task

- Start from actual current branch, working tree, and repository instructions; do not infer uploads exist in the remote. Locate newly added PNGs even when currently untracked.
- Inspect the 12 retained images visually and check their original provenance.
- Preserve the bytes of the selected approved sources; compare SHA-256 before and after move/copy, and check simple PNG readability and dimensions. Do not regenerate, upscale, crop, normalize, or resave originals.
- Only canonicalize clear duplicates/old versions **within this import's scope**. Before archiving/removing an old file, check its references, original authority role and unique bytes. Keep historically approved art and image evidence for the retained characters intact.
- If a duplicate is referenced from code/docs, update only the relevant references after verifying the intended authority. No bulk text replace across unrelated documentation.
- Store the actual SHA-256, dimensions, role and source basename of each imported PNG in a small machine-readable manifest beside these inputs (per character or one shared index). Never invent hashes.
- Preserve user edits and uncommitted state. One focused image/manifest commit and push on the actual working branch; do not force-push, merge `main`, or do unrelated repairs.
- When technical preflight is incomplete, report `BODY_ONLY_REFERENCE_ACCEPTED / TRIPO_PREFLIGHT_PENDING`, not `TRIPO_READY`.

## 4. Character-specific 3D risks

| Character | Preserve / later Blender QA |
| --- | --- |
| Jill | Leaf mane as anatomy; horn-like peach appendages; two wing roots; thick grounded tail with leaf ridges; distinct limb roots; inspect canonical clover/body markings after generation |
| Pino | Huge rounded *single* tail joining the rear pelvis, compact low body, short limbs, complete eye anatomy (original wink is an expression), underside paw pads |
| Shushu | Large plush head, pink ear volumes and round body, short distinguishable limbs, grounded squat/sitting motion capability, sole/pad details; floral crown/bouquet are independent props |

### Decision log — 2026-10-11 (Human)

- **Jill Right:** Exclude the previous Right image because it faced screen-left like the existing Left. Old SHA-256: `f745cbd01b8224b45354e9c3f1621b4668f51cc00df3cfc9287deda415ef019a`. Replace it with original `ChatGPT 画像 2026年10月11日 18_08_13.png` (1145×1374; SHA-256 `9572b69c0bbbe66eda9ef2e1011f8f0e040126b3d84cec10446da47a9233c9dc`) at `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`. The new image faces screen-right.

## Current registration — 2026-10-17

12/12 retained PNGs: Jill / Pino / Shushu each have Front / Left / Right / Back. All original bytes, dimensions, hashes and approval boundaries remain unchanged. `BODY_ONLY_REFERENCE_ACCEPTED / TRIPO_PREFLIGHT_PENDING`; no new 3D, Rig, Motion or Human PASS. Preserve approved full-design art. Do not resize a source to match another canvas; report hash discrepancies. Tripo camera-slot mapping and actual reconstruction quality remain unverified.
