# Grimo — Body-only Multiview Asset Register

**Status:** All 15 currently selected PNGs are registered at their production paths with hash-verified manifest entries. Carol Back is intentionally omitted by Human decision; the planned three-view Tripo input is not yet confirmed as supported. Tripo technical preflight is pending for all registered images.
**Updated:** 2026-10-11
**Scope:** Carol has three selected views; Jill, Pino, and Shushu have four each. This is a scoped production registry, **not** replacement canonical identity.

## 1. Authority and safety

1. Current explicit Human decisions and each character's **canonical identity** govern completed visible appearance.
2. Approved full-design art and established Carol geometry/support documents are preserved; body-only views are **derived image-to-3D inputs only**.
3. Retain anatomical/identity-critical fleece, leaves, horns, wings, ears, eyes, paws/hooves, tail, markings. Remove only independently authored props (Carol moon/stars; Jill loose flowers/butterflies; Pino bubbles/water; Shushu crown/bouquet/loose flowers).
4. The 2026-10-11 Human visual decisions accept Jill/Pino/Shushu **Front, left-facing Side, right-facing Opposite Side, Back** as 2D candidates. Jill's peach-colored paired head appendages are interpreted as **horn-like anatomy**, rather than conventional ears; do not perform an automatic "ear-back recolor" that would rewrite accepted appearance. Preserve head leaves, wing and tail relationships. Body markings that may have drifted (e.g. Jill's canonical clover) remain a later identity/material QA obligation.
5. Carol's body-only Front, left-facing Side and right-facing Opposite Side are the approved inputs. Human decided on 2026-10-11 not to create or use a Back image because repeated Back candidates failed the lower-body taper, hoof shape, and three-dimensional connection quality checks. Try the three approved views in Tripo if supported; this does not guarantee accurate reconstruction of unseen rear anatomy.
6. No 2D approval implies successful Tripo reconstruction, mesh topology, rigging, motion, material, or mobile performance. No paid Tripo use without approval.

## 2. Proposed canonical *production-input* placement

Create each file below, retaining the **original PNG bytes**. These paths are distinct from completed-design/canonical image paths.

| Character | Front | Left-facing Side | Right-facing Opposite | Back |
| --- | --- | --- | --- | --- |
| Carol | `carol_bodyonly_front.png` | `carol_bodyonly_left.png` | `carol_bodyonly_right.png` | *intentionally omitted by Human decision* |
| Jill | `jill_bodyonly_front.png` | `jill_bodyonly_left.png` | `jill_bodyonly_right.png` | `jill_bodyonly_back.png` |
| Pino | `pino_bodyonly_front.png` | `pino_bodyonly_left.png` | `pino_bodyonly_right.png` | `pino_bodyonly_back.png` |
| Shushu | `shushu_bodyonly_front.png` | `shushu_bodyonly_left.png` | `shushu_bodyonly_right.png` | `shushu_bodyonly_back.png` |

Place the four files for each character in:

`assets/grimo/source/<character>/tripo-generation-pose/`

Here **left/right mean the direction the character faces *on the image***: `left` = nose facing screen left, `right` = nose facing screen right. They are **not** Tripo's left/right camera-slot labels. Establish actual camera/character coordinates and map slot names explicitly at upload.

## 2.1 Byte-exact source verification (15 verified originals)

The registered SHA-256 values identify the original PNG bytes. Different PNG canvas sizes are intentional source facts, **not** instructions to resize the artwork. If a user-supplied local file does not match, report the discrepancy rather than silently replacing it. Carol Back has no selected or registered source by Human decision; no pending file entry is required.

| File | Dimensions (px) | SHA-256 |
| --- | --- | --- |
| `carol_bodyonly_front.png` | 1254x1254 | `8b30a279067d55f7e9185b7bba173da05b1e40de30d83e3fea3b4a5726bc6c47` |
| `carol_bodyonly_left.png` | 1448x1086 | `40c8c09826afc9e7d9b0e128cc63930df7a994ae12a13766084ad7944f9384eb` |
| `carol_bodyonly_right.png` | 1448x1086 | `bdd05b4dc067e32f720f861d361f525e9c6eaebd82618fea0c78eac194dc8b4b` |
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
- Inspect the 15 selected images visually and check their original provenance. Carol Back is excluded by the current Human decision; do not create a substitute or treat its absence as a pending asset task.
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

**Execution status (2026-10-11):** Fifteen selected PNGs are registered under the paths above; `assets/grimo/source/body-only-multiview-manifest.json` records measured dimensions and hashes. The 15-image count reflects the current selected set: three Carol views and four views for each other character. Carol's three approved views are the planned Tripo input; Studio support for three views and any recovered rear quality are unknown. All registered assets remain `BODY_ONLY_REFERENCE_ACCEPTED / TRIPO_PREFLIGHT_PENDING`; no Tripo-ready status is claimed.

### Decision log — 2026-10-11 (Human)

- **Jill Right:** Exclude the previous Right image because it faced screen-left like the existing Left. Old SHA-256: `f745cbd01b8224b45354e9c3f1621b4668f51cc00df3cfc9287deda415ef019a`. Replace it with original `ChatGPT 画像 2026年10月11日 18_08_13.png` (1145×1374; SHA-256 `9572b69c0bbbe66eda9ef2e1011f8f0e040126b3d84cec10446da47a9233c9dc`) at `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`. The new image faces screen-right.
- **Carol Back:** Repeated generated Back candidates did not meet quality for the lower-body taper, hooves, and three-dimensional connections. Do not generate or use a Back source for this input plan; try the approved Front/Left/Right set only if Tripo supports three views.
- **Still unverified:** Tripo camera-slot mapping, support for three-view input, and the quality of any generated Carol model, especially unseen rear anatomy. The 2D selections do not establish Tripo or Rig readiness.
