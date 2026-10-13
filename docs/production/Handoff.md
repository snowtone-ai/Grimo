# Grimo — Handoff (last verified, not live authority)

このファイルは`main`のローカル作業案内。実行時のNOWは実際の制作ブランチ/HEAD、未コミット変更、制作StateとEvidenceで必ず再確認する。正式な仕様やHuman承認を上書きしない。

## Last verified: 2026-10-13 / Codex
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`
- **Continuation baseline:** `93869a8771045d7ed79ab036bd61d66ed97bd437`。2026-10-13の局所再判定修正は本更新と同じ制作ブランチにある。実行時にHEAD/remote/未コミット差分を確認する。
- **Shushu v003:** 保存済みモデルを局所編集。眼球部品総寸法と遮蔽後の見える寸法を分離。旧「眼球全体20〜30%拡大」推定は撤回のまま。見える横/縦はDonor約0.09627×0.10482に戻し、既存のまばたき構造を保持して中間lid環を緩和。座位の近位腿をpelvisへなじませ、立位・足裏・接触制御は保持。既存小開口/笑顔に独立MouthDonorOpenを追加。編集用Geometry・既存285フレームproof・静的FBX/GLBを更新。**Human Geometry Gate PENDING / Tripo HOLD**。
- **Evidence:** [現在のHuman Gate比較・計測・対象検証](shushu/evidence/geometry-v003/human-gate-revision/REVIEW.md)。正面/側面/3/4の同条件Clay＋簡易カラーで目3案、口Neutral→小→大→笑顔、立位/遷移/座位、閉眼を比較。簡易カラーは仮診断で、Donorに未符号化のピンク模様の3D実寸はUNKNOWN。旧REVIEWボード/GIFは変更前履歴。
- **再検証:** 保存再読込、Neutral復帰、upright/restで斜めblink、41段階支持、hold/self-contact、FBX/GLB往復、口36組の組合せsweepを確認。原本Donor・Canonical/4方向・承認参照・ユーザー差分のhashを保護。技術検証は可愛さ・生命感・自然さの承認ではない。
- **残る外観確認:** 採用併用案の目周り・半閉/閉眼、Donor規模の開口と笑顔の可愛さ、座位の腿〜臀部の柔らかさを新ボードでHuman再判定する。最終Rig・Motion演技・スマホruntime、最終注視印象は未確定。
- **Shushu v002:** 限定的Technical PASSだがHuman Visual FAIL（側面顔の奥行き、座位の腹部・短脚シルエット）。Technical PASSは外観品質の代替にならない。
- **保護した判断/資産:** Canonical・承認済み参照#01–26を維持。修正版#27はUNKNOWN。v001/v002を造形ドナーにせず、既存のローカル変更を保存。`main@526a1b3`の3文書方針を確認し、制作ブランチへmainを一括マージ/リベースしていない。
- **Tripo:** upload・Texture・Auto Rig・課金・無料試行を実行していない。Studio適合性・アカウント/クレジットはUNKNOWN。ローカルFBX/GLB往復だけでGOにしない。

## Next
**次のHuman操作:** 新比較資料で目・大開口/笑顔・座位を再判定する。Codexは外観指摘があれば該当部位を修正し、承認を捏造しない。Tripo操作には別途明示承認が必要。Goal√mapは制作WHY、製品仕様・Canonicalは別の正本。Handoff更新は重要な進捗・承認・障害・担当変更時のみ行い、履歴はGitとEvidenceへ残す。

**Migration:** 今後の3ファイルの正本は`main`上のローカルパス。旧`coord/grimo-ai-handoff`は履歴用であり、制作を始めるたびに取得しない。進行中の制作ブランチは勝手にマージしない。
