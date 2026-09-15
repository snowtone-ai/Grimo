# Grimo 3D Production

Use this skill for Grimo's Blender-to-PlayCanvas asset production and tooling work.

## Authority and scope

Follow the repository's `AGENTS.md` authority order: current user instruction, approved canonical identity / production references, `DESIGN.md`, current product/data/motion/3D specifications, decision/state/task documents, then external research. Do not revive archived PixiJS, 2D, or 2.5D architecture.

The production baseline is fixed:

`Blender -> GLB/glTF -> PlayCanvas -> Next.js/React smartphone-first PWA`.

Carol is the first vertical slice. Preserve the four canonical identities and the current Grimo icon. Never overwrite canonical assets as part of a probe or temporary test.

## Production contract

- Pin Blender, Blender MCP, PlayCanvas, `@playcanvas/react`, physics, exporter, and validation versions in `docs/setup/3D_TOOLCHAIN.md`.
- Keep reproducible operations in version-controlled Blender Python and background CLI scripts. MCP is an actuation/inspection surface, not the only source of truth.
- The source of truth is Git plus Blender source assets, exported GLB/glTF, and TypeScript runtime code. PlayCanvas Editor is for authoring, inspection, preview, and QA.
- Keep the future export set explicit: `carol.raw.glb`, `carol.runtime.glb`, and `carol.manifest.json`.
- Preserve source hashes, export hashes, tool versions, semantic map versions, counts, clip names, and generation time in the manifest.

## Rig and deformation

CloudRig is a prototype comparison path (`Carol Rig Prototype A`), not an automatic production decision. Compare it with a compact custom rig before adoption. Use semantic bone names and maintain a versioned semantic bone map. EasyWeight is for weight cleanup. Pose Shape Keys is for corrective, facial, and fleece deformation.

Hero acting, facial acting, primary touch reaction, and primary fleece performance are authored animation. Do not let physics choose a hero pose. Physics is limited to props, collisions, joints, environment interaction, bounded residual secondary motion, and Secret Motion.

## Interaction and forbidden patterns

Touch zones describe semantic intent and hit volumes, not arbitrary mesh regions. A meaningful interaction is a coordinated visual, motion, sound, optional haptic, and result/loading response.

Reject whole-image squash/stretch, generic whole-body bobbing, physics-led hero acting, the same personality animation retargeted to every character, weak acting hidden by VFX/audio, always-on motion in every channel, and unbounded simulation.

## GLB workflow

1. Inspect the source and current specifications before authoring.
2. Produce or update a version-controlled Blender source and deterministic export script.
3. Export raw GLB, apply only documented runtime transforms/optimization to a separate runtime GLB, and generate the manifest.
4. Run `pnpm 3d:validate -- <file.glb>` and `pnpm 3d:inspect -- <file.glb>`.
5. Inspect in PlayCanvas, then run browser/mobile QA. Automated metrics are evidence; the final visual decision is the Human Gate.

Temporary cubes and test scenes must be in-memory or disposable and must be deleted/cleaned before delivery. Never download an external asset or read credentials, `.env` files, browser profiles, or files outside the repository for routine production automation.
