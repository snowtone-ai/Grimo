# Shushu v003 — Human Geometry Gate 再判定資料

**履歴資料：このページは2031076の基点を示す。現行の口・座位・まぶたの再判定は[appeal-revision](../appeal-revision/REVIEW.md)を参照。**

2026-10-13。**Human Geometry Gate PENDING / Tripo HOLD**。`93869a8771045d7ed79ab036bd61d66ed97bd437`の保存済みv003を局所編集した続き。再制作・Donorの再生成ではない。

## 今回の比較

| 内容 | Clay | 簡易カラー |
| --- | --- | --- |
| Donor / 変更前 / サイズのみ / 周囲のみ / 採用した併用案 | [目の比較](01-eyes-clay.png) | [目・ピンク模様を分けた診断](01-eyes-colour.png) |
| Neutral → 小開口 → Donor相当の大開口 → 開口笑顔 | [口の比較](02-mouth-clay.png) | [口のカラー診断](02-mouth-colour.png) |
| 立位 → 25 / 50 / 75% → 座位 | [遷移比較](03-seat-clay.png) | [座位カラー診断](03-seat-colour.png) |
| 半閉眼 / 閉眼 / 片側制御 | [まばたき](04-blink-clay.png) | [まばたきカラー診断](04-blink-colour.png) |
| 太もも〜臀部の局所修正前後 | [座位の前後比較](05-seat-before-after.png) | 上記座位カラー参照 |

全ボードは正面・厳密な側面・3/4を併記。各用途内でカメラ方向、注視点、正投影スケール、解像度480×540、Cycles 12 samples、照明・背景を共有する。[カメラ記録](cameras.json)、[108レンダー/10ボードのhashと同一カメラ検証](review-manifest.json)、[未加工レンダー](renders/)を保存。[一覧画像](00-overview.png)からも確認できる。ボード化は縮小・配置・ラベルだけ。簡易カラーは一時的な材質/頂点色であり、承認テクスチャ・眼のハイライト・最終注視表現ではない。Donorにも同じ仮のピンク目元マスクを適用し、ピンク領域を眼球面と混同しない。

## 目：何が大きく、何を戻したか

同一正投影の最前面ray hitで、**実際に見える眼球面**を眼窩に隠れた部分から分けた。ピンク模様は計測に含めない。サンプル間隔は横0.000633、縦0.000647 scene unit。Shushu全高は約1 unit。

| 片眼の正面投影 | 元Donor | 修正前v003 | 修正後v003 |
| --- | ---: | ---: | ---: |
| 見える眼球面：幅 | 0.096267 | 0.109567（+13.8%） | 0.096267 |
| 見える眼球面：高さ | 0.104824 | 0.132647（+26.5%） | 0.104824 |
| 見える面積（左眼） | 0.007896 | 0.011292 | 0.007862 |

左右は同じ幅・高さ。修正後はこの計測格子の精度内でDonorの見える寸法へ戻る。これは旧「眼球全体が20〜30%拡大」推定の再採用ではない。Donorの眼球部品全体は幅0.12256 / 0.12305、高さ0.14404。修正前v003の前面capは幅0.10906、高さ0.13198で、既に部品全体より小さい。**部品の総寸法と、眼窩から見える寸法は別。**

採用案は、既存の閉じた眼球volume・局所lid・inner wall・半閉眼補正・独立まばたき/視線・頭姿勢合成を維持し、眼球面と開口部の横/縦をそれぞれ0.8786 / 0.7902倍にした上で、中間のまぶた環だけを最大0.0025 unit内側へ滑らかになじませる併用案。開口の内縁と外側境界に環の補正は加えない。

- **サイズのみ:** 見える寸法をDonorへ戻せる。構造・制御を保持する有力案で、採用案の軸。
- **周囲のみ:** 縁の張り出しは軽減するが、眼球面の寸法差は残る。単独では今回の指摘を十分に解消しない。
- **併用:** Donor寸法を保ちつつ環の張り出しを局所的に緩和。正面・側面・3/4で確認し、まばたき回帰も通ったため制作候補として採用。可愛さの承認はHumanに残す。

眼球の幾何学的中心±0.129 / z0.660は維持した。Donorの見える輪郭中心±0.13443 / z0.66065に完全な位置一致を主張しない。元FBX/GLBにはピンク模様が符号化されていないため、その3D実寸のDonor差は**UNKNOWN**。仮マスクを眼球として測定しない。[前計測](eye-measurements-before.json)、[後計測](eye-measurements-after.json)、[分離した眼球cap・lid内縁・眼窩編集範囲・仮ピンク範囲の3方向投影](focused-revision-checks.json)を参照。

## 座位：付け根の段差を局所修正

