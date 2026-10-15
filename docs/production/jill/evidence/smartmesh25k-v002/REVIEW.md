# Jill Smart Mesh 25K v002 — Human Geometry Gate

**2026-10-15 / HOLD / Human判定待ち。HOLD解除には未達。Tripo操作・upload・Texture生成・消費は0。** 正式Rig/Motion/Textureは制作していない。数値上の保護・復帰を外観承認へ読み替えない。GOはHumanだけが決定する。

開始branch `codex/jill-smartmesh25k-inspection-20261015`、開始HEAD `e513dc7c5c605ab1b6a0f9c85597520667e61490`。開始時cleanの既存Jill worktreeを使用し、別作業場所のShushu未コミット変更には触れていない。

## Authorityと編集系統

現行AGENTS / Character appearance lock、Goal√map、一般Handoff・Jill HANDOFF、[v001 REVIEW](../smartmesh25k-v001/REVIEW.md)、Jill Canonical、承認済みBody-only Front/Left/Right/Backを参照。Motion-to-Anatomy Q01/03/04/06はorigin/mainの仕様で照合。34枚のMotion画像は未承認で、診断姿勢や可動域の承認根拠にしていない。

既存の唯一の編集正本 `smartmesh25k-v001/jill-geometry-master.blend` を開き、[v002別名保存](../../../../../assets/grimo/production/jill/tripo/smartmesh25k-v002/jill-geometry-master-v002.blend)へ継続した。原本GLB/FBXから別メッシュを再生成していない。v001、元アップロード、Canonical/Body-only等の保護入力219ファイルはSHA-256不変。12三角形の板除去はv001を継承。

- v001 master SHA-256: `6b8ec3a53772686e6bf49491acf4f53e190eb2c9cda7ba1039893266b7608fe0`
- v002 master SHA-256: `8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97`
- 28,050 vertices / 28,809 polygons / 54,361 triangles換算。面構成・頂点順・全体bounds・object transformはv001と一致。全身Remesh/Decimate、比率変更なし。

## 今回の局所変更

**Neutralの変更は眼内部64頂点と下側口縁24頂点の計88頂点だけ。** 眼の既存輪郭を固定し、内部に最大約0.003946 model unitの浅い凸を加えた。下側口縁は一回の局所平滑化、頂点移動上限0.0008。変更部と一隣接範囲の法線だけを再計算し、それ以外のimport法線を保持。身体・翼・葉・尾・足のNeutral座標は完全一致。眼の寸法/位置や翼・尾を作り直していない。

目口を先に仮材質で分離し、既存Geometryと無彩色の読みにくさを比較した。暗い眼と口内色で読みやすさは上がるが、眼窩の隙間と浅い眼、口縁の粗さは残る。虹彩・ハイライト・模様を描いて解決扱いにはしない。仮材質の口境界の階段状の色は面単位選択によるもので、全てをGeometry段差とは判定しない。仮材質は撮影process限定で、保存blendに採用していない。Textureで必ず解決するとも断定しない。

`TEST_ONLY_`の局所変形経路を補修した。翼はweight/pivotを調整し、開く側に最大0.040の背側移動を加えて首葉の衝突を減らす。腕は旧maskで手先が取り残される問題を補い、肩へのweightを接続関係で滑らかに伝える。尾は巻いた先端をmaskが切らないようにし、隣接する尾葉も同じ場で動かす。既存8キー・12ケースの時刻/補間は保持。これは**診断変形の補修**で、根のGeometryの干渉解消や正式Rigの完成ではない。角度表記が同じでもpivotと経路を変えたため、v001と同一終点姿勢の比較とは主張しない。

最初の翼案は交差候補181→208、167→262へ悪化し棄却（[記録](rejected-first-probe.json)）。尾pivot変更も悪化し元pivotへ戻した。preview.logは中間履歴。提出画像は最終保存v002を再読込して撮影した。

## Codexの実画像目視結果

