# Shushu Auto Rig v001 — Deformation Gate

2026-10-15 JST。開始branch `codex/grimo-motion-zero-based-design-20261011` / HEAD `718b618762d5375407191f5cd4fe06948a2c3b60`。最新Humanの**v006静的外観PASSを維持**。この検査は正式Geometry/Rig/Motionへの置換・新しいHuman承認ではない。

**判定：骨階層を局所補修の出発点として条件付き採用。入力ウェイトのままの正式Rig採用はHOLD。** Bind/受渡し/復帰は成立するが、頭→前肢の誤連動、右腕→胴の引きつれ、座位の支持と肉付きが未達。再Tripo・全面リトポを要求する根拠は得られていない。補修可能性そのものは次の別候補で実証する。

## 独立成果・保存検証

- [入力GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-tripo-autorig-v001.glb) SHA256 `803aeec97cb455a289e28baa9dd8cd281b97d2b54b92048a2e782228172f8932`。
- [検査GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-autorig-deformation-probe-v001.glb) SHA256 `9cd083f971bc5256e3118c56d9c339dec180a6dbb9cd36152164d89d5df40e3d`。**元BIN全バイト・元accessor/mesh/node/skin/材質/UV/weights/12画像を保持し、17代表時点の診断Animationだけ追加**。原本への変更なし。
- [検査Blender](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-autorig-deformation-probe-v001.blend)：タイムラインに姿勢名。0–384f、24fps、16秒の診断。大量Motion制作ではなく、機械的な変形/復帰検査。自然な演技timingの証明ではない。
- [保存GLB監査](saved-glb-audit.json)：65 joints、12 skinned meshes、99,565 triangles、Morphなし、12 Texture。階層はHips→Spine/Neck/Head・左右上腕/前腕/手・左右股/膝/足。循環なし。glTF Y-up / 正面+Z / 足底Y≈0 / 身長≈1。実動物の実寸・関節角度ではない。BlenderはZ-upへ変換。
- Bind skin評価の最大位置残差 `1.224e-6`単位。weightsは非負/有限、joint範囲内、合計誤差≤`1e-5`。全meshに有限UV、Blender各1 UV layer。12画像はrigprepの圧縮バイトとも一致。正規化は意味上の所有が正しいことを保証しない。
- Auto Rig出力とrigprepの頂点順は異なる。対応を仮定せず双方向最近傍属性集合で比較：眼球は約`0.006`単位奥へ、他部位は最大`3.42e-5`。UV集合差0だが厳密三角形対応の証明ではない。Neutralの全身・顔の印象は概ね保持、眼球の奥行き差は保留事項。v006と完全同一とは認定しない。

## 同条件画像と検査範囲

保存GLBをfactory Blender 5.2.1へ再読込し、固定正面/左3Q/左側面、768²、Cycles16 samples/seed0、元材質・同じ照明/地面で検査。[カメラ](cameras.json)、[独立Blender評価](blender-reload.json)、[glTF skin数値](deformation-measurements.json)、[原寸](renders)。両評価の最大変位値の差は最大`1.251e-7`。

[Neutral：v006/lowpoly/入力/保存](01-neutral-identity.png) / [左右頭回旋・傾斜・低頭](02-head.png) / [左右短前肢](03-short-forelimbs.png) / [未成立の座位試行と途中復帰](04-seat-unachieved.png) / [7復帰点](05-return.png) / [接点とrelease](06-contact-tangency-only.png)。画像は等方縮小・配置・ラベルのみ。外観の修整なし。原寸も確認した。

頭yaw±15°、Neck roll10°/pitch12°、上腕/肘各25°・手首10°、股25°/膝40°から股50°/膝80°へ、足首の逆向き回転・骨盤下降を代表試行した。[指定](poses.json)の軸はrest世界方向から各骨へ変換した診断差分で、解剖学的可動域/安全上限ではない。独立した肩甲帯運動、全可動域、全途中フレーム、動的荷重は未検証。

