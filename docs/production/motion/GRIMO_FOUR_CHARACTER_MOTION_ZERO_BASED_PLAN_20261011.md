# Grimo — Three-Character Motion Zero-Based Design Plan (TEMPORARY)

**Date:** 2026-10-11  
**Status:** TEMPORARY PLANNING / NOT AN APPROVED MOTION SPEC  
**Scope:** Jill, Pino, Shushu; experience identity through production-ready Motion / anatomy / Tripo handoff
**Execution branch:** `codex/grimo-motion-zero-based-design-20261011`  
**Working principle:** Outcome-constrained, process-autonomous. Use this file to understand the end goal, phase boundaries and review gates; it is not permission to execute future phases early.

## 0. North Star and boundaries

Design **three distinctly alive, lovable, causally responsive companion characters** whose user-facing performance is emotionally compelling for a 30-second to 5-minute Grimo interaction. Inspiration: the *quality principles* evidenced in Partner Pikachu / Partner Eevee footage, not copied Pokémon poses, clips, character performance or technical implementation.

Outcome chain:

```text
Primary evidence + present Grimo authority
  → experience identity for each of the three
  → motives, attention, relationship and behavioral grammar
  → authored Motion Families / variants / temporal performance
  → anatomy, deformation, rig capabilities, screen-space performance
  → Tripo-first generation / rig / base-motion plan + Codex/Blender fallback
  → independent adversarial audit + Human approval
```

**New user decision (2026-10-11):** Maximize practical reuse of **Tripo Studio 3D, auto-rig, preset Motion, and eligible Text-to-Motion**. Evaluate actual suitability and quality per creature before adoption; let Codex + Blender repair or create the missing parts. Do not assume humanoid auto-rig or a generic preset will fit an unusual creature. Never spend Tripo credits without explicit Human approval.

This work is **research and design only** until specifically authorized otherwise: no Tripo generation, Blender modeling/rigging, asset replacement, application code edits, Motion implementation, credit spend or old approved document replacement.

## 1. Authority and relevant evidence

Read `AGENTS.md` and `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md` first. Distinguish:

- **Current durable authority:** `docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md`, `GRIMO_CHARACTER_EXPERIENCE_SPEC.md`, `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`, `GRIMO_PRODUCTION_OPERATING_SYSTEM.md` in that directory; three original canonical identities; explicit Human decisions.
- **Research — experience / development perspective:** `docs/grimo/knowledge/research/GRIMO_LIVING_COMPANION_EXPERIENCE_RESEARCH.md`. This includes historical proposals; read for evidence and design insights, not its old technical prescriptions.
- **Research — directly observed Pikachu/Eevee timing, gaze, local touch, agency, afterglow:** `docs/grimo/knowledge/research/GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md` and `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md`.
- **Research — motion catalog/traceability:** `docs/grimo/knowledge/research/motion-masters/EEVEE_MOTION_MASTER_INVENTORY.md`, `PIKACHU_MOTION_MASTER_INVENTORY.md`. They summarize eleven and six video-specific inventories respectively, not additional direct video reanalysis.
- **Research — motion/anatomy:** `docs/grimo/knowledge/research/GRIMO_PARTNER_EXPERIENCE_MOTION_ANATOMY_EVIDENCE.md`. This is explicitly a research-only edited extraction from a historical architecture report.
- **Input pose hypotheses:** `docs/grimo/knowledge/character-production/GRIMO_TRIPO_GENERATION_POSE_CONTRACT_DRAFT.md`. Generation pose, rig Rest Pose and game Neutral Pose are distinct; numeric hypotheses are unvalidated; Pino/Shushu seated game Neutral is still a candidate.

Evidence labels must remain distinct: **video observation / measured**, **temporal or spatial inference**, **external claims requiring source verification**, **proposed Grimo choice**, **already approved Grimo decision**. Do not upgrade a research proposal to authority. No need to reread or recreate all original MP4 analysis unless a material evidence gap requires it.

## 2. Six-phase execution plan

### Phase 0 — Evidence compression and authority/conflict register

**Owner:** Account A (reported 18% weekly remaining), GPT-6.1 Sol / Medium.  
**Now authorized by this planning handoff:** yes, when launched by the user.

