# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-14 / Codex
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`。今回の開始HEADは`6f4822362aaec9e795023f08349d4bb14c5188e0`（Shushu appeal成果`153dba5`＋Carol資料）。成果とこの文書は同じ制作branchへcommit/pushする。最終HEADはGitで確認する。
- **Authority:** fetchした`origin/main@d655f9606b2785ac8be7484e5f22b84dbaee9f55`のGoal√map/Handoff、9/25正式方針、Shushu Canonical・4方向・Human指定の承認#18–26。#27は未承認。main一括merge/rebaseなし。
- **Shushu v003:** appeal保存モデルの鼻先〜鼻下だけを局所編集。長い鼻先と鼻下の稜線を、小さな丸いふくらみと浅い面へ変更。HeadのX/Z・面・口境界128頂点は不変、奥行きだけ変更。表情/座位の相対変形を保持し、頭姿勢合成を更新。前回のU字開口・曲面口腔/舌・連続胴/脚外皮・後方へ延びるまぶた内壁を維持。**Human=PENDING / Tripo=HOLD**。
- **Evidence:** [現行の鼻先/鼻下の前後比較・検証・未達](shushu/evidence/geometry-v003/muzzle-revision/REVIEW.md)。Front/Side/3QのClay＋診断色、開口笑顔、06-companion相当、小/大開口。顔Sideは旧鼻先が端に切れるため前後同じ位置へcameraを移動。先行appeal/human-gate revisionは当時の履歴として保持。
- **保護/機能:** 保護入力56ファイルをhash確認（元FBX/GLBはintake hash一致）。Head以外の全shape座標、全Action曲線、制御/driver/modifier/weightは開始時と同一。口境界の全キー差0、7組の口内rayに欠損なし。285フレームproofの代表Neutral復帰5点で評価表面差0、releaseを確認。眼球はDonor復元値を維持、ピンク模様を眼球に含めず旧20〜30%推定は撤回のまま。FBX/GLB往復も更新。技術PASSを可愛さPASSにしない。
- **方式の限界:** 胴/脚の編集元とキーは残り、外皮は非破壊modifierで評価する。評価後トポロジーは姿勢により変わる。これはGeometry再判定候補であり、固定トポロジーの最終Rig/morph・Motion演技・スマホruntime完成ではない。静的FBX/GLBは描画外皮を出力し、非描画の脚を二重exportしない。
- **残る外観判断:** 今回の鼻の小ささ・丸さ・鼻下の柔らかさはHuman再判定待ち。口周辺の横の境界と診断鼻色の粗い境界は残る。まぶた内眼角/半閉の柔らかさ、座位の足首/胴の重み、開口笑顔の本人らしさ・安心感、最終質感・毛並みも未確定。
- **Tripo:** upload・Texture・Auto Rig・無料試行・課金を実行していない。ローカル保存/往復の確認でGOにしない。

## Next
Humanは現行REVIEWの鼻先〜鼻下をFront/Side/3Qと着座全身で再判定する。Codexは外観指摘を根拠に方法を選び直し、承認を捏造しない。Tripo操作は別途明示承認が必要。Goal√mapはWHY、Canonical/製品仕様は別の正本。重要な進捗・承認・障害・担当変更時だけHandoffを更新する。
