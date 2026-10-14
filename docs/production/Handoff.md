# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-14 / Codex
- **Latest offline Texture task:** 開始HEAD `cfc10d459c09f1e781b544c9d56b59a00c7aa16f`、下記Production branchを継続。Humanの黒線をもとに、両目のピンク目囲み上〜外周の淡い並走帯と鼻側〜下側の白い二重境界だけを修正。ピンク面本体・濃い輪郭・瞳・チーク・v001の口修正を保持。元GLB実LFS hash `338ad5f8…bf077b`とv001 `8d4420d5…a5eac09`を照合。正式Geometry/Rig/Motionへの置換は禁止。
- **Texture candidate NOW:** [v002の保存GLB5角度・承認画像・拡大・マスク・不採用試作・検証](shushu/evidence/tripo-eye-outline-v002/REVIEW.md)。Headの約3.0734%だけ変更、選択範囲外画素0、口修正texelとの交差0。メッシュ/UV/材質設定・他11 Texture・保護758入力は一致。独立候補 `assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v002.glb`、SHA256 `d9bfbac0…3d40b4d7`。原寸/拡大の実モデルとBody-onlyを比較し、Codexは対象の二重縁が解消して不自然さなく可愛さを維持したと判断。**対象外観Codex=PASS / Human=PENDING**。元GLB・v001・以下の正式Geometry状態は保持。外部Tripo操作/課金なし。
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`。先行Geometry修正の開始HEAD `b92aa7683beb2c1ca7d0c7a4e0173c5ee32773d9`。対象成果のみcommit/pushし、最終HEADはGit照合。
- **先行Geometry Authority:** Humanは、saved Sideの開口した下顎が前へ尖ることを指摘し、参照のなだらかな曲線へ、この部分だけを修正しFrontの可愛さを維持するよう指示。承認済みLeft/Front・Canonical Identity・スクリーンショット(525)を参照。#18–26を保護、#27は未承認。remote main `d655f9606b2785ac8be7484e5f22b84dbaee9f55`を当時照合。ローカルGoal√map・9/25正式方針を適用。main一括統合なし。
- **Shushu v003 NOW:** 小/大開口時の下側口縁から顎へ、奥行きの滑らかな後退を適用。Head局所と対応口内だけ。閉口Basis・GentleSmile元形状・通常開口X/Zを保持。頭姿勢との既存合成補正を再計算。鼻・鼻下・上側口元・目/まぶた・耳・身体/座位のshape座標、全制御/driver/Action/modifier/weightを開始時から保持。**Human=PENDING / Tripo=HOLD**。
- **Evidence:** [最新の参照/前後・保存検証・限界](shushu/evidence/geometry-v003/lower-mouth-revision/REVIEW.md)。Front/Side/3Q開口笑顔、Side Clay、小/大開口の6組。同条件640×640原寸。参照との実寸mm/pixel完全一致は証明していない。先行nose/muzzle/appeal/human-gate資料は履歴。
- **対象別検証:** asset/proof再読込、対象外全shape座標と全Action/構造を照合。対象も閉口・対象外キー不変、通常開口X/Z不変。4表情の評価面、7表情/姿勢の口内ray、285フレームproofのNeutral復帰5点/releaseを確認。保護入力56ファイルhashを照合。静的FBX/GLB往復更新。眼球はDonor復元値を維持し、ピンク模様を眼球に含めず、旧20〜30%推定は撤回のまま。
- **限界/未達:** Humanの側面曲線・Front可愛さ承認は未受領。既存上側口周辺の横境界は今回触れていない。最終毛並み/材質・Rig/morph・スマホruntime完成ではない。胴/脚の編集元は維持し、評価後トポロジーは姿勢で変わる。
- **外部Tripo:** upload・試行・Auto Rig・課金なし。今回の既存Textureのoffline局所編集とは別。保存/技術PASSをGOにしない。

## Next
Humanはv002 Texture Evidenceで両目の一重境界と口・可愛さ維持を判定できる。Codexの局所外観PASSはHuman承認や正式Rig採用を代用しない。正式Geometryの下側口縁〜顎とFrontも先行判定待ち。外部Tripo操作は別途明示承認が必要。Goal√map変更なし。
