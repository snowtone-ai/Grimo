# Codex model policy — ChatGPT Planner / Luna Executor

Updated 2026-09-16.

## Default workflow

The default cross-surface development loop is:

```text
Codex task completes
→ commit + push
→ classify the next task
→ simple/deterministic: Codex Luna / Low
→ substantial reasoning: ChatGPT Planner
  → read the latest pushed GitHub state
  → investigate, reason, and produce a complete Luna / Low prompt
  → Codex Luna executes, validates as needed, commits, and pushes
→ Astra-class: Codex Astra / Medium directly
```

GitHub's latest pushed state is the session handoff boundary. Unpushed local
state is not a source of truth for the next session.

## ChatGPT Planner

Use ChatGPT as the default planner for substantial planning, architecture and
multi-file implementation planning, repository investigation, implementation
or refactor strategy, debug strategy based on pushed logs/code, integration
design, and task decomposition. The Planner reads the specified branch from
GitHub, confirms the current repository state, completes the reasoning, and
outputs one exact Codex Luna / Low execution prompt. It does not modify the
repository.

Planner prompts must require no re-asking of known information, no guessing
about local-only state, enough specificity that Luna need not redesign, lean
targeted validation, and `commit + push` at the end of the Luna task.

## Codex Luna / Low

Luna is the default executor for file editing, deterministic implementation,
clerical changes, well-specified coding, moves and renames, documentation,
targeted validation, and git operations including commit and push. A task that
has been fully planned may be large and still belongs with Luna. Luna follows
the prompt and does not independently redesign the solution.

## Codex Astra / Medium

Reserve Astra for Carol geometry interpretation, critical canonical identity
decisions, high-value visual or spatial reasoning, explicitly selected special
architecture reasoning, and other explicitly designated Astra-class work.
Astra is not for routine implementation, validation, or git operations.

## Codex Sol / Terra — exception only

Sol and Terra are not part of default routing. Use them only when the
ChatGPT-Planner-plus-Luna workflow cannot succeed and at least one condition
holds: repeated local execute/observe/reason/edit loops are required; ChatGPT
cannot observe required local state; Luna failed a clearly specified task and
non-trivial local reasoning is needed; or the user explicitly requests Sol or
Terra. A large task alone is not a reason to use them. Automatic escalation is
prohibited.

## Handoff and completion

Tracked repository changes are complete by default only after:

```text
edit → targeted validation if needed → commit → push
```

Exceptions are an explicit no-push instruction, a security concern, an
unresolved merge/failure, an explicit Human Gate before commit/push, or an
unavailable remote; report the exception clearly. The short final report must
state branch, commit, pushed status, validation, and next handoff.

Multi-agent remains disabled in `.codex/config.toml` (`multi_agent = false`).
