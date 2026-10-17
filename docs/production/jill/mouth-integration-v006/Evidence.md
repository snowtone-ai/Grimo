# Jill v006 — W上口と口周囲の一体化

2026-10-18。**口の局所修正候補を作成・検証。モデル全体の完全完成は未達。2026-10-18 Human回答「口の外観はGO」を受領。** 元v005/v004は置換していない。[成果物](../../../../assets/grimo/production/jill/tripo/mouth-integration-v006/README.md) / [比較](before-after.jpg) / [口の拡大](mouth-detail.jpg) / [保存6状態×4視点](saved-states.jpg) / [中間・同時入力](overlap-sweep.jpg) / [頬接触・頭/呼吸](interaction.jpg) / [実runtime遷移GIF](runtime-mouth-transition.gif)。

## Authorityと開始状態

専用worktree `codex/jill-texture-return-v005-20261017`、開始HEAD `74596c9673434f4120b300ec0c96fb9c663fc4d0` / remote一致、開始clean。fetch main `336997db2b95244c17774258e2f5ff874a2adbc1` のAGENTSと当該branchのAGENTS、Goal√map、production Handoff、Jill HANDOFF、v004/v005 Evidence、Canonical/承認Body-onlyを参照。ユーザーの最新GOALは、Motion/表情変化/中間/復帰でも外観を守り口周囲の派生問題を解消したTexture込み完成モデル。技術数値をHuman外観承認へ置換しない。[作業方針](Plan.md)。

元checkoutには他キャラのuser変更があるため編集しない。元v005 blend/GLB/PNG、v004 blend、CanonicalはGit blob一致・SHA保存済み。[保護照合](protected-sources.json)。過去の失敗候補と証拠は [上口W v005履歴](../texture-return-v005/upper-w-local/REVIEW.md) に残す。

保存前に再fetchしたmainは `8b9d736abca118de5bd1e2e1f64b961e25f0ba42`。AGENTS/Goal√map/Jill HANDOFFの差なし、production Handoffのapp/backend決定追加を確認。Jillへmainを一括merge/rebaseしていない。

## 根本原因と選択肢

元のW字マズル、後付け `mouth-skin` 外皮、後付け口腔の境界が別々に存在し、追加上辺がWより下にあった。cream fillはこの物理的な帯を塗り、不要面を見えやすくした。口上辺のTextureはみ出しだけでも、Morph時だけの露出でもない。neutralと開口の実レンダーに既に存在する。

1. Texture/maskのみ：面の段差/上辺位置は残る。元面を隠すだけでは裏の旧口内/旧歯を露出する。前回実試験で不足を確認。
2. 追加口縁をWへ移動：neutral/大開口で改善しても、独立した下唇/hostの閉口接触が交差し口角にしわ。前回不採用。
3. **局所の肌・口縁・口腔を共有境界で一続きにする**：元の顔比率を保ち、重複面と別々の接触面を解消する今回案。全顔/Rig/Texture再制作は原因解消に不要。

単に保存やGLB輸送に成功したことを採用理由にせず、前案の閉口・小開口・Side欠陥が消えるかを実画像で評価した。

## 実施修正と明示差分

- 元bodyの鼻下〜口の局所511 polygonと、重複する追加 `mouth-skin` / `mouth-inner` を除き、一体の肌/口縁/口腔へ置換。鼻・目・顔輪郭/全身は保護。これは局所Geometry/UV補助修正であり、全Geometry/全UV不変という主張はしない。
- W位置は元v005/v004形状の実レイ交点から取得。旧歯の不連続を除いて左右を対応付ける。上辺と下辺の口角を共有し、閉口時はWの上下へ接触させる。
- 途中案の口角の折れは、上側にある笑顔口角を、楕円の角度と同一視して外周へ対応させたことが原因だった。口縁の実位置から外周への対応を取り直し、面の反転を除去。境界と内側の接続に制約付き三角分割を使用、交点生成0。[境界検証](border-triangulation.json)。
- 残した30,425 faceのvertex順・owner・3UV loop値に差0。既存vertexのウェイトは全保持。新961 vertexは既存 `DEF_head` へウェイト1。mesh総vertex 31,739→32,700（削除面の未使用旧vertexも保持）、polygon 32,280→31,494。GLBには使用30,880 vertexを対応付け、seam分割後52,947 vertexとして再import。
- 新しい肌/口腔UVは、除いた同ownerの専用島を再利用/分割。残存面/他部位のUVは変更しない。元packed 4K PNGはバイト一致。alpha切り抜きや新しいTexture塗装は使用しない。
- 既存の小さな歯8 vertexをWへ追従、閉口では内部へ退避。舌は既存形状を保持。閉口Morphに残っていた元局所34 vertexの旧補正を除去し、新しい一体面へ閉口を担当させる。他の元vertexのBasis/Shape差分は歯8点に限定。
- 開口と左右smileの3 driverへ `open/smile × (1-close)` のゲートを追加。閉口優先で同時入力と中間を連続化。39ch/20Morphを増減せず、130骨/16anchorとその他driverは保持。

