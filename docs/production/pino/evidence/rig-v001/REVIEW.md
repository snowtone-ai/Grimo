# Pino C — Tripo基礎Rig v001 / Humanレビュー

**入力受入・保存: 完了。Human Rig/Geometry Gate: PENDING。制作採用: HOLD。**

新しいTripo Mixamo FBXを、既存Geometry Masterとは別の基礎Rig入力として保全した。Neutralを保つ編集候補と4系統の実変形を作成したが、**自然な閉眼・両前肢接触・深い低休息は未成立**。4試験合格や、Canonicalの見た目のHuman承認を宣言しない。

## 最初に見る資料

- [元GLB外観基準と候補のNeutral・同条件3視点](neutral-comparison.png)。上段が元GLB、下段がRig候補。Cycles、512px、16 samples。
- [尾 GIF](tail.gif) / [代表姿勢](tail-representatives.png)
- [左右閉眼 GIF](eyes.gif) / [代表姿勢](eyes-representatives.png)
- [左右High-five・両前肢接近 GIF](paws.gif) / [代表姿勢](paws-representatives.png)
- [浅い荷重姿勢→立位復帰 GIF](rest.gif) / [代表姿勢](rest-representatives.png)
- [Canonical・承認Body-onlyと未承認Motion参照の区別](../geometry-c-v001/appearance-authority-context.png)。Motion参照34枚は[Human PENDING](../../../../../assets/grimo/production/pino/references/REVIEW.md)。数値と立位一致を、参照姿勢の可愛さの代用にしない。

GIFは正面・側面・3/4を一つにまとめた4本だけ。計40姿勢を描画し、一時フレームは各系統の組み立て後に削除した。最終Motionではなく、変形能力と不成立域を確認する診断。

## 資産と読み込み

制作ブランチ: `codex/pino-base-rig-v001-20261015`。開始はGitHubのPino Geometry branch `81432f9`。`origin/main@8e4996c`のAppearance lockを継承し、最新fetchで照合した。作業元のShushu等のユーザー差分は別checkoutに残した。

| 資産 | 役割 |
|---|---|
| [新FBX原本](../../../../../assets/grimo/production/pino/candidate-c/rig-v001/input/pino-c-tripo-mixamo-original.fbx) | 追加された `tripo_convert_e41db652-3438-43d9-b501-1000972256cf.fbx` のバイト同一コピー。上書きなし |
| [無編集import .blend](../../../../../assets/grimo/production/pino/candidate-c/rig-v001/pino-c-tripo-import-unaltered.blend) | 骨・Skin・変換を読み込んだ直後。補修なし |
| [基礎Rig候補 .blend](../../../../../assets/grimo/production/pino/candidate-c/rig-v001/pino-c-base-rig-v001.blend) | Neutral保存、70骨、左右閉眼Shape Key、IK目標。Human未承認 |
| [再生用 .blend](../../../../../assets/grimo/production/pino/candidate-c/rig-v001/pino-c-base-rig-v001-proof.blend) | 1–235f / 24fps。尾1f、眼55f、前肢109f、浅い荷重187f。失敗した接触試行も含む診断専用 |

入力は18,858頂点、21,099ポリゴン、65骨、最大4ウェイト。尾専用骨・Morph・UVは0、未割当は入力番号15212の1頂点。[全骨階層・rest/pose行列・集計](input-and-build.json)、[入力全ウェイト](input-skin.npz)。

新FBXは元Cから**頂点番号が並べ替えられている**。番号順の転送は行わず、最近傍座標と各頂点に接続する全ポリゴンの署名から、重複候補0の全単射を作成した。ポリゴンの位置署名は全数一致し、対応後の最大座標差は `1.9443e-7`。[対応表](input-to-master-map.npz)。既存65骨のrest行列差は0、親子関係を保持した。

既存[Geometry Master FBX](../../../../../assets/grimo/production/pino/candidate-c/source/cute%20blue%20creature%203d%20model.fbx)と[元GLB外観基準](../../../../../assets/grimo/production/pino/candidate-c/source/cute%20blue%20creature%203d%20model.glb)は不変。[geometry-c-v001](../geometry-c-v001/REVIEW.md)で定めた通り、Master由来頂点に元GLBの三角形化・corner法線・材質を保つ出力規則を使った。Rig側の並べ替え番号に合わせてGeometryを再構築していない。

## 採用候補に加えた変更

- 尾: Hipsの下に5骨を追加。3つの既存殻を同じ連続ウェイトで曲げ、根元側はHipsへ滑らかに固定。殻の除去や根元の溶接は行っていない。
- 眼: 左右の既存眼パッチに独立した `PinoBlink_L/R`。閉眼時のみ頭表面に沿う細い弧へ変形。既存の開眼Neutral、顔・耳・頭の形は変更しない。**完全な眼球・上下瞼の機構を新設したものではない。**
- Skin: 未割当1点を補完。生成された指のウェイトを同側Handへ集約し、骨自体は保持。頭・眼をHead所有にし、胴→短脚→足裏の連続配分を補修。前肢の内部関節配分は元Rigを使い、腹へ広がる影響を制限。Dual Quaternionで体積保持を試みた。
- 前肢・支持: 骨長を伸ばさない左右IKと足裏方向の制御を追加。茶色の球は予め固定した低い接点であり、到達後に手へ合わせて動かしていない。製品itemや汎用把持の証明ではない。

