# 口の側面修正に使った参考資料

調査日: 2026-10-14。調査は構造と制作方法の手掛かりであり、Shushuの形のAuthorityは承認済みBody-onlyとHumanの指示。実動物の長い吻・歯列・顎をこのキャラクターへ追加しない。

1. [North Carolina State University — GI structures of the head](https://ncstate.pressbooks.pub/unit6alimentary/chapter/chapter-1-2/)
   獣医解剖の教材。口腔前庭は歯・歯肉の外、唇・頬の内にあり、舌は口腔底につながる。口を単なる外表面の色として扱わず、口縁・頬・内部のつながりで見るための資料。取得できた本文と検索抜粋の範囲を利用し、掲載解剖画像は成果物へ転載していない。
2. [Blender Studio — Facial Rigging for Stylized Character Animation](https://conference.blender.org/2025/presentations/4069/)
   Blender StudioのLead Animatorによる公式発表概要。口・目・頬・眉を各部の表現要求に合わせて扱う制作方針を確認した。発表概要のみ確認し、動画内の未確認手順を実施済みとは扱わない。
3. [Pierrick Picaut — Creating a Stylized Blender Character](https://blog.cgcookie.com/posts/workflow-tips-from-pierrick-picaut-creating-a-stylized-blender-character/)
   制作者自身の工程解説。基本の比率と参照を先に確認し、口周辺の面の流れを自然な筋肉の流れに沿わせるという助言。今回はリトポロジーを追加せず、既存の面の奥行きのつながりに適用。

## 今回の診断からの推論

v005のHeadに口の輪郭・開口・舌がほぼ全て描かれている。独立MouthInteriorは上縁付近の浅い帯。側面で口が細い赤線になる主因は、この描画領域の左右の頬が口を隠す既存断面にある。資料だけから原因を断定したのではなく、保存GLBの局所座標・Texture対応・実レンダーで確認した。

口のX/Y（幅/高さ）とTextureを固定し、口角と隣接する頬のZ（奥行き）だけを滑らかに後退させる。MouthInteriorの同じ部位も同じ写像で追従させる。傾斜が急すぎると3/4の奥側口縁と舌を自己遮蔽するので、実画像の比較で急な試作を棄却し、傾斜を抑えた写像を使う。これは既存静的GLBの局所外観修正であり、完全な解剖学的口腔、表情Rig、正式Geometryの修正を意味しない。
