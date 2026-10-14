# v005 局所材料

Built-in `image_gen`を1回使用。入力の[比較パネル](imagegen-source-panels.png)はv004の独立保存側面レンダー2枚と承認済みBody-onlyの左右側面。出力の[局所材料](imagegen-local-material.png)は1254²で、**モデルの検証画像ではない**。実モデルの判断には保存v005 GLBをBlenderへ独立再読込した`renders/candidate-*.png`のみを使う。

右頭部は生成画像を実レンダーに合わせ、耳〜肩の線の左右で色差をゼロへ戻した局所補正をHead Textureへ投影。左頭部は生成画像より周囲クリーム色の横方向補間の方が自然に見えたためそれを採用。試行中に生じたピンクの塗り跡、白筋、横境界は採用していない。いずれも[修正範囲](repair-config.json)内のHeadだけを更新し、v004の目・口変更画素は保護した。