[局所差分・全保護照合](local-preservation.json) / [保存blend再読込](saved-blend-proof.json)。新patchに関係するedgeの面共有数は全て2で、接続の開き・3面以上の接続は0。

## 実検証

**保存blend実レンダー:** neutral、mouth-closed/small/large、combined、復帰をFront/Side/左右3Qで撮影。同一カメラで元v005と比較。前案のcream帯、閉口/小開口の口角しわとSideで露出する口腔面は、この範囲の確認画像では見えない。Wが上辺として読め、cream/green境界を保つ。この口の修正は2026-10-18にHuman外観GO。モデル全体GOとは分ける。

**中間/干渉:** close=0/.25/.5/.75/1 × open=0/.5/1にsmile L=1/R=.5を重ねた15状態。左右smile、両側smile、大開口+両smile、閉口+開口+両smile、片/両頬接触、頭のyaw/nod/tilt、呼吸/胸と開閉口を重ねる。[実レンダーと参照値](expression-sweep.json)。保存neutral復帰は4視点で画素一致。[復帰](recovery.json)。

**39ch:** 全authoring範囲のmin/0/maxで有限Geometryとneutral復帰を確認。[全channel実測](all-channel-sanity.json)。個々の非zero端点をFront/Side/3Qで実レンダーし、[可動範囲1](motion-envelope-1.jpg) / [2](motion-envelope-2.jpg) / [3](motion-envelope-3.jpg) / [4](motion-envelope-4.jpg) / [5](motion-envelope-5.jpg)へ整理。これは全Motion演技/IK接地/座位/スマホの完成承認ではない。

**fresh static GLB:** owner+UV+positionによる単一頂点対応で使用30,880 vertexを被覆、未対応0。10顔状態の最大位置差3.073e-7m、130骨/20Morph/23材質/16anchor、TEXCOORD_0/1/2、BaseColor UV0を確認し実レンダー。[再import証明](reimport-proof.json)。ここでのcombinedは顔Morphの組合せ。全身骨のcombinedは次の実runtimeで確認する。最初に全身combinedをstatic neutral rigへMorphだけ与えて比較した誤った検証は、骨姿勢差を検出してFAILとなったため、検証範囲を正して再実施した。

**実PlayCanvas:** Engine2.22.2 / Desktop WebGL2。13代表状態+neutral、4.5秒の連続再生と復帰。23skin/20Morph/16anchor/4K UV0、Morph最大差9.537e-7、代表骨のworld変化、全anchor有限、neutral復帰を確認。[実測](playcanvas-runtime.json) / [照合](runtime-validation.json)。[neutral](runtime-neutral.png) / [閉口](runtime-mouth-closed.png) / [小開口](runtime-mouth-small.png) / [大開口](runtime-mouth-large.png) / [同時入力](runtime-closed-open-smile.png) / [combined](runtime-combined.png)。短いbaked検証clipであり、汎用39ch runtime solver/全Motion/実機mobileの認証ではない。

**GLBの直接操作:** Blender driverはglTFへ運べないため、[口controller](../../../../scripts/3d/jill-mouth-v006/mouth-controller.mjs)を提供。既存4 Morphだけを設定し、他Morph/骨には触れない。GLB clipのanimation writerを止めた直接入力15状態が全23instanceで保存blendのdriver値と一致。[照合](direct-mouth-runtime.json)。さらにanimationを含まない**static GLBそのもの**を別の実PlayCanvasへロードし、同じ15同時入力と21段階の連続開閉、neutral復帰を操作。[static実測](static-mouth-runtime.json) / [static証明](static-mouth-runtime-proof.json) / [static実画像](static-runtime-mouth.jpg)。口制御はbakedポーズ専用ではない。生の4weightを独立加算するconsumerはこの閉口ゲートを適用する必要があり、汎用Engineが自動でBlender driverを復元するとはしない。

