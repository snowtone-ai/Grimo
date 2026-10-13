# Grimo — Handoff (last verified, not live authority)

実行時のNOWは実作業branch/HEAD、未コミット差分、保存成果とEvidenceで再確認する。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-14 / Codex
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`。今回の開始HEADは`530f75c4cc7e4fbc06545c420b337155e67c8212`。保存済みv003の続き。成果とこの文書を同じbranchへcommit/pushし、最終HEADはGitで確認する。
- **Authority:** 最新Human「鼻はこんなふうになる。これにぴったりにして。」とスクリーンショット(525)。表示された承認済みShushu Left、Front、Canonical Identityを鼻の基準にした。承認#18–26を保護。#27は未承認。remote mainは`d655f9606b2785ac8be7484e5f22b84dbaee9f55`と再照合済み。ローカルGoal√map、9/25正式方針を適用。main一括merge/rebaseなし。
- **Shushu v003:** 元Headの不規則な鼻先・色境界を引き継ぐ方式を変更。局所Head面を滑らかにし、上が広く下が丸い小さな鼻と短い鼻下を`Shushu_Nose`に追加。新規操作制御はなく、既存Headの70キー/driver/Action/頭姿勢合成へ追従。HeadのX/Z・面・口境界128頂点は不変。既存の口/目/まぶた/座位/支持/接触機構を保持。**Human=PENDING / Tripo=HOLD**。
- **Evidence:** [現行の参照・前後比較・保存検証・未達](shushu/evidence/geometry-v003/nose-reference-revision/REVIEW.md)。承認Front/Leftと候補、Front/Side/3Qの同カメラClay＋開口笑顔の診断色、小/大開口。2D参照との完全pixel一致は証明していない。先行muzzle/appeal/human-gate revisionは履歴として保持。
- **保護/機能:** 保護入力56ファイルをhash確認。Head以外の既存全shape座標、全Action曲線、制御/driver/modifier/weightは開始時と同一。口境界の全キー差0。7組の表情/姿勢で口内rayに欠損なし、鼻追従は有限。285フレームproofの代表Neutral復帰5点で新しい鼻を含めて評価表面差0、releaseを確認。眼球はDonor復元値を維持、ピンク模様を眼球に含めず旧20〜30%推定は撤回のまま。FBX/GLB往復を更新。
- **方式の限界:** 胴/脚の編集元とキーは残り、非破壊外皮の評価後トポロジーは姿勢で変わる。新しい鼻も既存geometry proofへ接続した候補で、固定トポロジーの最終Rig/morph・Motion演技・スマホruntime完成ではない。静的出力は鼻追加後12描画mesh、非描画の脚を二重exportしない。
- **残る外観判断:** 提示画像に対する鼻の小ささ・丸さ・本人らしさ・鼻口元の柔らかさはHuman再判定待ち。元の口周辺の横の境界、まぶた内眼角/半閉、座位の重み、開口笑顔の安心感、最終質感・毛並みも未確定。技術PASSを可愛さPASSにしない。
- **Tripo:** upload・Texture・Auto Rig・試行・課金なし。ローカル保存/往復確認でGOにしない。

## Next
Humanは現行REVIEWの参照比較とFront/Side/3Qで鼻先〜鼻下を再判定する。Codexは外観指摘から方法を選び直し、承認を捏造しない。Tripo操作には別途明示承認が必要。Goal√mapはWHY、Canonical/製品仕様は別の正本。重要な状態・承認・障害・担当変更時だけHandoffを更新する。