7復帰点すべてでBlender評価頂点差0、各3方向画像の画素差0。入力Neutral/保存Neutralも画素一致。[復帰比較](return-image-comparison.json)。途中の破綻が解決されたことや実演技の自然さを意味しない。

## 観察 → 専門的根拠 → 原因仮説 → 最小補修

既存[解剖・変形notes](../geometry-v003/ANATOMY_AND_DEFORMATION_NOTES.md)、[Motion-to-Anatomy契約](../../../motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md)のQ02/03/04/08、H/J4/K2–3、[Motion空間観察](../../../../grimo/knowledge/research/GRIMO_PARTNER_EXPERIENCE_MOTION_ANATOMY_EVIDENCE.md)の支持・局所因果・復帰を使用。以下の角度/数値はこの資産の観測値、補修案は制作上の提案。

| 観察結果 | 根拠と区別 | 原因仮説 | 次候補の最小方針 |
|---|---|---|---|
| 頭yaw15°だけで左右pawが最大0.0282/0.0291移動。耳の剛体Head追従との差は最大約0.0091、眼は約0.0012。顔の印象は保つが耳/肩/首のつながりは要補修。 | Blenderのvertex-group所有規則[3]、契約Q02/04。動物角度の転用なし。 | PawのHead平均1.08/1.02%、耳のSpine2平均9.2%、顔部品にもSpine2。首下の柔らかい移行と無関係部位の混入が未分離。 | 首/耳根の意図した柔らかさを残し、pawのHead混入と顔部品の相対ずれを局所修正。全Head100%への一括置換はしない。 |
| 肩根〜肘/手首の曲げで左右pawのsigned surface volume約95.3/95.5%。右では胴も最大0.0622引かれ、胴edge比の極値0.20–2.65。脇の輪郭と短腕の丸みが崩れる。 | 関節近傍の縮みはBlender資料[3]、輪郭を別制御する制作研究[2]。数値は表面幾何で筋肉/脂肪の実測ではない。 | TorsoにRightArm/RightForeArm平均0.199/0.448%、左の対応混入なし。丸pawに人型指系の複雑な配分。 | 胴/前肢の所有境界を先に整理。左右を盲目的にコピーせず各root/自由区間を確認。残る肘/脇/手首の潰れだけ局所corrective候補。腕の伸長/指新設なし。 |
| seat-entryでも足低帯0.0183ずれ、最低Y=-0.0172。seat-attemptは最低Y=-0.0534、513頂点がY<-0.001。側面でお尻の支持がなく、座位ではない。 | 犬の立ち上がり実験/モデル[1]は多関節と支持の連動を扱う。他種からの類推でありShushu用の角度/荷重値ではない。 | 診断FKの骨盤下降/股膝足首回転に足接点拘束がない。失敗は今回のpose/controlにも依存し、骨格では座れないとの証明ではない。 | 足支持frameと骨盤下降を協調する制御を先に作り、お尻支持・足裏・重さを側面/3Qで確認。床への頂点flattenで隠さない。 |
| 腹に局所的な凹み/陰影の乱れ、腿/足が腹へ押し込まれた印象。seat-attemptでTorso表面volume約96.4%だが、局所輪郭は未達。 | Pixar[2]は見えるprofileとsurface detailを制御。既存notesのDisney/DreamWorks事例も基礎変形と局所形状の分担を示す。これは制作技術の根拠。 | Skinだけでは座位の腹・お尻・腿の形を保てず、関節位置/weights/controlと表面補正の切分けが必要。 | 支持を解いた後に腹/臀/腿の少数局所correctiveを検討。総volumeが近いことを丸さのPASSにしない。筋肉/脂肪simulationは不要。 |
| 左pawへ検査sphereを接線配置し、最短surface gap≈0、releaseで0.0419。顔/胴/他部位にはsphere干渉なし。足は立位位置を保つ。 | 契約K2の実面/ownerとrelease、既存短腕接触notes。幾何観測のみ。 | [接触検査](contact-check.json)は一頂点の接線到達。押圧応答・把持・荷重・自発的接近の制御は入力にない。 | 届く低いtargetを保ち、次候補で小さな局所圧縮と解放を検査。現在のsphereを「持った」「柔らかく受けた」とはしない。 |

