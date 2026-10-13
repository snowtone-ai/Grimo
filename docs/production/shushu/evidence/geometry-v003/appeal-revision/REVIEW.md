# Shushu v003 — 口・座位・まぶたの再判定候補

2026-10-14。**Human=PENDING / Tripo=HOLD**。`2031076828185dd714cf9aca8438c289942986fd`の保存済みv003を継続編集した。Canonical、元Donor、承認参照、ユーザー差分は保護。Humanの可愛さ・安心感・本人らしさの承認を代行しない。

## 比較を見る

[一覧](00-overview.png)から、以下の原寸レンダーとボードへ進める。

| 対象 | Clay | 診断カラー |
| --- | --- | --- |
| 閉口 → 小開口 → 大開口 → 笑顔 | [口](01-mouth-clay.png) | [口](01-mouth-colour.png) |
| 立位 → 25 / 50 / 75% → 着座 | [座位](02-seat-clay.png) | [座位](02-seat-colour.png) |
| 半閉・閉眼・閉眼笑顔・片眼 | [まぶた](03-lids-clay.png) | [まぶた](03-lids-colour.png) |
| 基点2031076との同条件比較 | [修正前後](04-before-after-clay.png) | [修正前後](04-before-after-colour.png) |
| 元Donorと大開口・笑顔 | [Donor比較](05-donor-clay.png) | [Donor比較](05-donor-colour.png) |

