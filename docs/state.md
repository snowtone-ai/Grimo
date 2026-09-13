# Production state

As of 2026-09-14, the Grimo foundation, production deployment configuration, and Google/Vercel integration foundation are present. Four canonical character images and eight implementation references per character are present.

Carol PixiJS Phase 1 passed Human Gate 1. The first Phase 2 idle/presence attempt failed Human Gate 2 at 0/100 because its motion/presence quality was rejected; that historical state is preserved at commit `03a52a5` on the pushed branch `codex/carol-phase2-idle-hg2` and was not merged to `main`.

An Eevee-motion-based Phase 2 rebuild is prepared on `codex/carol-phase2-eevee-motion-rebuild`: 11 visually inspected Let's Go Eevee videos and 33 episodes underpin nine source-traceable authored motions, composed deterministically as Calm/Balanced/Attention-Seeking candidates. Human Gate 2 retry remains pending Chrome full-screen review; it is not approved or deployed, and Phase 3 has not begun.

The Grimo PWA icon source is owned at `assets/grimo/source/app-icon.png`; install icons, Apple touch icon, maskable icon, and favicon are derived under `public/` and declared in application metadata.
