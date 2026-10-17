# Jill v005 — Tripo 4K Texture移植 / 技術候補完成・外観HOLD

**2026-10-17 上口W追加調査：Human指摘のcream帯はtextureだけでなく追加 `mouth-skin` 面がWの下を塞ぐ形状問題。局所mask＋補助形状候補を別名保存したが、閉口/小開口の口角に破綻が残り修正FAIL・HOLD。元v005は置換していない。最新の原因・比較・保存/GLB/runtime検証・未達は [上口W REVIEW](upper-w-local/REVIEW.md)。以下のimage-only保持記録は元v005の履歴であり、新しい局所Geometry候補の主張ではない。**

2026-10-17。Human v004形状GOを継承しTexture付きblend / static GLB / 限定PlayCanvasレビューを作成。**正式外観GOはHuman専権、今回はHOLD。全Motion量産には進んでいない。**

## 成果とAuthority

[候補README](../../../../assets/grimo/production/jill/tripo/texture-return-v005/README.md) / [Gate](Gate.json) / [Manifest・全ファイルSHA](Manifest.json) / [remote照合](RemoteReceipt.json)。形状源は `codex/jill-mouth-profile-v004-20261016` の `3e40a529cee78c521b1de703c2257953e7e4f6f1`。開始main `8b5d13bc38061c0d574444416a039e70b9c61930` のAGENTS / Goal√map / Handoff、v004 Manifest / Evidence / TripoHandoff、v003 TextureSpec、Canonical / 承認Body-onlyを参照。古いv004文書の形状PENDINGは今回のHuman形状GOが更新するが、Texture GOを推定しない。

元checkoutは `codex/shushu-v004-motion-ready-gate-20261015` / `a4a90851c1ff85e584671f7c3decd7561e2baea1`、他キャラのdirtyあり。専用managed worktree / `codex/jill-texture-return-v005-20261017` で別名派生し元差分はstageしない。再生成・課金・サブエージェント・全Rig/Geometry再制作は未実施。

## 原本と対応検証

指定名 `jill-texture-input-neutral-v004.glb(1).glb` は不在。実名は `jill-texture-input-neutral-v004.glb.glb`、5,055,892 bytes / SHA256 `e5a76605ca3e6a6f43bc6dc9875d88923cfe3e07b44f3439a9c05e987b1cc117` で指定内容と一致。`source/tripo-return-original.glb` にbyte不変コピー。無変換抽出JPEGは4096×4096 / 2,695,970 bytes / SHA256 `cc11bd0bc9f839ecba4173c4202f770def2c26d8baa4f8564baa646af6913bb7`。

返却は1 Material・50,698頂点・61,321tri・UV0のみ・Skin/Morphなし。元neutral GLBは23 owner / 52,216頂点 / 同tri数。厳密な数値一致は全頂点で不成立。根本差は同じglTF Y-up軸・原点で高さ0.9995115995→1.0の均一倍率1.00048863888、UVの1/4096量子化、材質境界/seam分割の減少だった。

[双方向検証](correspondence.json)はUVと正規化座標からcorner候補を作り、三角形3corner・順序・winding・全face被覆・ownerを照合。位置だけの最近傍を合格条件にしていない。正逆の未対応0、61,321faceの単一対応、未被覆0・重複0・逆winding0。微小tongue4faceは未使用source face制約で解消しowner未決定なし。最終corner差は位置最大0.0213mm、UV最大0.7064px@4K。対応indexとcorner値をNPZ保存。

返却UVの微小faceには縮退があり失われた細部の完全復元は主張しない。面数/面積は[Gate](Gate.json)。正本UVを保持し検証face対応で元JPEGをbilinear resampleした。返却mesh / UV / skinで正本を置換していない。

## 局所補修

[処理記録](texture-repair.json)。v003の23owner mask、v004既存mouth-host-fill-maskを継承。左右瞼・眼周囲host・上口host・口外肌・口腔・舌・歯・角を局所maskで補修。肌は実JPEGの緑/cream、口内/舌/歯はCanonicalの明示位置から採色。全閉眼時の評価座標を使い瞼の緑/creamを連続化し、固定の開眼・二重の印刷アイラインを除去。口外肌/hostを同系creamで充填し、閉口へ開いた口/歯/舌を焼き込まない。実nose模様と立体形を保持。

レビュー用の暫定採色であり承認RGB swatchを創作せず、正式palette承認を推定しない。診断paletteの流用なし。PNGは補修用のlossless派生、元4K JPEGは不変保持。Normal/ORMは返却に存在せず採用なし。

