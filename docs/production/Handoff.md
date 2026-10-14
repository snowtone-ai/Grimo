# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-15 / Codex
- **Shushu Production Rig v001:** 開始HEAD `6b86aa4e3692310fd6d0a3ac44cee308b47e4602`。入力Auto Rig SHA `803aeec9…172f8932`から別名の編集可能Rig/proofとGLBを制作。[能力Gate・比較・残HOLD](shushu/evidence/production-rig-v001/REVIEW.md)。頭→Paw/腕→胴の漏れを解消、左右耳/顔/腕手/足を独立制御。局所weights、足world pin、腹臀/腕root Corrective、v003評価変位の顔移植（旧絶対座標コピーなし）、小口内/舌、7 Anchor。67 joints/14mesh/101,053面、元12 UV/Texture/Material保持、眼球奥行き約0.006復元。603支持条件と589f/50時点proof、座位＋表情/片保持＋対側接触/割込み復帰/解放を検証。GLB頂点往復差≤1.044e-6、Anchor/fixtureも保存照合。**測定したRig能力PASS / 正式採用・Human可愛さHOLD**。任意stroke経路、実花束/Wear/Gift/Food5様式、物理COM、任意FK支持、スマホruntimeは未検証。原本/旧proof/他キャラ/ユーザー差分・Goalを保護。全Motion/PWA/外部課金なし。
- **v006最新Human判断:** 2026-10-14、Humanがv006の静的外観PASSを明示。SHA256 `9c479122…34f10f`。旧[口v006 REVIEW](shushu/evidence/tripo-mouth-depth-v006/REVIEW.md)の未達/PENDINGは当時の履歴として保持し、現承認を上書きしない。正式Rig/Motionの承認ではない。
- **最新offline lowpoly v001:** 開始HEAD `6805096e811246401599651cbfaa9fc23834e459`。v006から別名GLBを作成、523,683→99,565三角形（80.99%削減）、6.07 MB。顔/チーク/頭下端60,176面と他10メッシュを保持、頭後部と胴体を属性考慮削減。[成果・14組比較・保存検証・未検証](shushu/evidence/tripo-rigprep-v006-lowpoly/REVIEW.md)。全12 Textureバイト/材質一致、残した位置/法線/UVは元頂点と一致、退化0、新しい境界/非多様体辺増加0、保護991入力一致。足首の退化試行は局所保護で解消。**Codex相対静的外観保持PASS / lowpoly Human未検証 / Tripo受入UNKNOWN**。SHA256 `780f1f9c…f41309`。原本/歴代候補/正式v003 Blender・Shape Keys・285f proof/他キャラ/ユーザー差分は不変。
- **先行offline毛線v005:** Humanはv004の目をOKとし、両側の耳→肩に「頭を半分に分ける」毛線が残ると再指摘。先行v004毛線外観PASSを撤回。[v005局所Texture・原寸/拡大比較](shushu/evidence/tripo-fur-seam-v005/REVIEW.md)を独立保存。Head 247,007 texelのみ変更、正面の両目/口は画素一致。v004眼球奥行き、v002目囲み、v001口、v003頭頂修正を保持。Codex局所外観PASS、**v005 Human=PENDING**。SHA256 `a9c1681c…536982`。元Tripo GLB・先行候補・正式Geometry/Rig/Motion・他キャラ・ユーザー差分を保持。
- **Latest offline Texture task:** 開始HEAD `cfc10d459c09f1e781b544c9d56b59a00c7aa16f`、下記Production branchを継続。Humanの黒線をもとに、両目のピンク目囲み上〜外周の淡い並走帯と鼻側〜下側の白い二重境界だけを修正。ピンク面本体・濃い輪郭・瞳・チーク・v001の口修正を保持。元GLB実LFS hash `338ad5f8…bf077b`とv001 `8d4420d5…a5eac09`を照合。正式Geometry/Rig/Motionへの置換は禁止。
- **先行Texture v002:** [v002の保存GLB5角度・承認画像・拡大・マスク・検証](shushu/evidence/tripo-eye-outline-v002/REVIEW.md)。Headの約3.0734%だけ変更、選択範囲外画素0、口修正texelとの交差0。メッシュ/UV/材質設定・他11 Texture・保護758入力は一致。SHA256 `d9bfbac0…3d40b4d7`。保存時のCodex局所外観PASSに加え、**今回Humanが目囲み修正を「完璧」と明示**。これは新規v003/v004や正式Rigの承認ではない。
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`。先行Geometry修正の開始HEAD `b92aa7683beb2c1ca7d0c7a4e0173c5ee32773d9`。対象成果のみcommit/pushし、最終HEADはGit照合。
- **先行Geometry Authority:** Humanは、saved Sideの開口した下顎が前へ尖ることを指摘し、参照のなだらかな曲線へ、この部分だけを修正しFrontの可愛さを維持するよう指示。承認済みLeft/Front・Canonical Identity・スクリーンショット(525)を参照。#18–26を保護、#27は未承認。remote main `d655f9606b2785ac8be7484e5f22b84dbaee9f55`を当時照合。ローカルGoal√map・9/25正式方針を適用。main一括統合なし。
- **Shushu v003 NOW:** 小/大開口時の下側口縁から顎へ、奥行きの滑らかな後退を適用。Head局所と対応口内だけ。閉口Basis・GentleSmile元形状・通常開口X/Zを保持。頭姿勢との既存合成補正を再計算。鼻・鼻下・上側口元・目/まぶた・耳・身体/座位のshape座標、全制御/driver/Action/modifier/weightを開始時から保持。**Human=PENDING / Tripo=HOLD**。
- **Evidence:** [最新の参照/前後・保存検証・限界](shushu/evidence/geometry-v003/lower-mouth-revision/REVIEW.md)。Front/Side/3Q開口笑顔、Side Clay、小/大開口の6組。同条件640×640原寸。参照との実寸mm/pixel完全一致は証明していない。先行nose/muzzle/appeal/human-gate資料は履歴。
- **対象別検証:** asset/proof再読込、対象外全shape座標と全Action/構造を照合。対象も閉口・対象外キー不変、通常開口X/Z不変。4表情の評価面、7表情/姿勢の口内ray、285フレームproofのNeutral復帰5点/releaseを確認。保護入力56ファイルhashを照合。静的FBX/GLB往復更新。眼球はDonor復元値を維持し、ピンク模様を眼球に含めず、旧20〜30%推定は撤回のまま。
- **限界/未達:** Humanの側面曲線・Front可愛さ承認は未受領。既存上側口周辺の横境界は今回触れていない。最終毛並み/材質・Rig/morph・スマホruntime完成ではない。胴/脚の編集元は維持し、評価後トポロジーは姿勢で変わる。
- **外部Tripo:** upload・試行・Auto Rig・課金なし。今回の既存Textureのoffline局所編集とは別。保存/技術PASSをGOにしない。

## Next
Production Rig v001の4方向比較、閉眼/閉口/座位/保持をHuman確認へ。未検証MUSTはCAPABILITY-MAPのHOLDを残し、任意stroke経路と実itemの接面/両手grip/Food5様式は対象別Rig検証が必要。採用後の演技・runtimeは別scope。座位Game Neutralは未決定。静的v006 Human PASSをRig/Motion/runtime承認へ拡張しない。
