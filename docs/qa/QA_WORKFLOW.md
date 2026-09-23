# QA workflow

QA is change-based and targeted by default.

- Documentation, references, and prompt-only changes need no automated tests.
- Small code changes use at most one relevant check.
- A reproducible bug fix may use one focused regression test.
- A changed/exported GLB gets one targeted `pnpm 3d:validate -- <file.glb>`.
- Broader UI, browser, Storybook, 3D, Lighthouse, or device QA is opt-in for
  an explicit QA task, release gate, Human Gate, or concrete regression risk.

Pull requests run the core regression through GitHub Actions:
`pnpm check:full`. Local agents do not need to reproduce full CI; they should
run the smallest relevant check and investigate a CI failure when one occurs.

Gate order for character work is **Experience → Probe Validity / Evidence → Functional → Technical Hygiene**.
Automated checks are evidence, not approval of identity, acting, or interaction
feel. Before a Human perceptual conclusion, visible assets and interaction
mechanics must be representative enough to answer the Decision Question; otherwise
record **PROBE_INVALID**, not candidate FAIL. Technical diagnostics block only when
they protect a material visible, full-spatial, or functional requirement.

Do not run `pnpm verify` by default. It remains only as a compatibility alias
for the full check.
