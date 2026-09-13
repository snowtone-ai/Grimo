# Product source use

`source-pack/` preserves the pre-rebuild Grimo project sources as evidence. Do not edit them to hide historical assumptions.

Current overrides, which have higher priority:

1. Product and repository name is **Grimo**.
2. Development continues in a **new repository** (`snowtone-ai/Grimo`), not inside the old Grimoire repository.
3. Task and Calendar behavior/security boundaries are selectively migrated; old UI/gamification are not.
4. Main navigation is Tasks / Grimo / Calendar; Items is under Grimo.
5. Settings can choose startup page Tasks or Grimo; Tasks is the default.
6. PixiJS 8 layered 2.5D remains the formal character runtime.
7. Full 3D/Blender/Three.js legacy experiments remain excluded.

For architecture decisions read `../decisions.md` first, then use the source pack for character/product quality details.
