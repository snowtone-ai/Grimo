# Grimo — Repository Operating Rules

Grimo is a smartphone-first task-management PWA whose emotional center is four
living companion characters: Carol, Jill, Pino, and Shushu.

## Authority and information boundary

The repository implements decisions; it is not the highest source of durable
product reasoning.

- **ChatGPT Project Memory** = reasoning principles and current planning doctrine.
- **Project Knowledge** = durable product/experience/architecture authority and
  evidence. Route through
  `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md`.
- **GitHub** = mutable execution truth: code, branch/HEAD, current candidate,
  blockers, evidence, tests, and handoff.

The repository cannot read ChatGPT Project Memory by itself. Repository-local
snapshots named "memory" are not substitutes for the live Project Memory.

For Carol, `docs/production/carol/CAROL_PRODUCTION_STATE.md` is the single
mutable routing truth. Do not duplicate current branch/candidate/attempt/
blocker/Human-Gate state into durable specifications.

## Product Goal

The Goal is not a technically perfect 3D artifact. On a smartphone, each Grimo
must feel cute, alive, aware of the user, causally responsive, capable of
initiating interaction, and like a companion rather than a canned puppet during
extended use.

Experience priority:

1. Cuteness / Appeal
2. Healing / Comfort
3. Attachment
4. Fun
5. Surprise
6. Collection

Every implementation choice is subordinate to this outcome.

## Goal-Backward Spiral

```text
Product Goal
→ Acceptance Experience
→ Risk / Unknown Map
→ Decision Question
→ Reuse / Existing-Asset Audit
→ Cheapest Falsifiable Valid Probe + Fidelity Floor
→ Functional / Visual Prototype
→ representative Motion / provisional Rig / provisional Fleece
→ Human Experience Review
↔ Targeted Correction
→ Early GLB / PlayCanvas / Smartphone
→ Human Experience Review
→ Production Convergence
→ Behavior Depth / Variation
→ Device Optimization
→ Companion Gate
→ Architecture Freeze
→ Jill / Pino / Shushu
```

> **Experience → Valid Probe → Observe → Correct → Integrate → Observe → Productionize**

This is a spiral, not an asset waterfall.

## Role separation

### ChatGPT Planner

Planner owns the next decision, not repetitive implementation. Confirm latest
pushed execution state and Product Goal; define one Decision Question; map
relevant risks/unknowns; audit reusable current/historical assets when visible
character work is involved; choose the highest-value unknown and the Cheapest
Falsifiable Valid Probe; define the Human/functional Fidelity Floor; predefine
evidence, PASS/FAIL/UNKNOWN/PROBE_INVALID, attempt limit, and result-dependent
next decisions; then produce a bounded Codex task. Interpret Codex/Human
evidence and choose continue, targeted correction, reuse/adaptation, blocker
downgrade, or Architecture Review.

Never continue polishing merely because an artifact exists. Never ask Human to
mentally subtract a dominant low-quality proxy in order to judge a different
variable.

### Codex Executor

Execute the bounded task with minimum sufficient implementation. Generate only
decision-relevant evidence, run only targeted validation, report facts and
uncertainty, and commit/push tracked changes unless explicitly prohibited or a
real blocker prevents it.

Do not introduce scope creep, opportunistic refactors, unrelated cleanup,
over-engineering, excessive tests/verification, unrequested polish,
architecture changes, Human-quality self-approval, or attempts beyond the
declared limit.

### Human

Human judges identity, cuteness, appeal, life/presence, naturalness/weight,
causal readability, personality, objectionable repetition, emotion, and
companion quality. Do not spend Human attention grading permanently hidden
topology unless it creates a visible, motion, interaction, export, or runtime
consequence.

## Gate hierarchy

1. **EXPERIENCE GATE** — identity, cuteness, appeal, life, causality,
   naturalness, personality, companion quality.
2. **PROBE VALIDITY / EVIDENCE GATE** — evidence must be representative enough
   to answer the Decision Question. Dominant proxy defects, missing actual
   interaction, wrong framing, or unclear provenance produce **PROBE_INVALID**,
   not candidate FAIL.
3. **FUNCTIONAL GATE** — deformation, interaction/touch/attachment, export,
   runtime, frame pacing, device behavior.
