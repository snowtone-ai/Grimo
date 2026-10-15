# Jill Smart Mesh 25K — Human Geometry Gate

**2026-10-15 / Human判定待ち / HOLD。Texture着手可とは判定していない。**

FBXを唯一の編集入力に選定し、明らかな板状異物10ポリゴン＝12三角形だけを別コピーから除去した。編集正本は [jill-geometry-master.blend](../../../../../assets/grimo/production/jill/tripo/smartmesh25k-v001/jill-geometry-master.blend)。原本2ファイルは不変。左右翼・左右前肢・尾の限定的な診断変形とNeutral復帰を保存したが、翼根・肩付近の接触候補と局所的な伸びが残る。Identity・可愛さ・変形品質のHuman承認は得ていない。

## Humanが見る順序

1. [Canonicalと承認済みBody-only 4視点](boards/00-approved-authority.jpg)。色付き2Dと無彩色3Dの違いを、形状と色の問題に分けて判断する。
2. 同条件の補修前後：[Front / 左右Side / Back](boards/01-orthographic.jpg)、[左右Front 3Q / Rear 3Q](boards/02-three-quarter.jpg)、[翼裏・左右翼根](boards/03-wings.jpg)、[左右翼裏の拡大](boards/03b-wing-undersides.jpg)、[尾根・足底・顔](boards/04-tail-feet-face.jpg)。
3. 実際の変形画像：[左右翼](boards/05-posed-appearance.jpg)、[尾・左右前肢](boards/06-posed-appearance.jpg)、[左右翼同時・複合](boards/07-posed-appearance.jpg)。各行にNeutral、50%、100%の3Qと最大姿勢のFront / Sideを掲載。
4. [翼の接触候補](boards/08-contact-screen.jpg)、[尾・前肢の接触候補](boards/09-contact-screen.jpg)。赤は最大姿勢で新たに交差候補になった面を示す。左欄は同じ面をNeutralで表示したものであり、Neutralの新規交差を示す図ではない。
5. 復帰を含むサンプル列：[翼GIF](boards/diagnostic-wings.gif)、[尾・前肢GIF](boards/diagnostic-arms-tail.gif)、[複合GIF](boards/diagnostic-combined.gif)。Front / Rear 3Qを併記。0→50→100→50→0の静止画列であり、完成Motionや連続衝突保証ではない。

元の900×900 PNGは [renders](renders/) に保存。レビュー用合成は縮小・配置・ラベル付けのみで、モデル画像の生成補完・修正を行っていない。

## Authorityと保護

- 開始時のローカル制作HEAD：`93a8d2480c44e90a9c6a6d693c0fd34f9f4487cb`。元作業場所の未コミットShushu成果とアップロードを保持し、独立worktree / `codex/jill-smartmesh25k-inspection-20261015`で作業。
- 指定されたリモート制作ブランチの `2abea76fad578281f74b9fa628987a80b56ad6dc` を最終commit前にfast-forward統合。途中のShushu commitを含む既存履歴を保持。Jillパスとの重複差分なし。force-push / resetなし。
- 同revisionのAGENTS Character appearance lockを適用。Neutral一致や数値結果でposed appearanceを承認しない。中間姿勢・極値をFront / Side / 3Qで目視した。生成用の立ち姿を、臀部支持の座りとして扱わない。
- WHY：ローカル `docs/grimo/knowledge/Goal√map.md`。Handoffは進行状態の参照であり承認ではない。
- 画像：`assets/grimo/source/jill/jill-Identity-canonical.png`、`tripo-generation-pose/jill_bodyonly_{front,left,right,back}.png`。2D承認は3D形状・変形承認を意味しない。
- 現行制作ブランチにないMotion-to-Anatomy資料は、確認済み `origin/main` の `940fc5ee3d9c2d155031a0c3030034d4999dea16` にある `docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md` のQ01 / Q03 / Q04 / Q06を参照した。
- 同mainの `assets/grimo/production/jill/references/REVIEW.md` の34候補はHuman PENDING。今回の翼開閉・前肢提示等の承認済みpose referenceとして利用していない。**pose reference未承認のためappearance lock上もHOLD。**

## 正式Geometry入力はFBX一つ

| 項目 | FBX（採用） | GLB（照合・保管のみ） |
|---|---:|---:|
| 頂点 | 28,050 | 28,050 |
| Quad | 25,554 | 0 |
| Triangle polygon | 3,265 | 54,373 |
| 三角形換算 | 54,373 | 54,373 |
| Material / UV layers | 1 / 0 | 1 / 0 |

同番号頂点のworld座標差は最大 `8.42937e-8`。全GLB三角形をFBXのポリゴン領域へ対応付けられ、未対応三角形・面の被覆不一致は0。FBXの三角形化では9 Quadの対角線が異なるため、完全に同じ三角形集合ではない。同一三角形は54,355 / 54,373。両方向の三角形重心→相手表面の距離は最大約0.000364（モデル高約1）、99 percentileは約8.1e-8。これはサンプル比較であり全表面の最大誤差保証ではない。

