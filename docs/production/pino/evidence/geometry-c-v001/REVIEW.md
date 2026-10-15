# Pino C — Geometry / 実変形試験 / Human Geometry Gate

**Human Geometry Gate: PENDING。Tripo引き渡し: HOLD / BLOCKED。** 原本とNeutral外観を固定した。4種類の実変形試験をFBX由来の複製で実行したが、接続・接触・低い休息に未解決事項がある。技術的な復帰一致を、可愛さ・本人らしさ・自然さの承認に置き換えない。

## 正本と外観基準

Humanは原本間の差異を確認した上で、2026-10-15に**FBXを唯一のGeometry Master**、続いて**元GLBを外観比較の正式基準**と指定した。[判断記録](master-decision.json)。原本2ファイルへ書き戻していない。

| 役割 | ファイル | SHA-256 |
|---|---|---|
| 固定Geometry Master | [原本FBX](../../../../../assets/grimo/production/pino/candidate-c/source/cute%20blue%20creature%203d%20model.fbx) | `3531eddb0578be8e4885b942db629a97a949d2039eb496c88ed1dc041372a111` |
| 固定外観基準 | [原本GLB](../../../../../assets/grimo/production/pino/candidate-c/source/cute%20blue%20creature%203d%20model.glb) | `ee7339f8e4339037b87880b75d90fd944fe7dda84f696c2be42db7ea0f24da11` |
| 編集用・補修未採用の保存 | [FBX由来Master .blend](../../../../../assets/grimo/production/pino/candidate-c/pino-c-master-retained.blend) | manifest参照 |
| 実変形試験用複製 | [4試験の再生ファイル](../../../../../assets/grimo/production/pino/candidate-c/pino-c-master-derived-four-tests.blend) | manifest参照。診断用で最終Rigではない |
| Master派生・Neutral候補 | [派生GLB](../../../../../assets/grimo/production/pino/candidate-c/delivery/pino-c-master-derived-neutral.glb) | `68c227e458a52ebe74631a1f51e6b28b056b3147635c672abbe16ce936df13b9` |

FBXネイティブ座標は18,858頂点すべてで元GLBのPOSITIONと完全一致する。一方、Blender読み込み後はFBXのn-gon三角形化が18三角形分異なり、表面サンプル差は最大0.000961（全高約0.096%）。頂点の座標変換誤差は最大8.94×10⁻⁸。FBXのPrincipled Specular IOR Levelは1.0、GLBは0.5。両方とも画像Texture・UV・Rig・Morphはない。[数値](fbx-glb-consistency.json)、[構造と材質](originals-comparison.json)、[比較画像](originals-comparison-01.png)。この原本間の差異を完成GLBへ持ち込んでいない。

派生GLBは**FBXから全頂点座標を出力**し、元GLBの三角形化・法線・材質を外観維持の出力規則にした。全37,848三角形がFBXの面に含まれることを確認した。元GLBを独立した補修対象にはしていない。出力の有効バイナリ属性・インデックスは元GLBとバイト一致し、材質も同一。差は出典を記したメタデータ。[出力対応関係](master-export.json)。

再importした頂点・三角形・corner法線・変換行列が完全一致し、同じCycles設定・640px・9視点で**変更ピクセル0、最大チャンネル差0**。[再import](export-reimport.json)、[ピクセル検証](export-pixel-comparison.json)、[正面・3/4・側面](export-comparison-01.png)、[反対側・後方](export-comparison-02.png)、[上・下を含む比較](export-comparison-03.png)。このPASSはNeutral外観維持についての判定であり、Geometry全体・Motion・Tripo適合性のPASSではない。

## Geometryの現状と内部補修

18,858頂点、37,848三角形、19個の非連結成分。胴・頭・前後肢は同一成分だが、眼・耳・装飾と尻尾は別成分。元GLBの境界辺455、3面以上で共有する辺390、向き不整合59。交差の総数には意図された装飾の重なりも含まれ、すべてを造形欠陥とは扱わない。[原本監査](initial-audit.json)、[成分解析](component-analysis.json)。

