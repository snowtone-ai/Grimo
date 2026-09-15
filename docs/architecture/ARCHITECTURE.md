# Architecture

```text
Next.js / React PWA
  routes + UI + app state + viewport host
        |
        +--> domain TypeScript (task/calendar)
        +--> Dexie repositories (local-first persistence)
        +--> Google/Gemini integrations
        |
        `--> future Grimo 3D viewport host
               |
               `--> planned PlayCanvas runtime
                    GLB/glTF assets authored in Blender
```

The character runtime must not own task persistence or application routing. Phase 0 does not implement the viewport, PlayCanvas runtime, Blender assets, models, animation, or touch interaction. The existing `/grimo` route remains a neutral placeholder so the PWA foundation continues to build.

## Browser target

The product is smartphone-first and PWA-oriented. Pixel 7a-class Chrome is the minimum future quality target; basic Task and Calendar use must not depend on character runtime availability.
