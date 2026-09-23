# Architecture

## Product/runtime boundary

```text
Next.js / React PWA
  routes + UI + app state + viewport host
        |
        +--> domain TypeScript (task/calendar)
        +--> Dexie repositories (local-first persistence)
        +--> Google/Gemini integrations
        |
        `--> Grimo companion viewport
               |
               `--> current hypothesis: PlayCanvas runtime
                    GLB/glTF assets authored in Blender
```

The character runtime must not own task persistence or application routing.

Character production follows
`docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`:
Front-Optimized 3D-First is the current baseline hypothesis, not a Full-3D
purity requirement. Local hybrid techniques are allowed; architecture may
change through evidence-driven Architecture Review.

## Device boundary

Grimo is smartphone-first.

- available real-device QA: **Xiaomi 14T Pro**
- Pixel 7a-class: lower-performance compatibility/design target
- real Pixel 7a: unavailable
- Pixel 7a status: **UNVERIFIED_TARGET**

Task/Calendar must remain usable independently of character-runtime availability.