Produce one focused file:
`docs/production/motion/GRIMO_MOTION_EVIDENCE_PACK_DRAFT.md`.

Efficiency constraints: search headings/index first, read targeted sections; avoid loading multi-thousand-line files end-to-end unless necessary. Do not reanalyze MP4, browse generally, or create extra documents. The target is a **high-signal handoff**, not an exhaustive reproduction. One deliverable, one focused commit/push only after checking relevant diff. No unrelated modifications or tests.

**Exit:** Evidence Pack is traceable, internally consistent, and separates knowledge from proposals; it gives the Astra phase sufficient reliable context.

#Required compact content:
2. Key emotional/interaction principles grounded in the living-companion research and detailed Eevee/Pikachu analysis: attention, agency, refusal, WAIT, asymmetry, temporal structure, touch locality, afterglow, memory/repetition and quiet life. Distinguish direct evidence from hypothesis.
3. A **source-linked reference matrix** identifying which sections/families demonstrate each principle; prefer path + section or timestamp, not untraceable assertions.
4. Evidenced camera/anatomy constraints and **unknowns**, but do not prematurely design three rigs.
5. A small ranked list of design questions for Astra, without answering those questions or generating Motion catalogs.
6. Explicit “approved / evidence / inference / unresolved” ledger.

Efficiency constraints: search headings/index first, read targeted sections; avoid loading multi-thousand-line files end-to-end unless necessary. Do not reanalyze MP4, browse generally, or create extra documents. The target is a **high-signal handoff**, not an exhaustive reproduction. One deliverable, one focused commit/push only after checking relevant diff. No unrelated modifications or tests.

**Exit:** Evidence Pack is traceable, internally consistent, and separates knowledge from proposals; it gives the Astra phase sufficient reliable context.

## Phase 1 — Four independent Experience Identities

Define per-character: emotional promise, intrinsic motives, preferred relationship distance, independent attention, delight/dislike/boundaries, agency, silence/stillness, signature behaviors, expression and physical identity envelope. The existing directional priors are Jill=attention-seeking+energetic, Pino=energetic+independent, Shushu=relaxed+independent. Go beyond adjective or speed differences.

**Output:** `docs/production/motion/GRIMO_FOUR_CHARACTER_EXPERIENCE_IDENTITY_DRAFT.md`. Design three original identities rather than three skins of the same agent. Surface genuinely novel options as proposals; do not change canonical art or approved behaviors.

### Phase 2 — Behavior grammar and staged performance direction

**Owner:** Account B, GPT-6 Astra / High; preferably continue the Phase 1 session while coherent.

Create representative **shared test situations** across all three: 30-second no-input idle, left/right head or cheek touch, repeated touch and mild refusal, character-initiated invitation + WAIT, interruption mid-happiness, staged item/feeding interaction, and a 3–5-minute repeated-contact sequence.

Design each character's **reason for action**, attention and face lead, primary body ownership, physical weight, micro-holds, temporal rhythm, afterglow, and next-state consequence. Define a common semantic runtime interface but forbid generic retargeting as a substitute for personal acting.

**Human Gate 1:** The user reviews Experience Identity and representative acting direction *before* dense Motion production. No silent promotion to FINAL.

### Phase 3 — Complete Motion architecture and three catalogs

**Owner:** Account A after reset if possible, GPT-6.1 Sol / High; fresh session from approved Phase 1–2 files.

Expand accepted behavior directions into Motion Families and performance variants. Every family must declare: semantic purpose, trigger/state/zone/history, attention/facial/physical lead, anticipation → action → moving hold → recovery → afterglow, body-part/channel owners, grounded support, interruption handling, meaningful variations, repeat suppression, dependence on audio/FX/props, camera readability, and acceptance scene.

**Output:** `docs/production/motion/GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`.

### Phase 4 — Motion-to-Anatomy, Tripo-first / Codex fallback

**Owner:** Account A after reset if possible, GPT-6.1 Sol / High.  
**Inputs:** Phase 3, three visual identities and body-only viewpoints, generation-pose draft and research anatomy/camera evidence.