左右の既存Seat025/050/075/100だけを編集。元立位でz0.095以下の足部は完全に不変。上側の太ももを座位のpelvisへ局所的に寄せ、近位の径を緩やかに減らして段差をなじませた。立位Basis・胴体・足裏・接触制御を変更せず、元の隣接Seatサンプルのcrossfadeを維持。最大変位は約0.0408 unit、影響は左右それぞれ1073 / 1080頂点。足部の最大変位は0。

側面に出ていた太ももの水平な棚状の張り出しが軽減し、臀部へのつながりが滑らかになる。独立した身体/脚moduleの重なりは残る。単一watertight meshや全姿勢の無干渉を主張しない。最終的な柔らかさ・重み・可愛さはボードでHuman再判定する。

## 口：小開口を保ち、大開口を追加

既存MouthOpen / GentleSmile / Surpriseは保持。保存済み口の変形差分から環の位置を復元し、頭を切り直さず**MouthDonorOpen**を追加した。既存頭姿勢に追従する合成補正も追加。口の縁と内部bowlが同じ目標輪郭に従う。

| 制御状態 | 縁の幅 | 縁の高さ |
| --- | ---: | ---: |
| Neutral | 0.0520 | 0.00487 |
| 小開口：MouthOpen=1 | 0.0520 | 0.02011 |
| 大開口：MouthDonorOpen=1 | 0.0680 | 0.05325 |
| 開口笑顔：MouthDonorOpen=0.65 + GentleSmile=1 | 0.0624 | 0.03579 |

Donorの深い口腔の近似投影は約0.071×0.052。これは外側muzzleの二次曲面継続からの奥行き差を使ったproxyで、厳密なlip分割ではなく上中央のcleftも含む。採用大開口はこの規模を満たす比較候補。寸法だけでDonor/Canonical相当の可愛さをPASSにしない。

Neutral→小開口は既存MouthOpenで制御。小開口→大開口はMouthOpen=1-t / MouthDonorOpen=tでcrossfadeし、両方を最大値で加算しない。大開口→笑顔は大開口量を0.65へ落としGentleSmileを1へ上げる。既存285フレームproofはそのまま保持し、新規大開口は独立した編集制御・今回の静止比較・組合せsweepで示す。最終Motion演技ではない。

## 再検証と保護

- [保存ファイルチェック](../saved-artifact-checks.json)：再読込、Neutral復帰10地点、元Donorのhash、既存release/prop非表示、斜めまばたき回帰（upright/rest、7左右対称+2左右非対称）。
- [Geometryチェック](../geometry-checks.json)：41段階座位支持、閉眼眼球cap遮蔽、局所self-contact、Neutral reset。
- [対象修正チェック](focused-revision-checks.json)：既存Shape Key名とdriver式を維持。立位の腿/胴/足/耳/腕Basisが完全不変。口のNeutral→full / small→full各9段階をuprightとseat+tiltで、smile/左右別blinkを併用して検証。計36組×96本の口面rayにrear/missing hitなし。有限座標も確認。
- [hold contact](../hold-contact.json)：既存propの両手gap各0.0001以内、胴体clearance>0.002。
- [Static往復](../static-roundtrip.json)：11 meshes / 123,270 triangles。FBX最大surface error約1.61e-7、GLBは記録上0。局所interchangeのPASSに限定。
- [保護入力hash](preserved-inputs.json)：ユーザー変更のv002 PNG、ルート参照、01–26参照packを保持。元Donor・Canonical・承認済み4方向も再hash確認。#27の承認状態はUNKNOWNのまま。

編集元・proof・静的FBX/GLBの現行hashは保存ファイルチェックに記録。中立Geometryの材質はClayのまま。簡易カラーは保存資産へ入れない。**Human Gate PENDING、Tripo HOLD、追加課金なし。** 最終Rig・Motion・スマホruntimeはこの作業の範囲外。

## 再現

Blender 5.2のbackgroundで`--python-exit-code 1 --python scripts/blender/revise-shushu-geometry-v003.py -- --measure / --trials / --apply / --render`を各段階で実行する。`--apply`は保存モデルを編集し、builderの全面再構築は呼ばない。開始revisionの保存済みモデルをGit/LFSから`.git/shushu-v003-pre-gate`へ解決し、上書き前に現行モデルhashを確認する。未記録のモデル変更があれば停止する。

保存検証は既存`verify-shushu-geometry-v003.py`と追加`verify-shushu-v003-revision.py`。Python/Pillowの`board-shushu-v003-human-gate.py`でボードを作る。旧v003 builderと旧reviewボード/GIFは変更前工程の履歴として残し、現行再判定はこのページの資料を使う。
