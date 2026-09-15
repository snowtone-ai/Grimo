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

Automated checks are evidence, not approval of character identity, acting, or
interaction feel. Those require human visual review through the Human Gate.

Do not run `pnpm verify` by default. It remains only as a compatibility alias
for the full check.