Codexが下記の比較板34枚を開き、実レンダリングを目視。Front・左右Side・Back・左右前3Q・後3Q、顔、翼根/膜裏、肩、首葉、尾根、足底を確認。12ケースの中間・極値・復帰、反対Side/3Qも比較した。

Neutralの丸い体型、顔配置、翼・葉・尾・足の外形はv001から大きく変わって見えない。口縁は小幅な改善候補、眼内部の変化は微小でCanonicalの生きた眼の再現には届かない。Canonical/Body-onlyとの本人性・可愛さはHuman未承認。次の欠陥があるため外観PASSにはしない。

| 部位 | 見えた改善と残存欠陥 | 判定 |
|---|---|---|
| 眼・口 | 仮色で認識できるが眼窩の暗い隙間・浅い眼が残る。下口縁はやや滑らかだが粗い面/輪郭が残る | HOLD |
| 翼根・首葉・胴 | 開閉の干渉は減る。極値で鋭い根、膜裏/葉境界、交差候補が残る。開き側の伸び指標は増えるtradeoff | HOLD |
| 肩・前肢根 | 手先の取り残しと大きな伸びを軽減。極値の肩の膨らみ/折れ、首葉付近の連続性が不自然 | HOLD |
| 尾根・尾葉 | 尾の体積と巻いた先端のまとまりは保つ。根/葉の継ぎ目・交差候補は未解消 | HOLD |
| 足底・全身 | 今回の診断で形を保持。支持・荷重・接地Motionの証明ではない | Human未承認 |

### Neutral・顔・細部

- [Canonical / 承認Body-only4視点 / v002](boards/00-authority-v002.jpg)
- [Front / Back前後比較](boards/01-front-back.jpg)、[左右Side](boards/02-sides.jpg)、[左右3Q・後3Q](boards/03-three-quarter.jpg)
- [顔Clay](boards/04-face-clay.jpg)、[仮材質の顔4方向](boards/08-face-material.jpg)、[左右顔Side・肩](boards/09-neutral-extra.jpg)
- [左右翼根](boards/05-wing-roots.jpg)、[左右膜裏](boards/06-wing-undersides.jpg)、[尾根・足底](boards/07-tail-soles.jpg)

### 限定変形：中間・極値・復帰

pose板はv001/v002中間3Q・極値3Q/Sideとv002中間/極値/復帰Front。roots板は中間/極値の局所、後3Q、反対Side/前3Q、復帰Side。左右は解剖学的左右。

| ケース | 全体・前後比較 | 根/裏/反対側 |
|---|---|---|
| WingL Open | [pose](boards/pose-01-WingL_Open.jpg) | [roots](boards/roots-01-WingL_Open.jpg) |
| WingL Close | [pose](boards/pose-02-WingL_Close.jpg) | [roots](boards/roots-02-WingL_Close.jpg) |
| WingR Open | [pose](boards/pose-03-WingR_Open.jpg) | [roots](boards/roots-03-WingR_Open.jpg) |
| WingR Close | [pose](boards/pose-04-WingR_Close.jpg) | [roots](boards/roots-04-WingR_Close.jpg) |
| Tail Left | [pose](boards/pose-05-Tail_Left.jpg) | [roots](boards/roots-05-Tail_Left.jpg) |
| Tail Right | [pose](boards/pose-06-Tail_Right.jpg) | [roots](boards/roots-06-Tail_Right.jpg) |
| ArmL Offer | [pose](boards/pose-07-ArmL_Offer.jpg) | [roots](boards/roots-07-ArmL_Offer.jpg) |
| ArmR Offer | [pose](boards/pose-08-ArmR_Offer.jpg) | [roots](boards/roots-08-ArmR_Offer.jpg) |
| BothWings Open | [pose](boards/pose-09-BothWings_Open.jpg) | [roots](boards/roots-09-BothWings_Open.jpg) |
| BothWings Close | [pose](boards/pose-10-BothWings_Close.jpg) | [roots](boards/roots-10-BothWings_Close.jpg) |
| Combined Left | [pose](boards/pose-11-Combined_Left.jpg) | [roots](boards/roots-11-Combined_Left.jpg) |
| Combined Right | [pose](boards/pose-12-Combined_Right.jpg) | [roots](boards/roots-12-Combined_Right.jpg) |