[着座＋笑顔＋軽い頭傾げの全身比較](06-companion.png)も併記。[Canonical・4方向・承認済み#18–26](10-authorities.png)は元画像を縮小配置した参照であり、Blenderの同一カメラで再撮影したものではない。#27は未承認で、採用根拠に使わない。

3D比較は正面・厳密側面・3Qでカメラ、照明、背景、解像度480×540、Cycles 12 samplesを固定。顔は正投影scale .54、全身は1.15。[未加工レンダー](renders/)、[カメラ記録](cameras.json)、[カメラ照合・画像hash](review-manifest.json)を保存した。ボードの画像操作は縮小・配置・ラベルのみ。

カラーは形と部位を読むための一時材質。眼球、上まぶたの縁、ピンク目元、口腔、舌を区別する。目の輝き・毛並み・花・肉球・最終テクスチャを再現した完成外観ではない。新外皮のピンク領域は、その姿勢の脚/胴の編集元への距離から作る診断マスクで、承認済み配色の確定ではない。保存したGeometry/静的FBX/GLBへ診断材質を焼き込まない。

## 何を変え、なぜ選んだか

**口。** 基点の大開口は上下に均等な楕円に近く、深い一点へ集まる口腔が丸穴の印象を強めていた。承認Front/Canonical/Donorの上唇中央と口角を残し、下へ開くU字の輪郭へ変更。口腔を浅い曲面へ作り直し、下側に追従する舌面を設けた。笑顔は口角の横広がり・持ち上げ・頬の小さな連動を伴う。Clayでも輪郭と口内面を確認し、カラーだけで穴を隠していない。

| 状態 | 操作 | 縁の幅×高さ（scene unit） |
| --- | --- | --- |
| 閉口 | 全て0 | .0520 × .00487 |
| 小開口 | MouthOpen=1 | .0560 × .0150 |
| 大開口 | MouthDonorOpen=1 | .0750 × .0580 |
| 開口笑顔 | MouthDonorOpen=.8 / GentleSmile=1 / HappyLids=.45 | .0784 × .04977 |

元Donorの口腔proxyは前回約.071×.052。今回の大開口はこの規模を保ちながら輪郭を表情に寄せた候補で、数値一致を可愛さの根拠にしない。小→大は`MouthOpen=1-t / MouthDonorOpen=t`、大→笑顔は`MouthDonorOpen=1-.2t / GentleSmile=t`で遷移。旧の口制御名と頭姿勢合成driverを維持。口内だけは65頂点の円錐状面から450頂点の曲面＋舌面へ変更した。

**座位。** 腿だけの平滑化・付け根移動では、独立した部品の交差境界が残り、一部ではさらに目立った。このため局所移動の反復を止め、腿の中心線・断面を整えた編集元から、胴・左右脚を一続きの外皮として評価する方式へ切り替えた。側面の棚と3Qの鋭い付け根が緩和され、足から臀部へのつながりを作れた。

胴・脚の元メッシュ、座位キー、Breath、元のproofを保持し、Torso上の非破壊modifierで結合・voxel評価・平滑化する。脚は外皮の入力として残し、二重に描画/静的exportしない。足の編集元の低い部分と立位Basisは不変だが、**描画される外皮は立位も含めて平滑化される**。元と完全同一表面とは言わない。全姿勢の評価トポロジーは固定ではないため、最終ゲームRig/morph資産としてそのまま完成したとは扱わない。

**まぶた。** 開眼の形・眼球の寸法を保持し、閉じる線の中央を緩やかに上げ、眼球面に沿う奥行きを調整した。原寸半閉の自己点検で、基点から残る片側の帯状の折り返しを発見。内壁を無効化すると消えることを確かめ、面の法線方向の厚み付けから、開口縁を後方へ延ばす内壁へ置換した。[原因切分けの比較](07-lid-wall-diagnosis.png)。追加した左右内壁は頭の全制御とproof actionに追従し、元のSolidifyは無効な状態で残す。半閉・閉眼・片眼とHappyLidsの組合せを再確認した。

眼球の可視幅/高さは左右とも前回のDonor復元値 **.096267 × .104824** のまま。新内壁を含む最前面rayで確認し、ピンク模様を眼球として数えない。旧「全体20〜30%拡大」推定を復活させない。

## 確認済みの機能と保存成果

- [対象チェック](focused-checks.json)：全11編集元の制御名・既存driver式を照合。追加2内壁の頭制御への追従も確認。口内以外のBasis座標は基点と一致。開眼寸法、42組の口遷移/頭傾げ/座位/左右別blink、各144本の口内rayにrear/missing hitなし。視線4方向・offer・self-contact・頭回転・restも評価した。
- 生成後の外皮を21段階の座位で検証。地面に対する最下点は約.000075〜.003327。脚の支持面と外皮の距離も確認。座位の胴〜両脚は1つの連結表面で、非2面共有edgeは0。これは接地・表面の連続性の証拠であり、重みや可愛さのHuman PASSではない。
- 両手holdのgapは約±.0000161、生成外皮までのclearanceは.002764。既存接触の成立を確認。
- [HappyLids併用の斜めまばたき](happy-lid-parallax.json)、[既存Geometry回帰](../geometry-checks.json)、[保存再読込・元285フレームproof・Neutral復帰・release](../saved-artifact-checks.json)を再確認。
- [静的FBX/GLB往復](../static-roundtrip.json)：11描画mesh / 516,694 triangles。FBX最大表面誤差約1.61e-7、GLBは記録上0。2つの非描画脚は外皮へ含まれ、静的exportで二重出力しない。これはローカルinterchangeの確認に限定。
- [保存資産hash](continuity.json)、[保護入力hash](protected-inputs.json)を記録。元Donor/Canonical/4方向、承認画像、既存ユーザー変更を照合した。

## 自己点検と未達

丸穴の印象と座位の段差は基点より改善したと判断し、この版を再判定候補に選んだ。ただし**「会いたくなるほど可愛い・安心できる相棒」の達成を自己承認しない**。まぶたの内眼角に残る折れ/くぼみ、鼻〜口〜頬の小さな面のつながり、座位の足首のくびれと胴の重みは、原寸Clayと診断カラーでHuman確認が必要。半閉時の表情の柔らかさもPENDING。

外皮は高密度の評価メッシュで、姿勢により頂点数が変わる。固定トポロジーへの仕上げ、最終Rig・Motion演技・質感・スマホ実機性能は未達/未検証。全身比較もGeometryの正投影ビューであり、実際のアプリruntime・透視カメラでの確認は未実施。保存した編集用制御と285フレームproofは利用できるが、ここからそのまま完成runtimeへ移せるとの主張はしない。Tripoの実行/無料試行/課金/アップロードなし。

## Authorityと再現

実作業branchは`codex/grimo-motion-zero-based-design-20261011`。開始HEADは`2031076`。ローカルmainは古く文書が存在しなかったため、mainをfetchし、**`origin/main@d655f9606b2785ac8be7484e5f22b84dbaee9f55`**のGoal√map/Handoffを読んだ。9/25の`GRIMO_PRODUCTION_OPERATING_SYSTEM.md`、Canonical、4方向、最新Human指定の承認#18–26、元Donor、前回REVIEWと原寸レンダーを判断根拠にした。main一括merge/rebaseや製品方針変更は行っていない。

Blender 5.2で`refine-shushu-v003-appeal.py -- --apply`は基点Git/LFSモデルから現行成果を再現。現行hashが基点/直前の自分の成果と異なる場合は上書きを拒否する。`--render`、`--references`で比較、`verify-shushu-v003-appeal.py`と`-- --happy-lids`、既存`verify-shushu-geometry-v003.py`で検証。`board-shushu-v003-appeal.py`はPillowでボードを配置する。前回`human-gate-revision/`は基点の証拠として保持し、現行の判断にはこのページを使う。
