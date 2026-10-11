# Grimo — Shared Live Handoff (ChatGPT ↔ Codex)

**Branch:** `coord/grimo-ai-handoff` (coordination-only; DO NOT use as the code-production base).
**File:** `docs/production/GRIMO_AI_HANDOFF.md`.
**Last interaction:** 2026-10-12 / ChatGPT Planner / completed multi-source research (11 requested platform checks), revised proposed Shushu Tripo×Codex production workflow and Codex execution brief. No production artifact changed, no Tripo credits/trials consumed.
**Status:** Last-known routing snapshot, **not** a substitute for Git/approved source files.

## 1. How to use / sync contract

1. At the beginning of **every Grimo-related turn or Codex task**, fetch the latest **remote** copy of this file **from `coord/grimo-ai-handoff`**, plus the actual Git branch/HEAD and relevant production state. Never assume `main` or the feature branch has the latest handoff.
2. Check only directly relevant authorities and evidence; never infer current work from old chat history. Label Human decisions vs AI proposals vs test results vs unknowns.
3. Before finishing **every turn**, update this one Markdown with materially new information, or at least the latest-interaction outcome if state did not change. Publish to the coordination branch, then verify the new remote HEAD. Preserve concise current state; Git commits supply history rather than a growing chronological transcript.
4. Concurrency: re-fetch this branch immediately before writing; optimistic/lease-safe commit and push without force. On conflict re-read/reconcile; do not reset, stash, clean, overwrite, or merge unrelated user work. Codex may use a separate temporary worktree for this coordination branch.
5. If connection/write access is unavailable, report **HANDOFF_SYNC_BLOCKED** with branch and path; never claim synchronization occurred. An inaccessible handoff never grants permission for paid Tripo operations or overwrites.
6. This file routes to the actual source: Canonical, Product North Star, Product Feature, Production Architecture, active character production state, Git and test evidence outrank it. Project Knowledge static overview: `docs/grimo/knowledge/GRIMO_PROJECT_OVERVIEW_STABLE.md`.

**Latest documentation note:** Produced `GRIMO_PROJECT_KNOWLEDGE_ROUTER_20261012.md` as a ChatGPT downloadable Project Knowledge replacement for the 2026-10-11 router. This output is not asserted to be committed to Grimo. The `GRIMO_PROJECT_OVERVIEW_STABLE.md` remains the stable product overview; the live remote handoff remains the mutable execution source.

## 2. Last-verified active execution

- **Primary production branch:** `codex/grimo-motion-zero-based-design-20261011`
- **Verified remote HEAD during 2026-10-12 research:** `749675cac5ebdb07587e715eb2cb59bfcae2768f`; no Shushu geometry change was made by this Planner.
- This latest commit and its two preceding ChatGPT documentation commits added the cross-agent rules + stable project overview; **Shushu production geometry was not modified** in them.
- **Last material Shushu evidence commit:** `6d6f7326ea901658f9cbf1b4ffea92a4dd1e6a0b` — Candidate B original assets, Blender feasibility evidence and scripts. Verify newer Git changes before acting.
- **Next owner:** Codex Executor (proposed, no execution yet): start new GPT-6.1 Sol / High session, no pre-/compact; carry out Canonical-safe Candidate B geometry/deformation convergence with simultaneous actual pose testing, especially lids/mouth and lower-body support. Produce real Blender asset + concise motion/visual evidence; stop at Human perceptual Gate, not final Rig certification.
- **Last Human instruction:** Thoroughly research Tripo + Codex user workflows on X, Discord, official docs, Axios, alphaXiv, Hugging Face, The Information, GitHub, Hacker News, BiliBili, Weibo, Reddit; reconstruct next Codex prompt. This is research/planning only, not permission for Tripo spending or Human approval.

## 3. Shushu — current evidence-backed state

- **Selected source:** Tripo Smart Mesh P2.0 **Candidate B**, `8,481` FBX polygons / `8,259` vertices, GLB `13,854` triangles. Source files in `assets/grimo/production/shushu/tripo/candidate-b-8481/`.
- **Authoritative evidence:** `docs/production/shushu/evidence/candidate-b-8481/VALIDATION_REPORT.md` and its measured JSONs, renders; disposable `assets/grimo/production/shushu/blender/shushu-candidate-b-feasibility.blend`.
- **Verdict:** **GO** for targeted production geometry and deformation repair; **HOLD** for final identity/rig/material/motion acceptance. Existing volume (large head, cheeks, ears, round torso, independent short arms and legs) is a viable donor.
- **Actually tested:** base eyelid folding FAIL; additive proof eyelid mechanically possible but not visually complete; small mouth conditional; head/shoulder/limbs conditional; deeper sitting setup FAIL (lower-body folds/penetration); localized plush recovery possible with eye protection; narrow feasible bounded holding example; focused skeleton/morph GLB round-trip PASS. Temporary rigs and proof renders are **not final**.
- **Next structural work:** converge on production-ready geometry around eye/socket/lid closure and gaze, small mouth opening/closure, short-leg/pelvis/thigh/knee/ankle sitting support, neck/shoulder ownership, localized plush deformation and reachable holding; actual test poses, canonical image comparisons and focused GLB handoff required. Keep Game Neutral and final rig choice undecided; return for Human perceptual gate.
- **Not yet confirmed:** completed eyes and mouth, production Rig, final Texture/UV, accessory crown/bouquet, five Food styles, actual PlayCanvas/mobile device performance, standing vs sitting Game Neutral, final Human acceptance.

