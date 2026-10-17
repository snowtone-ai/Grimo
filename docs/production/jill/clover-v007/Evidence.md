# Jill v007 — Canonical腿クローバー

2026-10-18。**Human: 口の外観GO、クローバーOK、角は変更不要・現状維持。** 角は今回変更していない。完全完成GOALは、既存の目周囲/閉眼の未解消外観を残すためHOLD。

[実PlayCanvas全身](runtime-body.png) / [実PlayCanvas顔・角](runtime-face.png) / [クローバー拡大Front](clover-detail-front.png) / [拡大3Q](clover-detail-3q.png) / [保存資産](../../../../assets/grimo/production/jill/tripo/clover-v007/README.md)。ユーザーがinlineを表示できなかったためPNGをDownloadsへコピーし、ファイルで提示後に「クローバーはOK」「角は勝手に変えた？変える必要はない」と回答。表示不能の時点では承認としていない。

## 変更と保護

Human承認済み[v006口](../mouth-integration-v006/Evidence.md)から別名派生。Canonicalで見える大腿（モデルX負側、正面画像左）だけに四つ葉と茎を追加。未表示側・裏側へ複製しない。見えている四つ葉の参照cutoutをimagegenで作成し、初回6枚葉の出力は不採用、4枚葉の出力を既存body_skin ownerの三角形に限ってUV0へ投影した。[projection](projection.json) / [生成記録](imagegen-provenance.md)。全Texture再生成ではない。

実全身比較で初回は大腿に対して小さかったため、配置幅.073m/高さ.090mへ調整。その画像にHuman GO。最終拡大実レンダーでUV島の境界に細い旧緑色の線が見つかったため、同じ投影を2texelだけgutterへ延長し、線の消失を直接開いて確認。ownerがbody_skin/余白の画素だけを許可し、意匠・位置・大きさは保持した。[局所Texture差分](texture-diff.json) / [UV mask](clover-uv-mask.png)。角・口を含むmask外の全画素は元v005と一致。

形状・topology・全3UV・weights・全Morph座標・driver・130骨/39ch/16anchorはv006と完全一致。保存blendを再読込して照合。[全保護contract](preservation.json)。口のneutral/閉/小/大/復帰Frontは、承認v006とレンダー画素一致。[最終照合](verification.json)。

## actual検証

- 保存blend: neutral/閉/小/大/combined/復帰をFront/Side/Canonical側3Qでレンダー。背面・反対側も確認し不要な複製なし。拡大Front/3Qを自分で開いてUV継ぎ目も確認。
- fresh GLB: owner+UV+positionで使用30,880頂点を対応付け、未対応0。7顔Morph状態を照合・実全身レンダー。130骨/20Morph/23材質/16anchor、3UV、BaseColor UV0。[再import](reimport-proof.json)。
- 実PlayCanvas2.22.2 Desktop WebGL2: 最終static GLBをロード。Front/左Side/左3Qの全身、閉口優先同時入力・小/大開口・smile・復帰を実操作・撮影。全23skin/23Morph instance/20Morph/16anchorと実モデルSHAを照合。[実測](static-runtime.json) / [検証](verification.json)。口の詳細な15同時入力/21中間/39ch端点/骨motion実検証はgeometry/Morph/weights/driver完全一致のv006を継承する。

全Motion量産・Tripo再課金・全面塗り直し・Rig再作成・他キャラ変更は実施していない。全Motionライブラリ/実機mobileは今回の限定検証範囲外であり、新たな完了必須要件を勝手に足さない。

## 残る完成条件

口とクローバーはHuman GO、角は現状維持。既存の眼窩外側の隙間、閉眼の瞼縁/隙間はこの派生でも未変更。元依頼の「瞼など他のHOLD事項に横滑りしない」を守り、配布v007へ混在させない。完全完成GOALとこの保護指定の扱いは明示し、技術PASSだけでモデル全体GOにしない。

再現: Blender `scripts/blender/jill-clover-v007.py -- surface` → `python scripts/qa/project-jill-clover-v007.py` → Blender `-- build` / `-- detail` → Blender `scripts/blender/verify-jill-clover-v007.py`。loopback viewerは既存serveへmodel=v007 static、evidence=本folder、port8850、mouth-controls=1、LEFT_SIDE=1を指定。Playwright `capture-jill-clover-v007.js` → `package-jill-clover-v007.py`。最終[Manifest](Manifest.json) / [remote照合](RemoteReceipt.json)。

## 最新Human指摘 — 2026-10-18

v007全身PNGへ赤線で、目外側の境界線とその外に残る眼球を指摘。「この線は消すか、この線より顔の外側の目の部分には、皮膚の膜を貼るべき」。これにより当該眼/肌境界の局所修正が明示対象になった。v007の承認口・クローバーと変更不要の角を保護し、次の別派生で原因を切り分ける。
