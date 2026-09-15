# Grimo Character QA

Use this skill for QA of Grimo character assets and their PlayCanvas runtime integration. This is a compact operational summary of the current repository rules; it does not create a new character specification.

## Gates

- **Identity Gate:** the canonical character identity, silhouette, proportions, face, palette, and approved references remain recognizable. No generic replacement or accidental recolor/crop.
- **Living Idle Gate:** idle reads as intentional life and attention without generic whole-body bobbing, continuous all-channel motion, or a physics-selected hero pose.
- **Touch Gate:** semantic touch zones produce clear, character-specific authored acting, with appropriate result/loading feedback and no physics-led meaning.
- **Interruption Gate:** a new input, navigation, pause, mute, reduced-motion setting, or loading state interrupts safely and returns to a coherent state.
- **Variation Gate:** timing, attention, and reaction variation preserves personality; the same animation is not blindly retargeted across Carol, Jill, Pino, and Shushu.
- **Runtime Fidelity Gate:** Blender source, raw/runtime GLB, manifest, semantic bone map, morphs, animation clips, materials, camera, and PlayCanvas runtime agree.
- **Mobile Gate:** validate a smartphone-first viewport with safe areas, touch targets, resize/rotation, network loading, PWA behavior, reduced motion, audio/mute, and Pixel 7a-class performance expectations.
- **Human Gate:** automated validation cannot approve visual identity or acting. A human must inspect the front-facing companion view and approve canonical quality before rollout.

## Evidence

Run GLB structural validation and metrics, Playwright user-flow smoke, and Chrome DevTools diagnostics where available. Record errors, warnings, file size, triangles, vertices, materials, textures, bones, morph targets, animation names, console/runtime/network failures, and mobile observations. Do not treat an empty asset repository as a failed GLB check; validation becomes mandatory when an asset is added.

## Safety

Use MCP on localhost only. Prefer read-only inspection before Editor writes. Never overwrite canonical assets, expose secrets, or use external downloads/generation services without explicit scope. When a gate cannot be evaluated because Carol is not yet present, report it as not applicable rather than inventing a fixture asset.
