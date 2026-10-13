# Shushu v003 — Tripo Texture局所診断と口のみの保存候補

2026-10-14。実branch `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `c728772e6113ad1c5741051f493e47fba838da33`。
**Human Gate=PENDING / 外観完成判定=保留 / 両目の修正=未解決。**

ユーザーの「実際にモデル画像と比較し、不自然さなく100%可愛いと判断してから完了」を適用。数値PASSだけで完了にしていない。正面・左右3/4・左右側面を開いて確認し、Canonicalと承認済みBody-only Front/Left/Rightを参照した。口は改善したが、目の白帯・ピンク境界の意図を確定できず、両目編集は不採用。目口すべての修正や100%の可愛さを達成したとは扱わない。

## 保存成果と比較

- [承認Body-only / 元GLB / 保存候補：正面](00-authority-before-candidate.png)
- [正面・左右3/4・左右側面：同条件の前後・差分](01-five-angle-before-candidate-difference.png)
- [承認Body-only / 元GLB / 保存候補：左右側面](02-approved-sides-before-candidate.png)
- [原寸1024×1024モデル画像](renders/)、[カメラ](before-cameras.json)、[保存候補の同一カメラ](candidate-cameras.json)
- 候補：[shushu-geometry-v003-tripo-texture-candidate-v001.glb](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v001.glb)

比較モデル画像は元GLB・保存候補GLBをそれぞれ独立にBlenderへ読み込んだレンダー。画像へのレタッチなし。ボードだけ縮小・配置。正投影、Standard、base colorのEmission、Cycles 8 samples、denoiseなし。照明・影で色残りを隠さない条件。画像上の左右はカメラ方向による名称で、キャラの解剖学的左右ではない。Body-onlyは2D参照で同一カメラではなく、可愛さ・表情・色意匠の参照。全照明条件・スマホruntimeでの品質は未検証。

## 確認できた原因と止めた範囲

入力はrepo直下 `shushu-geometry-v003-tripo.glb.glb`、実LFS実体SHA256 `338ad5f8c67906917579ddbb804a4f7f51d8fec6c42328bb545adc87c1bf077b`。12メッシュ／12個別JPEG。Head 2048²、Eye_R/L各512²、MouthInterior 128²。元のアニメーション数は0。正式Blenderの285f proofとは別の静的Tripo出力。

元GLBの[Headのみ](renders/diagnostic-head-only.png)にも、中央の笑顔・舌と左右へずれた薄い笑顔・舌の形が残る。[Headを単色化](renders/diagnostic-flat-head.png)するとこの二重像は消える。したがって口の色残りはHeadへの描画自体に含まれ、独立MouthInteriorとの重なりだけが原因ではない。

目はHeadにも濃い縁があり、独立Eye・LidWallと組み合わさる。[独立モジュールのみ](renders/diagnostic-modules-only.png)も比較した。Headの濃い縁はCanonicalの本人らしさを担うため一律除去できない。残る白帯・ピンクの境界を、意図したハイライト、生成時の重複描画、表面の重なりへ完全に切り分けるには至っていない。原因を確定したと報告しない。

初回局所試作は口の大きな二重像を減らしたが、UV島の補間境界に細かな色残りが出た。[不採用の初回](rejected-trial/front.png)。UV島周辺2 texelと周囲の色合わせを追加した目口試作も、側面の目周囲の白帯について自然さに確信を持てなかったため[不採用](rejected-eye-trial/left-side.png)。**最終候補では目の編集を撤回し、口だけを保持。** 無理な輪郭除去・全体ぼかしはしていない。

## 最小変更と視覚判断

built-in image_genで正面画像の局所修正材料を作成し、[プロンプトと入力](IMAGEGEN.md)を保存。生成画像は1254²で返ったため投影計算用に1024²へ合わせた。生成画像自体をモデル完成Evidenceへ使っていない。元モデルの正面可視Head UVへ、左右の口の色残りを指定した[局所マスク](projection-masks.json)とUV島周辺2 texelだけ反映。中央の濃い笑顔・舌・鼻は維持する条件で適用した。

最終Headの変更は43,479 / 4,194,304 texel（約1.04%）。頭のJPEGをlossless PNGに変更して再圧縮による全域変化を避け、マスク外のdecoded RGBは完全同一。元BIN全体を保持し、交換PNGを末尾へ追加した。正式Rig資産への置換や昇格はしていない。

実モデルの正面・3/4・側面で、口の左右の薄い笑顔と舌の二重像が解消し、中央の小さな笑顔・舌は維持されたことを目視確認。花柄瞳・ハイライト・ピンク目囲み・チークは最終候補で元のまま。残る目の白帯・上側ピンク境界と、参照に対する立体表情の自然さには未解決の判断があるため、最終外観PASSは出さない。

## 対象別検証

[候補の構造・画素検証](candidate-validation.json)、[画像hash・比較・保護入力照合](review-manifest.json)、[開始時717保護入力](protected-inputs.json)、[元GLB調査](source-inspection.json)。

- 12メッシュ、全accessor、UV、頂点／index／法線、nodes、materials、textures、samplers、skins、animations、scene、extensionsは元JSONと一致。元BIN prefixはbyte一致。変更JSONはHead画像のmimeType/bufferViewと、追加画像bufferView・buffer長のみ。
- Eye_R/L・MouthInterior・Nose・耳・Paw・Torso等の残り11 JPEGはbyte/hash一致。Headマスク外decoded RGBの差は0。
- 同一カメラの5組でモデルを再読込。正面の画像差分は目口を囲む限定範囲外0 pixel。目を撤回した最終候補は口のみの差になる。
- 正式Blender Geometry、Shape Keys、285f Motion proof、他キャラ資産、Canonical/参照、ユーザーの既存dirty/未追跡画像を含む717入力のhash一致。全体build・全体testなし。

## 次に判定する点

Humanは保存候補の口の清潔さ、元の可愛さの維持を比較できる。**両目の二重縁は解決済みではない。** 残る帯を消してよい境界と意匠を特定する前に追加の削除を進めない。Human Gate=PENDING、Tripo外部操作／課金なし、mainマージなし。

再現：`review-shushu-tripo-texture-v003.py --inspect / --protect`、Blender 5.2.1で同スクリプト `-- --render --diagnose` / `-- --projection`、Nodeの`patch-shushu-tripo-texture-v003.cjs <保存した生成画像>`（sharp、`SHUSHU_SHARP_MODULE`でbundled path指定可）、候補GLBを`-- --render --asset <候補path>`、bundled Python/Pillowで`--boards`。正式blendを開かず隔離したbackground Blenderで実行。