補修後は未割当0、ウェイト和の最大誤差 `4.47e-8`、最大6ウェイト。新規Texture・UV制作なし。Basis頂点、元GLBと同じ三角形・corner法線・Base Colorを保持。[保存検証](saved-verification.json)、[外観データ比較](neutral-reference-data.json)。

## 実変形の結果

長さは原本単位、全高は約0.999512。物理的なm/mmではない。全数値は[集計](summary.json)と[40姿勢の計測](deformation-metrics.json)を参照。

| 能力 | 実結果 | 判定・未解決 |
|---|---|---|
| 尾の連続曲げ | 9姿勢、左右約20°を5骨へ分散。尾の符号付き体積は0.999892–1.000003倍。顔・身体は静止し、Neutralへ復帰 | 限定bend制御は成立。3重殻・非溶接根元は元から残る。単一尾としての全範囲の連続性・衝突・自然な重さは **HOLD** |
| 左右閉眼 | 9姿勢。L/R独立、半閉、両閉、開眼復帰。片側操作時の反対眼の変位0 | 制御独立性は成立。閉眼は眼パッチの細線化で、灰色Geometry上で閉眼の厚み・柔らかさが十分読めず、Canonicalの愛らしい瞼としては **HOLD** |
| 左右High-five | 低い固定接点へ皮膚頂点をIKで合わせた。端点誤差L `5.546e-5`、R `5.220e-5`。骨長伸長なし、足支持を維持 | 限定到達は成立。掌面の向き・局所接触の厚み・可愛さはHuman確認待ち。任意位置への到達や自然な把持は **UNKNOWN** |
| 両前肢接近 | 両前肢を内へ寄せ、前回約0.1904だった同じ領域の最短頂点間隔を約0.005282まで縮めた | まだ隙間があり、肩〜腹の面が帯状に伸びる。辺の最大倍率3.022、99 percentile 1.450。**接触・自然な変形はFAIL。採用ポーズにしない** |
| 浅い荷重と復帰 | 胴18°、腰を0.032下げ、首を12°戻す限定姿勢。9姿勢すべてで足裏近傍60頂点を維持、床下−0.001を超える貫通0。立位へ復帰 | 深い休息の参照と異なり、腹/臀部の新しい支持は0。これは浅い荷重試験。**自然な深い低休息は未成立 / HOLD** |

72°の深い低休息初案は、脚・腹が崩れ足も浮くため不採用。[不採用の3視点](rejected-deep-rest.png)、[初案計測](rejected-deep-rest-metrics.json)。その形を補正Shapeとして候補へ焼き込んでいない。深い休息の代わりに浅い屈伸を合格扱いしない。

## Neutral復帰と保存後の確認

編集候補・再生ファイルを開き直し、8つのNeutral境界で基準との差最大 `6.144e-8`、Basis座標は完全一致。4本のGIFは開始/復帰の3視点画像がピクセル一致。元GLBとのCycles比較では、512²画素中、正面5・側面11・3/4は7画素だけ変化し、8bitチャンネル差最大は3/1/4。完全ピクセル一致とは記さない。[画素差](neutral-pixels.json)。

再生保存の初回不具合は、描画中にframe 1の既存Action評価が制御値を戻したことが原因。描画を終えてから記録した値でActionを構築する方式へ修正した。保存後に全40キー姿勢の尾・眼の変位量を計測と再照合した。

さらに補間途中の復帰232fで、IKの解除により210頂点が最大0.009468床下へ沈むことを検出。浅い荷重のゼロ強度終端まで足IKを維持し、同フレームの貫通を0へ修正した。[補間修正](interpolation-repair.json)。これは全235フレームの外観・自己衝突を保証するものではない。保存検証には9つの補間中間点も含む。

## Human Gateで見る点と停止状態

1. Neutralの顔・丸い頭・耳・短い前肢・腹・大きな尾が元GLBと同じ本人に見えるか。
2. 尾の限定bendと低いHigh-fiveを、次の補修の基礎能力として残せるか。
3. 閉眼の薄さ、両前肢接近時の帯状変形、深い休息の未達を確認する。これらを完成Rigや最終演技へ昇格しない。

**Human Rig/Geometry GateはPENDINGで停止。制作全体はHOLD。** 外観を変える修復、他キャラ編集、最終Motion・Texture制作、Tripo再生成を行っていない。GLB/FBXの編集後export・runtime再現性は今回の検証対象外で、6ウェイトとIK/Shape Keyの実装同等性も未検証。

[入力・成果ハッシュ](manifest.json)、[再現手順](REPRODUCE.md)。