同じ形状・パーツを保ち、Quadを維持でき、重大な追加欠陥は確認されなかったため、Blender編集に有利なFBXを選定した。選定は補修前に [editing-source-selection.json](editing-source-selection.json) に記録。Quadが多いこと自体は変形適性の合格を意味しない。両形式とも目・口・葉・翼の元の課題を持つ。

| 不変入力 | bytes | SHA-256 |
|---|---:|---|
| cute dragon 3d model (1).fbx | 1,133,424 | `5e9339437af5ad209c01597997006e96bd90d5489a08c28531ab5faa2b3f31db` |
| cute dragon 3d model (1).glb | 1,327,164 | `fb960ddb3a6a346508b77e0850c57ce9c6f4cdc7e8aaab035ff31ce03feafad1` |

入力コピーは [input](../../../../../assets/grimo/production/jill/tripo/smartmesh25k-v001/input/)。元アップロードとコピーをSHA-256で再照合した。原本GLBからの修正版は制作していない。

## 異物の根拠と最小補修

申告の「5個の非連結成分」は再現しなかった。該当12三角形は、面の辺接続で**3パッチ**だった。上側2枚は各2三角形の板。下側8三角形は保持する身体形状と頂点3・4だけを共有し、共有辺は0。このため「非連結成分を一括削除」という操作は採用していない。

巨大で平坦な面が肩・胴体の後ろを横断し、承認Body-onlyの翼・葉・太い尾に対応しないことを、隔離表示と全体Front / Side / Back / 3Qで確認。12三角形をFBX上の10面へ対応付け、**面だけを除外し、共有頂点を含め全28,050頂点を保持**した。該当面と原本FBXは.blend内の非表示コレクションに残した。

- FBX除外face ID：`0, 1, 2, 3, 5, 6, 7, 1479, 5513, 19053`（8 Triangle + 2 Quad）。
- GLB照合ID：`0, 1, 2, 3, 5, 6, 7, 1479, 7761, 7762, 34841, 34842`。
- 補修後：28,809 polygons、25,552 Quad + 3,257 Triangle、**54,361三角形換算**。名称の「25K」を三角形数とは解釈しない。
- 全頂点座標・保持面の頂点列は元FBXと完全一致。Materialを共有。元のcorner normalを復元したがBlenderの再符号化により最大ベクトル差0.00057545があり、法線のbitwise一致は主張しない。
- 新規boundary edgeは0。元からのboundaryは1,552→1,533、3面以上共有edgeは10→9、退化三角形1は残存。削除後の未使用頂点16も正本内に保持。これらを一律に溶接・穴埋めしていない。

根拠：[plate-investigation.json](plate-investigation.json)、[repair-validation.json](repair-validation.json)、[元データ診断](source-audit.json)。初期比較の `fbx-glb-equivalence.json` と `raw-import-comparison.json` のFBX面集合カウントはQuadとTriangleを直接比較した中間値で、形状不整合の判定には無効。正式な整合判定は `editing-source-selection.json` に置き換えた。

## 限定変形proofと合格基準

正式RigやAuto Rigは作らず、正本に8個の `TEST_ONLY_` shape keyを追加した。Basisは補修Neutralのまま。角度重み付きの局所試験であり、完成用の骨・ウェイト・許容可動域ではない。全体smooth / remesh / decimate / 比率変更なし。

| 試験 | 診断範囲 | 独立制御 |
|---|---|---|
| 左右翼 | 開き相当12°、閉じ相当20°の局所Z回転 | 左右別キー、同時開閉も確認 |
| 尾 | 左右12°の局所Z回転 | 尾および随伴する尾の葉だけ |
| 左右前肢 | 前へ提示する局所X回転25° | 左右別キー |
| 複合 | 同側の翼閉じ＋前肢提示＋尾曲げ | 左右各1ケース |

12ケース×5サンプル（0 / 50 / 100 / 50 / 0%）。フレーム1–289、24fps、各ケース24frame、最大姿勢は `13 + 24*i`。L/Rはキャラクター自身の左右（+Xが左、前−Y、上+Z）。[deformation-validation.json](deformation-validation.json) に全ケース・測定を保存。

| Human指定基準 | 今回の証拠と判定 |
|---|---|
| 外見保護：顔・比率・翼葉尾の輪郭 | 補修Neutralでは保持面・座標不変。全姿勢のFront / Side / 3Qを比較し、顔・胴の大きな連動変形は見られない。ただし目口の元形状、翼根・肩の極値、色のない状態の可愛さを未承認。**Human PENDING / HOLD** |
| 品質：潰れ・破れ・不自然な貫通なし | サンプル内に新規退化三角形なし。しかし根元の交差候補と局所伸縮が残る。前肢は最短edgeを含む長さ比最大約3.156、翼閉じ最大約1.608。無破綻・無貫通の合格とはしない。**HOLD** |
| Neutral正常復帰 | 12ケース全てで元Neutralとの差0、保存再読込でBasis一致、診断キー0。**この範囲の技術確認は成立** |
| 左右翼・左右腕・尾の独立制御 | 診断対象外頂点の最大移動0。計測した顔上部・足範囲（z>.64 / z<.10）の移動0。マスクは [diagnostic-masks.json](diagnostic-masks.json)、実画像は `mask-*`。**この診断制御の範囲で成立**。完成Rigの独立性保証ではない |

