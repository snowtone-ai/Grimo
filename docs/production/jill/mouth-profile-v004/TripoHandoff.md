# Jill v004 — Texture phase input

2026-10-16。最新Human指定は「赤線の口〜顎だけ直し、他視点の可愛さを保ってTextureフェーズへ」。v004でその局所修正を実装。Human最終visual GOを自動取得したとは扱わない。Tripo upload/課金/正式Textureは未実施、実UI/料金/Original UV/実返却はUNKNOWN。

入力は [v004 neutral FBXまたはGLB](../../../../assets/grimo/production/jill/tripo/mouth-profile-v004/README.md)。旧v003入力には戻さない。clay・UV0のみで、診断Texture/rig/animationを含まない。SHAと絶対パスは [Manifest](Manifest.json)。

- Rig blend `df3891bbd11c522631202e0dd32945a788ff370477731568514261a5e4100cb7`
- neutral FBX `c9442eec2d30f20409c27f82e5b1f3cb0769cb7c394c9e8b96bebb9d52d553f4`
- neutral GLB `4646cffdff8248e6e74b1dcd5f1c6095e7ed7af2b7ad7771001c9b22aa662eb2`

配色・Canonical/Body-only・桃色horn・左右クローバー・4K基準は [v003 TextureSpec](../rig-pretexture-technical-v003/TextureSpec.md) を継承。UV0/1/2の名前と全loop値も同じ。今回の口周囲の元肌を閉口時に後退させないため、返却画像には追加の [host肌mask](mouth-host-fill-mask.json) を適用し、`sanitize-jill-mouth-return-v004.py` を使用する。`mouth-host-skin` は承認済みの `mouth-skin` と同じRGBを明示する。診断用paletteを流用しない。入力/返却のhidden口内・舌裏・翼裏・葉根は引き続き部位maskで補完・実render確認する。

Original UV不可/不明なら停止。返却Geometry/bones/weights/Morph/anchorsでRigを上書きしない。UV一致はowner/position/UV cornerの双方向照合後、画像だけを別名Rigへ割当てる。UVが変わった場合は同Geometry・同三角形対応・owner一意を確認した場合だけ別画像へ転写。remesh/異なる三角形化/変形/owner欠落/曖昧対応では停止する。Normal/tangentをそのまま流用しない。詳細は [v003停止条件](../rig-pretexture-technical-v003/TripoHandoff.md) を継承するが、比較対象Geometryは必ずv004とする。

返却後は保存再読込、UV0明示、口のclose .5/1/open 1/復帰、front/左右side/3Q、肌への開口印刷なしを確認する。元Rigの130骨/39ch/20 Morph/16 anchorを保持。今回の合成FBX/GLB証明は [Evidence](Evidence.md) にあり、実Tripo返却の成功を保証しない。追加の造形変更を進めず、修正版の見た目と実TextureをHumanが判定する。
