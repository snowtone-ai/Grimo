# Grimo asset generation workflow

This is an on-demand, human-in-the-loop runbook. It does not authorize routine automation, bulk generation, or canonical replacement.

## Browser/session rule

When the user's existing signed-in Chrome/ChatGPT session is required, use:

`Codex Chrome extension / Browser Use → ChatGPT Web`

The Codex built-in browser must not be assumed to share the user's Chrome profile, cookies, or signed-in session. Use semantic UI targets (labels, roles, visible names); never hardcode screen pixel coordinates.

## Workflow

1. Write the asset specification and acceptance criteria.
2. Select the character canonical plus only the implementation references needed for that asset.
3. Open ChatGPT Web through Browser Use in the user's already signed-in Chrome session.
4. Upload those references and generate one candidate.
5. Inspect the candidate against canonical identity, `DESIGN.md`, layer/occlusion needs, and the requested runtime role.
6. Retry only a limited number of times when a specific, correctable defect remains.
7. Download the chosen candidate into temporary staging outside tracked source paths.
8. Verify dimensions, alpha, identity, duplicated parts/motifs, artifacts, intended usage rights, and absence of third-party copyrighted material.
9. Place only the approved file in the correct repo asset path. Never overwrite `assets/grimo/source/**` automatically.
10. Verify the asset in the actual PixiJS runtime at target viewports and DPR.
11. Record minimal provenance: date, tool/model when known, inputs by repo path, intended role, and human approval state.
12. Commit only the intended asset, derived outputs, manifest/provenance update, and directly related runtime change.

## Boundaries

- A generated reference never becomes character identity authority; the canonical remains the only authority.
- Never regenerate or replace a canonical automatically.
- Prefer a local crop, composite, alpha cleanup, or transform when generation is unnecessary.
- Do not mass-generate assets as a side effect of routine coding.
- Do not expose passwords, tokens, cookies, credentials, or user data in the repo, logs, uploads, or prompts.
- Respect the cost and approval boundaries in `AGENTS.md`; do not trigger paid work without approval.
- Do not import Pokémon artwork, audio, icons, frames, logos, or other copyrighted runtime assets.
- Generated files stay in temporary staging until dimensions, alpha, identity, duplication, rights, and runtime behavior pass review.
