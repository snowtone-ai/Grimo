# Shushu Tripo v005 — 残存した両側頭部の毛線

Humanは[v004比較画像で残る線](human-v004-residual-seam.png)を指摘し、目はOKと明示した。v003/v004の毛線「外観PASS」判断は撤回する。実際のv004保存GLBの側面を拡大すると、耳の下から肩へ続くピンク寄りの筋が、頭を前後の部品に分ける縫い目に見えた。

独立した[v005保存GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v005.glb)（SHA256 `a9c1681c5c245d15e0266002c2a618d607d1f6844cfe2bbecfa97827ca536982`）では、実レンダーの両側の線を追い、Head Textureの対応画素だけを局所修正した。左は周囲のクリーム色を細くつなぎ、右は[built-in image_genの局所材料](IMAGEGEN.md)から周囲と一致する差分を使った。目・口の先行修正とv004の眼球奥行きは保持。元GLB・v001–v004・正式Geometry/Rig/Motionを上書きしていない。

- [正面・左右3/4・左右側面の同条件比較](01-five-angle-before-v005-difference.png)
- [頭頂・背面の同条件比較](02-top-back-before-v005-difference.png)
- [左右側面の1.5倍拡大](03-side-seam-closeups.png)
- [Head変更マスク](textures/changed-texels.png)、[生成手順と局所マスク](repair-config.json)、[独立検証](targeted-checks.json)、[視覚判断](visual-review.json)

保存GLBを独立再読込した1024²の原寸7角度と拡大側面を実際に開いた。承認済みBody-onlyの左右側面とも照合。両側とも連続する「頭の分割線」としては見えず、耳根元の自然なピンクと頬下の毛色につながる。新たな白い縁、硬い塗り境界、目・笑顔の崩れは認めない。今回の局所外観はCodex判断でPASS。**Human GateはPENDING**で、正式Rigへの採用判定ではない。

[検証結果](targeted-checks.json)：v004とのメッシュ・UV・node・材質設定は一致。他11枚の埋め込みTextureもbyte一致。Headは247,007 / 4,194,304 texelが変化し、記録マスク外0、先行の目・口修正texelとの交差0。正面レンダーの両目と口の矩形は画素一致。v004の7枚の保存レンダーを比較元としてbyte照合し、全7角度のカメラ条件は一致。285f Motion proofや正式Blender資産は編集していない。異なる照明・スマホruntimeでの見え方はこのoffline比較の範囲外。
