# キャラクター廃止の棚卸し・実行記録

2026-10-17。Human依頼によりCarolを完全廃止。知見は先行commit `eca37a9` の [恒久知見](GRIMO_CHARACTER_3D_LESSONS.md) に保存済み。

## 棚卸しと確定方針（削除前）

- Grimo: `https://github.com/snowtone-ai/Grimo.git`。基点 `origin/main` = `8b5d13b`。元のShushu作業branch/HEADと未コミット変更は保護。
- task-plant: `C:/Users/chidj/project/task-plant`、remote `https://github.com/snowtone-ai/grimoire.git`。元branch `codex/product-system-map` = `84a759a666c5d2589685ff0aee3d098472ca1144`、当初clean。main = `0c067b8137346e94fba6ed38eb785f5c6d0acc33`。
- Grimo新branchはmain起点、task-plant新branchは現作業HEAD起点。どちらも `codex/retire-carol-20261017`。
- 専用ファイル: 下記64パス、各worktreeの名前が一致する専用assets/production/evidence/scripts/tempを削除候補に確定。共有ファイルは削除せず、専用節・行・表の列・manifest項目だけ編集。
- 専用worktree: face-ear-authority-match、face-ear-production-v003、face-repair-v001、mouth-v007、d42d、ffcfの6checkout。ffcfの11変更は全て廃止キャラ専用と確認。未知の共通/他キャラ未追跡データがなければ削除。
- 混在・他キャラworktree、統合branch、他タスク、IndexedDB/利用者データ、環境設定・秘密は保護。歴史的branch上の専用trackedコピーはsparse checkoutでローカルから外し、共有branchの履歴とユーザーの差分を改変しない。
- 名前に他キャラも含むbranch/画像は削除しない。用途不明の無名FBX/GLB・画像は保留。
- LFSは両repoの全refを棚卸し。用途非限定の `git lfs prune` / `git gc` / reflog失効 / 履歴rewriteは行わない。専用と証明できないobjectは保持。
- 専用branchだけを削除。混在branchの内容は保持。mainや他キャラbranchの過去commitはrewriteしない。廃止branchの削除は履歴からの物理消去を意味しない。
- 外部Tripo/クラウド生成物は本ローカル作業では確認・削除していない。

## 最新mainの専用削除パス

- `assets/grimo/production/carol/blender/.gitkeep`
- `assets/grimo/production/carol/manifests/.gitkeep`
- `assets/grimo/source/carol/approved-3d/.gitkeep`
- `assets/grimo/source/carol/approved-3d/authority.json`
- `assets/grimo/source/carol/approved-3d/carol-3d-production-canonical-sheet.png`
- `assets/grimo/source/carol/approved-3d/carol-back-ortho-transparent.png`
- `assets/grimo/source/carol/approved-3d/carol-front-ortho-transparent.png`
- `assets/grimo/source/carol/approved-3d/carol-side-ortho-transparent.png`
- `assets/grimo/source/carol/approved-3d/carol-top-plan-transparent.png`
- `assets/grimo/source/carol/approved-3d/carol_front.png`
- `assets/grimo/source/carol/approved-3d/carol_side.png`
- `assets/grimo/source/carol/approved-3d/carol_skin_front.png`
- `assets/grimo/source/carol/approved-3d/carol_skin_side.png`
- `assets/grimo/source/carol/approved-3d/modules/README.md`
- `assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.png`
- `assets/grimo/source/carol/carol-Identity-canonical.png`
- `assets/grimo/source/carol/rig-motion-references/CONTACT_SHEET.jpg`
- `assets/grimo/source/carol/rig-motion-references/MANIFEST.csv`
- `assets/grimo/source/carol/rig-motion-references/MANIFEST.json`
- `assets/grimo/source/carol/rig-motion-references/README.md`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-01-neutral-front-three-quarter.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-02-true-left-profile.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-03-natural-closed-eyes.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-04-opposite-front-three-quarter.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-05-rear-three-quarter.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-06-attentive.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-07-curious.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-08-anticipatory.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-09-content-small.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-10-content-deep.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-11-delighted.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-12-surprised-soft.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-13-uncertain.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-14-mild-discomfort.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-15-sleepy-dreamy.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-16-satisfied-savoring.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-17-forehead-lowered.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-18-left-cheek-offer.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-19-right-cheek-offer.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-20-front-fleece-compression.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-21-ear-root-touch.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-22-face-nestled-in-fleece.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-23-face-in-fleece-peek.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-24-affection-invitation-wait.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-25-low-forehoof-offer.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-26-hoof-adjustment.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-27-low-relaxed-rest.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-28-mild-withdrawal.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-29-warm-afterglow.png`
- `assets/grimo/source/carol/rig-motion-references/images/carol-ref-30-cloud-sigh.png`
- `assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_front.png`
- `assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_left.png`
- `assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_right.png`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `docs/production/carol/CAROL_AUTHORITY_MEASUREMENTS.md`
- `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- `docs/production/carol/CAROL_GEOMETRY_DECISION.md`
- `docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`
- `docs/production/carol/CAROL_MODELING_CONTRACT.md`
- `docs/production/carol/CAROL_NORMAL_SEMANTIC_RECONSTRUCTION_SPEC.md`
- `docs/production/carol/CAROL_PRODUCTION_STATE.md`
- `docs/production/carol/CAROL_REVIEW_LOG.md`
- `scripts/3d/build-review-packet.mjs`
- `scripts/blender/render-carol-gates.py`

