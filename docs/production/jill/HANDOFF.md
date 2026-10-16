# Jill — NOW

2026-10-16 / `codex/jill-mouth-profile-v004-20261016`。**Human指定の口〜顎の横顔修正を実装し、Texture用v004候補へ更新。修正版のHuman visual GOはPENDING。** 最新Humanは「この修正だけでTripoテクスチャフェーズへ」と指定。他の瞼/翼/葉の造形修正を追加必須化しない。

開始 `9c25c6bf86da6ffcced4439ea2456d112befe98c` / clean、再確認main `73617ce2d3c724c86aed82dfc2a09cd220e5d194`。worktree `C:/Users/chidj/.codex/worktrees/jill-pretexture-technical-v003/Grimo` を再利用。旧v002/v003正本・Evidence、元checkoutのShushu変更を保護。

[修正前後・Evidence](mouth-profile-v004/Evidence.md) / [横顔主要3状態](mouth-profile-v004/side-key-poses.jpg) / [正面・3Q比較](mouth-profile-v004/front-3q-before-after.jpg) / [反対側](mouth-profile-v004/opposite-side-before-after.jpg) / [投入候補](../../../assets/grimo/production/jill/tripo/mouth-profile-v004/README.md) / [Manifest・SHA](mouth-profile-v004/Manifest.json) / [remote照合](mouth-profile-v004/RemoteReceipt.json)。Rig SHA `df3891bbd11c522631202e0dd32945a788ff370477731568514261a5e4100cb7`。

原因は別曲面の追加口面と元肌の閉口時35mm後退。追加口面/口内のYを実顔曲面へ合わせ、元口周囲179頂点をYだけfairing、露出肌52頂点の閉口後退を解除。全key各1,948頂点に意図的Y変更。全21 keyのX/Zと局所以外の座標は完全一致。全Basis差0とは言わない。全体remesh/顔再設計なし、130骨/39ch/20 Morph/16 anchor、weights/drivers、polygon頂点順/23材質ownerと3層UVは保持。

neutral/close .5/1/open 1/blink .5/1/復帰のfront/side/3Q、反対側4状態を実renderし開いた。横の板状突出と閉口のギザギザ境界を解消し、他視点の口幅/高さ・目/顔の可愛さを保つ候補。最終visual GOはHuman。neutral復帰は3視点pixel一致/評価頂点差0。

UV0は `Jill_Texture_UV0_v003` のまま。UV1旧active/UV2元sourceも全loop値一致。自動三角形分割16行の変化を再測定し、overlap0/UV縮退0/4K最小島間23.894pxを維持。1K HOLD、2K細部UNKNOWN、4K基準、8K測定上候補。口外肌極小sliverの伸び最大44.676（面積比0.0213%）は既定の同系肌色充填、細密図柄/Normal品質は未保証。既存Geometry縮退1枚は不変。

更新したFBX/GLBから診断画像のみRigへ戻し、packed blend保存・再読込とRig GLB fresh importを再確認。UV0明示/130骨/20 Morphを保持。fresh GLBのclose .5/1/open 1は元Rigに位置差最大3.073e-7m、UV差2.98e-8。305frame/全Motion/mobileは重複実行しない。

[Tripo引渡し](mouth-profile-v004/TripoHandoff.md)。必ずv004 neutral FBX/GLBを使う。新たに残す元口周囲肌にも開口印刷を残さないため、既存owner充填に追加host肌maskを適用する。承認palette必須、診断色は正式Textureではない。Original UV不可/不明、返却remesh/owner不明なら停止しRigを置換しない。実UI/料金/Original UV/実返却はUNKNOWN。upload/課金/正式Textureは今回未実施。旧の技術経路/仕様は [v003 Evidence](rig-pretexture-technical-v003/Evidence.md) を継承し、形状NOWはv004で判断する。
