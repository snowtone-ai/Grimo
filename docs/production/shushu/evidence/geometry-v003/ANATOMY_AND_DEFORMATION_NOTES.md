# Shushu v003 — anatomy and character deformation

Research checked 2026-10-12. These are production hints, not new character authority or Human approval. Canonical identity and approved Shushu views remain the visual targets. Joint locations below are an implementation inference: the drawings do not establish a measured skeleton.

## シュシュの制作へ取り入れたこと

- **座るときは、お尻・脚・足を協調させる。** パンダの座位は前足を使える姿勢になる。犬の立ち座り研究は複数関節の協調を裏づけるが、犬の関節角度をシュシュへ移植する根拠にはしない。v003では足の向き、曲がる脚の軸、骨盤の下降を分け、お腹とお尻の輪郭も局所補正した。
- **関節が正しく動くだけでは、可愛い輪郭は保てない。** Pixarの輪郭カーブ、DreamWorksの局所的な膨らみ・絞り、Disneyの柔らかい組織の制作例を参考に、基本の動きとポーズごとの形の補正を分けた。これらの映画用ソルバーを実装したという意味ではない。
- **半目は独立した表情として作る。** 『Inside Out 2』の制作資料が示す、小さくなった目に見える問題と目尻の制御を参考にした。実際に発生した半目の隙間を、目頭・目尻を保ち、上まぶたが主に下がる補正で修正した。柔らかさや本人らしさは引き続き外観レビューの対象。
- **短い腕の接触では、頭や胴体も相手へ寄る。** これは資料からの制作上の推論。手だけを長く伸ばす代わりに頭を傾け、頬へ触れる形を検査した。両手で持つ動作には実際の検査用ボールを置き、接触と離れた状態を区別した。

既存キャラクターの具体例としては『Zootopia』のClawhauserの頬などが公開資料で確認できる。Po自身のRigについて直接の根拠は得られていないため、作品名から推測して手法を帰属させない。最終的な表情・体型の正本は、動物や映画キャラクターではなく承認済みのシュシュの参照画像。

## Findings that change the implementation

| Evidence | What it supports | Application to Shushu |
| --- | --- | --- |
| [Smithsonian: giant panda](https://www.nationalzoo.si.edu/animals/giant-panda) describes upright floor sitting that frees the forepaws for feeding. | A rump-supported seat and independently useful forepaws are plausible animal behavior. | Inspect rump contact, thighs, and free paw reach together; lowering a standing body is insufficient. |
| [Ellis, Rankin & Hutchinson, 2018](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2018.00162/full) models greyhound sit-to-stand with hip, knee and ankle motion and discusses passive tissue contributions. | Standing and sitting are coordinated changes across several joints. This is a dog study, not panda joint-angle evidence. | Separate the rotating foot from a bending leg centerline and a descending pelvis. Do not copy canine joint angles or assume a universal timing sequence. |
| [Pixar: Character Articulation through Profile Curves, 2022](https://research.pixar.com/docs/2022.SiggraphPapers.GSF.pdf), including a panda example, controls articulation through surface profile curves and reconstructs surface detail. | Artists can control the visible silhouette directly instead of asking a skeleton alone to preserve every appealing shape. | Use simple regional profile/pose corrections for seated abdomen, rump and thigh. Preserve the source head away from explicitly bounded face edits. This script is not an implementation of Pixar's solver. |
| [DreamWorks: Resculptors, 2014](https://research.dreamworks.com/wp-content/uploads/2018/07/resculptors-Edited.pdf) layers curve-based deformation on basic skinning, with localized bulge/pinch control; used on *How to Train Your Dragon 2*. | A base articulation plus local shape control is established character practice. | Keep the small-joint articulation and fleshy shape corrections separable and editable. No direct evidence about Po's rig was found; do not attribute this technique specifically to Po. |
| [Disney: Flesh, Flab, and Fascia Simulation on Zootopia, 2016](https://media.disneyanimation.com/uploads/production/publication_asset/134/asset/flesh_final_2016_04_22_10_00.pdf) combines base skinning, pose shapes, simulation and artist correction, including Clawhauser's cheeks. | Weight and soft-tissue motion need art direction as well as motion mechanics. | For this limited proof, use bounded cheek pressure and abdomen corrections. A soft-body simulation is not required to demonstrate the geometry, and no physically validated tissue simulation is claimed. |
| [Pixar: Inside Out 2 rig challenges, 2024](https://research.pixar.com/docs/2024.SiggraphTalks.HNSZ.pdf) discusses half-blink appearance and separately controllable eyelid corners. | Half-closed eyes need their own visual check; scaling an eye opening can read as a smaller eye. | Verify neutral, half, closed, unilateral blink and reopen independently; retain orbital volume and keep eye components behind the closing lids. |
| [Pixar: Sculpt Processing for Character Rigging, 2020](https://research.pixar.com/docs/2020.SiggraphTalks.GCCM.pdf) describes local corrective processing and preserving/restoring rest-surface detail. [Blender Studio Pose Shape Keys](https://studio.blender.org/tools/addons/pose_shape_keys) exposes editable posed targets. | Corrective targets can remain editable and localized. | Explicit rest-derived shape keys and separate proof targets; no dependency on the Blender Studio add-on and no broad smoothing that erases donor relief. |

## Review consequences

- Front alone cannot establish a seat. Exact side and three-quarter must show rump support, thigh-to-foot continuity, and a believable belly above the folded legs.
- Check intermediate poses. A good endpoint can still have collapsed joints, floating support, or penetrating feet during the transition.
- Foot-to-ground correction moves the entire foot support frame; it must not flatten individual vertices against an arbitrary height plane.
- Preserve the source cheek, muzzle and nose in neutral. Closed eyelid corrections are confined to the orbital patch and must not become a replacement analytic face surface.
- Bounded two-paw holding needs an actual inspection prop and a release state. A screenshot of two nearby hands is not contact evidence.
- Geometry and mathematical checks do not establish cuteness, naturalness, or Human acceptance. Record visible shortcomings and HOLD when they remain.

## Limits

The source is a stylized, very short-limbed panda-like character, not a measured animal. Internal anatomy is a working proxy. This stage does not establish final animation timing, muscle simulation, a production skeleton, or Tripo compatibility. No remote upload, credit use, texture operation or automatic rigging is authorized by this research.

## 2026-10-15 — Auto Rig Gateへの適用

既存研究を[保存GLBのDeformation Gate](../tripo-autorig-v001/REVIEW.md)へ適用した。頭→pawの誤連動、右腕→胴の引きつれ、座位途中の足貫通・腹の凹みを、観察→根拠→原因仮説→最小補修に整理。Ellisらの犬の実験/モデルは多関節と支持の協調の類推に限定し、角度/体型/荷重をShushuへ転用しない。Pixarのprofile制御は局所輪郭correctiveの根拠として再利用。総volume維持を可愛い輪郭のPASSにしない。

不足していた通常skinの関節縮みとweight所有の説明だけ、[Blender公式 Armature Modifier](https://docs.blender.org/manual/en/4.4/modeling/modifiers/deform/armature.html)およびbundled `manual/modeling/modifiers/deform/armature.rst`で追加確認。Preserve Volumeのquaternion方式は縮みを改善し得るが、誤所有・接地を直す根拠ではなく、GLB/runtimeへの同等受渡しも未検証。今回方式変更・形状補修は行わず、骨階層を補修の出発点として条件付き採用、現状Rig正式採用HOLD。押圧/臀支持/物理COMは未達・UNKNOWNを保持する。