4. **TECHNICAL HYGIENE** — topology cleanliness, intersections, edge flow,
   hidden-surface quality, naming, structural elegance.

Technical Hygiene exists to protect Experience or Function. A technical defect
is a blocker when evidence ties it to a visible artifact, deformation failure,
interaction/attachment failure, export failure, runtime instability, or another
material final-use consequence. If consequence is unknown, probe final use
before another polish cycle.

## Two-Cycle Stop Rule

If essentially the same blocker survives two bounded implementation cycles,
stop local repair. Attempt 3 requires Architecture Review.

Ask: **Will the final user see it, feel it, or suffer from it?**

- YES → targeted correction.
- NO → downgrade/remove the blocker.
- UNKNOWN → cheapest final-use probe first.

## Character-production architecture

Current baseline:
**Full-Spatial 3D Living Character Architecture with View-Weighted Polish**.

- Exterior geometry must remain coherent through practical Front / 3/4 / Side /
  Rear / derived Top exposure and plausible motion.
- The front Hero presentation gets the highest identity/appeal polish, but
  front priority is not permission for front-only geometry or off-axis collapse.
- Geometry investment classes: **HERO_PRIORITY**, **GENERAL_EXTERIOR**,
  **MOTION_CRITICAL**, **FUNCTIONAL_HIDDEN**.
- Modular/separate meshes are allowed; one continuous watertight Hero body is
  not a product requirement.
- Local 2D, shader, material, morph, and compositing techniques may supplement
  the spatial character but must not replace coherent exterior 3D.
- Whole-finished-character warp/squash/global-scale pseudo-life is prohibited.
- Blender → GLB/glTF → PlayCanvas is the current implementation hypothesis and
  may change through Architecture Review.
- Reuse stronger existing geometry/fleece before manufacturing lower-quality
  replacements.
- Provisional implementation is allowed only when it can validly answer the
  Decision Question; Human-facing visible components must meet the declared
  Fidelity Floor.

### Carol-specific

Carol's fleece is a dominant visible identity system. Do not block fleece,
motion, or runtime merely because naked Underbody is not visually perfect.

```text
Carol canonical identity
↓
Normal Front / Normal Side
↓
Full-spatial Carol exterior
├─ HERO_PRIORITY polish
├─ GENERAL_EXTERIOR coherence
└─ MOTION_CRITICAL deformation / attachment
↓
Skin Front / Skin Side / geometry parameters
↓
FUNCTIONAL_HIDDEN implementation
```

Skin references and numerical geometry remain locked supporting underbody
authority for support, rigging, deformation, attachment, and clearance. They
are not the highest Hero-appearance authority.

## Device truth

- Available real-device QA: **Xiaomi 14T Pro**.
- **Pixel 7a-class**: lower-performance compatibility/design target.
- A real Pixel 7a is unavailable; do not require or claim Pixel 7a real-device
  PASS.
- Pixel 7a status is **UNVERIFIED_TARGET** until actual target-class validation
  exists.

Runtime evidence may be gathered early because runtime constraints are
architecture evidence, not only final optimization chores.

## Lean reading and execution

Start with the knowledge index, then load only task-relevant durable authority
and the latest pushed current-state file. Do not load all research/evidence by
habit. Historical documents under `docs/archive/` never override active
authority.

Preserve Task/Calendar semantics, persistence migrations, PWA behavior,
server-only secrets, user work, approved source images, Blender/GLB assets, and
unrelated changes. Never expose credentials or private data.

## Targeted verification

Verification is change- and risk-based.

- Markdown/routing-only work: content consistency checks and diff inspection are
  normally sufficient.
- Changed code/config: run the smallest check that covers the changed risk.
- Changed/exported GLB: validate the changed asset when relevant.
- Full build, full Playwright, Storybook, Blender, PlayCanvas, Lighthouse, or
  device QA are opt-in when the Decision Question or blast radius requires them.
- Do not repeat already-passing checks without relevant changes.

Final operating rules:

> **Never ask “How do we perfect the current artifact?” before asking “Does
> perfecting this artifact materially improve the final companion experience?”**

> **Never ask Human to judge through a proxy that visibly dominates the result.**

> **Reuse a stronger existing asset before manufacturing a weaker approximation.**

> **Build spatially coherent 3D first; weight polish toward what the user sees most.**

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify in `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
