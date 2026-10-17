# Jill v009 — 両目外側の縦帯を除去

2026-10-18。branch `codex/jill-texture-return-v005-20261017`、開始HEAD `cc080bc30590247d8604d94c0a5d5dced6f595a5`。最新mainはfetchして `534694dae8087dec852de0f26b472a6dcd26ca70` を確認。mainにJill HANDOFFはなく、Jill制作branchの実資産と最新Human判断を参照した。AGENTS、Goal√map、production pointer、Jill HANDOFF、v004 shape GO / v005 history / v006 mouth GO / v007 clover OKを継承。別checkoutのShushu/user変更を保護し、mainを混ぜていない。

**Human最新判断:「目の外見はOKだ。」目外観GO（2026-10-18）。** 口Human GO、Canonical側の腿クローバーHuman OK、角は変更不要・元のまま。その後、Humanより「モデル全体も完成GO」を明示受領。v009をテクスチャ込み完成モデルとして採用。[完成承認記録](HumanApproval.json)。目視確認の報告には実画像を添える。

## 根本原因

Humanのattached screenshot 593 (user message)は、両目外側に浮いている立体の縦帯を指定した。[v008](../eye-boundary-v008/Evidence.md)はbody_skin上の古い眼の絵を消したが、後付け瞼の帯を残しており、Human FAIL。Texture-onlyで今回の指定対象が消えるという判断は誤りだった。

既存の瞼は片眼960頂点（外周64点＋64列×14段）の環状面。外周と中間面の奥行きが本体の肌・実眼面と合わず、浮いたcream帯と影になっていた。Blink時の元の眼の3.4cm後退も、斜め半目で眼が細く潰れて見える原因になった。

外側だけを折り込む試作は開眼では帯が消えるが、中間Blinkで三角の折れ・閉眼の隙間を発生させたため不採用。単純削除も閉眼面を失う。既存の瞼面を接続し直す局所位置補正が必要だった。

## 実施修正と保護

- 両眼の既存瞼外周を実body_skinへのray hitに合わせ、0.8mm肌内側へ接続。中間面は実眼の二次近似面に沿わせ、浮いた外側の帯を解消。
- 開眼の実眼輪郭を維持し、閉眼端は上下が同じU座標・同じ面に合流するよう補正。0.08mmの旧閉眼隙間も解消。原眼126頂点のBlink後退を解除し、目の位置を保って瞼で覆う。
- Basis変更は既存左右瞼の計1,920頂点のみ。全Morphを通じた変更候補は計2,046頂点。実眼のBasis、body_skin、口、角、クローバー、他部位のGeometryは完全保持。
- 頂点/面の追加削除なし。全体UV（3層）、owner、weights、全bone rest、driver、anchor完全一致。Blink以外の相対Morph差は2e-7m未満。130骨 / 39 authoring ch / 20 Morph / 16 anchor維持。[差分証明](preservation.json)。
- Textureはv008の局所body_skin残像除去を継承。元v007に対する変更は13,379画素、mask外は完全一致。[Texture差分](../eye-boundary-v008/texture-diff.json)。実眼の絵、口・クローバー・角を保持。全再生成、課金、Rig再作成なし。

## 実画像・検証

- [保存blend 修正前後](saved-cord-before-after.png)、[実PlayCanvas 修正前後](eye-before-after.png)、[実顔PNG](runtime-face.png)、[実全身PNG](runtime-body.png)、[瞬き21段階GIF](blink-runtime.gif)。実画像を開いて確認し、報告に添付。Downloadsのv009画像も提供。Humanの注釈入りv007画像と593原本を上書きしていない。
- 保存blendを再読込して、neutral / 閉口 / 小開口 / 大開口 / combined / 復帰、Blink .25/.5/.75/1、左右wink、gaze X/Y両極をFront / Side / 左右3Qで実レンダー。縦帯がなく、中間・閉眼で新しい穴や浮く紐がないことを確認。
- [fresh GLB再import](reimport-proof.json): 使用30,880頂点を対応付け、欠落0。7つの眼/口状態を比較して最大位置差<2e-6m。130骨、20 Morph、16 anchor、23 material、3 UVとUV0 texture routingを確認し、再importのFront / Side / 3Qも実レンダー。
- [口の回帰](mouth-pixel-regression.json): neutral / 閉口 / 小開口 / 大開口 / 復帰のFront口領域はHuman GO済みv007と画素一致。
- [実static PlayCanvas](static-runtime.json): Engine 2.22.2、23 skin/Morph instances、20 Morph各、16 anchor。左右Blink中間とwink、口同時入力、21段階の閉眼→開眼、neutral復帰。全23 instanceの入力一致を検証し、復帰canvas画素一致。
- [実bounded runtime](bounded-runtime.json): 既存の頭/翼/尾/顔の限定schedule、代表状態と連続再生・復帰。実runtime画像を開いて確認。[検証集約](verification.json)。全Motionの量産やmobile実機認証は実施していない。

## 判定

**指定の両目外側の縦帯: 修正実施、Human目外観GO。** 口GO / クローバーOK / 角は変更不要を保持。今回の検証範囲に未解決の縦帯・眼の漏れ・復帰不良は見つからなかった。**最終Human判断「モデル全体も完成GO」を受領（2026-10-18）。v009完成GO。** 今回は承認記録だけを更新し、承認されたblend/GLB/Texture本体を一切変更していない。[Gate](Gate.json) / [Manifest](Manifest.json)。commit/push/remote一致は[receipt](RemoteReceipt.json)。