巨大な尻尾には**3つの閉じた殻**がある。外・中の殻は8頂点を共有し、内殻は別成分。胴体と尻尾の共有頂点は0で、根元は重なりによる見かけの接続。単一で連続した尾根の成立は未確認。[根元・中央・先端断面](tail-sections.png)、[殻の集計](tail-shells.json)。

両眼の表面は左右とも存在するが、それぞれ34本の境界を持つ開いたパッチで、閉じた眼球・瞼機構ではない。短い前肢は腹部と同一の面成分。[両眼・前肢・腹部の断面](eyes-paws-sections.png)。Neutralでは両足の接地候補19頂点を確認し、尾の最低点は床より0.050293高い。尾を支持柱と見なしていない。[接地図](support-footprint.png)、[支持計測](support.json)。物理スケール・密度が未定で、重なりと非manifoldもあるため、頂点平均を重心と呼ばない。

**採用した内部補修: なし。** Master一本化の指定前にGLB複製で内殻1つを非表示化する予備診断を行い、9視点のピクセル一致を確認した。しかし殻は残り、根元も解決せず、外観絶対固定を全周・変形中について保証できない。これは保全した参考証拠であり、正式Masterへの補修・納品GLBには採用していない。[隔離した予備試験](trial.json)、[比較](trial-comparison.png)。外面の頂点移動・Smooth・Remesh・再構築・美化を行っていない。根元の溶接や表面変更を伴う解決はBLOCKED。

## 4種類の実変形試験

全試験はFBX Masterから派生した複製のみ。正面・側面・3/4の実メッシュを毎フレーム描画し、GIFにした。静的な構造推測でPASSにしていない。Cyclesの極値画像も添えた。[参照ポーズと実際の極値の並列比較](pose-reference-comparison.png)、[眼周囲の拡大動画](actual-eyes-detail.gif)も確認できる。範囲は診断のための選択であり、Human承認済み可動域ではない。

| 試験 | 実行内容と技術判定 | 証拠 | Neutral復帰 |
|---|---|---|---|
| 尻尾 | 25フレーム、根元側固定部から先端へ左右連続曲げ。殻の符号付き体積は約0.999757〜1.000070倍、3断面の面積は約0.999761〜1.000246倍。限定的な体積保持はPASS。3重殻・非溶接根元・胴との重なりが残るため、要求全体は**FAIL / HOLD** | [動く3視点](actual-tail.gif)、[遷移の極値](actual-tail-extremes.png)、[Cycles極値](cycles-tail-extremes.png) | 元座標と一致。開始／復帰画像も3視点一致 |
| 両眼 | 左右独立瞬き・左右ウィンク・半目・全閉への変形・再開眼、54フレーム。既存眼パッチを頭表面に沿う線状へ変形する試験で、瞼を再構築していない。独立操作は実行できたが、眼球／瞼の成立・閉眼の柔らかさ・可愛さは**UNKNOWN / HOLD** | [動く3視点](actual-eyes.gif)、[遷移の極値](actual-eyes-extremes.png)、[Cycles極値](cycles-eyes-extremes.png) | 同上 |
| 前肢 | 左右挙上・低いHigh-five・両手接触の試行・Food把持・Gift提示、78フレーム。両手の最短頂点間隔は約0.1904残り、手同士の接触は不成立。境界付近の辺倍率は最大約2.96、腹と前肢の自然な分離も未成立。要求全体は**FAIL**。小物に対する一般的な把持成立性はUNKNOWN | [動く3視点](actual-forepaws.gif)、[遷移の極値](actual-forepaws-extremes.png)、[Cycles極値](cycles-forepaws-extremes.png) | 同上 |
| 低い休息 | 25フレーム、低姿勢への移行・復帰。試した胴体回転／頭部追従では最大255頂点が床を貫通、最下点−0.1306。極値で腹部・尾の接地支持は0、足だけを固定した状態。顔と胴の自然さも保てず**FAIL**。安定支持・物理重心はUNKNOWN | [動く3視点](actual-low-rest.gif)、[遷移の極値](actual-low-rest-extremes.png)、[Cycles極値](cycles-low-rest-extremes.png) | 元座標へ明示復帰。画像一致と再読込を検証 |