Map critical Motion families to *capability requirements* (not an invented exact bone count): face/eyes/lids/muzzle, head/neck, asymmetric appendages, short limbs, planted supports and center of mass, Jill wings/leaf mane/tail, Pino heavy broad tail and eye/wink completeness, Shushu short-leg/plush compression/sitting, prop/contact anchors, moving holds, screen-space/occlusion, export/runtime needs.

Categorize each capability/Motion as **A preset**, **B Text-to-Motion**, **C Tripo + Blender adaptation**, **D custom Codex/Blender**, or **? needs live Studio suitability test**. These are hypotheses, not claims of availability for the specific creatures. Account separately for model generation, texture, auto-rig, preset, Text-to-Motion and postprocessing; no unapproved credits spent. Define minimal credit-saving preflight, failure triage and only-when-warranted regeneration decision, not a promise of three one-shot successes.

**Output:** `docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`.

### Phase 5 — Independent adversarial audit and Human approval

**Owner:** Account B, GPT-6 Astra / High in an independent fresh session; reserve this capacity in advance. Escalate to XHigh only for a concrete difficult unresolved contradiction; do not use it by default.

Audit against current formal authority, all three canonical identities, original Eevee/Pikachu *principles*, all three human-facing scenario traces, anatomy feasibility and Tripo risk. Actively simulate: similar acting across characters, repetitive loops, floaty center of mass, touch on wrong side, bad idle, lost afterglow, forced neutral between clips, rig misfit, identity-distorting poses, Jill wing/root failure, Pino tail-body fusion and Shushu sit-foot collapse.

Resolve *design* contradictions without silently rewriting Human decisions. Record acceptance evidence and explicitly unresolved technical hypotheses. Require Human signoff of experience/personality and major concessions before promoting any DRAFT to FINAL.

**Exit labels (do not conflate):**
- `DESIGN_READY`: complete, coherent design awaiting or having passed Human experience approval, as explicitly stated.
- `TRIPO_PREFLIGHT_READY`: input imagery, planned poses, known Studio limits and credit budget prepared for controlled tests.
- `TRIPO_READY`: only after actual input/plan and suitability gates pass; planning alone cannot assert it.

## 3. Resource/session strategy (provisional, not actual quota measurement)

Two separate Plus accounts reported by Human: **A ~18%**, **B ~50%** weekly remaining. They are not additive into one pool. Recheck each account's usage and reset time at phase boundaries. Do not assume a numerical token conversion.

| Phase | Account | Model/effort | Session | Allocation intent |
|---|---|---|---|---|
| 0 | A | GPT-6.1 Sol / Medium | New | Dense, faithful evidence compression at minimal cost |
| 1 | B | GPT-6 Astra / High | New | Highest-value creative/reasoning effort |
| 2 | B | GPT-6 Astra / High | Continue Phase 1 if healthy | Consistency of three character personalities |
| 3 | A after reset | GPT-6.1 Sol / High | New | Exhaustive structural catalog from approved identity |
| 4 | A after reset | GPT-6.1 Sol / High | Continue if context healthy, else new from files | Capability traceability and Tripo triage |
| 5 | B, reserved/after reset | GPT-6 Astra / High | **New and independent** | Unbiased quality/counterfactual audit |

Avoid subagents by default, duplicate source scans, full-repo tests, or parallel writes on the same document. Prefer a fresh session plus short handoff files over long chat history and premature auto-compaction; do not run `/compact` at fresh-session start. The user owns final visual/emotional acceptance.

## 4. Work rules, lifecycle and next step

- Preserve existing assets and approved documents; no reset, force-push, overbroad staging, or unrequested code.
- **Current next task only:** run Phase 0 with Sol. Do not start Phases 1–5 without the next explicit user instruction. Future agents should read this file and the latest approved outputs, not infer authority from stale planning.
- After final Human-reviewed specification handoff, archive or remove this temporary roadmap through a focused commit when explicitly directed; never leave it masquerading as a new FINAL specification.

**Current state at writing:** `PLAN_RECORDED / PHASE_0_NOT_STARTED / FOUR_CHARACTER_MOTION_REDESIGN_PENDING`.