新しい表面交差候補（50% / 最大、隣接頂点を共有する三角形ペアを除外）：

| ケース | 新規ペア数 |
|---|---:|
| WingL Open / Close | 113 / 181、40 / 64 |
| WingR Open / Close | 104 / 167、30 / 59 |
| Tail Left / Right | 3 / 3、1 / 1 |
| ArmL / ArmR Offer | 56 / 88、57 / 80 |
| BothWings Open / Close | 217 / 348、70 / 123 |
| Combined Left / Right | 99 / 151、88 / 138 |

[collision-screen.json](collision-screen.json) はBVHによる動く面と静止面の交差候補。Neutralにも交差があり、候補数をそのまま欠陥数や貫通深さとは扱わない。Neutralの三角形化を用いるため、変形Quadの表示時対角線とは異なる可能性がある。閉じた体積内への侵入、動く領域内部の自己交差、未サンプル時間、大振幅、全組合せを保証しない。目視でも翼根・首葉・肩に重なりが残るため、単なる検出誤差として無視していない。

## 目視所見・未検証事項（Human Gate）

| 領域 / 要件 | 所見・次の判断 |
|---|---|
| 顔・目・口 / Q01 | 元の目は平坦な面と窪んだ縁が目立つ。口内・下縁に粗い輪郭がある。目の輝きや頬、口の色は存在しない。Textureだけで承認表情へ届くか、限定Geometry補修が先かをHuman判断。blink・口開閉・視線は未検証。 |
| 角・葉・頭身 | 除去前後で保持。葉には面の折れ・継ぎ目が残る。2Dの柔らかさ・葉と角の読み分けが3Dで十分か未承認。独自の美化は行っていない。 |
| 翼 / Q06 | 輪郭は保ち、左右を別に動かせる。翼根と葉・胴の重なり、膜厚・裏面の見え方、閉じ極値の局所伸びがHOLD。完全折り畳み・飛行は今回の試験外。 |
| 前肢 / Q04 | 左右提示と復帰を確認。肩〜首葉との接触候補、根元の局所伸びを残す。小物保持・物への接触・大振幅は未検証。 |
| 尾 / Q06 | 太いボリューム・先端カールを保持して小さく左右曲げ。尾根・葉周辺に少数の交差候補。大きい曲げ、胴体・翼・前肢との全組合せは未検証。 |
| 足・支持 / Q03 | 足底と脚の形状は不変。足底拡大を提出。重心、荷重移動、歩行、IK接地、真の臀部支持座りは未検証。尾を支持脚とみなさない。 |
| 材質・UV・runtime | 原本にUV・画像Textureなし。表示の灰緑色は診断用Workbench色。Canonical配色・模様・clover・目の反射は未承認。スマートフォンruntime・スキニング・Texture工程は実施していない。 |

**Humanに必要な判断**：①12三角形の除去範囲、②顔・角・葉・翼・尾・身体比率と可愛さをGeometryとして採用できるか、③翼根・肩・尾根のHOLDを解消する次の限定補修範囲、④承認pose reference、⑤その後にTextureへ進めるか。現状の資料から自動的にTexture着手可とはしない。Human承認までここで停止する。

## 正本・書き出し・再現性

- 正本 `.blend`：`00_REFERENCE_FBX_LOCKED`（非表示の未編集FBX）、`01_EDITABLE_MASTER`、`02_REMOVED_PLATES_ARCHIVE`（非表示の除去面）。保存時frame1。診断再生は各試験後Neutralへ戻る。手動試験時はanimationによる値の再設定に注意し、Basisを書き換えない。
- `jill-original-inspection.blend` は両原本を読み込んだ**照合専用**保存。補修・Rigの編集正本ではない。GLBは保管・照合以外に用いない。
- [jill-repaired-neutral.glb](../../../../../assets/grimo/production/jill/tripo/smartmesh25k-v001/jill-repaired-neutral.glb) は保存済み正本からのみ出力。診断shape key / animation / armatureを含まない。54,361三角形、再読込で両方向の頂点距離最大2.666e-7。Normal分割によりGLB頂点28,058、正本の使用頂点28,034。 [保存・書き出し検証](saved-master-export-validation.json)。GLBはレビュー用派生物でありTripoへ送信していない。
- [scripts](../../../../../assets/grimo/production/jill/tripo/smartmesh25k-v001/scripts/) に監査・選定・最小補修・診断・撮影を保存。Blender 5.2.1、Workbench、正投影900×900、Standard、同一studio light / cavity / scale。カメラ位置は `build_master.py` 等に明示。
- [provenance.json](provenance.json) に原本・authority・成果物のSHA-256を記録。静止画も含むファイル一覧は [artifact-manifest.json](artifact-manifest.json)。同じGit commitの成果を一組として読む。