大頭の質量・密度は未定義。足の位置と見かけの支持は評価したが、**重心の実数/動的安定はUNKNOWN**。座位の臀接触も未達。閉じた部位のsigned surface volumeは補助指標で、自己交差/局所体積/物理組織の保証ではない。頭の表情合成、独立gaze/耳、押圧、実機もUNKNOWN。Humanの可愛さ・自然さの確認は別Gate。

## 採用した出典と次タスク

[1] [Ellis, Rankin & Hutchinson (2018), Limb Kinematics, Kinetics and Muscle Dynamics During the Sit-to-Stand Transition in Greyhounds](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2018.00162/full)：既存notesの一次研究を必要箇所だけ再確認。犬の実験/モデル結果と、Shushuの制御提案を区別。

[2] [de Goes, Sheffler & Fleischer (2022), Character Articulation through Profile Curves](https://research.pixar.com/docs/2022.SiggraphPapers.GSF.pdf)：既存研究を再利用。profileとsurface detailの分担のみ適用。映画用solverを導入したとはしない。公開PDF全文の取得は容量制限で失敗し、今回の確認は検索で読めた一次論文の要旨/該当節と既存notesの範囲。

[3] [Blender公式 Armature Modifier](https://docs.blender.org/manual/en/4.4/modeling/modifiers/deform/armature.html)：追加確認はvertex groupsとPreserve Volumeのみ。公式bundled manual `manual/modeling/modifiers/deform/armature.rst`も確認。quaternion方式は縮みを改善し得るが、誤所有ウェイト/支持を直さず、GLB受渡し先でも同じ結果になるとは仮定しない。今回は入力と同じ通常skinを維持。

次タスクは**v006の眼球奥行き差を同条件で扱ったうえで、Head/前肢/胴の局所所有ウェイトと足支持を別候補で補修し、同じGateを再実施**。その後、必要部位だけcorrectiveを追加。

[v003読み取りinventory](v003-readonly-inventory.json)：正式asset/proofともArmature0、457 Shape Keys（Basis/合成補正含む）、290 drivers。proof12 Actionsは1–285f。`HeadTurn/HeadTilt/HeadRest`、`Seat025/050/075/100`、`Offer/Hold/SelfContact`、blink/gaze/口/頬と合成driverを、**意味・到達target・表現分離・座位profileの参照**として再利用する。今回GLBは静的書出し→削減→Auto Rigで頂点/部品構成が異なり、旧shape座標/Actionsの直接コピーや骨retargetは不可。必要な局所deltaの対応付け/再作成、bindで0に戻る検証、driver結果のMorph/Animationへの受渡し検証が次段階。既存285f proofは保存したまま比較正本にする。

原本/v006/v003 Shape Keys/proof/他キャラ/開始時ユーザー画像差分等1,035入力をhash保護。変更はHandoffと既存解剖notesへのEvidence追記のみ許容。[保護結果](protected-inputs-result.json)。Goal√map変更なし。Tripo再実行/課金/全面リトポ/PWA改修/全体build/網羅testなし。

再現：`python -B scripts/3d/probe-shushu-autorig-v001.py prepare` → factory Blenderで `scripts/blender/review-shushu-autorig-v001.py`、`-- --contact`、`-- --v003` → `python -B scripts/3d/probe-shushu-autorig-v001.py boards` / `verify`。既存Blender UIは使用せず独立background process。最終commit/remote HEADはチャットのGit照合結果を参照。
