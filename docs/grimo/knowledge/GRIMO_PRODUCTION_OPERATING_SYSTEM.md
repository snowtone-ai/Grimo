# Grimo — Production Operating System

**Status:** Active durable workflow / role authority  
**Updated:** 2026-09-24

## 1. Purpose

This document defines **how Grimo work is decided, executed, evidenced, and judged**. It does not define the current branch or next task; mutable execution truth belongs to latest GitHub.

Core workflow:

> **Experience → Valid Probe → Observe → Correct → Integrate → Observe → Productionize**

The workflow is a spiral, not a strict asset waterfall.

A cheap experiment is valuable only when it can validly answer its Decision Question.

## 2. Three roles

### ChatGPT Planner — decide what must be learned next

Planner owns decisions, not repetitive implementation.

For every materially new task class:

1. Restate the user-visible Product Goal.
2. Define the current **Decision Question**.
3. Identify relevant Unknowns / Risks.
4. Rank unknowns by user impact, uncertainty, late-failure cost, and probe cost.
5. Audit whether a reusable existing asset/evidence source can answer the question before authorizing reconstruction.
6. Choose the **Cheapest Falsifiable Valid Probe** capable of changing a production decision.
7. Define the probe's **Fidelity Floor**: what must already look/function realistically enough for the result to be interpretable.
8. Define required evidence.
9. Define `PASS / FAIL / UNKNOWN / PROBE_INVALID` conditions before implementation.
10. Define the attempt limit.
11. Define what decision follows each possible result.
12. Produce a bounded Codex execution prompt only after the above is clear.
13. Interpret Codex and Human evidence and choose: continue, targeted fix, downgrade blocker, reuse/adapt an asset, or Architecture Review.

Planner must never keep polishing an artifact merely because the artifact exists.

Planner must also never ask Human to mentally subtract a dominant visual defect in order to judge a different variable.

### Codex Executor — build the bounded experiment or implementation

Codex owns execution inside Planner-defined boundaries.

- Do not silently redefine Product Goal or architecture.
- Build the minimum sufficient **valid** implementation required to answer the Decision Question.
- Audit required existing assets before generating replacements when the prompt declares reuse-first scope.
- Preserve authority files and unrelated work.
- Avoid opportunistic refactors, unrelated cleanup, extra features, over-engineering, and unrequested polish.
- Run only targeted validation justified by changed scope or a concrete risk.
- Produce only decision-relevant evidence.
- Report factual results and uncertainty.
- Do not self-approve identity, cuteness, life, naturalness, or final companion quality.
- If the attempt limit is exhausted, the premise fails, or the probe cannot meet its Fidelity Floor without scope expansion, stop and return to Planner.
- Never convert `PROBE_INVALID` into candidate `FAIL`.

### Human — judge perceptual experience

Human authority is reserved for what requires human perception:

- canonical identity;
- cuteness / appeal;
- life / presence;
- causal readability;
- weight / naturalness;
- personality;
- emotional quality;
- objectionable repetition;
- whether the result feels like a companion rather than a demo/puppet.

Human should review evidence as close as practical to final use:

- representative Hero appearance;
- actual motion;
- actual interaction when interaction causality is the question;
- appropriate camera/framing;
- real-device runtime when device behavior is the question.

Human should not be asked to:

- grade permanently hidden details without visible/functional consequence;
- infer touch causality from a non-interactive artifact when actual interaction is required;
- ignore a visibly off-model proxy that dominates the judgment;
- decide whether a candidate failed when the probe itself is invalid.

## 3. Standard task shape

Every substantial execution task should be expressible as:

```text
PRODUCT GOAL
↓
DECISION QUESTION
↓
UNKNOWN / RISK
↓
REUSE / EXISTING-ASSET AUDIT
↓
CHEAPEST FALSIFIABLE VALID PROBE
↓
HUMAN-EVALUABLE / FUNCTIONAL FIDELITY FLOOR
↓
REQUIRED EVIDENCE
↓
PASS / FAIL / UNKNOWN / PROBE_INVALID
↓
ATTEMPT LIMIT
↓
NEXT DECISION FOR EACH RESULT
```

