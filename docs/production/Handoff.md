# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-15 / Codex
- **Shushu v004 NOW:** 2026-10-15 Human外観PASS（比較画像＋座位→復帰動画）。原本/v001–v003/他キャラ/ユーザー差分を保護。[承認済み制作Evidence](shushu/evidence/production-rig-v004/REVIEW.md)。今回[PlayCanvas実ロード・91姿勢・3視点・動画・費用/実機手順](shushu/evidence/production-rig-v004-runtime/REVIEW.md)を追加。2.22.2は追加Weight欠落357頂点、幾何差最大0.0175131H。4-weight正規化の唯一候補は効果不足で不採用。限定binding PASS、Desktop640²約60fps。Motion量産/全Skin・normal同等/スマホ・実item・物理臀支持はHOLD。ADB接続0、実機UNKNOWN。
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
承認済みv004の外観を固定し、追加Weight互換性を限定修復して同じFront/Side/3Q・遷移で比較。Xiaomi 14T Pro実機とruntime外観Human判定の後にMotion量産Gate。立位/座位は同じrigで共存し、座位Game Neutralは未決定。v006静的PASSをRig/runtimeへ拡張しない。
