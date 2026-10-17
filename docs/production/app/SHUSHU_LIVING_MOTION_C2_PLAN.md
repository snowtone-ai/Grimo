# Shushu Motion C2 — Codex-only living idle and first interaction plan

**Date:** 2026-10-18. **Status:** Human requested Codex-only Motion production, implementation not yet run. **Not** evidence of Human animation approval, smartphone PASS or release GO. Tripo upload/Animation step is no longer a prerequisite **for Shushu**; do not change the unrelated Jill/Pino plans without Human input.

**Shushu-specific Motion evidence amendment (2026-10-18):** [Shushu Bear-Cub Motion Research & Performance Bible](../../grimo/knowledge/character-experience/SHUSHU_BEAR_CUB_MOTION_RESEARCH_AND_DIRECTION.md) is the evidence-backed *research and production-direction candidate* for sit→four-paw stand, stand→sit, walk start/stop, face/gaze/idle/touch mechanics. Use its evidence tags and contact/weight-shift QA; **all timing numbers are directorial hypotheses, not measured animal motion, and Human Motion approval is pending**. No full all-family expansion without gates. For C2 start with short idle; if adding a larger sit/stand movement, honor the transition and support constraints here.

## Fixed source-of-truth and branches

- Latest shared main when planned: `534694dae8087dec852de0f26b472a6dcd26ca70` (Gate B and prior design contracts integrated). Recheck it.
- C1 live runtime **unmerged**: `codex/grimo-shushu-runtime-c1-v001`, remote `dfeac982f443dbc77906a9a8b12dd39adb6c82a6`. Draft [PR #12](https://github.com/snowtone-ai/Grimo/pull/12) for CI and technical review; **C1 remains HOLD for Human app-stage appearance, Xiaomi actual performance and Vercel Preview/browser delivery**. Do not merge C1 into main, deploy or bypass phone permissions.
- Selected Shushu donor `codex/shushu-abc-motion-repair-v004-20261017`, `c5bed8b7cf0e7963388f9d20699fedd2c08c2c44`. Actual GLB v004 SHA256 `a082195104713c21b9a219ff19bd9d37702486aaa4cdf2bbf2e9f0ad58b5c91f`; donor editable Blender `assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004.blend` (read/derive only; never modify donor original); flower v002 and hind-sole pads. C1 real PlayCanvas 2.22.2 custom loader includes eight-influence Torso/Paw skin, CPU updated surface normals, purpose blending and Hold normal-offset anchor.
- **New C2 implementation branch**: `codex/grimo-shushu-living-motion-c2-v001` **from C1 HEAD**, not from main and not from entire donor branch. Does not merge itself to main. C1 review and C2 candidate work can proceed independently.

## Outcome and decision

**Primary next slice C2-A:** 15–30 seconds of **natural living idle** in the actual `/grimo` app, faithful to Shushu's relaxed, independently content personality and approved body/eyes/face/flower/paws. Include meaningful stillness. After sufficient technical and visual evidence, **optional next slice C2-B**: semantic head/cheek tap → localized recognition → attention/face → small body follow-through → settle and afterglow; opposite-side input redirects continuously, never queues canned loops.

This is **not** implementation of all 28 Shushu Motion families, all poses, walking/running, food, reward, Gift, Seat as default, deep petting or Secret Motion. Continuing beyond C2-B needs evidence, branch review and Human experience approval, not an arbitrary quantity of clips. Existing Phase 1–4 three-character Motion docs are **DRAFT**, useful as non-binding inspiration; current North Star / Character Experience Spec / approved Shushu donor are authoritative.

### Why authored hybrid, not Tripo preset or monolithic GLB

- Author character-owned clips and/or independent bone/morph tracks in Blender using existing rig **or** correct PlayCanvas runtime-level expressive controllers where more maintainable. Codex may choose after preflight. **No Tripo dependency, credits or model re-rig.** Export only small additional animation data if useful; reuse existing GLB binary; avoid re-uploading/rebuilding a 62.6MB character for every motion.
- Blend semantic channels (`attention/gaze/head`, `face/blink`, `body/breath/weight`, `ears/flower follow-through`, `paw/support`) with explicit owner, precedence, clamp and continuity. Use PlayCanvas Anim layers/masks/blends if verified with **installed 2.22.2** and custom v004 controller; use a smaller deterministic mixer otherwise. No speculative general animation engine.
- Full-body root-scale oscillation, arbitrary rigid-root bobbing, fake puppet yaw and regular sinusoidal everything are prohibited. Blink is not constant closed-eyes, gaze is not random eye flicking, ears respond with plausible delayed motion. Subtle plush breathing must preserve the silhouette and fixed support; avoid visually stretching approved face/feet, flower clipping, lip contour separation and paw/torso intersections.
- Beware v004 diagnostic 821-frame Action: **proof/witness only**; don't ship/replay as living idle. Do not reintroduce legacy arm FK: `Hold > SelfContact > Offer` purpose, `Wrist`, `Seat` control and owned Paw shape layer must remain consistent with body/face tracks. If a channel is unavailable, record BLOCKED and choose a genuinely valid localized substitute; do not add bones/modify canonical morphology solely to meet a prompt checklist.

## Implementation milestones and *stop* decisions

**C2-0: preflight** (small, no full rescans). Identify actual existing bones/morph channels/neutral state/diagnostic animation and relevant donor control semantics from shipped v004 GLB + loader. Test **one** representative non-neutral pose and restoration in saved actual PlayCanvas, without re-exporting entire model. Write compact channel map and feasibility list. If critical head/eyes cannot move separately or deformation breaks under small motion, stop `C2 BLOCKED` and request targeted rig repair rather than manufacture fake motion.

**C2-A: living idle**. Minimum production-relevant channels where physically available: small non-global breathing, real blink/face recovery, eyes-first attention then *optional small head* follow, ear asymmetry/delayed settle, brief self-chosen pause. A single coherent 15–30s expressive phrase + non-mechanical subtle variation and stable quiet is enough for v001; do not build 30 profiles before Human review. Use state- and event-driven timing, authored curves/hold/settle, deterministic QA seed (production may vary within bounded limits), avoid frequent React re-renders. Lightly constrained support and self-correcting fade to proper neutral; correct single update/render owner. Start loop only while visible/mounted; release all C1 owned WebGL listeners/assets when leaving; hidden tab paused and resume coherent.

**C2-A technical gate**. Source neutral must remain the same within tested tolerance. Compare 3D app frames front + selected 3/4/side against approved Shushu, checking pupils/eyelids/mouth, face volume, arm/abdomen, sole/support, and head flower at neutral, motion peak, mid, and settle. Make real 15–30s video plus stills and a brief identity-specific motion timeline with sampled timings. Repeat 60–180s or several seeded sessions for abrupt loops, repetition and unnatural robotic oscillation; do not equate technical continuity with **Human Living Idle PASS**. Assess PlayCanvas frame timings (p50/p95 where possible), CPU extra work, resource lifetimes, app navigation and input responsiveness. No synthetic/desktop-only declaration of phone PASS.

**C2-B conditional**. Only if C2-A real app motion stable and quality appears plausible: add **one** low-risk hit-tested semantic head/cheek tap interaction (not touch everywhere). Touch region must be genuine screen→3D picking / semantic zone and not conflict with scrolling, overlay, mobile tap cancellation. ACK in locally appropriate head/cheek first; then eye/face optional small head movement; calm settle/afterglow. While reacting, new opposite-side touch interrupts/redirects from the **current** pose. Head/gaze, blink, ears and any occupied paw share explicit arbitration with idle, no snapping or fully restarting to neutral. No fake food/inventory claims. Review short real-time tap video with side-dependent outcome. Stop before hero acting/interaction variants if any key quality invariant fails.

**C2-C integration QA**. New persistent RAF/renderer activity only inside mounted visible `/grimo` while needed; hidden page throttled/paused; route dispose, WebGL context fail/retry and fetch abort unchanged. Cold Task and Calendar with SW have **zero** PlayCanvas/GLB/animation downloads; normal data operations and Task/Calendar preserve. Run narrowly relevant tests, TS/lint/build and browser smoke (not repeated full suite). Device Xiaomi 14T Pro if operator-authorized; ADB auto-approval was blocked by policy on C1, **do not bypass**. If unavailable mark PHONE UNKNOWN with reproducible manual steps. Do not modify Vercel settings or production deploy.

### Technical benchmark and quality guardrails

- Identity / approval is higher priority than number of new motions. Preserve head identity, wide gentle eyes, plush torso support, short limbs, mouth rim, flower v002 and sole pads. No bulk donor branch merge; no silent `.blend` or GLB overwrite.
- Measure frame time 60fps target / 30fps graceful fallback, jitter, additional CPU for normal/morph updates. Dynamic skin/Paw computations are a known potential bottleneck; first profile with realistic motion before enabling expensive always-on update paths; optimize without changing visible body.
- Local C1 initial one-shot browser load ~6.590s measured on Windows desktop, **not phone**; adding motion must not accidentally introduce further giant GLB downloads or eager initialization outside Grimo.
- Memory leak / lifecycle: multiple navigations, listener count, active contexts and RAF after destroy; startup failure/503/LFS pointer/context loss still visible and retryable. No touch when overlay covers canvas.
- Preserve `DESIGN.md`: premium pale soft shell and 2D/2.5D background; original identity, never redesign Task/Calendar/Collection in this C2 work.
- Fixed constraints from real device: smartphone-first, Pixel 7a-class compatibility unverified and Xiaomi real performance currently UNKNOWN. Human visual PASS ≠ CI PASS.
- Done: scoped commit + push, remote HEAD match, branch clean, concise evidence and review assets, **GO/HOLD separated**: technical animation, Human living idle, Human tap, actual phone, C1 delivery, overall release. No merge without reviewing pending C1 + C2 stacking.

## Research for executor (already selected, validate installed 2.22.2 behavior)

- PlayCanvas layered blend/state graph: https://developer.playcanvas.com/user-manual/animation/anim-state-graph-assets/
- PlayCanvas animation mask: https://developer.playcanvas.com/user-manual/animation/anim-layer-masking/
- Official current AnimComponent: https://api.playcanvas.com/engine/classes/AnimComponent.html
- Blender glTF action/keyframes: https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html
- Page visibility / rAF: https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API

**Inputs, bounded:** local `AGENTS.md`; `docs/grimo/knowledge/Goal√map.md`; `docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md`; `docs/production/Handoff.md`; C1 evidence; donor `final-v004/REVIEW.md` and actual loader/GLB; `DESIGN.md` only relevant §23–24. Optional DRAFT Shushu S01–S03 reference as direction not approved plan. No general media scraping or third-party library install without a need.

**Model/effort:** GPT-6.1 Sol / Medium new session, no `/compact`, no subagents. Medium chosen for bounded local work; upgrade to Sol / High only on demonstrated structural or deformation blocker, NOT to compensate for unclear scope or over-testing. Report blockers rather than guessing.
