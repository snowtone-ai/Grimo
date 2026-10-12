# Grimo — Production Operating System

**Status:** Active durable workflow / role authority  
**Updated:** 2026-09-25  
**Scope:** How Human, ChatGPT Planner, and Codex cooperate across Grimo production

---

## 0. Core decision

Grimo uses an **Outcome-Constrained / Process-Autonomous** production model.

The destination is constrained.

The route is not.

The default rule is:

> **Human / Planner define the Goal, Authority, observable problem, acceptance target, and true external boundaries. Codex owns the execution process.**

Codex is not a patch executor following a prewritten repair recipe.

Codex is the implementation owner responsible for finding the strongest path from the current state to the defined outcome.

---

## 1. Purpose

This document defines role ownership and execution boundaries.

It does **not** prescribe:

- a fixed production sequence;
- a fixed modeling method;
- a fixed testing method;
- a fixed diagnostic method;
- a fixed iteration count;
- a mandatory reuse strategy;
- a mandatory patch-vs-rebuild strategy;
- a mandatory probe architecture;
- a mandatory topology, rig, shader, or tool workflow.

Those decisions belong to the executor unless an explicit product-level decision or external constraint genuinely removes an option.

The objective is not procedural compliance.

The objective is:

> **maximum progress toward the approved Grimo experience with minimum unnecessary Human work.**

---

## 2. Authority is strict; process is free

The project distinguishes two categories.

### 2.1 Outcome / authority constraints

These may be strict.

Examples:

- current explicit Human decisions;
- Product North Star;
- canonical identity;
- approved visual authorities;
- approved product behavior;
- current architecture decisions;
- required runtime/device capability;
- repository truth;
- external cost or safety limits;
- required final deliverables.

Codex must not silently redefine these to make execution easier.

### 2.2 Process choices

These belong to Codex by default.

Examples:

- diagnosis;
- task decomposition;
- order of work;
- modeling technique;
- topology strategy;
- sculpting vs procedural editing;
- local repair vs broad rebuild;
- reuse vs reconstruction;
- scripts and tooling;
- temporary assets;
- measurements;
- overlays;
- rendering strategy;
- comparison method;
- internal tests;
- iteration count;
- rollback / alternate approach;
- internal stopping judgment.

A Planner prompt should not convert process choices into rules merely because the Planner can imagine a plausible method.

---

## 3. Role ownership

## 3.1 Human

Human owns:

- Product Goal;
- explicit preference changes;
- canonical / approved perceptual authority;
- final perceptual acceptance;
- identity;
- cuteness / appeal;
- emotional quality;
- naturalness;
- whether something feels like the intended companion;
- major product or architecture changes when they alter the intended experience.

Human feedback should describe what is observed whenever possible.

Example:

> “The forehead-to-muzzle transition does not read like the approved Side.”

This is evidence.

It is not automatically an instruction such as:

> “Move these vertices by X and preserve every surrounding loop.”

The executor should determine the actual cause and best repair.

---

## 3.2 ChatGPT Planner

Planner owns **problem definition and information compression**, not the implementation recipe.

For an execution task, Planner should normally provide only what materially improves the executor's decision quality:

1. **Goal** — what successful final result is wanted.
2. **Authority** — what defines truth.
3. **Current state** — latest relevant repository / asset state.
4. **Human observations** — what currently appears wrong or incomplete.
5. **Acceptance target** — what should be true when the task returns.
6. **External boundaries** — only real constraints that are not executor choices.
7. **Required handoff** — what must be saved / committed / reported.

Planner should deliberately avoid prescribing:

- exact vertex moves;
- detailed construction order;
- exact attempt count;
- mandatory intermediate versions;
- mandatory reuse;
- mandatory local-only repair;
- mandatory rebuild;
- arbitrary file freezes;
- unnecessary test matrices;
- speculative root-cause claims presented as fact.

Planner may give hypotheses, but they must be labeled as observations or hypotheses, not disguised implementation commands.

---

## 3.3 Codex Executor

Codex owns the execution process.

Codex is expected to:

