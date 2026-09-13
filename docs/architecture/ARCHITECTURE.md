# Architecture

```text
Next.js / React
  routes + UI + app state + viewport host
        |
        +--> domain TypeScript (task/calendar/reward/interaction)
        +--> Dexie repositories (local-first persistence)
        +--> Google/Gemini integrations
        |
        `--> GrimoViewport host
               |
               `--> PixiJS 8 layered 2.5D runtime
                    rendering / hit / secondary / particles / ticker
```

The character renderer never becomes the owner of task persistence or application routing. React does not animate individual Grimo layers frame-by-frame.

## Initial browser target
Smartphone Chrome/PWA. Pixel 7a is the minimum quality/performance acceptance target; higher-end Android devices must not be required for basic interaction.
