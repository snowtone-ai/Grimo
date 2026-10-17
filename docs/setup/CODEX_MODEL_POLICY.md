# Codex model policy — quota first

Updated 2026-09-16.

Use the least expensive model that can safely handle the task:

- **Luna Low** — clerical work, deterministic coding, targeted tests, and git.
- **Sol Medium** — substantial implementation and integration.
- **Astra Medium** — high-value geometry, identity, or architecture reasoning.
- **Astra Low** — bounded review when needed.
- **Astra High** — exceptional only.

Do not use Astra for routine validation, command execution, test-failure triage,
or repository-wide scans. If deterministic validation is needed in an Astra
session, assign it to Luna or let GitHub Actions handle it. Automatic model
escalation is prohibited.

Multi-agent remains disabled in `.codex/config.toml` (`multi_agent = false`).

## 2026-10-17 scope-specific decision — next Grimo app data foundation

Human selected **GPT-6.1 Sol**. For the narrowly scoped `GrimoLocalV1` / Task repository / PENDING reward-event foundation work, select **Sol 6.1 / Medium** (new session, no `/compact`). Medium balances agentic code reliability with reasoning-token use; Low is suitable for later simple clerical work, High only after concrete hard blocker and explicit planner re-evaluation. Never automatically increase effort, spawn agents, re-read unrelated 3D evidence or run redundant full builds; read the authority contract once, reuse code, apply targeted tests, and report concrete results. This scope-specific override does not mandate Sol 6.1 for all future tasks.