- inspect the actual current state;
- independently diagnose the problem;
- identify additional relevant issues not explicitly named by Human;
- choose the implementation strategy;
- choose which existing assets are useful;
- decide whether to preserve, reshape, replace, or rebuild;
- create diagnostics when useful;
- iterate internally as much as useful;
- abandon weak approaches;
- compare alternatives;
- validate the result;
- generate decision-useful evidence;
- report remaining uncertainty honestly.

Codex may disagree with the Human's or Planner's proposed technical explanation when direct inspection supports a better one.

Codex should optimize for the approved result, not literal compliance with a guessed repair theory.

---

## 4. Default execution brief

The preferred Codex prompt is compact.

A normal high-quality execution brief looks like:

```text
GOAL
What final result must be achieved?

AUTHORITY
What defines correctness?

CURRENT STATE / OBSERVATIONS
What is known now, including Human-visible problems?

ACCEPTANCE TARGET
What should no longer be meaningfully wrong when Codex returns?

EXTERNAL BOUNDARIES
Only genuine product, cost, safety, authority, or irreversible-action limits.

HANDOFF
What artifacts / evidence / commit state must be returned?

EXECUTION FREEDOM
Codex owns diagnosis, decomposition, method, tooling, iteration, validation, and internal stopping.
```

If a section adds no useful information, omit it.

Prompt length is not a quality target.

A short prompt that gives the executor the correct destination and authority is better than a long prompt that narrows the search space without evidence.

---

## 5. Codex execution freedom

Unless an explicit higher authority says otherwise, Codex may autonomously decide:

- which files to inspect;
- which historical assets to inspect;
- whether reuse is beneficial;
- whether reconstruction is beneficial;
- whether a local fix is enough;
- whether a larger structural change is justified;
- which Blender techniques to use;
- whether to write or modify scripts;
- which diagnostics to generate;
- whether numerical measurement is useful;
- whether visual comparison is more informative;
- which test is worth running;
- how many internal iterations to perform;
- when an approach should be abandoned;
- how to organize intermediate work.

There is **no default attempt limit**.

There is **no default two-cycle stop rule** for Codex's internal work.

There is **no mandatory cheapest-probe rule**.

There is **no mandatory reuse-first rule**.

There is **no mandatory patch-first or rebuild-first rule**.

There is **no default requirement to preserve an existing implementation simply because it already exists**.

There is **no default requirement to replace an existing implementation simply because a cleaner reconstruction is possible**.

The executor chooses based on the final Goal.

---

## 6. Exploration and convergence are both valid

Grimo work commonly has two outcome types.

### 6.1 Exploration

The objective is to learn enough to make a decision.

Codex is free to choose how to obtain that evidence.

The work ends when the relevant uncertainty is sufficiently resolved or genuinely blocked.

### 6.2 Convergence

The objective is to finish or materially complete an artifact.

Codex should continue improving the artifact while meaningful, achievable discrepancies remain.

The work should not stop merely because:

- one metric passes;
- one view looks correct;
- the candidate is better than before;
- an initial issue was fixed;
- a minimum implementation exists.

A convergence task returns when the executor judges that further work is unlikely to produce a material improvement toward the stated acceptance target without changing the authority itself or requiring a new external decision.

These are outcome semantics, not fixed workflows.

---

## 7. Validation and evidence

Validation exists to reveal truth, not to satisfy a ritual.

Codex decides which validation is useful for the task.

Possible evidence includes:

- direct visual comparison;
- overlays;
- measurements;
- rendered views;
- runtime tests;
- interactive tests;
- deformation tests;
- device tests;
- code/tests;
- topology diagnostics;
- performance measurements.

No validation class is mandatory by habit.

No passing technical metric can overrule an obvious Human-visible failure.

No flattering presentation may hide a meaningful failure.

Evidence should make the state easier to judge, not merely make the result look favorable.

---

## 8. Quality hierarchy

When priorities conflict:

```text
1. Product / Experience Goal
2. Canonical identity and approved visible authority
3. Functional behavior required to deliver that experience
4. Runtime / device viability
5. Technical implementation quality
6. Internal elegance / cleanliness
```

Technical cleanliness matters when it protects the higher levels.

Technical purity is not an independent product goal.