翼表裏/edge・葉根の既存maskは露出確認/coverageに使用し返却artを保持。表裏を単色で塗り潰していない。元maskとface raster境界には7,106px差があり葉根/surfaceと翼front/back/edge共有境界に限定して確認。論理face-owner対応と画素raster完全一致を混同しない。後面と翼/尾のposed renderも確認した。

角の返却cream領域だけをCanonical舌の桃色系へ暫定補修し輝度差を保持。角/葉境界や色はHuman確認待ち。Canonicalで見える腿クローバーは返却にない。承認Body-onlyにも明示されず左右/位置/輪郭判断が必要なため推測で追加・鏡写ししていない。

## 保存・実レンダー・runtime

[保存contract](preservation.json)はGeometry/Basis/全20 Morph座標・polygon順/23 owner・全3 UV・weights・130骨・drivers・39ch・16 anchor差0。材質にUV0 `Jill_Texture_UV0_v003` を明示した画像nodeを追加しpacked blend保存→再読込。static GLB fresh importは全31,696 source頂点被覆、UV最大差6.053e-7、130骨/20 Morph/23材質/16 anchor、3 UV / BaseColor texCoord0。[reimport-proof](reimport-proof.json)の顔7状態（復帰を含む）は最大位置差3.073e-7m。材質外観まで数値PASSで保証しない。

[顔6状態×Front/Side/3Q](candidate-face-review.jpg) / [返却artと補修後](raw-vs-repaired.jpg) / [翼/尾/複合4状態×4視点](body-motion-review.jpg) / [Canonical/Body-only比較](authority-comparison.jpg) / [保存blendとfresh reimport](saved-vs-reimport.jpg)。Neutral・半/全閉眼・閉/小/大開口・翼open/fold・尾・複合・復帰のactual renderを直接開いて評価。元v004clay閉口横顔も参照し鼻下の立体縁を印刷口と誤認して形状変更しない。Workbench textureとPlayCanvas PBRは照明条件が異なりpixel一致を主張しない。reimport比較も背景/照明差あり。

PlayCanvas 2.22.2 / Desktop WebGL2で23 meshInstances全てSkin・20 Morph、16 anchor、全材質4096×4096 UV0。実UIで9代表状態、短い連続再生とneutral復帰を実施。[実測report](playcanvas-runtime.json) / [参照Morph照合](runtime-validation.json)。full blink=1、half=.5、口/翼/尾/複合の重み・代表骨world変化・全anchor有限を検証。限定texture動作確認であり39ch汎用runtime solver・全Motion・mobile・接地/IK再認証ではない。static GLBと確認clip GLBを別保管。

[PlayCanvas neutral](jill-v005-neutral.png) / [全閉眼](jill-v005-blink.png) / [閉口](jill-v005-closed.png) / [大開口](jill-v005-large.png) / [複合](jill-v005-combined.png)。

## Humanへ返すHOLD

1. 全閉眼の開眼印刷を除去したが、瞼の盛り上がる縁と外眼角の暗い隙間が目立つ。保持したv004形状の可愛さ判断が必要。Textureだけで消せたとはしない。fresh import比較には瞼の細かな面状の濃淡差も見え、座標/UV合格だけで描画の完全同一性を認定しない。この濃淡差の描画要因は未確定でHOLDに含める。
2. Canonical腿クローバー不在。Body-onlyとのAuthority解決と左右/位置/輪郭指示が必要。
3. 桃色角の境界/色、肌・瞼・口周囲の緑/cream連続性はPBR実表示でHuman判断が必要。暫定採色を正式paletteへ昇格しない。
4. 返却UV量子化/微小縮退により細部完全保持とは言えない。4K実見で判断する。

具体的阻害条件を残して安全な候補を提出。Human外観判断前に全Motion量産へ進めない。

## 再現

Blender 5.2.1 LTS。`blender --background --python-exit-code 1 --python scripts/blender/audit-jill-tripo-return-v005.py` → Python `scripts/qa/transfer-jill-basecolor-v005.py` → Blender `scripts/blender/jill-texture-review-v005.py -- lid-field` → 同Python `--repair-only` → Blender同script `-- build` / `-- render` / `-- clip` → Blender `scripts/blender/verify-jill-texture-glb-v005.py`。初回transferはscratchとメモリを使う。元GLBは書き換えない。

Node `scripts/3d/jill-texture-v005/serve.mjs` → loopback `http://127.0.0.1:8846`。他環境は `JILL_PLAYCANVAS_MODULE` に既存2.22.2 moduleの絶対pathを設定。確認状態をUIで保存しPython `scripts/qa/verify-jill-runtime-v005.py` → `scripts/qa/package-jill-texture-v005.py`。全体build不要。RemoteReceiptはartifact commit後に別commitで保存し自己hashを再帰参照しない。
