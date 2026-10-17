# Jill v005 上口W — 原因確定 / 修正候補FAIL・HOLD

2026-10-17。**要求は未達。Human承認待ちだけではなく、閉口・小開口の形状欠陥が残る。** 元のv005/v004を置換しない。全Motion量産へ進まない。

[鼻下の修正前後](before-after-detail.jpg) / [閉・小・大開口の比較](before-after-states.jpg) / [実PlayCanvas閉口の残欠陥](jill-upper-w-mouth-closed.png) / [小開口](jill-upper-w-mouth-small.png) / [neutral開口](jill-upper-w-neutral.png) / [反対3Qを含む保存blend](saved-states.jpg)。画像は実際に開いて確認した。数値PASSを外観PASSにしない。

## 開始時のAuthority

専用worktree `C:/Users/chidj/.codex/worktrees/jill-texture-return-v005/Grimo`、branch `codex/jill-texture-return-v005-20261017`、HEAD/remote `c4043471dbac3e58a39603802ecd18794a2bb9d6`、clean。fetch後main `336997db2b95244c17774258e2f5ff874a2adbc1` のAGENTS/Handoffも確認。元checkoutはShushu branch/他キャラdirtyを保持。ローカルAGENTS、Goal√map、Jill HANDOFF、v005 Evidence、v004 Evidence/形状源、Canonical/承認Body-onlyの比較画像を確認。Humanの最新v004形状GOを継承するが、今回派生のGOは推定しない。

会話の赤囲みは修正箇所の指示として使用。指定DownloadsパスのPNGは実filesystemでは不在だったため、会話添付を参照し、同名の別画像を指示原物として保存していない。

## 根本原因の切り分け

1. **主因は追加 `mouth-skin` の立体面。** 元bodyが持つW輪郭より低い位置に、v002由来の追加上口縁がある。その間の面をv004/v005のcream fillが肌色として見せる。単色でも帯は残り、[owner色](renders/diagnosis-owners-front.png)では追加面がWの下を塞ぐ。[単色](renders/diagnosis-clay-front.png) / [元texture](renders/diagnosis-texture-front.png) / [ray実測](diagnosis-rays.json)。
2. owner/maskの広さだけを狭めても物理面は残る。上側追加面を診断で隠すと、[旧口内・旧歯が露出](renders/diagnosis-upper-collar-removed-front.png)し、現在の口腔と二重になる。これは保存成果へのface削除ではない。
3. texture転写のWより上への印刷だけが原因、という仮説は単色レンダーで否定。鼻下の陰影にも形状要因がある。textureだけのoral塗り試験は[平面と境界線](renders/mask-trial-neutral-front.png)が残るため不採用。
4. 純texture問題ではなく、追加上口面・元W・裏の旧口内面の重なり。通常neutral開口で発生し、Morph時だけの露出ではない。ただし修正案の接触問題は閉口/中間Morphで悪化する。

## 保存した候補と差分（採用不可）

`assets/grimo/production/jill/tripo/texture-return-v005/` の別名 `jill-upper-w-local-v005.blend` / `.glb`、確認clip `jill-upper-w-review-bounded-v005.glb`、局所RGBA画像 `jill-basecolor-upper-w-local-v005.png`。元v005/v004・返却原本・元PNG/JPEGは変更なし。

mask単独で裏面露出を解消できないことを確認し、Humanが許可した局所補助修正を試した。元Wの深度不連続をrayで取得し、追加上口面と上側口腔/歯をそこへ接続。元body所有の旧口内/歯の2,918texelだけalpha=0（RGBは全画素同一）、body材質をglTF MASK/cutoff .5にした。UV再展開・材質owner再割当なし。

**追加口面のGeometryも変更したため、image-only修正ではない。** Basisの変更700頂点、最大36.185mm。閉口keyは接触をWへ移す試験を含む1,314頂点、最大32.344mm。[全21keyのID・範囲・最大差](geometry-delta.json)。閉口補助は下側追加口面にも及び、要求された鼻下〜上唇だけの完成修正として採用できる範囲・品質を実証できていない。下顎全体/顔全体を再設計した正本として扱わない。

[original-body-preservation](original-body-preservation.json)により、元bodyの28,050頂点はBasis/全20 Morphで完全一致。W・鼻・目・元の顔比率もそのまま。130骨/39ch/20 Morph/16 anchor、polygon順/owner、3 UV、weights、driversは[保持契約](preservation.json)で一致。舌の形状は保持。骨・Rig再制作、Texture全再生成、課金、他キャラ編集なし。

## 検証結果と未達

保存blend再読込の保持照合、Front/Side/右3Q/左3Qで閉口・小開口・大開口・combined・neutral/復帰の実レンダーを確認。fresh static GLB importは31,696 source頂点を全被覆、7顔状態の最大位置差3.073e-7m、3UV/130骨/20Morph/23材質/16anchorを保持。[reimport-proof](reimport-proof.json)。

PlayCanvas 2.22.2 / Desktop WebGL2で同候補clipを実ロードし、9代表状態・neutral・短い連続再生・復帰を操作、実画面を保存。[runtime-validation](runtime-validation.json)は149sample、Morph差最大6.358e-7、有限anchor、neutral復帰を確認。汎用39ch solver/全Motion/mobile試験ではない。runtimeで見える閉口欠陥もHOLD根拠に含む。

- neutral/大開口のFront/3Qでは、元のcream帯は消えW上辺になる。
- **閉口：口角から下側の追加面にしわ・面境界・食い込み。小開口：口角・歯の二重感/交差。** [実閉口](jill-upper-w-mouth-closed.png) / [実小開口](jill-upper-w-mouth-small.png)。Sideにも上側口腔の面が強く出る。可愛さ/自然さを保てたとはしない。
- 復帰の保存レンダーはneutralと画素一致。復帰できることは、途中の破綻を解消した証明ではない。
- 完了条件1/2は開口の限定状態で改善、**3/4/5/6は未達**（保存/runtimeに破綻が再現）。正式採用FAIL、総合HOLD。

次はこの候補を基準形状にせず、元v005から、上口のowner/旧口内面の可視境界と閉口時の接触を一体で再検討する必要がある。閉口の下側面を大きく持ち上げる今回の方法は繰り返さない。角・クローバー・瞼等の別HOLDは今回変更していない。

## 再現

Blender5.2: `jill-upper-w-local-v005.py -- diagnose` / `-- profile` / `-- field` → Python `scripts/qa/jill-upper-w-mask-v005.py` → Blender同script `-- build` / `-- review` / `-- audit` → Blender `verify-jill-upper-w-local-v005.py`。mask用xyz/owners cacheがなければ、既存v005のtransfer手順で再生成する。`--field`は一時場の計測だけでsourceを保存しない。

既存serveへ `JILL_REVIEW_MODEL`=新clipの絶対path、`JILL_REVIEW_EVIDENCE`=本directoryの絶対path、`JILL_REVIEW_PORT=8847` を指定。loopback限定。UI操作/保存後 `scripts/qa/verify-jill-upper-w-runtime-v005.py`。比較/Manifestは `scripts/qa/package-jill-upper-w-v005.py`。元v005の結果と混在させない。commit/remote照合は [RemoteReceipt](RemoteReceipt.json)。
