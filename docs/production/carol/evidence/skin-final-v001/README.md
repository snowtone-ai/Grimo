# Carol Skin final candidate v001

**Status:** Ready for strict Human Skin review. No Human approval is claimed.

- Production asset: `assets/grimo/production/carol/blender/carol-skin-final-v001.blend`
- Source: `carol-face-ear-authority-match-v001.blend`, incorporated from the latest pushed face/ear branch into the latest pushed repository state
- Active reference manifest: `assets/grimo/source/carol/approved-3d/authority.json`
- Rebuild: `blender -b --python scripts/blender/refine-carol-skin-v001.py`, then `python scripts/blender/compose-carol-skin-final-evidence.py`

## Human review sequence

1. [skin-authority-comparison.png](skin-authority-comparison.png): approved Skin Front/Side, complete neutral 3D candidate, and 50% overlays. The Front uses its locked 994 px/H registration. Skin Side has no locked whole-body canvas transform in the refreshed authority; this board aligns planted supports and ground once at approximately 1030 px/H. Treat the Side overlay as a visual diagnostic, not a fit score.
2. [profile-closeup.png](profile-closeup.png): the Side forehead, bridge, muzzle, jaw, ear, shoulder, and foreleg at that same fixed registration.
3. [spatial-review.png](spatial-review.png): Front, Side, and legitimate derived 3/4, Rear, Top from the same saved neutral mesh. Derived views expose volume and attachments; they are not independent artwork authorities.
4. [normal-identity-context.png](normal-identity-context.png): approved Normal Front/Side beside the final Skin renders for qualitative Carol identity, face, ear, and hoof context. Normal has fleece, so this is not a silhouette overlay.
5. [renders/](renders/): untouched Blender Cycles RGBA renders, including isolated face views. The contact sheets composite transparent renders on white and transform the approved images only by uniform scale and translation.
6. [validation.json](validation.json): input and authority hashes, changed objects, saved asset hash, finite/manifold/outward checks and nonadjacent self-intersection checks.

The prior face/ear evidence in `../face-ear-authority-match-v001/` shows the inherited reconstruction against Normal Front/Side and the approved Ear Module. The final Skin asset keeps those approved-source comparisons relevant except for the disclosed local Skin changes.

## What changed

- A restrained advance of the central upper forehead forms the approved short-muzzle-to-forehead turn. The nose, mouth, eye apertures, cheek width, and front face silhouette remain located with the approved face fitting.
- The dorsal head/body strip is broadened; the ventral chest cap is tucked back to soften the neck and front underbody transition.
- Fore and hind limb stations were rounded and resized through their Front width while retaining the four planted support locations and compact low stance. The hind pair was brought inward to preserve the approved partial hind-foot reveal in Front.
- Each hoof remains one three-lobe module. Its footprint and height were reduced to the approved small-hoof read, its side crown and sole transition are rounder, and inherited inward mesh winding was corrected.
- The cream body/limb material was warmed to reveal the underbody against a neutral review background. Approved reference images were not edited.

## Critical limits

- The Skin Front and Skin Side head-top silhouettes disagree after aligning their support structure. The candidate preserves the Front height; the Side crown remains lower than the Skin Side image by roughly a few hundredths of `H` in the support-based overlay.
- The lower muzzle turn, chest cap and limb-root shading, plus ear attachment in Side and 3/4, remain the most useful areas for strict perceptual scrutiny. The fixed overlays expose them directly.
- Skin is supporting geometry for the fleece-dominant final Carol. This candidate does not establish final fleece appearance, rig deformation, motion clearance, runtime behavior, or Human acceptance.
