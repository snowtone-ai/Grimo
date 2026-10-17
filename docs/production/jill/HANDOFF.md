# Jill — NOW

**2026-10-18 / NOW v009。口Human GO、Canonical腿クローバーHuman OK、目外観Human GO。角は変更不要・現状維持。** [最新Evidence](eye-join-v009/Evidence.md) / [実顔PNG](eye-join-v009/runtime-face.png) / [比較](eye-join-v009/eye-before-after.png) / [瞬きGIF](eye-join-v009/blink-runtime.gif)。各部位のGOをモデル全体のHuman完成GOへ読み替えない。

branch `codex/jill-texture-return-v005-20261017`、今回開始 `cc080bc30590247d8604d94c0a5d5dced6f595a5`。main fetch `534694dae8087dec852de0f26b472a6dcd26ca70`。既存Jill worktreeで継続し、別checkoutのShushu/user変更を保護。最新GOALはTexture込みJillがMotion/表情/中間/復帰でも承認外観を維持する完全完成。技術PASS≠Human完成GO。公開commit/remoteは[receipt](eye-join-v009/RemoteReceipt.json)。

Human screenshot593の指定は「両目外側の縦の紐を削除」。v008はhostの古い眼Textureを消しただけで帯を残しHuman FAIL。原因は後付け瞼の外周/中間面が肌・実眼面から浮くこと。外側だけの折込み試作は中間/閉眼の破綻で不採用。v009は既存左右瞼1,920頂点をbody_skinと実眼面へ沿わせ、Blink閉眼面も接続。原眼126頂点のBlink後退を解除。Topology追加削除なし。実眼Basis/他Geometry、3UV、weights、全driver、130骨/39ch/20Morph/16anchor保持。Blink以外の相対Morph差<2e-7m。

保存blendのneutral・口閉/小/大/combined/復帰、Blink .25/.5/.75/1、左右wink、gaze両軸をFront/Side/左右3Qで実レンダー。fresh GLB再importは30,880使用頂点被覆・欠落0、7顔状態位置差<2e-6m。口5状態Front領域画素一致。実PlayCanvas2.22.2で23skin/Morph・20各・16anchor、左右Blink/口入力、21段階閉眼→開眼・復帰、頭/翼/尾/顔の限定clipも確認。復帰canvas画素一致。実画像を自分で開き、報告にも添付する。

**Human判断:** v006口GO。v007腿クローバーはCanonical側だけ追加し「クローバーはOK」。角はv005から一切変更しておらず「変える必要はない」で維持。v009比較の後「目の外見はOKだ。」を受領（2026-10-18）。この外観を固定して保存/GLB/runtimeの証明を完了する。

最新保存候補 `assets/grimo/production/jill/tripo/eye-join-v009/jill-textured-rig-v009.blend/.glb`、別bounded QA GLBあり。[成果README](../../../assets/grimo/production/jill/tripo/eye-join-v009/README.md)。v004 shape GO / v005 texture history / v006口 / v007クローバー原本は保護。v008は歴史的失敗候補として明記し、最新版扱いしない。

**残る判断:** 各部位のHuman GOは受領済み。全モデルのHuman完成GOは未受領のため捏造しない。全Motion量産・mobile実機認証は今回の限定範囲外。新しい外観指摘があれば、承認口/眼/クローバー/角を保護し局所対応する。
