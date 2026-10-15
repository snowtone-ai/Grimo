# Jill Pre-Texture v002 — implemented repair / HOLD

2026-10-15 JST。**別名の実装修正版は保存したが、Pre-Texture Technical GO候補には未到達。最終GOはHuman専権。** 瞼/口元の連続性、翼・葉の接合、自然なfold、UVの密度/伸びが未解消。upload・課金・正式Texture生成・全Motion量産は実行していない。これは承認済み正本への昇格ではない。

## 継承と保護

- 実確認した継承枝 `codex/jill-rig-other-v001-20261015` / HEAD `379fe79ac2561b9a5796a4657c36d503d248cf04`、dirtyなし。専用枝 `codex/jill-pretexture-v002-20261015` / worktree `C:/Users/chidj/.codex/worktrees/jill-pretexture-v002/Grimo` に分離した。
- fetchで確認したmainは `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`。そのAGENTS/Goal√map/production Handoff、Jill HANDOFF、既存Plan/Evidence、Motion-to-Anatomy Q01/Q06/Q09/Q15を読んだ。既存Planへの事前追記を `202eae98ea92be431b4e8062330ab8b637891fa2` で先にcommitした。
- AuthorityはCanonicalと承認Body-only front/left/right/back。[直接比較](00-authority-comparison.jpg)。未承認Motion画像はAuthorityにしていない。承認済みの瞬き/口/収納極値poseは不足している。
- 元checkoutはShushu枝 `a35f645858f806edb162bd521f1b85f7871481f4`。並行Shushu変更、ルートのFBX/GLB、旧Rig正本、旧Evidence、他キャラは編集していない。事後再確認でも旧Jill worktreeは元HEADでclean。保護元ファイルと成果物の絶対パス/SHA256は [Manifest](Manifest.json)。

Manifestのhashは記載した絶対パスの作業ファイルbytes。binary正本はGit/LFS往復でも同hashを照合する。textのhashは別checkoutの改行変換（本repoはcore.autocrlf=true）で変わり得るため、他環境でのtext同一性はGit commitも参照する。

## 実装差分

130骨 / 39意味ch / 20 Morph / 16 anchorを継承。別々だった左右瞼Morphをbodyに統合し、眼の退避も同じblink Morphへ含めた。瞼・口縁・顎側の皮膚、奥行きのある口腔、短い立体舌、小牙を追加。元の深い口内面だけを局所除去し、外側の顔/体型を切り直す案は外観が崩れたため採用しなかった。現在は31,739頂点 / 32,280 polygon / 61,321 triangle。元28,050頂点のBasisは座標差0で残るが、追加面の存在と口内部の面除去により元モデルと同一トポロジーではない。

翼は胸→root→外側/膜への局所weightsを調整し、左右の所有を分離。首葉・尾葉の付根をowner骨へ段階追従させた。既存WingOpen/Fold correctiveの変位を0.5倍に抑えた（新しいDQ solveではない）。root foldは0.48→0.30 radへ制限。これは後方スイープであり、自然な胴沿いの収納を保証しない。[修復記録](repair-report.json)、[制御契約](control-contract.json)、[Blender mapping](runtime-mapping.json)。全身再生成・一括remeshなし。

## 実レンダーの所見

Front/Side/3Qで中間・終端・復帰をレンダーし、顔拡大・後3Qの根も直接開いて目視した。比較用画像のclay色は正式Textureではない。Canonicalの配色や眼の輝きによる可愛さはまだ検証できない。

| 部位/遷移 | 実画像 | 判定と具体的な残り |
|---|---|---|
| 閉→小→中→大→閉 | [顔3視点](face-mouth.jpg)、[全身](motion-mouth.jpg) | 実立体の口腔・舌は動き、閉口で暗い開口は閉じる。顎が別の板に見え、上口縁が二重。大開口の内側も粗く、自然な閉口/Canonical笑顔の本人性はHOLD |
| 開→半閉→閉眼→開 | [顔3視点](face-blink.jpg)、[全身](motion-blink.jpg) | 上下皮膚と閉じ線を持つが、全閉眼が丸い蓋に見える。半閉時の輪郭も厚く、Sideで黒い眼面の隙間が残る。HOLD |
| 頭回転 | [3視点](motion-head.jpg)、[根](04-roots.jpg) | 顔全体の体積は大きく潰れない。首葉の根と重なりは硬い。首肩の自然さHOLD |
| 独立翼・fold | [L](motion-wing-L.jpg)、[R](motion-wing-R.jpg)、[fold](motion-wings-fold.jpg) | 左右独立変形と復帰を確認。膜は板状に見え、根/首葉/肩の層の接続が未完成。限定スイープを安全な収納foldとは認定しない |
| 低paw | [L](motion-paw-L.jpg)、[R](motion-paw-R.jpg) | 低い差し出しと復帰、胴の丸みは維持。肩の重さ/根の接合はHOLD。接触支持・荷重の証明ではない |
| 尾・葉 | [3視点](motion-tail-leaves.jpg)、[根](04-roots.jpg) | 太い巻尾のボリュームは維持。葉の独立性はあるが付根が重なった部品に見える。接合HOLD |
| 複合 | [L](motion-combined-L.jpg)、[R](motion-combined-R.jpg) | 頭・翼・paw・尾・表情を同時評価。顔の上記欠陥が残る。全組合せの貫通なしを主張しない |

[追加の右側/尾/複合一覧](06-other-motion-review.jpg)。55点で有限座標、mouth以外の復帰はneutralと差0。[pose検査](pose-validation.json)。305フレーム/24fpsのbounded proofだけを作成し、完成Motion集には広げていない。連続再生と実行環境の範囲は下記。

