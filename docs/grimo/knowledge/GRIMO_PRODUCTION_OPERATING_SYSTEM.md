# Grimo — Production Operating System

**Status:** Active durable workflow / role authority  
**Updated:** 2026-09-23

## 1. Purpose

This document defines **how Grimo work is decided, executed, and judged**. It
does not define the current branch or next task; mutable execution truth belongs
to latest GitHub.

> **Experience → Prototype → Observe → Correct → Integrate → Observe → Productionize**

The workflow is a spiral, not a strict asset waterfall.

## 2. Three roles

### ChatGPT Planner — decide what must be learned next

For every materially new task class:

1. Restate the user-visible Product Goal.
2. Define the current **Decision Question**.
3. Identify relevant Unknowns / Risks.
4. Rank them by user impact, uncertainty, late-failure cost, and probe cost.
5. Choose the **Cheapest Falsifiable Probe** capable of changing a production
   decision.
6. Define required evidence.
7. Define PASS / FAIL / UNKNOWN before implementation.
8. Define the attempt limit.
9. Define the next decision for each result.
10. Produce a bounded Codex task only after the above is clear.
11. Interpret Codex/Human evidence and choose continue, targeted fix, blocker
    downgrade/removal, or Architecture Review.

Planner must not keep polishing merely because an artifact exists.

### Codex Executor — build the bounded probe/implementation

- Do not redefine Product Goal or architecture.
- Build the minimum sufficient implementation.
- Preserve authority files and unrelated work.
- Avoid scope creep, opportunistic refactors, unrelated cleanup, extra features,
  over-engineering, excessive testing, and unrequested polish.
- Run only targeted validation justified by changed scope or concrete risk.
- Produce only decision-relevant evidence.
- Report factual results and uncertainty.
- Do not self-approve identity, cuteness, life, naturalness, or companion quality.
- Stop when attempt limit is exhausted or the premise fails.
- Commit/push tracked work unless the task explicitly says otherwise or a real
  blocker prevents it.

### Human — judge perceptual experience

Human authority covers canonical identity, cuteness/appeal, life/presence,
causal readability, weight/naturalness, personality, emotional quality,
objectionable repetition, and whether the result feels like a companion.

Review evidence as close to final use as practical: Hero camera, motion,
interaction, and real-device runtime. Do not ask Human to grade permanently
hidden details without visible/functional consequences.

## 3. Standard task shape

```text
PRODUCT GOAL
↓
DECISION QUESTION
↓
UNKNOWN / RISK
↓
CHEAPEST FALSIFIABLE PROBE
↓
REQUIRED EVIDENCE
↓
PASS / FAIL / UNKNOWN
↓
ATTEMPT LIMIT
↓
NEXT DECISION FOR EACH RESULT
```

If a task cannot state its Decision Question and result-dependent next decision,
it is probably artifact-polish rather than Goal-backward work.

## 4. Goal-Backward Spiral

```text
Product Goal
→ Acceptance Experience
→ Risk / Unknown Map
→ Decision Question
→ Cheapest Falsifiable Probe
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

## 5. Gate hierarchy

1. **Experience Gate** — identity, cuteness, appeal, life/presence, causality,
   naturalness, personality, companion quality.
2. **Functional Gate** — deformation, touch/attachment, export, runtime, frame
   pacing, device behavior.
3. **Technical Hygiene** — topology cleanliness, self-intersections, edge flow,
   hidden-surface quality, naming, implementation elegance.

Technical Hygiene is mandatory only to the level required to protect Experience
or Function. It must not independently block a downstream probe when final-use
consequence is unknown.

## 6. Two-Cycle Stop Rule

If essentially the same blocker survives two bounded cycles:

```text
Cycle 1 → FAIL
Cycle 2 → FAIL
      ↓
STOP local repair
      ↓
Architecture Review before attempt 3
```

Ask: **Will the final user see it, feel it, or suffer from it?**

- **YES:** targeted correction.
- **NO:** downgrade/remove the blocker.
- **UNKNOWN:** prototype the final-use condition first.

## 7. Prototype-before-polish

Static intermediate perfection is not prerequisite for every downstream probe.
Where cheaper, use provisional geometry/rig/fleece, representative motion,
export/runtime framing, or device testing before production lock.

This is especially important for Carol: final identity depends strongly on
fleece and motion, while much naked Underbody is not Hero-visible.

## 8. Human-time compression

The objective is not maximum autonomous AI activity.

> **Compress human work and maximize the impact of human judgment.**

AI absorbs exploration, repetitive implementation, numerical checks,
diagnostics, evidence generation, bounded experiments, and runtime plumbing.
Human attention concentrates on identity, appeal, life, emotion, and
naturalness.

## 9. Planner information-loading order

1. Read ChatGPT Project Memory for reasoning policy.
2. Read `GRIMO_PROJECT_KNOWLEDGE_INDEX.md`.
3. Read only task-specific durable knowledge.
4. Retrieve only relevant reference evidence.
5. Read latest pushed GitHub for mutable truth.
6. Plan from Product Goal backward.

Never use Project Knowledge to infer current branch/candidate state.

## 10. Technical verification policy

Verification is change- and risk-based: no full suite by habit, no repeated
passing check without relevant changes, no broad Blender/PlayCanvas/browser/
device QA unless the Decision Question requires it, and no unrelated evidence
generation.

## 11. Final operating rule

> **Never ask “How do we perfect the current artifact?” before asking “Does
> perfecting this artifact materially improve the final companion experience?”**
