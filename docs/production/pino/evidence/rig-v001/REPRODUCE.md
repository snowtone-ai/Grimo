# Reproduce Pino base rig v001

Use Blender 5.2.1 LTS. Run from the checkout root, with Pino LFS files hydrated (`git lfs pull --include='assets/grimo/production/pino/**,assets/grimo/source/pino/**' --exclude=''`). The build creates derived files only. Review the scripts before rerunning over generated outputs.

```powershell
blender --background --factory-startup --python scripts/blender/build-pino-base-rig-v001.py
blender --background --factory-startup --python scripts/blender/prove-pino-base-rig-v001.py
blender --background --factory-startup --python scripts/blender/verify-pino-base-rig-v001.py
& '<Python with Pillow and numpy>' scripts/3d/package-pino-base-rig-v001.py --finalize
```

The proof script's `PY` variable points to the bundled Codex Python on the original workstation; adapt that executable path for another machine. Its package helper holds only one test's low-resolution temporary frames at a time and removes them after composing its GIF and representative board. No permanent frame dump is produced.

`--preview` on the proof script renders only representative poses. `--quick` on verification repeats saved pose/Neutral checks without repeating Cycles comparisons. `repair-pino-proof-support-v001.py` records the focused repair used on the first serialized proof; it is **not** needed after a current clean proof build, which already keeps support at the rest endpoints.

Proof timeline: tail 1–49, eyes 55–103, paws/contact 109–181, shallow relaxation 187–235. Views use original scene units and fixed framing. GIF samples do not certify every interpolated frame. The saved authoring candidate contains no animation and starts with all IK influences off. In proof, foot support stays enabled at zero-strength rest endpoints, with the mesh returning to Neutral.

If saved verification asserts, treat the artifact as unverified; do not publish a technical PASS. Human Rig/Geometry Gate remains PENDING regardless of numeric results.