A beautiful topology does not compensate for an off-model Carol.

A visually correct temporary solution is not automatically sufficient if it will break required motion or runtime.

The executor should resolve the real product consequence.

---

## 9. Human review

Human perceptual approval remains authoritative for:

- identity;
- cuteness;
- visual appeal;
- naturalness;
- emotional read;
- weight;
- companion quality;
- objectionable visible artifacts.

Codex must not self-declare Human approval.

Codex may state:

- what improved;
- what evidence supports the result;
- what remaining discrepancy it can still see;
- whether it believes the result is ready for Human review.

Human review should receive evidence close enough to the real use condition that the judgment is meaningful.

---

## 10. Repository and information truth

Project information is separated by role.

### Durable Project Knowledge

Defines:

- Goal;
- product requirements;
- identity;
- experience principles;
- architecture;
- stable character authority;
- durable evidence.

### Git / latest pushed repository state

Defines mutable execution truth:

- current branch;
- current assets;
- current implementation;
- current evidence;
- current blockers;
- current production state.

When mutable state matters, Codex should inspect the current repository rather than trust an old prompt or chat summary.

Historical files are resources, not current instructions, unless current authority explicitly promotes them.

---

## 11. External boundaries

Maximum process autonomy does not mean unlimited authority.

Codex must respect genuine external boundaries such as:

- do not alter canonical / approved authority merely to make the implementation pass;
- do not silently redefine the Product Goal;
- do not perform destructive unrelated repository changes without reason;
- do not incur unauthorized monetary cost;
- do not claim real-device or Human approval that did not occur;
- do not perform external irreversible actions that require Human authorization.

These are boundaries on outcome and side effects, not instructions for how to solve the work.

---

## 12. When Planner may constrain process

Process constraints are exceptional.

Planner should add one only when at least one of the following is true:

- Human explicitly requests the method;
- a tool / environment has a proven hard limitation;
- a method creates unacceptable monetary or irreversible cost;
- a method would violate a higher authority;
- previous evidence has clearly demonstrated that a specific approach cannot achieve the Goal;
- the task is intentionally testing one specific implementation hypothesis.

Even then:

> **Constrain only the proven-invalid or externally forbidden option. Do not replace it with a full recipe unless necessary.**

A failed approach is evidence against that approach, not permission to micromanage every remaining choice.

---

## 13. Superseded workflow rules

The following are **not** default Grimo production rules:

- Planner-defined attempt limits;
- mandatory two-cycle stopping;
- mandatory bounded implementation scope;
- mandatory cheapest falsifiable probe;
- mandatory reuse-first;
- mandatory minimum-sufficient implementation for convergence work;
- mandatory local repair before broader change;
- mandatory reconstruction after local failure;
- mandatory predefined test sequence;
- mandatory predefined internal PASS/FAIL gates before Codex can explore;
- detailed Planner-authored modeling recipes.

If old prompts, archived documents, or historical production notes contain these rules, they are historical context only unless a current explicit Human decision reinstates them for a specific task.

---

## 14. Human-time compression

The system should maximize:

> **useful progress per Human review cycle**

AI should absorb as much execution work as practical:

- inspection;
- diagnosis;
- search;
- comparison;
- implementation;
- iteration;
- measurements;
- diagnostics;
- evidence generation;
- repository work.

Human attention should be concentrated where Human judgment adds unique value.

The goal is not to maximize AI activity.

The goal is to minimize avoidable Human work while maximizing final quality.

---

## 15. Standard completion report

For repository production work, a concise handoff should normally include:

1. branch;
2. final commit SHA;
3. push / remote verification;
4. what materially changed;
5. what materially improved;
6. remaining known discrepancy or uncertainty;
7. evidence entry point;
8. next Human / Planner handoff.

Codex may add information when it is genuinely useful.

---

## 16. Final operating rule

> **Specify the destination precisely. Give the executor the room to discover the route.**

And:

> **Do not turn an observation into an implementation instruction unless evidence requires it.**

And:

> **Do not stop autonomous iteration merely because the Planner did not predict the next useful step.**

And:

> **The approved result matters more than procedural obedience.**