If the task cannot state the Decision Question, Fidelity Floor, and result-dependent next decisions, it is not ready for execution.

## 4. Goal-backward loop

```text
PRODUCT GOAL
   ↓
[ChatGPT Planner]
Acceptance scene / Decision Question / highest-risk unknown
   ↓
[ChatGPT Planner]
Existing-asset audit / reuse opportunity
   ↓
[ChatGPT Planner]
Cheapest falsifiable VALID probe
+ Fidelity Floor
+ criteria
+ attempt limit
   ↓
[Codex]
Bounded prototype / implementation / evidence
   ↓
[Probe Validity Check]
Is the evidence representative enough to answer the question?
   ├─ NO → PROBE_INVALID → no candidate conclusion
   └─ YES
        ↓
[Human when perception is required]
User-visible experience judgment
        ↓
[ChatGPT Planner]
Interpret evidence
   ├─ continue / production convergence
   ├─ targeted blocker correction
   ├─ blocker downgrade/removal
   ├─ reuse/adapt better asset
   └─ Architecture Review
        ↓
[Codex]
Next bounded implementation
        ↓
motion / fleece / runtime / device work as justified
        ↓
[Human]
experience review
        ↓
production convergence
        ↓
Carol Companion Gate
        ↓
architecture freeze / expansion
```

## 5. Gate hierarchy

### 1. Experience Gate — highest

Identity, cuteness, appeal, life/presence, causal readability, naturalness, personality, and companion quality.

### 2. Probe Validity / Evidence Gate

Before Experience conclusions are drawn, the probe must be capable of representing the variable being judged.

Typical validity requirements:

- visible identity components are representative enough;
- unrelated proxy defects do not dominate;
- camera/framing matches the decision;
- motion evidence contains the relevant temporal information;
- actual interaction exists when interaction causality is being judged;
- comparison authority is correct;
- source/donor provenance is known.

A technically successful but perceptually misleading prototype is **PROBE_INVALID**.

### 3. Functional Gate

Deformation, touch/attachment, export, runtime, frame pacing, device behavior, and any function necessary to deliver the approved experience.

### 4. Technical Hygiene

Topology cleanliness, self-intersections, edge flow, hidden-surface quality, naming, and implementation elegance.

Technical Hygiene is mandatory only to the level required to protect Experience, Probe Validity, Functional requirements, or credible future full-spatial exposure. It must not become an independent polishing loop.

## 6. Two-Cycle Stop Rule

If essentially the same blocker survives two bounded implementation cycles:

```text
Cycle 1 → FAIL or unresolved
Cycle 2 → FAIL or unresolved
        ↓
STOP local repair
        ↓
Architecture Review before attempt 3
```

Architecture Review asks:

> Will the final user see it, feel it, suffer from it, or will future plausible motion expose it?

- **YES:** perform targeted correction.
- **NO:** downgrade/remove the blocker.
- **UNKNOWN:** use a valid final-use-oriented probe.
- **PROBE_INVALID twice:** redesign the probe/architecture, not the same artifact for a third time.

## 7. Prototype-before-polish rule

Static intermediate perfection is not a prerequisite for every downstream probe.

Where it answers a material risk more cheaply, provisional geometry, rigging, fleece, representative motion, export/runtime framing, or device testing may precede production lock.

However:

> **Provisional does not mean perceptually arbitrary.**

If Human is judging identity, cuteness, motion ownership, naturalness, touch causality, or companion quality, every visible component that materially affects that judgment must meet the task's **Human-Evaluable Fidelity Floor**.

Examples:

- cheap hidden support mesh for a COM test: valid;
- provisional bone hierarchy for a clearance test: valid;
- simplified shader for a silhouette-only test: valid;
- visibly wrong fleece used to judge Carol cuteness or head/fleece ownership: invalid;
- prerecorded video used to judge whether an actual tap interaction feels responsive: insufficient unless the Decision Question is only about the authored animation itself.