`iterations/` は失敗した局所切除/接合や途中版の記録。採用正本/承認参照ではない。元の外観を守るため、傷状の切り口が出た案を撤回した。元Basisが一致すること自体は、追加瞼/口縁が本人らしいことの証明にならない。

## UVとTexture入力の対応

[全可視方向・口内・閉眼・掌・膜裏のchecker](05-uv-checker.jpg) を目視した。範囲はFront/左右Side/3Q/Back/後3Q/Top/Bottom、閉口/閉眼/大開口、翼open/fold、両paw。重なった根や口腔最奥は単一の外側cameraから全ては見えず、隠れ面まで完全塗装可能と認定しない。部位間の密度差、追加面の伸び/細長い島が目立つためUVもHOLD。大きな空白面をTextureで埋めて接合を隠す扱いは禁止。

**UV継承の例外**：元UVは第2層 `v002_Source_UV_Preserved` に差0で保存。active `Tripo_Input_UV` は継承島を `.006 + .88*source` へ縮小移動し、右帯に瞼/口/舌/歯を配置した。空き領域不足への実装上の選択であり、元active UVをそのまま保持したとは言わない。変更したactive atlasはHuman未承認。元の縮退UV三角形1枚をactiveだけ局所補修（loops 54601/54603/54604）。最終のゼロ面積UV三角形は0/61,321。全重複/十分なpadding/texel densityの合格は未証明。[UV検査](uv-validation.json)。

同じ保存Rigの全ch=0 neutralから骨/Morph/anchor/animationを除いたTexture投入専用FBX/GLBを作成。再読込でSkin面の位置とactive UVを照合した。出力のseam分割/triangulation/浮動小数丸めにより量子化corner hash自体は一致しないため、距離/UVの許容差検査を対応の証拠とする。元RigをTripo返却meshで置き換える用途ではない。

## 保存・再読込・表示の限定検査

| 検査 | 測定結果 | 限界 |
|---|---|---|
| 継承Basis / 保存した元UV | 28,050頂点の最大差0 / 保持111,777cornerの差0 | 追加面・面除去・active UV変更は上記の通り |
| Skin weights | 最大4 influence、合計誤差 ≤8.16e-8 | 自然な接合や接触を保証しない |
| 保存blend fresh process | 13代表poseの最大差0 | 全ch組合せではない |
| Rig GLB fresh import | 13pose、Skin面の双方向最近点最大9.7841e-6m、許容1e-5m以内 | 頂点order同一ではない。全frameの数値比較ではない |
| GLB anchor | 16個、代表pose最大差4.432e-7m | 任意接触面/装備fit未保証 |
| Texture neutralとRig | 面の最大差0 | clay材質のみ |
| Texture GLB再読込 | 位置差0、UV差2.981e-8 | UV品質承認ではない |
| Texture FBX再読込 | 位置差1.745e-7m、UV差0 | FBXのRig保持検査ではない。骨を含めていない |

[継承検査](inheritance-validation.json)、[再読込検査](roundtrip-validation.json)。初回の大きな比較誤差はBlender GLB importが作る非Skinの骨表示用Icosphereを含めたため。ARMATURE modifier付きの実Skin面に限定して再検査した。[診断](roundtrip-diagnostic.json)。この修正を外観の合格理由には使わない。

ローカルPlayCanvas **2.22.2** で保存GLBを表示した。[実画面](playcanvas-playback.png)、[runtime記録](playcanvas-runtime.json)。130 joint/5 skin instance、各20 Morph、16 anchor、3 camera、sampled animationの骨/Morph変形とUV checker切替を確認。元driver/IKはGLBに移植されず、39chから任意poseを作るruntime solverとスマホは未実装/未検証。viewerは作業用loopbackのみで本番appを変更していない。2.22.2には2.23以降のEngine inspector hookがないため、viewer内の実状態をJSON出力した。

ブラウザ録画は背景タブの制限で17コマしか記録できなかった。`iterations/browser-recording-throttled.*` はその失敗記録で、連続性の合格証拠にしない。保存Rigの全305frameをFront/Side/3Qで実レンダーした連続映像と、その目視範囲は `PlaybackReview.md` に記録する。

## Texture仕様と次の阻害条件

[TextureSpec](TextureSpec.md) はCanonical配色、最新Human指定の桃色horn、クローバー、眼、口内の仕様。[TripoHandoff](TripoHandoff.md) はOriginal UVの公開案内、実ログインUI/実料金のUNKNOWN、返却で骨/Morph/UV保持を仮定しない転写手順。追加調査は不足していた公式Original UV資料に限定した。Tripo操作なし。

次の局所修復は、顔の外側と連続した眼窩/瞼・口縁/顎の面構成、歯/舌の大開口形状、根の接続と膜foldの形状、active UVの密度とpaddingを対象とする。承認済みの閉眼/閉口/fold極値参照も必要。現状の見え方をHumanに承認済みと扱わず、Textureで救済するためのuploadは行わない。

## 再現

Blender 5.2.1 LTS。`scripts/blender/repair-jill-pretexture-v002.py` → `prove-jill-pretexture-v002.py` → `update-jill-pretexture-uv-v002.py` → `package-jill-pretexture-v002.py` → `audit-jill-pretexture-contract-v002.py`。checkerとplaybackは保存正本を変更せず診断画像だけ出力する。`inspect-jill-pretexture-v002.py` が前処理。全てこの専用worktree内で実行する。

viewer: `node scripts/3d/jill-pretexture-v002/serve.mjs`、`http://127.0.0.1:8842/`。engineの実パスは `JILL_PLAYCANVAS_MODULE` で指定可能。現環境は元checkoutの既存PlayCanvasを参照する。正式Texture生成や外部送信を行う機能はない。
