# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-14 / Codex
- **Latest offline Texture task:** 開始HEAD `c728772e6113ad1c5741051f493e47fba838da33`、下記Production branchを継続。HumanはTripo生成済みTextureの目口の薄い二重線だけを修正し、実モデルを参照比較して不自然さなく100%可愛いと判断してから完了するよう指示。元GLB実LFS hash `338ad5f8…bf077b`を照合。正式Geometry/Rig/Motionへの置換は禁止。
- **Texture candidate NOW:** [元GLB/保存候補5角度・承認画像・不採用試作・検証](shushu/evidence/tripo-texture-v003/REVIEW.md)。口の左右の薄い笑顔/舌の二重像はHead描画由来と確認し、Headの約1.04%のtexelだけ修正。目の試作は白帯の自然さを確定できず撤回し、最終候補の両目は元のまま。独立候補 `assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v001.glb`。メッシュ/UV/材質設定・他11 Texture・保護717入力は一致。**両目未解決 / 外観完成判定保留 / Human=PENDING**。以下の正式Geometry状態は今回変更していない。外部Tripo操作/課金なし。
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`。先行Geometry修正の開始HEAD `b92aa7683beb2c1ca7d0c7a4e0173c5ee32773d9`。対象成果のみcommit/pushし、最終HEADはGit照合。
- **先行Geometry Authority:** Humanは、saved Sideの開口した下顎が前へ尖ることを指摘し、参照のなだらかな曲線へ、この部分だけを修正しFrontの可愛さを維持するよう指示。承認済みLeft/Front・Canonical Identity・スクリーンショット(525)を参照。#18–26を保護、#27は未承認。remote main `d655f9606b2785ac8be7484e5f22b84dbaee9f55`を当時照合。ローカルGoal√map・9/25正式方針を適用。main一括統合なし。
- **Shushu v003 NOW:** 小/大開口時の下側口縁から顎へ、奥行きの滑らかな後退を適用。Head局所と対応口内だけ。閉口Basis・GentleSmile元形状・通常開口X/Zを保持。頭姿勢との既存合成補正を再計算。鼻・鼻下・上側口元・目/まぶた・耳・身体/座位のshape座標、全制御/driver/Action/modifier/weightを開始時から保持。**Human=PENDING / Tripo=HOLD**。
- **Evidence:** [最新の参照/前後・保存検証・限界](shushu/evidence/geometry-v003/lower-mouth-revision/REVIEW.md)。Front/Side/3Q開口笑顔、Side Clay、小/大開口の6組。同条件640×640原寸。参照との実寸mm/pixel完全一致は証明していない。先行nose/muzzle/appeal/human-gate資料は履歴。
- **対象別検証:** asset/proof再読込、対象外全shape座標と全Action/構造を照合。対象も閉口・対象外キー不変、通常開口X/Z不変。4表情の評価面、7表情/姿勢の口内ray、285フレームproofのNeutral復帰5点/releaseを確認。保護入力56ファイルhashを照合。静的FBX/GLB往復更新。眼球はDonor復元値を維持し、ピンク模様を眼球に含めず、旧20〜30%推定は撤回のまま。
- **限界/未達:** Humanの側面曲線・Front可愛さ承認は未受領。既存上側口周辺の横境界は今回触れていない。最終毛並み/材質・Rig/morph・スマホruntime完成ではない。胴/脚の編集元は維持し、評価後トポロジーは姿勢で変わる。
- **外部Tripo:** upload・試行・Auto Rig・課金なし。今回の既存Textureのoffline局所編集とは別。保存/技術PASSをGOにしない。

## Next
HumanはTexture Evidenceで口の改善と可愛さ維持を判定できる。両目の白帯/ピンク境界は消してよい意匠を特定できておらず、完了扱いにしない。正式Geometryの下側口縁〜顎とFrontも先行判定待ち。外部Tripo操作は別途明示承認が必要。Goal√map変更なし。