## 4. Tripo UI / costs — last observed, not live entitlements

- Studio model URL from user screenshots: `https://studio.tripo3d.ai/ja/workspace/rigging/2d61630a-3df9-44a0-9d77-0441ab225837` (do not assume persistent authenticated accessibility).
- Screenshot 2026-10-12: UI displayed balance **3,200 Credits**; Rig Type **Humanoid**, Skeleton Preset **Mixamo**, Auto Rig **20 Credits**. This combination is a preliminary sensible biped/Mixamo choice, **not yet executed or proven suitable for final deformations**.
- Texture screen showed four body-only references, **4K / 20 Credits**, Remove Lighting OFF in screenshot; recommended check ON for clean lighting-independent PBR, but actual generation is pending.
- Retopology screen showed **Quad P1.0 / 10,000 target faces / 10 Credits** (whole-remesh; not guaranteed joint-specific improvements).
- Segmentation screen showed **Standard 6–15 parts**, first trial price **0** in screenshot; not necessary as default.
- Region Mesh Edit screen displayed **(×3)** remaining and user reported **one** remaining free whole-model generation. These are **last-seen/unverified current balances**, not entitlements we can spend. Neither should be consumed by default.
- Tripo API **Rig Check** is documented as a free API endpoint, but no independent Studio UI control was verified; API access/credits are separate. Do not create API key/paid service without permission.
- **2026-10-12 official documentation check:** Tripo Help Center states existing GLB/OBJ/STL/FBX models can be uploaded for Auto Rig (pose restrictions apply); public Studio Generate page shows Upload 3D Model; Tripo developer documentation also describes import and uploaded-model texture/rig workflows. This establishes documented support in some Tripo interfaces/APIs, **not verified availability, pricing, compatibility or no-cost behavior of the user's authenticated Studio session**. Sources: https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation ; https://docs.tripo3d.ai/model-generation/import-model.html . Tripo geometry-changing remesh/segmentation operations do not preserve rigs; finish mesh changes before rigging.
- **2026-10-12 cross-source research outcome:** Independent Tripo user posts (Reddit r/Tripo_ai) expose real Mixamo retarget axis/origin issues and stylized-rig shoulder/hip fold; Japanese independent panda character study (2026-09-26, https://xn--68jtc1d819rk6e.jp/diary/250016) finds unnecessary five-finger Humanoid/Mixamo bones and wrist twist even after re-rig. Tripo official imported-model Auto Rig help states T-pose humanoid / standard standing quadruped support; atypical Shushu A-pose short-limb compatibility is UNKNOWN (https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation). Official pre-rig docs say geometry-remesh/segmentation destroys rig and skin (https://docs.tripo3d.ai/animation/pre-rig-check-v2-0-20250506.html). Blender 5.2 exporter and PlayCanvas GLB support shape keys/morphs/skinning but actual exported scene must be tested (https://developer.playcanvas.com/user-manual/assets/models/building/). User posts and press claims cannot override actual Shushu evidence. Research found no verifiable task-specific original Discord/Weibo posts, or directly relevant Axios/The Information pipeline tests; no invented consensus. Process implication: repair and deformation-test iteratively using temporary rig; avoid assuming Tripo Auto Rig as final. Optional Tripo suitability check only if zero-credit/no-trial; do not block geometry repairs on authenticated Studio access. After topology/staging gate, consider UV/Texture/Auto Rig only by user approval, verify morph/material preservation.
- **Order:** preserve model and do consequential mesh/topology repairs before Smart UV / Texture / Auto Rig. Verify whether **uploaded, Blender-repaired GLB/FBX** can use those Studio operations before committing to that route. Tripo-generated content must be checked against Canonical, motion needs and rights. Repair may still be followed by Blender facial/corrective work.
- **No Tripo Mesh Edit/Retopo/Texture/Auto Rig/generation/credits were executed by ChatGPT.** Screenshots show settings only; user action afterwards must be rechecked.

## 5. Other characters and global authority

- Four Grimo: Carol (dream-cloud sheep), Jill (spring-green dragon), Pino (blue otter), Shushu (white/pink panda). Four main screens: Task, Calendar, Grimo, Collection.
- Carol's character-specific mutable state: `docs/production/carol/CAROL_PRODUCTION_STATE.md` (must be fetched if Carol is task target).
- Motion contract (DRAFT design, not finished execution): `docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md` and `GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`.
- Stable overview and source navigation: `docs/grimo/knowledge/GRIMO_PROJECT_OVERVIEW_STABLE.md` and `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md`.
- Never make a historical Shushu/Carol candidate, a 2D body-only input, or a temporary diagnostic rig into final Canonical or Human-accepted production truth.

## 6. Next handoff update requirements

Replace stale facts with directly verified ones; retain concise important open issues only. Record actor/date/current production HEAD/decision/evidence/next action. Do not append unbounded chat summaries. If only discussing/explaining, still update the last-interaction outcome and verify GitHub publication. This is an intentional per-turn cross-agent user rule.
