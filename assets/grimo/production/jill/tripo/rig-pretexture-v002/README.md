# Jill Pre-Texture v002 — implemented review / HOLD

Original v001 is untouched. This derivative inherits `379fe79ac2561b9a5796a4657c36d503d248cf04` and the implementation-plan amendment `202eae9`.

| File | Purpose |
|---|---|
| `jill-rig-pretexture-v002.blend` | Authoring master, 130 bones / 39 semantic channels / 20 body morphs / 16 anchors. Saved at Canonical smile. Contains a bounded 305-frame review action. |
| `jill-rig-pretexture-v002.glb` | Same rig's sampled review playback. Blender drivers/IK are not portable runtime logic. |
| `jill-texture-input-neutral-v002.glb` | Neutral evaluated surface, one active UV, no skeleton/morph/anchors/animation. Inspection clay only. |
| `jill-texture-input-neutral-v002.fbx` | Equivalent texture-only neutral input. Same restrictions. |

**No upload or Texture execution. Not a Technical GO candidate yet.** Lid/socket continuity, mouth/chin appearance, root layering/fold and UV density remain HOLD. Human alone can approve appearance and final GO.

See [Evidence](../../../../../../docs/production/jill/rig-pretexture-v002/Evidence.md), [Texture specification](../../../../../../docs/production/jill/rig-pretexture-v002/TextureSpec.md), [Tripo transfer](../../../../../../docs/production/jill/rig-pretexture-v002/TripoHandoff.md) and [SHA/path manifest](../../../../../../docs/production/jill/rig-pretexture-v002/Manifest.json).

Active UV is `Tripo_Input_UV`. Original source UV is retained separately as `v002_Source_UV_Preserved`; active inherited islands use `.006 + .88*source` with one documented local degenerate-triangle repair. Use the active UV for returned texture maps. Do not replace the master with any returned Tripo rig or mesh.
