# Shushu v003 — 鼻先〜鼻下のHuman再判定候補

**履歴:** 最新Humanが提示した側面鼻への候補は [nose-reference-revision](../nose-reference-revision/REVIEW.md)。以下は `530f75c` 時点の奥行き修正の比較として保持する。Human=PENDING / Tripo=HOLD。

2026-10-14。**Human=PENDING / Tripo=HOLD**。実作業branch `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `6f4822362aaec9e795023f08349d4bb14c5188e0`。保存済みappeal revisionを継続編集した。鼻先〜鼻下の局所奥行きだけを変更し、最終Rig・高密度外皮の方式は今回の対象に含めていない。

## Humanが比較する画像

| 対象 | 修正前 → 修正後 |
| --- | --- |
| 閉口・Front / Side / 3Qの実形状 | [Clay比較](00-nose-clay.png) |
| 同じ鼻の色領域で奥行きを比較 | [診断カラー](01-nose-colour.png) |
| 開口笑顔・Front / Side / 3Q | [笑顔Clay](02-smile-clay.png) |
| 指摘された06-companionと同じ着座・頭傾げ・表情 | [全身の診断カラー](03-companion-colour.png) |
| 小開口・大開口の退行確認 | [3Q比較](04-open-mouth-check.png) |

各ボードの上段が修正前、下段が修正後。小/大開口ボードは左が前、右が後。[原寸480×540レンダー](renders/)と[カメラ・hash照合](review-manifest.json)を保存。新候補14視点、旧画像11視点を再利用、旧モデル3視点を再撮影した。画像の操作は縮小・配置・ラベルだけ。

Front / 3Qと全身は前回のカメラを保持。**顔Sideだけは旧カメラで鼻先が左端に切れるため、前後ともtarget Yを−.040から−.058へ移した**。正投影scale .54、照明、解像度、Cycles 12 samplesは同一。全身はscale 1.15。[カメラ記録](cameras.json)に全14組を記録し、各前後で完全一致を確認した。

Canonical Identity、4方向、Human承認#18–26は[前回の参照一覧](../appeal-revision/10-authorities.png)を使用。元2D参照は同一3Dカメラでの再撮影ではない。#27は未承認で採用根拠にしない。カラーの鼻領域は旧モデルの頂点領域を維持し、後退した鼻が旧Y閾値から外れて消えないよう診断時だけ扱った。色や画像で尖りを隠す処理はしていない。保存モデル・静的exportの材質はClayのまま。

## 原因と採用した修正

原寸Side / 3Qと[局所断面](diagnosis.json)から、元形状を継承した鼻先の長い前方突起と、鼻下の前向きの稜線が印象を硬くしていると判断した。最初の奥行き修正では鼻下の角が残ったため、鼻下から上唇への奥行きも緩やかにつないだ。

Headの局所に滑らかな減衰を持つ奥行き場を適用し、小さな丸い鼻のふくらみと浅い鼻下へ変更。範囲は元Basisで `|X|<.046 / .602<Z<.667 / Y<−.235`。11,299頭頂点のうち1,821頂点を変更し、最大奥行き移動は.018305 scene unit。**X/Z、面構成、口の開口境界128頂点は不変**。表情・Seat・correctiveへ同じBasis差分を加え、Headの回転・傾げ・rest合成だけを更新した。

| 同じX=0の前面rayによる比較 | 前 | 後 |
| --- | --- | --- |
| 鼻の最前面（Z=.626–.650、.002刻み） | Y=−.291247 | Y=−.278841 |
| 鼻下（Z=.618） | Y=−.278636 | Y=−.269999 |

鼻の最前面は約.012406後退、鼻下の該当断面は約.008637後退した。顔の平面化を目的にせず、小さなふくらみを残した。これは同条件の寸法差であり、Canonicalへの厳密な寸法一致や可愛さのPASSではない。

## 対象別の保存成果検証

- [保存再読込と退行チェック](targeted-checks.json)：asset / proof双方で全13編集対象＋元Donorの構造を比較。制御名、driver/参照、modifier、頂点weight、面・edge、全Action曲線は同一。Head以外の全shape座標はbyte単位で同一。Headは変更域外を確認し、口境界の全キー最大差は0。既存の相対変形差は1e-7未満。
- 口・閉眼笑顔・半閉・着座＋頭傾げの7組で各72本の口内rayを確認し、rear/missing hitは0。小開口/大開口では反対側の頭傾げ、閉眼笑顔では中間座位と頭回転を併用。小/大/笑顔の原寸画像も自己点検した。
- 285フレームproofの曲線を維持。Neutralへ戻る代表frame 1 / 83 / 189 / 249 / 285で全対象の評価表面差0。release移動.122577、復帰後のprop非表示も確認。目・まぶた・胴/脚外皮・視線・支持・接触は形状/制御/Actionを変更していない。以前の全件検証を繰り返していない。
- [局所表面チェック](surface-checks.json)：新規collapse 0、前面投影の表裏反転0、評価後X/Z差0。断面を平滑化したため旧面と90°以上法線方向が変わる三角形150は存在するが、これは旧法線との角度比較。新しい面反転の判定と混同せず、固定の三角分割・投影方向・面積で別に確認した。
- [静的FBX/GLB往復](static-roundtrip.json)：11描画mesh、516,694 trianglesを維持。FBX最大誤差約1.61e-7、GLB記録上0。保存資産の[前後hash](continuity.json)、元Donor/Canonical/承認資料/ユーザー差分を含む[保護入力56ファイル](protected-inputs.json)も照合。元FBX/GLBはintake manifestのhashとも一致。

## 自己点検・Human判定の未達

Clay、診断カラー、着座全身のFront / Side / 3Qで、長い鼻先と鼻下の鋭さは改善したと判断し、再判定候補として保存した。正面の顔幅・鼻の位置・口の開口は維持。鼻下の横方向の口周辺境界は薄く残り、診断色の鼻領域にも既存の粗い色境界がある。最終質感・鼻色の仕上げや毛並みでの完成外観は今回の成果に含めない。

**Humanによる「Canonicalらしい小ささ・丸さ・柔らかさ」「開口笑顔の本人らしさ・安心感」の再判定は未受領。Human=PENDINGを維持する。** 前回から残るまぶた内眼角、半閉の柔らかさ、座位の重み、最終Rig/スマホruntimeの未達をこの局所修正で解決したとは扱わない。Tripo実行・upload・無料試行・課金なし。

## Authority・再現

最新Humanの鼻先/鼻下への指摘、Canonical/承認資料、ローカルAGENTS、Goal√map、Handoff、9/25 Production Operating Systemを参照。mainの参照revisionは前回検証済み `d655f9606b2785ac8be7484e5f22b84dbaee9f55`。Goal変更・main一括統合なし。

Blender 5.2.1で `refine-shushu-v003-muzzle.py -- --apply` は保存した開始モデルから局所修正を再現する。開始モデル/直前の自分の成果以外のhashは上書きを拒否。バックアップは `.git/shushu-v003-muzzle-6f48223/`。`--render`の後に`--side-margin`で上記の鼻先が切れないSide比較を生成。`verify-shushu-v003-muzzle.py`、`-- --surface-only`、`board-shushu-v003-muzzle.py`で検証と配置を再現する。先行のappeal revision / human-gate revisionは当時の比較履歴として保持。
