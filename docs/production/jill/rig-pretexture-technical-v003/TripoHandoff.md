# Jill v003 — Tripo handoff / 実行HOLD

2026-10-16。Human最終GOを代行しない。Tripo upload、課金、正式Texture生成は未実施。**実UI、料金、対応解像度、Original UV可否、実返却はすべてUNKNOWN。** この文書は実行許可ではない。

投入候補は [README](../../../../assets/grimo/production/jill/tripo/rig-pretexture-technical-v003/README.md) のneutral FBXまたはGLB。正確なSHA/絶対パスは [Manifest](Manifest.json)。両方同時投入しない。元Rigやdiagnostic画像、合成返却モデルは投入しない。

- FBX SHA-256 `6a267f2e6aaa81514b726e940f9fd35e1274d9f1f7e609d0264b804989f70ad8`
- GLB SHA-256 `775576faef6ea468e3d3d910965e10316faba7029649b6c5b1932afafe05eaa2`
- Rig派生SHA-256 `ad9f867e87a6006259aec5d8b01e1981fc823ae97bc92a87dc49a906770a9050`

## 実行前

Humanが現形状を凍結して進めるか、残る顔/翼/根の造形修正を先にするか判定する。形状・topology追加が必要なら本候補GO失効。承認palette、角mask、左右クローバー意匠、実UIのresolution/Original UV/見積額と操作条件を確認するまでHOLD。1K使用不可。4K基準、8Kは実画像pipeline再検証付き。外観を変えるauto-remesh/新規riggingを混ぜない。

Original UVが選べない・存在を確認できない場合は、その場で停止する。保持できると推定してupload/課金しない。元UV層の削除やSmart UVでの上書きも不可。返却UV変更経路は下記の限定条件で実証しただけなので、実際の返却契約が分からなければUNKNOWN/HOLDをHumanへ提示する。

## 返却を受けた後

1. 別フォルダへ原物を保存しSHA、画像解像度、UV層/active、material/owner、geometry/topology/三角形構成を記録。元Rig派生を置換しない。
2. UV0一致なら、owner+position+UV cornerを双方向照合する。FBX単位/軸変換も測る。画像のdecodeとmaterial→UV0参照を確認し、画像だけをRigの別名コピーへ割り当てる。返却骨・weight・Morph・anchor・Geometryは採用しない。
3. UV変更なら同じGeometry/三角形ごとのownerに一意対応できる場合だけ別名画像へbarycentric転写。[試験](uv-changed-transfer-proof.json)と `scripts/qa/reproject-jill-uv-return-v003.py` は合成U反転fixtureであり、任意返却へそのまま実行する一般importerではない。実返却を別入力として準備し、完全対応を検証してからbakeする。隣接する眼・瞼・口へnearest rayを飛ばさない。
4. remesh、三角形化変更、変形、owner欠落、曖昧対応、UV/画像欠落、左右混線なら停止。新しい対応付けの実証がない限りHOLD。NormalはUV変換後のtangentが別なので別途rebake/検証する。
5. 承認paletteでprotected ownersを充填し、閉口肌への口内、瞼への開眼印刷を排除。膜裏/葉根/舌裏もmaskで補充し、画素の欠落や隣ownerへの漏れを確認。現在のsanitizerは4K固定、8Kならmaskと余白・画像照合を再検証する。
6. packed blendを保存・再読込。Rig GLBのTEXCOORD_0/1/2とbaseColor texCoord=0、130骨/20 Morphをfresh import確認。39ch・16 anchor・元UVはeditable Rigの契約で保護する。glTFにBlender solverが移るとは仮定しない。
7. 顔front/side/3Qのneutral→mid→closed/open→neutral、blink遷移、翼fold/open/表裏、葉根を実レンダーで開く。Canonical/Body-onlyと比較しHuman最終GOを得る。全Motion/mobileは別gate。

今回のFBX/GLBの保存往復は [transfer-proof](transfer-proof.json)、見た目は [Evidence](Evidence.md)。合成画像の成功は実Tripo返却の成功ではない。実返却後に停止条件へ触れたら無理に転写せずHOLDを保存する。
