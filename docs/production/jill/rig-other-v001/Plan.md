# Jill Rig Other v001 — Research → Plan → Implementation

2026-10-15 / Plan frozen before rig edits. Outcome gate: **Human visual PENDING**.

## Outcome and authority

Jill専用の六肢Rigで、独立した2翼・2前肢・2脚、太い巻尾、葉、頭首、視線/瞬き/小口、接触/装備anchorを制御する。G3 Rig/GLB → G2 局所反応・支持と表情の合成 → G1 幼さ・可愛さ・本人性 → G0 再会したくなる体験。正式Textureと全Motionライブラリは対象外。証拠用pose sweepは完成演技ではない。

- main authority: `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b` (fetch verified)。AGENTS、Goal√map、一般Handoffを読了。mainにはJill v002未統合。
- Jill state authority: `7f16127322685216bbd8bb93065cb3de4203568c`、[HANDOFF](https://github.com/snowtone-ai/Grimo/blob/7f16127322685216bbd8bb93065cb3de4203568c/docs/production/jill/HANDOFF.md)、[v002 Evidence](https://github.com/snowtone-ai/Grimo/blob/7f16127322685216bbd8bb93065cb3de4203568c/docs/production/jill/evidence/smartmesh25k-v002/REVIEW.md)。v002 Geometry HOLD、眼/翼根/肩/尾根に残欠陥。最新Humanの本依頼が実Rig制作を許可するが、外観承認を与えるものではない。
- v002 master SHA256 `8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97`。28,050頂点 / 54,361三角形換算。原本保存禁止、別名派生のみ。
- [Canonical](../../../../assets/grimo/source/jill/jill-Identity-canonical.png)、承認Body-only Front/Left/Right/Backを直接開いたv002比較板で照合。34枚のMotion候補/contact sheetを直接確認したが全てHuman PENDING。承認pose referenceとして採用しない。
- `docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md` C2/F/J2、Q01–Q15を照合。Q05/07/08は他個体固有。Q11–14の商品/状態/演技全実装は本Rigだけでは証明できない。
- Initial user checkout: `codex/shushu-v004-skin-compat-20261015@0947d03`、Shushu dirtyとルート追加FBX/GLBあり。専用managed worktree、main基点 `codex/jill-rig-other-v001-20261015`で隔離。main/Jill枝の一括mergeは行わない。

## External research (2026-10-15)

Exa SearchとFirecrawlで、制作実務・比較解剖/力学・Blender/glTFの3方向を調査。下表は原文/抄録または公式講演概要の読めた範囲のみを採用。検索結果を公開事実の検証と取り違えない。論文の動物実験値やゲーム固有の骨数をJillの正解値に転用しない。

| Source / provenance | 公開事実・読了範囲 | 採用理由 / Jillへの推論・設計 / 限界 |
|---|---|---|
| [CEDEC2025: モンハンワイルズのプロシージャルな姿勢補正](https://cedec.cesa.or.jp/2025/timetable/detail/s67ad91775bcd8) / Capcom講演者、公式概要 | 地形sensor/IK、犬・熊・鳥型の汎用補正と胴長トカゲ等の個別例。概要を読了、講演全録画は未視聴 | 形態別の支持補正を採用。Jillの足IKと翼FKを分離。汎用人型IKだけで合格にしない。RE ENGINE内部実装を推定再現しない |
| [Autodesk: ワイルズ制作基盤、開発陣インタビュー](https://area.autodesk.jp/case/game/monster-hunter-wilds/) / 2025-12-11 | 骨格→筋/皮膚脂肪simulation、架空生物に近い実動物を参照。画像/動画を伴うdirector feedback、記録と段階review | 実レンダーの根/膜/肩と全身を同時確認。Jillは筋simulationの代わりに局所correctiveを使う創作上の実装。数値だけの品質判定を避ける |
| [CGWORLD: サン・ムーン3Dアセット制作](https://cgworld.jp/feature/201707-cgw227GG-pokemon-3.html) / 開発現場取材 | キュウコンの多尾、ドヒドイデの傘状機構等、個体別rig。参照/ゲームモデルで異なるjoint構造。マングース等を演技参照 | 個性に必要な自由度から骨を決める。Jillも部位ごとの所有/機構で再設計。掲載の約110 joint制約を本作の仕様にしない |
| [Baier/Gatesy/Jenkins: avian shoulder ligament](https://pubmed.ncbi.nlm.nih.gov/17173029/) / Nature 2007, DOI 10.1038/nature05435、抄録 | 鳥の肩は筋・靱帯・軟骨・慣性/空力荷重の釣合い。AHLに重要な安定化機能 | 翼rootを一点の自由球関節として過剰回転させず、胸との荷重経路とroot体積を表現。Jillに鳥の胸骨や靱帯が実在すると断定しない |
| [Panyutina et al.: bat shoulder girdle](https://doi.org/10.1002/ar.22650) / Anatomical Record 2013、抄録 | 肩甲帯の寄与は上腕運動より小さく、鎖骨/肩甲骨の連動と実用可動域を観察 | wing girdleと主翼の段階的変形、小さいroot滑走を別制御。蝙蝠の骨数/運動角をコピーしない |
| [Cheney/Allen/Swartz: bat wing elastin and muscles](https://pmc.ncbi.nlm.nih.gov/articles/PMC5345682/) / J Anat 2017, DOI 10.1111/joa.12580、本文冒頭/抄録 | 膜は骨を覆い肢/指間に広がる皮膚。130種にelastin束と膜内筋、方向性と地域差 | 膜を硬板1枚として動かさず、根/前縁/外側/後縁のownershipと局所camberを設計。生体膜simulationや飛行性能の再現は主張しない |
| [Andrada et al.: Beagle forelimb inverse dynamics](https://doi.org/10.2460/ajvr.78.7.804) / AJVR 2017、抄録 | scapulaの回転が前肢運動に大きく寄与。皮膚markerと透視で推定差 | 前肢scapulaと上腕/肘/手先を別制御。犬の荷重分担を二足主体Jillへ同一視しない |
| [Fischer et al.: canine hindlimb 3D kinematics](https://www.nature.com/articles/s41598-018-34310-0) / Scientific Reports 2018、検索本文 | 体型で骨盤/大腿の回転軌道が異なる。biplanar fluoroscopyとskin markerの差 | 足接地/骨盤shiftを独立評価。外面だけから内部関節が唯一確定するとはしない |
| [Ritter: Axial Muscle Function During Lizard Locomotion](https://doi.org/10.1242/jeb.199.11.2499) / JEB 1996、抄録 | epaxialの体幹安定化とhypaxialの側屈寄与をEMG/kinematicsで比較 | 胴を振り続ける仕掛けにせず支持を保ちつつ胸/腹の小曲げ。脊椎を尾へ連続接続する。種/実験差は残る |
| [Libby et al.: Tail-assisted pitch control](https://www.nature.com/articles/nature10710) / Nature 2012、抄録/検索本文 | トカゲ尾の慣性運動は跳躍中のpitch安定化に寄与。質量分布で有効性が変わる | 太尾は一根＋連続した複数区間、rootを絞らず曲げを分散。Jillの飛行/跳躍/尾支持は追加要求にしない。物理安定solverは別 |
| [Blender Studio: Rigging](https://studio.blender.org/tools/pipeline-overview/asset-creation/rigging) / 制作チーム公式workflow | control rig生成→手動weight調整→corrective shapes、制作ごとにanimator要求へ調整 | 自動Rigの骨数を完成指標にせず、意味maskとcorrectiveを併用する。CloudRig導入を必須にしない |
| [Blender Studio: Pose Shape Keys](https://studio.blender.org/tools/addons/pose_shape_keys) / 公式tool docs | poseとshapeを対応、骨変形後の形を設計しdriverで発火、weights変更後もiterate | root/肩/尾のpose別局所shapeを作る。neutral Basisを不変とし、補正に顔/比率改造を隠さない |
| [Blender Studio: Facial rigging proposal](https://studio.blender.org/blog/proposal-facial-rigging-with-shape-keys/) / 2025-04-01, 公式提案 | artistが設計したlocal形状＋jaw/head骨を組合せるprototype。これは映画向け提案 | Jillの左右瞼/小口/頬を意味chで分離。提案中のprototypeをゲーム実績と呼ばない。眼瞼の成立は本モデル実画像で別判定 |
| [Blender 4.5 glTF manual](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) / 公式、Exa本文/Firecrawl対象抽出確認 | skin、bone TRS、morph weightsのexport。bone driverのmorph samplingはarmature直下mesh。その他のpropertyはそのままglTF制御にならない | authoring controlsとexport deform bones/morphを区別し、constraint/driver出力をbakeする。再importの同時刻で比較。latestページ404は記録し4.5参照、実行版は5.2.1でAPIを確認する |

### 比較・統合

鳥/蝙蝠/四足爬虫類はいずれも基本は四肢動物で、翼は前肢の変形。**Jillは2翼＋2前肢＋2脚の創作六肢であり、対応する実在の脊椎動物骨格はない。** 生体資料から借りるのは連続した根元、荷重経路、膜の地域差、体型に合う関節運動という原理。追加の左右翼肩甲帯を背側胸に置き、前肢肩甲帯を胸外側に置くのはJillの創作上の設計で、解剖学的事実ではない。

大型ゲーム資料は「個体の演技/機構に合わせたrigとreview」を支持し、Blender資料はその反復方法を与える。生体の自由度を全て足すと制御/検証が膨れるため、既存の丸い外形に必要な意味領域を優先。DQ preserve volumeだけに頼るとglTF LBSとの差が出るため、LBSをexport基準としlocal correctiveで補う。

## Intake facts before implementation

Read-only isolated Blender 5.2.1 import, no asset saved:

| Local file | SHA256 | 判定 |
|---|---|---|
| `tripo_convert_77a7aeee-faff-4d3b-8082-d15dddbe9fc8.fbx` | `1d9ecfae60f0fcb1a8bbffeb81fd2a931b1dba0907af43487bf0d1f1e3a7dc14` | Jill第一候補、28,050v / 54,361tri / 78 joints、UV1、51 weighted groups |
| `jill-v002-neutral-tripo.fbx.glb` | `a93cd56d4b9658596284288ef8f5ebabffae0d3c5f7024e591269ce95eff0378` | 照合、78 joints、seam split 46,003v / 同tri数、余分なIcosphereと異なるworld配置あり。自動的に等価としない |
| `tripo_convert_e41db652-3438-43d9-b501-1000972256cf.fbx` | `b728b4e7275d9431e148cbb3eaeb6f65b328493fc39cb990b9eb6e90ceaa4b37` | 18,858v / 65 joints。Jill v002と異なるため対象外、移動/編集しない |

Phase 2でJillのFBX/GLBとv002 neutral donorのbyte copyを`assets/grimo/production/jill/tripo/rig-other-v001/source/`に保管しhash前後照合。入力FBXのuniform normalization/座標系/頂点orderをv002と測定。最終Basisはv002のworld外形を優先し、FBXの骨/UV/weightsは照合後に必要部位へ移す。無関係meshを完成物へ含めない。

## Skeleton / controls / deformation design

| Region | 設計 | 主要リスクと対策 |
|---|---|---|
| root/pelvis/spine/chest | master/root、pelvis、lower/upper spine、chestを分離。rest座標固定。支持と胸演技は別mask | 胴の一体scale禁止。上体起こしで脚を伸ばさない。足world targetと骨盤shiftで評価 |
| forelimbs L/R | scapula slide/rotate→upper arm→forearm→paw、FKと低target IK、paw接触anchor | 既存人型肩/指の誤割当を再構成。肩blendを接続性とgeodesic的な伝播で制限し、翼weights混入を排除。肩volume corrective |
| wings L/R | 独立wing girdle→root/arm→outer edge、膜地域の補助骨/局所morph。foldとflap/camber別ch、root小滑走 | 首葉/腕/胸の交差。胴固定の根→自由部へsmooth blend、膜は前縁と後縁の支持を保つ。root/camber corrective。隠れている接合欠落はHOLD |
| legs L/R | thigh→shin→foot、独立foot target/pole、接地foot/paw markers | 接地lock、反転/伸長を防ぐ。足裏を支持に使い尾/翼を支柱にしない。低休息は可、真の座位完成を偽らない |
| thick tail | pelvis所属rootから巻形に沿う複数joint、rootとdistal curl/tip独立、隣接葉は同断面owner | 直線distanceで巻尾を横断するとweight誤配。曲線arc順/局所nearest segment、太根は広く段階blend。root/twist corrective。巻尾を細くしない |
| leaves / horns | connected component/付根でhead、neck/chest、tailへ分類。葉ごとの小FKまたは地域control、rigid horn head owner | 全葉head固定や首葉の置き去りを防ぐ。根のowner変形を追い、局所followは小角。骨数は必要性で決める |
| head/neck | chest→neck→head、yaw/pitch/rollを胴と分離。neck/cheek local correction | 葉の顔遮蔽/細首/隙間。大角度を能力保証しない。頭shape/位置/眼輪郭はneutral固定 |
| gaze / eyelids / mouth | 左右眼領域・左右blink/half-lid、小口close/open/微笑/頬のmorphとjaw/eye controls | 既存の浅い眼/眼窩隙間が最大リスク。眼表面だけの縦潰しを本物の瞼合格にしない。必要なら局所lid/口内追加を別partで根拠明記。幼い顔の外周は維持。形状不足が残ればHOLD |
| touch / wear / holding | head中央、cheek L/R、chest、paw L/R、wingroot L/R、tailroot、mouth、gift/assist、foot support anchor | owner骨所属をGLB node/boneで出力。変形面とのずれをposeで測る。装備実物未承認のclearanceは保証しない |

Correctiveは翼root、肩、尾root、必要な首/顔について、問題poseの実変形との差分として作者側で作り、pose readerで滑らかに0→1。Basis 0、他領域mask 0。複合時に加算し過ぎれば強度clamp/複合専用補正。constraint/driverそのものはGLBへ渡らないため、意味chとdeform bone/morphの対応JSONとsampling/bake済みproofを納品。

## Implementation order (Plan complete before step 1)

1. Freeze this plan by commit; source整理・hash、FBX/GLB/v002 equivalence、neutral authority renderを確定。
2. 新規派生blendでFBX骨/weightsを実見し、六肢構造を再設計。Basis・元の面/UV/材質を保存、元78骨はsourceのみ保持。
3. 胴/脚/前肢→翼/膜/尾→owner葉/頭首の順でweights。左右/対象外の独立性を確認。
4. 顔の局所morph/骨とanchorを追加。root等のpose correctiveを作り、neutral復帰を確認。
5. bounded representative sweep: 片/両翼open/fold、左右low paw、左右tail bend、head lean、blink/gaze/mouth、低支持、複合。中間/極値/復帰をFront/Side/3Q、必要な根/裏詳細で実renderし直接開く。未承認pose画像は方向参考のみ。
6. 不具合に対応する局所修正を行い、保存→別process再読込→GLB export→fresh import。骨TRS/morph/anchorsと同時刻の形/画像を照合。全Motion制作へ広げない。
7. Evidenceにfacts/視覚所見/未達/受入判定を分け、完成候補blend/GLB、制御対応、hash、再現scriptを保存。commit/push後にremote SHA確認。Human視覚承認PENDINGならRig完成承認を主張しない。

## Acceptance and bounded checks

- Preservation: source byte hash不変。Canonical/Body-only/v002正本/他キャラ/開始dirty未変更。候補Basisとv002を座標照合、意図しないneutral頂点差なし。追加local部品は別記し隠さない。
- Functional: 独立6肢/頭首/葉/尾/左右faceを実操作でき、weights正規化、欠落頂点・NaNなし。IK/接触anchorのholdとfree limbが区別可能。これだけで自然さPASSにしない。
- Visual: 同一cameraでFront/左右Side/3Qと根の実画像。Neutral＋中間＋代表極値＋戻しで顔/胸/翼膜/太尾の体積、重さ、接合と遮蔽を評価。継続する潰れ/浮き/貫通・瞼/口の破綻はHOLD。承認pose不足もHOLDとしてHuman判断へ。
- Roundtrip: 保存blend再読込後にcontrolを再操作、GLB fresh importにdeform joints/morph/anchorとproof animationが存在し、pose/戻し比較。drivers/IKはGLB実行機能ではないと明記。driver評価はBlender、任意runtimeでは対応mappingの再実装が必要。
- Q coverage: Q01/02/03/04/06/09/10/13/14を本Rigで限定実証。Q11/12の商品state/Secret、全5Food演技・全Motion、Q15 PlayCanvas/スマホ実機は対象外またはUNKNOWN。正式Textureなしの眼の印象は最終確定できない。
- Release gate: bounded technical success / Codex visual findings / Human approvalの三つを別々に報告。未達なら具体画像と構造上の原因・阻害条件を残す。計画だけで終了せず実装成果を保存する。

## Stop / recovery

局所補正で顔/体型を改造する必要が出たら、その問題範囲をHOLD。全身再生成・remesh・承認asset置換で救済しない。必要なら不完全な候補でも開けるblend/GLBを提出し、未成立能力を列挙する。新規課金・Tripo操作・外部uploadなし。サブエージェントなし。研究は上記で終了し、実装/根拠ある修正へ移る。

## 2026-10-15 Pre-Texture v002 implementation amendment (before asset edits)

Humanの今回の依頼を実装範囲とする。継承HEADは実確認 `379fe79ac2561b9a5796a4657c36d503d248cf04`、dirtyなし。fetch後mainは`8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`。元checkoutは別Shushu枝`a35f645`に並行変更があるため、専用worktree `C:/Users/chidj/.codex/worktrees/jill-pretexture-v002/Grimo`、枝`codex/jill-pretexture-v002-20261015`へ分離。旧正本と旧Evidenceは保存し、このPlan追記以外の結果は新規`rig-pretexture-v002/`へ出す。

1. 130骨/39ch/16anchorを継承。既存18 body morphと左右blinkの合計20を維持するため、局所瞼と必要な口内部をbodyの独立surfaceとして統合し、左右blinkを同meshへ移す方法を検討する。既存bodyのindexed Basis/UVを原則保持し、変更/除去した局所面と追加UVは明示する。元の眼/周囲socketも同blinkで退避/追従させ、円盤蓋の輪郭を顔から浮かせない。瞼は立体の上下皮膚と閉じ線を持つ。
2. 口縁の閉→小→中→大→閉を、局所顎/口縁のshapeと奥行きのある内壁/短舌で作る。歯・内部が閉口から突き出す場合は局所修復。固定の開口絵をskinへ印刷しない。Canonical笑顔の輪郭を基準に、閉口と半閉眼の本人性はHuman判定へ残す。
3. 翼root/膜は胸と独立前肢の所有を保持し、局所weights/小correctiveと安全域のfoldを反復する。首葉の根はhead/neck/chestの遷移に合わせる。肩/尾根は局所変形だけを補修し、全身remesh/再生成はしない。
4. Front/Side/3Qの実renderを、中間/終端/復帰と連続再生で直接確認。顔は拡大、接合は後3Qも確認。bounded proofだけを作り全Motionへ拡張しない。問題に応じてだけ再検証する。
5. UV checkerで外面/膜裏/瞼/口内/舌を表示。元UVの継承と新規局所UVの場所/面積/重複を測定する。同一neutral geometry/UVのTexture投入専用FBX/GLBを別出力し、再importと対応表で証明する。
6. 保存blend再読込、GLB fresh importと必要最小のPlayCanvasでskin/morph/anchor/UV/代表変形を確認。Tripo返却で骨/morph/UVの保持を仮定せず、Original UVの利用条件と元Rigへのtexture転写/再投影手順、Canonical色・最新Human指定の桃色horn・clover・眼・口内の仕様を記録する。Tripo公開公式情報は不足分だけ確認し、実UI/料金/アカウント状態の未観測はUNKNOWN。
7. 新規Evidenceへ比較、直接目視所見、失敗/修正、SHA256/絶対パス、Technical GO候補かHOLDの理由を保存。commit/push/remote照合。Human承認前の最終GO・upload・課金・正式Texture・全Motion量産は行わない。サブエージェントなし。

### 実装後の差分と判定

別名 `rig-pretexture-v002` に立体瞼/口縁/口腔/短舌/牙、root weightsと0.30rad限定foldを実装。元28,050 Basis頂点と保存した元UVは差0。20 Morphをbodyへ統合し130骨/39ch/16anchorを維持した。active UVは追加面の場所を確保するため `.006+.88*source` と右帯へ変更し、元UVを第2層に保持。これは未承認の明示的例外であり、元active UV不変とは扱わない。

実レンダーを反復したが閉眼が蓋状、口顎の段差、根とfold、UV伸びが残りHOLD。顔の局所切除案は外観を損ねたため撤回し、旧正本は変更していない。保存blend/GLB再読込、同一neutral surface/active UVのTexture専用FBX/GLB、限定PlayCanvas表示を確認。数値検査と外観合格を混同しない。新しい[Evidence](../rig-pretexture-v002/Evidence.md)に採用/撤回・連続再生・限界・Texture転写契約を記録する。Technical GO候補には未到達、Human最終GOなし、Tripo実行なし。
