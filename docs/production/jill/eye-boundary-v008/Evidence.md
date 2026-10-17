# Jill v008 — texture-only trial: Human FAIL

**Superseded:** Human screenshot 593 explicitly rejected the remaining physical vertical bands outside BOTH eyes. The texture cleanup does not satisfy the requested cord removal. The diagnosis below describes only the separate host texture residue. The geometry interpretation was not disproved; the earlier selection was insufficient. Continue with [v009 local lid join correction](../eye-join-v009/Evidence.md).

2026-10-18. Branch `codex/jill-texture-return-v005-20261017`, start `cc080bc30590247d8604d94c0a5d5dced6f595a5`. Latest main verified `8b9d736abca118de5bd1e2e1f64b961e25f0ba42`. Work is isolated in the existing Jill worktree; the unrelated dirty primary checkout is protected. Local AGENTS, Goal√map, production pointer and Jill HANDOFF govern this continuation. Canonical, v004 shape GO, v005 texture history and v006/v007 evidence remain the authority chain.

Human: mouth appearance GO; Canonical-side thigh clover OK; horns need no change. New explicit scope: [red-marked v007](human-markup-v007.png) reports an eye/skin line with apparent eye remaining farther outside. Human permits either removing the line or covering the outside eye with skin. This authorizes this local eye diagnosis; it does not reopen approved features.

## Diagnosis and selected repair

The pale vertical line is the existing added lid collar. The black part beyond it is not wholly exposed eye geometry: [owner-color diagnostic](diagnosis-owners-3q.png) / [opposite 3Q](diagnosis-owners-left3q.png) leaves that dark area on `body_skin` even when actual eyes are cyan and lids magenta. The v005 host repair used `front > .278 m`, missing lateral old eye art on host skin. Its BaseColor residue was carried through unchanged v006/v007.

The initial decision to reject the geometry interpretation was mistaken for the Human-designated cord. Trial lid folding and closure reshaping removed the open strip but produced thick raised borders during partial blinks. **No trial geometry is delivered.** A texture-only correction is sufficient to remove the host's false eye artwork. It keeps the actual eye artwork and existing lid edge. This chooses the requested skin outside the real eye boundary without adding a new membrane or redesigning the eye.

`repair-jill-eye-boundary-v008.py` rasterizes only existing nearby body triangles into existing UV0. Within a bounded eye region, it identifies dark residual pixels and adds <=2 texels for filtering. The fill uses the same sampled green/cream skin field as v005. [Mask](host-eye-uv-mask.png), [exact texture diff](texture-diff.json). 13,379 pixels changed in a 14,282-pixel mask. Every pixel outside that mask is exact v007; actual eye/lid owners, mouth, clover and horns are protected. No full regeneration or paid service.

There is still a shaded outer crevice in some 3Q/Side views. [Camera-ray diagnosis](surface-hit-diagnosis.json) resolves sampled pixels to `body_skin`, with RGB around (203,232,116), not eye artwork. Its darkness is the existing local surface shading. This distinction is evidence of cause, **not Human approval of the remaining crease**. Existing partial-blink lid volume and the fine dotted closure seam are unchanged; full-model visual completion remains HOLD.

## Actual results

- [Before / after detail](eye-detail-before-after.png), [full face comparison](eye-before-after.png), [actual runtime face](runtime-face.png), [body](runtime-body.png), [21-step blink GIF](blink-runtime.gif). v008 was shown in the local viewer; the Human's annotated v007 file is never overwritten.
- Saved blend: neutral, mouth closed/small/large/combined/recovery, blink .25/.5/.75/1, each wink, gaze X/Y both extremes, Front / Side / both 3Q. Actual renders were opened and inspected. The false outer dark art is removed; the inherited physical crease is visible and not hidden in the comparison.
- [Preservation](preservation.json): all vertices/topology, all 3 UV layers, weights, all Morph coordinates/drivers, 130 bones, 39 channels and 16 anchors exact vs v007. [GLB binary preservation](glb-preservation.json): exported hierarchy/transforms and all 1,105 geometry/skin/Morph/UV accessors exact; only packed image/review extras differ.
- [Fresh static GLB import](reimport-proof.json): all 30,880 used source vertices covered, unmatched 0; seven eye/mouth states maximum position delta 3.073e-7 m, 23 materials, UV0 texture routing / 3 UV sets, 20 Morphs / 130 bones / 16 anchors. Fresh-import Front / Side / 3Q actual renders were opened.
- [Mouth pixel regression](mouth-pixel-regression.json): protected front mouth ROI is exact across neutral, closed, small, large and recovery vs Human-approved v007/v006.
- [Static PlayCanvas](static-runtime.json): actual Engine 2.22.2 / WebGL2, 23 skin/Morph instances, 20 Morphs each, 16 anchors. UI-driven blink intermediates and winks, mouth combinations, combined blink/mouth, 21-step close/reopen sweep. Neutral canvas after recovery is pixel exact.
- [Bounded runtime](bounded-runtime.json): existing limited head/wing/tail/face schedule, actual rendered states and continuous playback/recovery. This is not full motion-library production or mobile certification. Focused verification details are in [verification](verification.json).

## Gate

Mouth Human GO / Clover Human OK / horns unchanged. **v008 eye appearance: Human FAIL (physical cord remains); full-model complete: HOLD.** The supplied fix removes the texture residue. Whether the inherited lid edge/crease is sufficiently natural must be judged from the supplied files. Do not convert a numeric PASS or the texture-only scope into full visual GO. If the remaining physical crease is rejected, the next change must target that local lid/host join, preserving the eye size and approved face; do not repeat the rejected raised-collar trial.

[Assets](../../../../assets/grimo/production/jill/tripo/eye-boundary-v008/README.md) / [v007 authority](../clover-v007/Evidence.md) / [v006 mouth](../mouth-integration-v006/Evidence.md) / [manifest](Manifest.json) / [remote receipt](RemoteReceipt.json).