If Human says “I cannot tell because the model/proxy itself is too low quality,” record `PROBE_INVALID`.

## 8. Full-spatial coherence principle

Grimo uses a full-spatial 3D character baseline.

Production may prioritize the front Hero view, but AI work must not create view-specific geometry debt that collapses when a later motion exposes a new angle.

Therefore:

- exterior geometry must remain coherent through plausible views/motions;
- polish can be view-weighted;
- hidden internals can remain functional;
- modular meshes are allowed;
- front-only/camera-dependent geometry hacks are not the default solution;
- new motion should not routinely require rebuilding geometry that was intentionally left invalid outside the original camera.

This principle is defined in detail by `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`.

## 9. Reuse-first principle

Before creating a visible asset from scratch, check whether a better reusable asset already exists.

Relevant sources may include:

- current production assets;
- historical Grimo branches;
- prior Blender/GLB assets;
- generators/scripts;
- validated evidence;
- recoverable local production artifacts when available.

Reuse must remain subordinate to current canonical/approved authority.

Use existing assets as:

- donor geometry;
- benchmark;
- implementation reference;
- validated starting point.

Do not lower quality by replacing an existing strong asset with a cheap proxy merely for execution convenience.

The Planner should explicitly state whether reuse audit is required. High-impact character-appearance tasks default to reuse-first.

## 10. Human-time compression principle

The objective is not to maximize autonomous AI activity.

> **Compress human work and maximize the impact of human judgment.**

AI should absorb:

- search/recovery of existing assets;
- repetitive implementation;
- numerical registration;
- diagnostics;
- evidence generation;
- bounded experiments;
- runtime plumbing.

Human attention should concentrate on:

- identity;
- appeal;
- life;
- emotion;
- naturalness;
- whether the evidence is actually judgeable.

Do not waste Human review cycles on knowingly invalid low-fidelity presentations.

## 11. Planner information-loading order

At the start of a new Grimo planning task:

1. Read ChatGPT Project Memory for durable reasoning policy.
2. Read `GRIMO_PROJECT_KNOWLEDGE_INDEX.md`.
3. Read only the task-specific durable Project Knowledge needed.
4. Retrieve relevant authority/evidence.
5. Search reusable current/historical assets when the task concerns a visible asset already worked on before.
6. Read latest pushed GitHub for mutable current truth.
7. Plan from Product Goal backward.

Do not let stale prompts, old chats, or Project Knowledge snapshots override latest GitHub on mutable execution state.

Historical assets may be useful donors/evidence even when they are not current authority.

## 12. Technical verification policy

Verification is change- and risk-based.

- no full test suite by habit;
- no repeated passing check without relevant changes;
- no broad Blender/PlayCanvas/browser/device QA unless the Decision Question requires it;
- no evidence generation unrelated to the decision;
- specialized checks are opt-in based on concrete failure risk;
- multi-view checks are required when a geometry task claims full-spatial coherence in the affected region;
- interaction checks must be interactive when the Decision Question depends on input-response feel;
- perceptual review must use representative visible assets.

## 13. Result semantics

### PASS
The valid evidence supports the predefined success criterion.

### FAIL
The valid evidence demonstrates that the candidate/architecture does not meet the predefined criterion.

### UNKNOWN
The probe is valid enough to inspect, but evidence is genuinely insufficient or ambiguous.

### PROBE_INVALID
The implementation/evidence cannot fairly answer the Decision Question because of an unrelated fidelity, interaction, framing, ownership, provenance, or delivery defect.

`PROBE_INVALID` does not count as evidence that the underlying candidate failed.

## 14. Final operating rules

> **Never ask “How do we perfect the current artifact?” before asking “Does perfecting this artifact materially improve the final companion experience?”**

and:

> **Never ask Human to judge a variable through a proxy that visibly dominates the answer.**

and:

> **Reuse a stronger existing asset before manufacturing a weaker approximation.**

and:

> **Build spatially coherent 3D first; spend polish according to actual user-facing importance.**