# Jill mouth profile v004 — local plan

2026-10-16。Humanはv003横顔の口縁〜顎の貼付け板感をFAIL、そこだけ顔曲面へなじませ、正面/3Qの可愛さを保持するよう指定。他の修正を追加せずTexture投入候補を更新する。最終Human visual GOと課金許可は代行しない。

継承9c25c6b、作業branch codex/jill-mouth-profile-v004-20261016。元checkoutのShushu変更・v002/v003正本/Evidenceは保護。最新main73617ceを再fetchしAGENTS/Goal/Handoff確認。既存worktreeをcleanから再利用。

G3の局所顔面奥行き/Morph接続→G2の自然な開閉口→G1の本人性/可愛さ→G0の愛着。旧追加口面の解析曲面が顔本体の顎曲率へ追従しないことを疑い、元faceの実表面と比較する。口の正面輪郭x/zを維持し、追加口縁/顎のyと連続する口内のみを同じ曲面へ整合。無関係な目/瞼/翼/葉・骨/weight/anchor/元UVを保持。

neutral/close-mid/closed/open/回復を同条件front/side/3Qで実renderし、v003と比較して改善を判断。違和感が残れば数値PASSで終了しない。トポロジーとUVが維持できれば過去overlap/padding証拠を再利用し、変わる局所密度/伸びのみ測る。別名blendとneutralFBX/GLBを保存・fresh importし、契約/画像UV0転写の影響を重点確認。305frameや全Motionを再実行しない。

Evidence/Manifest/HandoffへHuman修正指示と結果/未検証範囲を保存、commit/push/remote照合。Tripo upload/料金/正式Textureは今回未実施。
