# MERUNE — Production State / Source Register

**Checked:** 2026-10-18 (ChatGPT, user-provided local artifacts + main documents).  
**Status:** `CANONICAL_APPEARANCE_HUMAN_ADOPTED` / `RIG_ASSET_RECEIVED` / `GEOMETRY_HUMAN_FINAL_GO_UNKNOWN` / `RIG_DEFORMATION_HOLD` / `MOTION_NOT_IMPLEMENTED` / `RUNTIME_UNKNOWN`.  
**Release boundary:** Initial Shushu-only app remains unchanged. MERUNE is parallel R&D / future companion, not approved for launch.

## 1. Canonical authority / binary import ledger

| Asset | Actual observed local source | Registration |
| --- | --- | --- |
| MERUNE adopted identity | `merune-identity-canonical.png`, RGBA 1565×1005, 1,694,771 bytes, SHA-256 `0e49d2d76f0c95e3236a30e564af8adab000b27d926f2f3322f170047c259382` | **ORIGINAL PNG NOT YET COMMITTED**; intended `assets/grimo/source/merune/merune-identity-canonical.png`. Do not create a substitute or claim registry complete |
| Body-only Front / anatomical Left / anatomical Right / Back | User previously generated reference candidates; source bytes and hash not present in this documentation pass | **UNVERIFIED / NOT REGISTERED**; preserve role distinction; do not fabricate hashes or Human 3D-input GO |
| Rigged Tripo export | Local attachment `merune rig 8k.glb`, 7,676,572 bytes, SHA-256 `8dbb299d6b9ceab9fd8d751ce2c96438bd0fff9d49c76bafae58d5b4867c0c53` | **ORIGINAL GLB NOT YET COMMITTED**; remain external donor; do not silently replace source Geometry or source asset |

**Important:** The source image and GLB are held only in the current conversation/runtime at this checkpoint. A text digest is not a replacement for source bytes. Before any downstream task, import the user-provided exact bytes to a safe, appropriate repository/workspace location, validate hashes and licensing/storage policy, and record remote SHA. Do not claim they are GitHub-tracked until verified.

## 2. Geometry / rig inspection facts

- User: Tripo Smart Mesh produced 4 candidates; candidate **B**, `fantasy cat 3d model (1).glb`, was chosen as the leading Geometry candidate on appearance/structure; user then completed Tripo UV, 8K Texture and Rig.
- Original selected Smart Mesh Tripo display: **28,073 vertices / 31,306 mixed faces**; GLB triangles previously counted at **54,780**. Do not conflate these display counts with an exported rigged GLB's per-primitive vertices.
- **Rigged GLB inspection (2026-10-18):** glTF2, 1 mesh, 1 skin, **62 skin joints**, `JOINTS_0` and `WEIGHTS_0` present, one material image/texture, 0 animations. The rigged export's `POSITION` accessor reports **32,484** vertices and index accessor **164,340** indices / **54,780** triangles (texture seams can duplicate vertices). No facial morph target is evidenced.
- GLB joint nodes do not declare local translation/rotation/matrix attributes while skin specifies inverseBindMatrices. This raises a **bind-pose interoperability concern**; previous analytical prediction suggested an issue, but authoritative pass/fail requires actual Blender/reimport deformation and GLB runtime proof. No Human deformation GO.
- Texture is embedded and 8K-class according to local export/earlier inspection. Runtime memory/format costs are unknown until actual target export and mobile profiling.

## 3. Gates and no-regression rules

| Gate | Current | Minimum evidence needed |
| --- | --- | --- |
| Canonical Identity | **HUMAN ADOPTED** (2D only) | Original bytes in source location + SHA verification |
| Four-view input | **UNKNOWN** | Original 4 images, direction/layout/body-marking check, separate Human acceptance |
| Geometry | **CANDIDATE / HUMAN FINAL HOLD** | Front, 3/4, side, back under equivalent light; nose/eye socket, inner ears, harp, four feet, tail root and curl |
| UV / Texture | **DATA PRESENT / HUMAN QUALITY UNKNOWN** | Saved textured renders vs Canonical, seams and body motif positions |
| Rig | **DATA PRESENT / DEFORMATION HOLD** | Blender import + neutral + head, ears, chest, limbs, tail bends + reexport and reimport |
| Facial | **NOT IMPLEMENTED** | Eyelids, gaze, mouth, neutral-to-emotion-to-return |
| Motion | **NOT IMPLEMENTED IN EXPORTED GLB** | Two hero reactions, stance/support/contact, locomotion, real sit, interruption |
| Runtime | **UNKNOWN** | PlayCanvas+smartphone PWA evidence incl. load, responsiveness and thermal/frame pacing |
| Release | **OUT OF SCOPE** | Explicit future Human product decision |

Protect the accepted appearance, original attached bytes, existing Jill/Pino/Shushu and Shushu-only launch plan. Tripo credits/paid work require explicit approval. Never report numerical gates as human attractiveness GO.

## 4. Most valuable next action

**Bring the exact original Canonical PNG and Rig GLB into the controlled project workspace (not as a synthetic replacement) and perform Blender bind-pose/reimport + representative deformation audit.** Correct only reproducible defects before importing basic animations or spending credits. Capture minimal front/side/3Q and moving deformation evidence for Human review. Track asset intake on a scoped character branch; update main Handoff only after material state change.
