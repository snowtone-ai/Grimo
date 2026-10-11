# Grimo — Shared Live Handoff (ChatGPT ↔ Codex)

**Branch:** `coord/grimo-ai-handoff` (coordination-only; DO NOT use as the code-production base).
**File:** `docs/production/GRIMO_AI_HANDOFF.md`.
**Last interaction:** 2026-10-12 / ChatGPT Planner / refreshed Project Knowledge router file for upload; no Shushu production change.
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
- **Verified remote HEAD when this handoff was authored:** `749675cac5ebdb07587e715eb2cb59bfcae2768f`.
- This latest commit and its two preceding ChatGPT documentation commits added the cross-agent rules + stable project overview; **Shushu production geometry was not modified** in them.
- **Last material Shushu evidence commit:** `6d6f7326ea901658f9cbf1b4ffea92a4dd1e6a0b` — Candidate B original assets, Blender feasibility evidence and scripts. Verify newer Git changes before acting.
- **Next owner:** new ChatGPT Planner session to read this handoff + stable overview, inspect latest code/evidence, then prepare an outcome-driven Codex repair task or equivalent tested execution plan. Codex may choose precise implementation steps.
- **Last Human instruction:** Add one cross-agent live handoff file/rules; deliver a separate project-wide stable knowledge Markdown; continue work next session. No permission to spend Tripo credits or consume trials was given here.

## 3. Shushu — current evidence-backed state

- **Selected source:** Tripo Smart Mesh P2.0 **Candidate B**, `8,481` FBX polygons / `8,259` vertices, GLB `13,854` triangles. Source files in `assets/grimo/production/shushu/tripo/candidate-b-8481/`.
- **Authoritative evidence:** `docs/production/shushu/evidence/candidate-b-8481/VALIDATION_REPORT.md` and its measured JSONs, renders; disposable `assets/grimo/production/shushu/blender/shushu-candidate-b-feasibility.blend`.
- **Verdict:** **GO** for targeted production geometry and deformation repair; **HOLD** for final identity/rig/material/motion acceptance. Existing volume (large head, cheeks, ears, round torso, independent short arms and legs) is a viable donor.
- **Actually tested:** base eyelid folding FAIL; additive proof eyelid mechanically possible but not visually complete; small mouth conditional; head/shoulder/limbs conditional; deeper sitting setup FAIL (lower-body folds/penetration); localized plush recovery possible with eye protection; narrow feasible bounded holding example; focused skeleton/morph GLB round-trip PASS. Temporary rigs and proof renders are **not final**.
- **Next structural work:** canonical-faithful eye/socket/lid interface and gaze/blink, small mouth rim/interior and closure, pelvis/thigh/knee/ankle support deformation, neck/shoulder ownership and contact/holding conflict. Repair only where measured; re-test seated and held-paw/contact poses; keep Human perceptual gate.
- **Not yet confirmed:** completed eyes and mouth, production Rig, final Texture/UV, accessory crown/bouquet, five Food styles, actual PlayCanvas/mobile device performance, standing vs sitting Game Neutral, final Human acceptance.

## 4. Tripo UI / costs — last observed, not live entitlements

- Studio model URL from user screenshots: `https://studio.tripo3d.ai/ja/workspace/rigging/2d61630a-3df9-44a0-9d77-0441ab225837` (do not assume persistent authenticated accessibility).
- Screenshot 2026-10-12: UI displayed balance **3,200 Credits**; Rig Type **Humanoid**, Skeleton Preset **Mixamo**, Auto Rig **20 Credits**. This combination is a preliminary sensible biped/Mixamo choice, **not yet executed or proven suitable for final deformations**.
- Texture screen showed four body-only references, **4K / 20 Credits**, Remove Lighting OFF in screenshot; recommended check ON for clean lighting-independent PBR, but actual generation is pending.
- Retopology screen showed **Quad P1.0 / 10,000 target faces / 10 Credits** (whole-remesh; not guaranteed joint-specific improvements).
- Segmentation screen showed **Standard 6–15 parts**, first trial price **0** in screenshot; not necessary as default.
- Region Mesh Edit screen displayed **(×3)** remaining and user reported **one** remaining free whole-model generation. These are **last-seen/unverified current balances**, not entitlements we can spend. Neither should be consumed by default.
- Tripo API **Rig Check** is documented as a free API endpoint, but no independent Studio UI control was verified; API access/credits are separate. Do not create API key/paid service without permission.
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
