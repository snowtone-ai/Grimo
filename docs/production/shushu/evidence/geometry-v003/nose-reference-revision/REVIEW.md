# Shushu v003 — Human指定の丸い鼻への再判定候補


**後続修正:** 開口した下側口縁〜顎のみを修正した[最新保存候補](../lower-mouth-revision/REVIEW.md)を参照。この鼻比較はb92aa76時点の履歴。鼻自体は後続で変更していない。
2026-10-14。**Human=PENDING / Tripo=HOLD**。開始HEAD `530f75c4cc7e4fbc06545c420b337155e67c8212`、実作業branch `codex/grimo-motion-zero-based-design-20261011`。保存済みv003を継続編集した。

最新Human指示「鼻はこんなふうになる。これにぴったりにして。」とスクリーンショット(525)を鼻の基準とした。画面に表示された承認済み `shushu_bodyonly_left.png`、同じ4方向のFront、Canonical Identityを参照。承認#18–26と元Donorは保護し、未承認#27は採用根拠にしていない。[参照hash](authority.json)。

## Humanが見る最小比較

| 比較 | Evidence |
| --- | --- |
| 提示画像と同じ承認済みFront / Leftの鼻口元 → 保存候補 | [参照比較](00-reference-match.png) |
| 閉口・Front / Side / 3Qの形状、前 → 後 | [Clay](01-clay-before-after.png) |
| 開口笑顔・Front / Side / 3Q、前 → 後 | [診断カラー](02-colour-before-after.png) |
| 小開口 / 大開口・3Q、前 → 後 | [開口確認](03-open-regression.png) |

同条件の前後8組、合計16枚。[640×640原寸](renders/)、[カメラ](cameras.json)、[画像hash・比較ペア](review-manifest.json)。正投影scale .36、Cycles 16 samples、照明は各前後で同一。鼻が十分に見える拡大カメラであり、以前の全身カメラとのpixel比較はしない。参照画像は切り抜き・縮小・配置だけ。3Dレンダーのレタッチ・変形はない。

**2D参照には校正済み3Dカメラがないため、参照と候補の完全なpixel一致を証明したとは扱わない。** 前後の3D比較はカメラが完全一致。鼻の輪郭・厚み・口元へのつながりをHumanが再判定できる資料として提示する。

## 原因と採用方式

前候補は鼻先の奥行きを減らしたが、元Headの不規則な表面と粗い鼻色領域を残した。拡大確認では、色の輪郭にも細かな凹凸が現れた。既存面に丸い奥行き場を付ける試作も同じ問題を残したため、表現方式を変更した。

鼻先だけを小さな滑らかな独立曲面 `Shushu_Nose` にし、上が広く下が丸い輪郭、柔らかい側面の厚み、鼻下の短い線を作った。Headではその下の不規則なふくらみを滑らかな面へ変更。既存Headの頂点・面構成、X/Z、口の開口境界は維持している。上側の減衰を短くし、額の輪郭へ新たな張り出しを加えないよう調整した。

| 保存した局所形状 | 値 |
| --- | --- |
| 鼻先のsource幅 / 高さ | .036203 / .019000 scene unit |
| 鼻先のsource Z範囲 | .626500–.645500 |
| 鼻先のsource Y範囲 | −.286233–−.261767 |
| 新しい鼻のsource頂点 | 858（鼻先722＋鼻下136） |
| Head変更域 | 元Basisで `|X|<.046 / .602<Z<.650 / Y<−.235` |
| Head最大奥行き変更 | .012809 scene unit |

丸い鼻の厚みを表現するため、鼻先は前候補の平らな鼻より少し前へ出ている。参照の小さな鼻の幅・高さと丸い側面を優先し、細長い尖りを残さない形にした。上記は保存形状の寸法であり、可愛さPASSや参照との寸法完全一致ではない。

新しい鼻に新規操作コントロールは追加していない。既存Headの全70キー、driver、Action/slotを共有し、Head表面の三角形へ相対変形を追従させた。頭回転・傾げ・restの合成は鼻自身の奥行きも回転するよう生成した。鼻下も既存の開口・笑顔に追従する。旧メッシュや編集用の口・目・まぶた・座位機構を置換していない。

## 保存成果・対象別の検証

[targeted-checks.json](targeted-checks.json) はasset / proofを保存後に再読込して確認した。

- 元の全対象＋Donorの構造、driver、modifier、weight、全Action曲線は同一。追加は鼻1object。Head以外の既存対象の全shape座標はbyte単位で同一。Headの変更域外とX/Zを保持し、通常の相対変形差は1e-7未満。口境界128頂点の全キー差は0。
- 鼻はHeadと同じキー/driver/Actionを持つ。三角形への追従と姿勢合成を保存座標から照合。鼻先・鼻下の閉じた面のedge使用数は全て2、新規collapseは0。Headも新規collapse / 前面投影の表裏反転0。
- Neutral、小開口、大開口、笑顔、閉眼笑顔、半閉、着座＋頭傾げで鼻の評価表面は有限。鼻の参照点とHead評価面の距離は約6.13e-5以下。小/大開口には逆側の頭傾げ、閉眼笑顔には中間座位と頭回転を併用。各72本の口内rayにrear/missing hitなし。
- 285フレームproofの代表Neutral復帰1 / 83 / 189 / 249 / 285で、新しい鼻を含む全対象の評価表面差0。release移動.122577、復帰後のprop非表示を確認。既存の支持・接触・視線の形状/制御/曲線を保持。不要な全件テストを繰り返していない。
- [静的FBX/GLB往復](static-roundtrip.json)：鼻追加後12描画mesh、523,702 triangles。FBX最大表面誤差約1.61e-7、GLB記録上0。非描画の元脚を二重exportしない。静的出力はClay・材質なしで、診断色は最終textureではない。
- [保護入力56ファイル](protected-inputs.json)のhashを照合。Canonical・承認資料・元Donor・ユーザー差分は保持。[asset/proof前後hash](continuity.json)。

## 自己点検と未達

正面の四角い鼻色と輪郭の凹凸は、滑らかな上広・下丸の鼻へ改善した。Side / 3Qで丸い厚みと鼻下への連続を確認し、閉・小・大・笑顔の開口を保持した。元の口周辺の横方向の境界は残る。最終質感・毛並み、まぶた内眼角/半閉、座位の重み、最終Rig/スマホruntimeは今回の対象外で、完成とは扱わない。

**提示画像に対する鼻の小ささ・丸さ・本人らしさ・安心感のHuman再判定は未受領。Human=PENDING。Tripo=HOLD。** Tripo実行、upload、試行、課金、main一括統合なし。

## Authority・再現

最新Human、Canonical/承認済み4方向、ローカルAGENTS、Goal√map、Handoff、9/25 Production Operating Systemを適用。remote mainは `d655f9606b2785ac8be7484e5f22b84dbaee9f55` と照合済み。Goal変更なし。

Blender 5.2.1：`refine-shushu-v003-reference-nose.py -- --apply` で開始時の保存モデルから局所変更を再現。開始hash/直前の自分の成果以外は上書きを拒否。開始資産は `.git/shushu-v003-reference-nose-530f75c/` に保持。`-- --render`、`verify-shushu-v003-reference-nose.py`、`board-shushu-v003-reference-nose.py` で画像・検証・ボードを再現する。先行Evidenceは当時の履歴として保持。
