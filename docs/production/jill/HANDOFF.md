# Jill — NOW

2026-10-15 / branch `codex/jill-pretexture-v002-20261015` / **実装修正版を保存、Pre-Texture Technical GO候補には未到達・HOLD。最終GOはHuman専権。**

実継承HEAD `379fe79ac2561b9a5796a4657c36d503d248cf04`、最新main `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b` を確認。旧Jill worktreeはclean、旧正本/旧Evidence/元checkoutの並行Shushu変更を保護。専用worktreeは `C:/Users/chidj/.codex/worktrees/jill-pretexture-v002/Grimo`。既存[Plan](rig-other-v001/Plan.md)へ事前追記を `202eae9` でcommitしてから実装した。

[別名blend/GLB・Texture専用FBX/GLB](../../../assets/grimo/production/jill/tripo/rig-pretexture-v002/README.md) / [Evidence・阻害条件](rig-pretexture-v002/Evidence.md) / [顔・口](rig-pretexture-v002/face-mouth.jpg) / [閉眼](rig-pretexture-v002/face-blink.jpg) / [SHA・絶対パス](rig-pretexture-v002/Manifest.json)。130骨/39ch/20 Morph/16 anchor。元28,050頂点のBasis差0。局所立体瞼/口縁/口腔/舌/牙、根のweights、限定foldを実装。全身再生成/一括remeshなし。

**残り**：閉眼が蓋状、半閉眼の厚い縁とSideの隙間。閉口の顎が板状で口縁二重、大開口内部も未完成。翼根/肩/首葉/尾葉の層と接合、膜の柔らかさが不足。foldは0.30radの後方スイープまでで自然な収納ではない。可愛さ・本人性・接合はHOLD、Human外観判定PENDING。承認済み閉口/閉眼/fold極値参照もない。

元UVは第2層で差0保持。active UVは元島を`.006+.88*source`へ移し、新規面用右帯と縮退三角形1枚の局所補修を追加。このactive変更は未承認。checkerの全方向/掌/口内/膜裏を確認したが密度差・伸び・隠れ根はHOLD。Texture専用FBX/GLBは同じneutral surface/active UVから作成し、fresh import対応を確認。

保存blend/GLB再読込の代表poseとanchor、ローカルPlayCanvas 2.22.2のsampled proofを確認。[連続3視点再生の範囲](rig-pretexture-v002/PlaybackReview.md)。driver/IKや任意39ch solverをGLBへ移植したものではない。スマホ/全Motion/厳密接触・装備fitは未検証。数値一致で外観HOLDを解除しない。

[Texture仕様](rig-pretexture-v002/TextureSpec.md) はCanonical配色、最新Human指定の桃色horn、クローバー、眼、口内。[Tripo引渡し](rig-pretexture-v002/TripoHandoff.md) にOriginal UVの公開案内と実UI/料金の未確認、返却骨/Morph/UV保持を仮定しない元Rigへの画像転写手順を保存。upload/課金/正式Texture生成なし。HOLDのままTexture実行へ進めない。

次は顔の局所面接続と根/膜fold、UV密度を修復し、承認参照と比較。現状を完成/GOと宣言しない。旧v001状態は[旧Evidence](rig-other-v001/Evidence.md)と継承HEADのHANDOFFに残る。