## 実行結果・限定検証

- Grimoでは専用追跡ファイル64件を削除。共有docsの専用節・行・列・routingを除去し、Jill/Pino/Shushuの共通説明・データ項目・capability要件を保持した。アプリコードの専用依存は見つからず、アプリの実装変更はない。
- Grimo専用worktreeは5件を削除した。棚卸し候補ffcfは実行時に既に消えており、自分の削除件数・回収量に算入していない。
- Grimo専用branchはremote 11本/local 35本、task-plantはremote 1本/local 3本を削除。混在branch `codex/carol-pino-jill-main-integration-20261015` は他キャラ履歴を含むため保持。本タスクの `codex/retire-carol-20261017` も保持。
- task-plantの親のない旧復元履歴には共通アプリ/Muu/複数キャラ画像が含まれる。元commit `15bfa8e4c3a8ba24c246fe806bd125b307d8f076` をremote tag `archive/grimoire-shared-provenance-20261017` で保護した。現役制作への復帰導線ではない。
- 他キャラworktreeの専用trackedコピーはsparse除外。除外操作直後に既存dirty/untrackedファイルのSHA-256一致を確認した。その後240件は同じhashを維持。並行作業中のJill/Pinoスクリプト5件は後続照合で変化しており、本作業から上書き・復元はしない。既存branchのHEADは維持。
- 削除branch・worktree・pathと保護hashの詳細ログはローカル `C:/Users/chidj/.codex/retire-carol-audit-20261017/` の `inventory-before.json`、`local-cleanup.json`、`refs-lfs-cleanup.json`、`disk-after.json` に保存。
- 限定検証: app/test/publicおよび他3キャラの160追跡ファイルは内容不変（テキストのcheckout改行差だけ正規化）。Body-only manifestの他3キャラ12項目は元の値と一致し、全PNGのSHA-256一致。84 Familyカードは元の内容を保持し、廃止キャラとの比較文のみ除去。共有のMUST 77/238、OPTIONAL 7/14、合計84/252を維持。削除ファイルを指すMarkdownリンク0、現役Carol参照0（知見・廃止記録・Handoffの廃止宣言を除く）、両repo `git diff --check` を確認。
- フルテスト/build、3D生成・render・Human再承認は実施していない。見た目・Motionの新しいPASSを出す変更ではない。

## 容量測定

値は論理ファイルサイズ。対象pathの前後照合と専用LFS objectの実削除bytesを合算し、Git pack/共有履歴/他プロセスの増減を回収量へ混ぜない。NTFS割当サイズ・圧縮率とは異なる。

| Repo | 対象checkout・生成物 前→後 | ローカルLFS削除 | 確認した削減合計 |
|---|---:|---:|---:|
| Grimo | 8,693,067,564 → 0 bytes | 412,580,967 bytes | 9,105,648,531 bytes (8.480 GiB) |
| task-plant | 4,230,866 → 0 bytes | 0 bytes | 4,230,866 bytes (0.004 GiB) |

