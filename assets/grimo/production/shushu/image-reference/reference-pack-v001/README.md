# Shushu Reference Pack v001

Completed 2026-10-12 with built-in image_gen. Human explicitly accepted all three Stage A anchors in this chat: “人間レビューは合格だ。そのまま完遂しろ。” This acceptance is Stage A only; the fourteen new expression/pose/extended/additional images remain Human review pending. No geometry, topology, rigging, skinning or Tripo operations were performed.

Open [review.html](review.html) for grouped clickable full-resolution review. Exact final prompts and direct-input order are in [manifest.json](manifest.json). Each successful generation directly attached canonical identity plus all four body-only authority PNGs. The tool has a five-path limit, so generated anchors were used for visual comparison and consistency decisions, not attached as a sixth input. This is a documented limitation relative to the requested anchor-input workflow.

## Images and status

| No. | Image | Status |
|---|---|---|
| 1 | [正面全身・ニュートラル](anchors/01-standing-neutral-front.png) | Human accepted |
| 2 | [顔アップ・ニュートラル](anchors/02-face-neutral-closeup.png) | Human accepted |
| 3 | [全身・3/4](anchors/03-standing-neutral-three-quarter.png) | Human accepted |
| 4 | [半目](expressions/04-half-blink.png) | AI selected; Human review pending |
| 5 | [完全な閉眼](expressions/05-full-blink.png) | AI selected; Human review pending |
| 6 | [小さな開口](expressions/06-small-mouth-open.png) | AI selected; Human review pending |
| 7 | [閉眼笑顔](expressions/07-closed-eye-smile.png) | AI selected; Human review pending |
| 8 | [小さな驚き](expressions/08-tiny-surprise.png) | AI selected; Human review pending |
| 9 | [低い休息・正面](poses/09-low-rest-front.png) | AI selected; Human review pending |
| 10 | [低い休息・側面](poses/10-low-rest-side.png) | AI selected; Human review pending |
| 11 | [片手差し出し・3/4](poses/11-one-paw-offer-three-quarter.png) | AI selected; Human review pending |
| 12 | [両手保持・正面](poses/12-two-paw-hold-front.png) | AI selected; Human review pending |
| 13 | [首かしげ・3/4](poses/13-head-tilt-three-quarter.png) | AI selected; Human review pending |
| 14 | [頬の局所圧縮・正面](poses/14-cheek-pressure-front.png) | AI selected; Human review pending |
| 15 | [セルフグルーミング・3/4](extended/15-self-groom-three-quarter.png) | AI selected; Human review pending |
| 16 | [食べ物への期待・3/4](extended/16-food-anticipation-three-quarter.png) | AI selected; Human review pending |

| 17 | [座位・正面ニュートラル](additional/17-seated-neutral-front.png) | AI selected; Human review pending |

| 18 | [顔・左向きニュートラル](additional/18-face-neutral-left-profile.png) | Human-provided revised reference; Human review pending |
| 19 | [顔・左向き小さな開口](additional/19-face-small-mouth-open-left-profile.png) | Human-provided revised reference; Human review pending |
| 20 | [顔・左向き閉眼](additional/20-face-closed-eyes-left-profile.png) | Human-provided revised reference; Human review pending |
| 21 | [顔・正面3/4ニュートラル](additional/21-face-neutral-front-three-quarter.png) | Human-provided revised reference; Human review pending |
| 22 | [顔・正面3/4閉眼笑顔](additional/22-face-closed-eye-smile-front-three-quarter.png) | Human-provided revised reference; Human review pending |
| 23 | [座位・左向き](additional/23-seated-left-profile.png) | Human-provided revised reference; Human review pending |
| 24 | [座位・正面3/4](additional/24-seated-front-three-quarter.png) | Human-provided revised reference; Human review pending |
| 25 | [座位・後方3/4](additional/25-seated-rear-three-quarter.png) | Human-approved camera angle |
| 26 | [立位から座位への遷移・左向き](additional/26-standing-to-seated-transition-left-profile.png) | Human-provided revised reference; Human review pending |
| 27 | — | Not installed: no verifiable latest revised source found locally |

## Selection and corrections

- Main anchors: 01 front for proportions, 02 face for identity/expression, 03 3/4 for volume; all three Human accepted.
- Expressions 04–08: retained illustrated eye identity and small-mouth language. 06 first attempt was rejected for too-large opening and regenerated with a narrow aperture.
- Poses 09–14: shallow foot-supported rest front/side, short one-paw offer, smooth mitten-paw helper-bar contact, attentive tilt and local cheek pressure. 12 first attempt was rejected for finger-like divisions; selected revision uses smooth rounded paws.
- Extended 15–16: paw-to-cheek grooming and tiny-item anticipation. 16 first attempt was rejected for digit-like lines/large opening; selected revision uses relaxed paws and a tiny floating feeding-position marker near mouth. The marker does not imply a physical levitating prop in production.
- Only selected final images are in this pack; rejected outputs remain outside it in the generator's default directory.

## Visual ambiguities for later reconstruction

These images are stylized appearance references, not measured orthographic geometry. Brushwork, framing, eye foreshortening and subtle ear/head dimensions vary. Standing anchors govern base proportions, not individual pose silhouettes. The low rest is deliberately shallow; front/side are not quantitatively calibrated to identical lowering. Head-tilt output is visibly stronger than the prompt's approximate 8-degree request; do not treat the prompt as a measured angle. Cheek compression is a localized shallow dimple, not a validated 3D indentation field. Short-paw self-contact, helper-bar clearance and feeding positions need actual 3D reach/collision/deformation tests. Nothing here establishes topology, rigging or skinning success or final geometry acceptance.


## Additional seated reference

17 was explicitly requested by Human after the 16-image pack. It depicts true rump-supported seated front, distinct from shallow feet-supported rest. Canonical central/three-toe sole pads are directly grounded in the canonical image. This adds an appearance target; actual seated 3D mechanics and any choice of standing versus seated Game Neutral remain unapproved/unproven.

## Supplemental images 18–27

Images 18–26 were copied from the locally supplied revised PNG files without pixel editing or recompression; their SHA-256 digests and byte sizes are recorded in [manifest.json](manifest.json). The user explicitly approved the camera angle of 25. Image 27 was not copied: the only local package note says its file was retained from an earlier export, and no separately verifiable latest revision or archive was found. Do not substitute an unconfirmed older image. Existing images 01–17 and the Canonical source remain unchanged.