[翼GIF](boards/diagnostic-wings-v001-v002.gif) / [腕・尾GIF](boards/diagnostic-arms-tail-v001-v002.gif) / [複合GIF](boards/diagnostic-combined-v001-v002.gif)。左v001・右v002、上Front・下後方。各ケース0→50→100→50→0%。戻り50%は同じキー値の往路画像を再利用、復帰0%は実際の復帰評価画像。連続Motion完成品ではなく5点の診断GIF。

v001と同一camera/orthographic scale/Workbench studio light/cavity/900×900。2D Authorityは同一投影3D比較ではない。v001 PNGとv002 JPEGの画素一致は主張しない。容量不足で最初のPNG保存が失敗し、今回作成した撮影ファイルだけをJPEGへ切替して全画像を最終blendから再撮影。画像の補修・生成・描き足しなし、比較板は配置/縮小/ラベルのみ。

## 必要最小限の保存・変形検証

[保存blend検証](saved-gate-validation.json)、[外見保護検証](preservation-validation.json)、[局所頂点・mask仕様](repair.json)、[保護hash](protected-inputs.json)。

| 極値ケース | 新規交差候補 v001→v002 | 最大辺長比 v001→v002 |
|---|---:|---:|
| WingL Open / Close | 181→13 / 64→11 | 1.012→1.272 / 1.601→1.080 |
| WingR Open / Close | 167→13 / 59→5 | 1.011→1.272 / 1.608→1.080 |
| Tail Left / Right | 3→3 / 1→1 | 1.596→1.227 / 1.596→1.228 |
| ArmL / ArmR | 88→11 / 80→10 | 3.156→2.098 / 3.156→2.129 |
| BothWings Open / Close | 348→26 / 123→16 | 1.012→1.272 / 1.608→1.080 |
| Combined Left / Right | 151→25 / 138→16 | 3.156→2.098 / 3.156→2.129 |

交差候補は各ケースのv001/v002移動頂点unionを同じ対象にし、v001固定三角化で移動面対静止面のBVH重なりを計数。共有頂点ペアと各Neutral既存重なりを除く。侵入深さ/欠陥総数ではなく、全ての移動面同士・自己交差・連続時間を網羅しない。候補減少を無干渉や外観PASSとは呼ばない。

12ケースの0/.5/1/.5/0で新規退化三角形0、Neutral復帰差0。対象外最大移動1.49e-8、顔/足7.45e-9（座標変換の浮動小数差）。独立性は1e-7内で、全サンプル完全0とは言わない。保存Neutral/Basis一致、Animation時刻/補間保持。Armature0、UV0、Image0、元1材質を保持。技術確認は本人性・可愛さ・可動域・Motion/runtime合格を証明しない。

## Human判定事項

1. 眼内部/下口縁の小変更がCanonicalと承認Body-onlyの可愛さ・本人性を守るか。承認/差戻し箇所を判断する。
2. 翼根/膜裏/首葉、肩、尾根の残HOLDを確認し、外見を変えない追加局所補修範囲と承認pose referenceを指定する。未承認Motion画像や診断極値を承認poseに昇格しない。
3. Geometry GateとTripo Texture開始可否をHumanが明示する。現提出はHOLDで、自動的に次工程へ進めない。

追加形状変更はここで止めた。v002はreview候補で、v001を置換採用していない。本レビュー時点では派生FBX/GLB未出力。後続Human指定の[基礎Rig投入準備](../tripo-input-v002/REVIEW.md)でNeutral派生のみ作成、正本不変・Geometry Gate HOLDを維持。正式Rig/Motion、荷重/接地、Texture・UV、PlayCanvas/runtime適合は未検証。
