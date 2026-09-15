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
