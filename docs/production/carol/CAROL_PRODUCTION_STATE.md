# Carol production state

This file is the mutable Carol execution routing source.

## Current state — 2026-09-28

- Branch: `codex/carol-normal-fleece-v004`. Verify exact HEAD in Git.
- State: **`NORMAL_FLEECE_V004_IN_PROGRESS`**.
- Current diagnostic asset: `assets/grimo/production/carol/blender/carol-normal-fleece-v004.blend`.
- Current evidence: `docs/production/carol/evidence/normal-fleece-v004/`.
- Active checkpoint: `iterations/37`, built with `--anatomical-base --sculpt-anatomy --painted-shade`. It recovers v002's spatial proportions and ear/hoof placement, applies localized cheek/bib/under-chin sculpting, and retains v004's wool shading. It is a structural recovery, not a newly completed semantic reconstruction. See the evidence README.
- Latest explicit Human direction: v004-33 improved texture but substantially regressed from v002 in shape. Fleece over the face and body is excessively swollen and biologically unnatural. Interpret the authority semantically as a coherent creature, rather than directly lifting Front/Side image shapes into volumes. Production method is unrestricted within the full-spatial goal. Preserve old Carol's perceived appearance and softness; the original `prompt.md` is not an immutable method contract.
- **v004-33 HUMAN VISUAL FAIL for shape.** Its high silhouette overlap is not evidence of natural anatomy. Do not resume that inflated guide/lock construction as the preferred shape baseline.
- v004 is undergoing geometry and material comparisons. It is **not** a Human-review candidate or a completed Normal/Fleece phase. Known defects are being corrected; intermediate images must not be presented as acceptance evidence.
- **Normal/Fleece v002 remains without Human acceptance.** Its prior visual failure is not erased by the latest decision, which explicitly prefers its shape over v004-33. It is now the better spatial construction baseline, not the final appearance authority. v001 also failed Human visual review.
- v003 diagnostic asset: `assets/grimo/production/carol/blender/carol-normal-fleece-v003.blend`.
- Evidence: `docs/production/carol/evidence/normal-fleece-v003/README.md`.
- Historical v003 used its authorized three attempts and failed geometry. Its crown/chest shelves, face/ear recesses and weak lock structure were implementation failures, not an unavoidable property of 3D. The subsequent explicit v004 and continuation instructions authorize current work; the old v003 attempt limit does not constrain it.
- **`NORMAL_FLEECE_V003_AWAITING_HUMAN_REVIEW` was NOT reached.** Its failure packet remains historical evidence, not the active candidate.

## Preserved authority and scope

- Accepted Skin remains `assets/grimo/production/carol/blender/carol-skin-final-v002.blend`, SHA256 `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`. That source file is unchanged. Candidate-only face, ear and hoof changes do not constitute a new accepted Skin asset.
- Current visible authority remains canonical identity and approved Normal Front/Side; approved Skin Front/Side and the active ear module are supporting authority. See `assets/grimo/source/carol/approved-3d/authority.json`.
- v004-37 starts from the saved Normal/Fleece v002 scene (hash recorded in `anatomy-construction.json`), not by regenerating Skin or reusing the inflated v004-33 guide. Candidate-only lower chassis and local wool edits do not change accepted Skin authority. Historical `snowtone-ai/grimoire` remains a visual-quality/method donor, not a compulsory recipe.
- Front has the highest perceptual priority, alongside believable oblique anatomy. The restored ear span and hoof proportions must not be compressed merely to improve silhouette overlap. Collar integration, lobe hierarchy and semantic form refinement remain open.
- Rear, opposite side, 3Q and Top remain diagnostics from the same saved asset, not new authorities.
- The existing Human ornament exception remains in force; it does not waive other visual requirements.
- **No Human, motion, deformation, runtime or device PASS. Phase 2 has not started.** No rigging, animation clips, GLB/runtime/device acceptance, merge or PR was performed.

## Next handoff

Continue from v004-37's v002-based spatial anatomy, not the rejected v004-33 construction. Use the evidence README's explicit flags. Review Front, both front-quarter directions, Side, Rear and Top together. Judge the head, face opening, ear attachment, torso and grounded feet as a creature before refining individual locks. Resolve known shape, attachment and pigment defects before changing the state to awaiting Human review. Historical evidence remains historical, not an active candidate.
