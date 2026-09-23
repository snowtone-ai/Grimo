# Codex model / effort policy

**Updated:** 2026-09-23  
**Status:** Routing guidance; Product/architecture authority lives elsewhere.

Model choice follows the bounded task and Decision Question. Do not force one
model across all Grimo work.

## Current routing

- **GPT-6 Luna — Low/Medium:** mechanical edits, repetitive file work, simple
  fixes, docs, narrow searches, deterministic validation, low-ambiguity tasks.
- **GPT-6 Sol — Medium:** default implementation workhorse for normal feature
  work, TypeScript/React, refactors, tests, and medium-to-hard debugging.
- **GPT-6 Sol — High:** harder bounded implementation/debugging where extra
  reasoning materially reduces failure risk.
- **GPT-6 Astra — Low/Medium/High:** architecture decisions, ambiguous
  requirements, high-consequence spatial/identity reasoning, repo-wide
  reasoning, and difficult failures where a wrong premise wastes substantial
  human time.
- Other high-cost models/efforts are exception-only when their expected value is
  higher for the specific bounded task.

Planner reasoning should happen before executor work so Codex receives a
Decision Question, required evidence, PASS/FAIL/UNKNOWN, attempt limit, and next
decision for each outcome.

## Execution invariant

```text
bounded edit
→ targeted validation only if justified
→ factual report
→ commit
→ push
```

Do not use model capability as a reason for scope creep, extra tests, broad repo
cleanup, architecture changes, or Human-quality self-approval.

`.codex/config.toml` keeps multi-agent disabled. Tool/MCP selection is
task-specific; do not permanently disable tools needed by future early
fleece/motion/runtime probes.