## 完了監査と残る仕事

| 要件 | 現在の証拠 / 判定 |
|---|---|
| 鼻下の不要帯を消し、口上辺W | 指定の開口Front/左右3Qとruntimeで改善確認、2026-10-18 Human口外観GO |
| 閉/小/大/複合/中間/復帰 | 保存blend・実runtimeと上記sweepで確認。全ての任意組合せの数学的保証とはしない |
| 口肌・歯・舌・口腔 | 共有境界/歯追従を実画像で確認。派生しわ/口腔露出は今回範囲で再現せず |
| 顔の可愛さ・比率 | 口はHuman GO。モデル全体の外観gateは別途残る |
| 保存blend/GLB/PlayCanvas | 上記範囲でデータ保持・実画像を確認 |
| Texture込みモデルの完全完成 | **未達/HOLD**。既存の全閉眼外眼角の隙間/瞼縁、角の暫定色境界、腿cloverは2026-10-18 Humanが「Canonicalに沿って追加」と指定しAuthority解決、追加作業は次の派生へ分離。全Motion/スマホは今回の認証範囲外 |

今回の元依頼の「他HOLDへ横滑りしない」を保護し、口の変更に瞼/角/模様の変更を混在させない。最新の完全完成GOALを縮小せず、上記を残作業として追跡する。原本破壊・新規課金・Texture全再生成・Rig再作成・全Motion量産は行っていない。

## 再現

Blender5.2: `scripts/blender/jill-mouth-integration-v006.py -- inspect` → `-- cutprobe` → `-- patch` → `scripts/blender/jill-mouth-validate-v006.py -- prepare` / `-- compare` / `-- sweep` / `-- interaction` / `-- motion-envelope` / `-- clip` → `scripts/blender/audit-jill-mouth-v006.py` → `scripts/blender/verify-jill-mouth-glb-v006.py`。intermediate blendは再生成できる開発出力としてignore、配布候補はREADMEの3ファイル。

既存 `scripts/3d/jill-texture-v005/serve.mjs` に `JILL_REVIEW_MODEL`=v006 bounded GLB絶対path、`JILL_REVIEW_EVIDENCE`=本directory、`JILL_REVIEW_PORT=8848`、`JILL_REVIEW_LABEL=Mouth Integration v006` を指定しloopbackで確認。実UI操作/保存後 `python scripts/qa/verify-jill-mouth-runtime-v006.py`、最後に `python scripts/qa/package-jill-mouth-v006.py`。Playwright skillのCLIで実ブラウザを操作した。最終hashは [Manifest](Manifest.json)、commit/push照合は [RemoteReceipt](RemoteReceipt.json)。

直接口操作は追加で `JILL_REVIEW_MOUTH_CONTROLS=1`。static実試験は `JILL_REVIEW_MODEL`=static GLB、port8849、`JILL_REVIEW_CAPTURE=static-mouth-runtime.json` を指定。runtime統合にPlayCanvas apply-conventions/inspect-runtime skillを参照し、installed2.22.2のMorphInstance宣言でname指定getWeight/setWeightを確認。Engine2.23 hookはこの版にないので追加global app参照は作らず、frameendで自前QAレポートを採取した。

実ブラウザで各URLを開いた後、Playwright CLIの `run-code --filename scripts/qa/capture-jill-mouth-v006.js` で定点・中間・連続開閉のactual canvasを再取得できる。GIFはstatic GLBの21段階の実canvas画像から作成し、返りを逆順で含む。生成/補間画像ではない。

## Human判断 — 2026-10-18

比較右側のW上口と閉/小/大開口を含む口修正は「口の外観はGO」。腿クローバーは「Canonicalに沿ってクローバーを追加する」。口の承認済みv006を保存し、模様は別派生で追加する。Canonicalに見える大腿の四つ葉と茎を参照し、裏側/未表示側への推測複製はしない。static runtimeの21段階のうち閉口付近を含む6 actual canvasも直接開き、帯/しわ再発が見えないことを確認した。
