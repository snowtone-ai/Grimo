# QA entry point

The full product QA principles live in `docs/product/source-pack/07_QUALITY_QA_WORKFLOW.md`.

Foundation gate:
1. `pnpm context:check`
2. `pnpm verify`
3. mobile browser smoke at 320 / 375 / 412-414 px widths
4. no console errors in launch → tasks/grimo/calendar/settings paths
5. offline shell does not destroy local task CRUD
6. Google/Gemini failure remains isolated from local task CRUD

Character gates are not considered passed until human visual review approves canonical identity and motion quality.