長さ・距離は原本単位（全高約0.999512）。身体寸法のメートル換算ではない。Food/Gift/High-fiveの茶色の小物は到達端に合わせた診断用fixtureで、製品の小物ではない。fixtureへの接触を汎用把持PASSにしない。低い休息の失敗を「Cでは永久に不可能」とは結論しない。**今回の変形方法のFAILと、未検証の代替Rig方式は区別する。** 失敗した変形を完成モデルへ適用していない。

[フレーム別計測](four-tests.json)、[集計と画像復帰](four-tests-summary.json)、[再生と保存検証](replay-verification.json)。計測には辺の伸縮、床貫通、殻の体積、断面積、胴・尾の交差、両手間隔、接地部位を含む。交差は元からある重なりを基準として読む。Neutralのローカル座標・corner法線・材質を元どおり保存した。ゼロ強度の計算式に生じた微小な浮動小数点残差は、元頂点の直接復帰に置き換えた。非ゼロ試験はハッシュ再照合し、やり直していない。

## Appearance lockとAuthority

`2abea76fad578281f74b9fa628987a80b56ad6dc`のCharacter appearance lockを確認し、同じAGENTS.md blobを含むmain `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`をPino専用ブランチへfast-forward統合した。元の制作checkoutにあるShushu等の未コミット成果には触れていない。

Canonical、承認済みBody-only 4面と、実レンダーの正面／側面／3/4・遷移極値を照合した。[参照の区別](appearance-authority-context.png)。Canonicalの丸い頭・短い前肢・ふっくらした腹・巨大な単一尾の本人らしさを優先する。今回の低休息・接触変形には視覚的不一致が残るためHOLD。生成立位や単なる屈伸を、お尻で支持する座位の成立と呼ばない。

- WHY: `docs/grimo/knowledge/Goal√map.md`。継続ポインタ: `docs/production/Handoff.md`。
- Canonical / 承認Body-only: `assets/grimo/source/pino/`と`GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md`。
- Motion要求: `GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`のPino節。DRAFT / Human PENDINGを承認済み角度やRig仕様と解釈しない。
- `assets/grimo/production/pino/references/REVIEW.md`の34枚はHuman PENDING。瞬き・尾・High-five・低い休息・Food/Giftの参照として並べたが、承認済みポーズとは扱わない。無着色Geometryから最終的な眼の印象や色の可愛さは確定できない。

## Human Geometry Gateでの判断事項

1. 元GLBの外観維持とMaster／派生GLBの対応を確認する。Neutral一致のみで動作を承認しない。
2. 3重の尾・非溶接根元をどう扱うか、外観完全固定を優先したまま判断する。内部除去の追加検証か、現状維持かを選ぶ必要がある。
3. 眼の自然さ、短い前肢の接触、低い休息について、今回の失敗を確認し、形を変えない範囲のpose専用補正／重み方式の別検証を許容するか判断する。承認済みの動作参照・許容範囲が未確定の項目はHOLDのまま。

**ここで停止する。Human Geometry Gate PENDING、Tripo UV/TextureへのGOは出していない。** Tripo操作・アップロード・課金・UV/Texture制作・最終Rig／Motion量産は実行していない。Studioへの実取り込み適合性はUNKNOWN。

再現手順・ハッシュ一覧・ブランチ情報は[manifest](manifest.json)と[実行手順](REPRODUCE.md)。
