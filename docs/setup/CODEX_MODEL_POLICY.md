# Codex / GPT-5.6 model policy — Plus quota conscious

Updated 2026-09-13.

## Default
- **Sol Medium**: planning, integration, milestone review, high-blast-radius changes.
- **Luna High**: clear routine coding, tests, command/log inspection, small refactors.
- **Terra Medium**: medium-complexity multi-file exploration or when Luna needs repeated correction.
- **Sol High**: security/auth/migration/architecture/difficult debug, or a demonstrated Medium failure.

Do not default to xhigh/max/ultra/Astra. Do not repeatedly poll subagents. Workers receive complete tasks and report only at milestone completion or when blocked; reuse an existing worker rather than duplicating work.

## Evidence quality
**High confidence:** OpenAI describes Sol as the flagship, Terra as balanced, and Luna as the fastest/most economical; Plus Codex users can choose all three and set effort. OpenAI also documents Luna delegation in Codex.

**Medium/low confidence:** recent r/codex user reports repeatedly favor Medium for general work and Luna for tightly-scoped work, but quota accounting and model behavior have changed frequently. Treat exact percentage savings and message counts as temporary anecdotes, not policy.

The X workaround about avoiding parent-agent status polling is adopted as a general orchestration rule. Its exact reported percentage savings are not treated as reproducible evidence.
