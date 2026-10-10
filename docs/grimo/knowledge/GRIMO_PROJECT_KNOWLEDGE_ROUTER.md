# Grimo — Project Knowledge Router

**Updated:** 2026-10-11  
**Repository:** https://github.com/snowtone-ai/Grimo  
**Knowledge branch:** `docs/project-knowledge-router-20261011` (not merged into `main`).  
**Purpose:** Keep ChatGPT Project Knowledge small; retrieve detailed specs from GitHub only when needed.

## 1. Durable project contract
Grimo is a smartphone-first **Task / Calendar / Grimo / Collection** PWA. Carol, Jill, Pino and Shushu are original living 3D companions. Priority: canonical appearance, cuteness, natural attention/autonomy, intentional stillness, causal touch, responsive local body action, emotional afterglow, interruption and variation. No absence penalties or relationship XP.

Technical design: coherent full-spatial 3D, maximum perceptual polish in the front interaction view, with plausible 3/4/side/rear geometry. Blender and GLB/glTF through PlayCanvas in a mobile PWA. Human visual acceptance outranks metric PASS. Planner sets Goal, approved authorities and acceptance; Codex selects production method without arbitrary test/attempt requirements.

**2026-10-10 approval:** Clearly detachable decorations (stars, moon motifs, bouquet, loose flowers, bubbles, floating particles) are separately authored assets. Identity-critical anatomy and markings (including fleece, head foliage, wings, tail, eyes) must remain. Body-only generation input is **not** the complete canonical identity.

**2026-10-11 draft:** Jill/Pino/Shushu Tripo generation poses require Human visual approval. Generation pose, rig rest pose and in-game neutral are distinct; numerical draft ranges are hypotheses. Do not incur new paid costs without authorization.

## 2. Fast repository map

| Question | GitHub path |
|---|---|
| Basic structure | `README.md`, `AGENTS.md`, `docs/repo-map.md` |
| Authority index | `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md` |
| Product North Star | `docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md` |
| Product functions, Collection, rewards, data | `docs/grimo/knowledge/product/` |
| Living companion experience | `docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md` |
| Full spatial character architecture | `docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md` |
| Planner / Codex / Human workflow | `docs/grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md` |
| Original identity artwork | `assets/grimo/source/{carol,jill,pino,shushu}/` |
| Carol original completed-design and Skin references | `assets/grimo/source/carol/approved-3d/` + `authority.json` |
| Carol geometry/hoof + 2026-10-10 body-only scope | `docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md` |
| **Mutable** Carol production state | `docs/production/carol/CAROL_PRODUCTION_STATE.md` **on the execution branch** |
| **Current** Carol MVP Motion (body-owned fleece) | `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md` |
| Jill/Pino/Shushu Tripo **DRAFT** | `docs/grimo/knowledge/character-production/GRIMO_TRIPO_GENERATION_POSE_CONTRACT_DRAFT.md` |
| Partner Eevee / Pikachu motion analysis | `docs/grimo/knowledge/research/`, `research/motion-masters/` |
| Full Eevee camera/framing measurements | `docs/grimo/knowledge/research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_DETAILED_EVIDENCE.md` |
| App implementation, tests and 3D tooling | `src/`, `scripts/`, `tests/`, `docs/architecture/` |
| Superseded/historical | `docs/archive/` |

## 3. Retrieval rules
1. Check **relevant branch and current HEAD** before citing implementation state. `main` is a historical Phase-0 base; later files are present on other branches.
2. Fetch **only 1–3 relevant documents first**; add research, historic evidence or code only if needed. Do not preload the entire repository.
3. Keep separate: newer explicit Human decisions, canonical identity, scoped approved references, draft pose images, detailed evidence, historical candidates and model hypotheses. A "new" image does not automatically supersede a final reference.
4. Carol’s current live Motion Spec contains later **no macro positional fleece lag** semantics than the Project-uploaded version; the upload was saved as a historical snapshot and never overrode it.
5. For appearance review use actual images, not just text descriptions. For important conclusions mention inspected file and revision.

## 4. Remaining visual-authority caution
Two Project-uploaded files (`carol_skin_front`, `carol_skin_side`) **do not match by bytes** the corresponding earlier inspected GitHub images. The authoritative version is not determined from file names alone. Their GitHub originals were **not overwritten** during Markdown synchronization; retain uploaded copies for a Human visual gate when needed. The other six character/Carol image uploads matched GitHub in the previous audit.

## 5. Project Knowledge housekeeping
The detailed uploaded Markdown documents are preserved or reconciled in this branch. Keep this compact router and useful source images in ChatGPT Project Knowledge; fetch detailed documents from GitHub as required. Changing the repository does not remove Project Knowledge attachments. Do not delete unmatched/sole copies before verifying accessible storage.