GrimoのローカルLFS全体は6,482,944,509 → 6,070,363,542 bytes。専用object 71件だけを削除した。task-plantのLFSは前後とも0。Cドライブ空きは参考値10,885,709,824 → 19,058,249,728 bytesだが、並行作業の影響があるため全差分を本タスクの効果としない。

## 残存・適用境界

両repoの変更は専用branchへcommit/pushする。mainと他キャラ作業branchの過去共有docsは本タスクbranchを取り込むまで廃止前の記載を含む。sparse除外はローカル実体を減らす操作であり、履歴上の依存除去commitの代わりではない。

無関係な歴史を保つため、Git commit/reflog/packと共有tag・複数キャラ画像・共有キャッシュは消去していない。remote LFS、Tripo等の外部生成物、所有不明の無名FBX/GLBは未削除。履歴rewriteは追加削減の可能性があるが、混在commit・共有画像・他branch・cloneとの整合を要する。安全な削減見込み量は未測定であり、今回実行しない。

## 最終清算の再確認 — 2026-10-17

上記は初回実行時の記録。再fetchしたremote mainは `28c1505b7aadf63db25f1be97eba8b99cd332cee`、task-plantは `6bca9b043196cce9941a8e4005c234938397e33b` で、廃止変更と恒久知見は既に統合済み。再merge/cherry-pickは行わない。

| 分類 | 今回の確認・処理 |
|---|---|
| SAFE_DELETE | Grimoの旧 `codex/retire-carol-20261017` はmainと同一SHA。cleanな専用worktree（367ファイル、論理152,421,160 bytes）とlocal/remote branchを削除。worktreeはmainに保存された共有ファイルの重複checkoutであり、Carol資産の追加削減量とは別計上 |
| SAFE_EDIT | 本監査の統合済み状態と残存境界を更新。コード・キャラクター資産変更なし |
| PROTECT | Jill/Pino/Shushuのbranch/worktree/dirty・untracked、混在統合branch、共有tag・Git履歴・sparse設定。task-plant旧廃止branchはmain未包含の別作業3コミット（`1a47f03`, `3101399`, `84a759a`）を含むためlocal/remoteとworktreeを保持。廃止差分のみmainへ移植済みで、当該branch全体が統合済みとは扱わない |
| UNKNOWN | 無名FBX/GLB、共有Git一時object、外部サービス資産。所有権・依存が証明できないため削除しない |

初回inventoryの既存worktreeを対象に専用名の残存を再確認し、削除済みlocal pathの復活0、既知のCarol専用LFS 71 OIDのローカル復活0。mainに専用名の追跡pathはない。履歴全体の再走査や広域pruneは行わない。Git packや一時objectには他作業が混在し、Carol専有容量を確定できないため保護。共有履歴rewriteによる追加実容量削減はUNKNOWN（ローカルで初回回収した412,580,967 bytesをremote削減見込みとみなさない）。

GitHub remote LFSは未削除。[公式案内](https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage)ではrepository削除・再作成、またはSupportへの相談が必要。共有repoの削除・履歴rewriteは本タスクではHOLD。管理者は初回OID台帳を添えてSupportへ個別purgeの可否と実容量を照会する。

Tripoの接続済み専用ツールはなく、plugin検索も該当なし。ブラウザー接続の確認はtimeoutし、アカウント内資産の確認・削除はできていない。外部削除はHOLD。所有者がTripoの自身のLibrary/生成履歴でCarolの名前と画像を照合し、専用モデルと派生exportだけを削除する必要がある。共有projectと他キャラは保持。追加クレジット消費なし。

task-plantのCI/保護設定は独立問題として別PRで記録・修正する。既存audit失敗を理由にmain保護をbypassしない。最終測定・保護設定前後・ref状態の機械証跡は `C:/Users/chidj/.codex/retire-carol-audit-20261017/final-*`。今回開始時のC空きは15,483,392,000 bytes。実空き差は並行作業を含むため上記論理削減量と同一視しない。
