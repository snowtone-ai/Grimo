# Carol production state

This file is the mutable Carol execution routing source.

## Current state — 2026-09-29

- Branch: `codex/carol-skin-default-v004`. Verify exact HEAD in Git.
- **`DEFAULT_BASELINE = PROMOTED`**: the working 3D Skin source is `assets/grimo/production/carol/blender/carol-skin-default-v004.blend` (SHA256 `c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d`).
- **`EAR_VISUAL_HUMAN_REVIEW = PENDING`**. This routing decision does not grant an ear, motion, deformation, runtime or full-character Human PASS.
- Composition: v003 Skin baseline with only `EAR_L`, `EAR_R`, and their existing `SoftInnerBowl` point values refined. All 19 retained non-ear Skin structures and both ear material node trees match v003. The standalone v004 contains Skin geometry only. v003 remains preserved as provenance/fallback at SHA256 `4f4661b672f8b2022ca819241c0624f36693e36505775736042fe821b703915a`.
- Evidence, technical checks and reproduction: `docs/production/carol/evidence/skin-default-v004/README.md`.
- The unchanged v004 Fleece was used only for temporary occlusion renders; its SHA256 remains `a73426d8483e5431e60bc5949b96506c447928682ad92ead6af3cbd1d1092420`. Historical v002 remains intact at SHA256 `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`.
- Next Human decision: compare the authority and v003/v004 boards. The front exposed-axis diagnostic is 10.94° (v003: 11.08°), below the 13–23° target; the inner pink trough is still subtle in the Front render. Decide whether the new fullness is enough or another local pass is needed. Do not infer approval from this default promotion.

## Preserved Normal/Fleece checkpoint — 2026-09-28

- Branch: `codex/carol-normal-fleece-v004`. Verify exact HEAD in Git.
- State: **`NORMAL_FLEECE_V004_IN_PROGRESS`**.
- Current diagnostic asset: `assets/grimo/production/carol/blender/carol-normal-fleece-v004.blend`.
- Current evidence: `docs/production/carol/evidence/normal-fleece-v004/`.
- Active checkpoint: `iterations/41`, built with `--anatomical-base --sculpt-anatomy --painted-shade`. Starting from v002's anatomy, it reduces the head mantle relative to the body, sets head fleece behind the nose, recesses the neck collar, and contracts the body fleece about a low attachment plane. An inner head backing bridges scalp gaps within the existing smaller envelope. Ear/eye/hoof geometry and the v004 wool shader are retained. This is an in-progress proportion study, not a completed semantic reconstruction. See the evidence README.
- Latest explicit Human clarification: the authority reads as a smaller fleece surround around the head/neck, with a larger round body behind it. Head fleece must not project ahead of the nose. The lower face wool belongs to the neck, not the jaw. Mareep's 3D head/body relationship is a comparative reference, not a replacement identity or geometry donor. The body fleece should also be slightly smaller because its spatial volume still feels inflated, even when Front/Side dimensions appear plausible.
- Prior explicit Human rejection: v004-33 improved texture but substantially regressed from v002 in shape. Fleece over the face and body is excessively swollen and biologically unnatural. Interpret the authority semantically as a coherent creature, rather than directly lifting Front/Side image shapes into volumes. Production method is unrestricted within the full-spatial goal. Preserve old Carol's perceived appearance and softness; the original `prompt.md` is not an immutable method contract.
- **v004-33 HUMAN VISUAL FAIL for shape.** Its high silhouette overlap is not evidence of natural anatomy. Do not resume that inflated guide/lock construction as the preferred shape baseline.
- v004 is undergoing geometry and material comparisons. It is **not** a Human-review candidate or a completed Normal/Fleece phase. Known defects are being corrected; intermediate images must not be presented as acceptance evidence.
- **Normal/Fleece v002 remains without Human acceptance.** Its prior visual failure is not erased by the latest decision, which explicitly prefers its shape over v004-33. It is now the better spatial construction baseline, not the final appearance authority. v001 also failed Human visual review.
- v003 diagnostic asset: `assets/grimo/production/carol/blender/carol-normal-fleece-v003.blend`.
- Evidence: `docs/production/carol/evidence/normal-fleece-v003/README.md`.
- Historical v003 used its authorized three attempts and failed geometry. Its crown/chest shelves, face/ear recesses and weak lock structure were implementation failures, not an unavoidable property of 3D. The subsequent explicit v004 and continuation instructions authorize current work; the old v003 attempt limit does not constrain it.
- **`NORMAL_FLEECE_V003_AWAITING_HUMAN_REVIEW` was NOT reached.** Its failure packet remains historical evidence, not the active candidate.

## Preserved authority and scope

- The former v002 Skin source remains preserved at `assets/grimo/production/carol/blender/carol-skin-final-v002.blend`, SHA256 `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`. It is historical fallback and provenance; the working Skin default is v003 above.
- Current visible authority remains canonical identity and approved Normal Front/Side; approved Skin Front/Side and the active ear module are supporting authority. See `assets/grimo/source/carol/approved-3d/authority.json`.
- v004-41 starts from the saved Normal/Fleece v002 scene (hash recorded in `anatomy-construction.json`), not by regenerating Skin or reusing the inflated v004-33 guide. Candidate-only lower chassis and regional wool edits do not change accepted Skin authority. Historical `snowtone-ai/grimoire` remains a visual-quality/method donor, not a compulsory recipe.
- Front has the highest perceptual priority, alongside believable oblique anatomy. The restored ear span and hoof proportions must not be compressed merely to improve silhouette overlap. Collar integration, lobe hierarchy and semantic form refinement remain open.
- Rear, opposite side, 3Q and Top remain diagnostics from the same saved asset, not new authorities.
- The existing Human ornament exception remains in force; it does not waive other visual requirements.
- **No Human, motion, deformation, runtime or device PASS. Phase 2 has not started.** No rigging, animation clips, GLB/runtime/device acceptance, merge or PR was performed.

## Preserved Normal/Fleece handoff (not the current task)

Continue from v004-41's head/neck/body proportion study, not the rejected v004-33 construction. Compare with checkpoint 37 at identical camera scale using `iterations/41/neck-comparison.jpg`; equal-height normalization would conceal part of the requested reduction. Use the evidence README's explicit flags. Review Front, both front-quarter directions, Side, Rear and Top together. Keep the head mantle smaller than the body, behind the nose, and the lower collar rooted at the neck. Ear-root continuity, bead-like cheek wool, collar/foreleg transitions and charm mounting remain unresolved. The new head backing has no local contact shape keys; do not infer deformation readiness. Resolve known defects before changing the state to awaiting Human review. Historical evidence remains historical, not an active candidate.
