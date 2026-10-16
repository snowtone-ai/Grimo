# Grimo — ChatGPT Project Knowledge Router

**Version:** 2026-10-16  
**Canonical:** `main:docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_ROUTER.md` ([GitHub](https://github.com/snowtone-ai/Grimo/blob/main/docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_ROUTER.md))  
**役割:** ChatGPT Project Knowledgeから必要な正式資料へ到達するための固定案内。現在のHEAD、制作候補、Tripo残回数を記録する台帳ではない。

## 1. 起動時の最短経路

Grimoの実質的な制作・設計・調査に必要な最新版を、GitHub `main` から確認する。

1. [`AGENTS.md`](https://github.com/snowtone-ai/Grimo/blob/main/AGENTS.md) — 恒久的な実行規則・安全・Evidence・最小十分な実行。
2. [`docs/grimo/knowledge/Goal√map.md`](https://github.com/snowtone-ai/Grimo/blob/main/docs/grimo/knowledge/Goal%E2%88%9Amap.md) — G0〜G4のWHYと優先順位。
3. [`docs/production/Handoff.md`](https://github.com/snowtone-ai/Grimo/blob/main/docs/production/Handoff.md) — 最終確認時点の入口。**Live StateやHuman承認ではない**。

対象の制作ブランチ・remote HEAD・制作State・実物・Evidenceを別途照合する。GitHubだけではCodexのローカルdirtyを確認できない。無関係な資料の一括読み込み、内容不変の無条件な再取得を避ける。

**移行済み:** `coord/grimo-ai-handoff` は歴史的な調整ブランチ。旧`GRIMO_AI_HANDOFF.md`や旧Project Knowledge Router（2026-10-11/12）にある「専用ブランチを毎ターン取得・更新」は廃止。現行の規則は`main`の3ファイルを優先する。過去の実装ブランチを現行Authorityへ自動昇格しない。

## 2. Authorityと評価原則

最新の明示Human判断 → Canonical Identity／承認済み外観 → 正式製品・体験・制作仕様 → 実際の現行Git・制作State・Evidence → DRAFT／研究／履歴。矛盾は勝手に補完せず区別する。

- **GOAL-first:** G0（再訪したくなるタスク体験）←G1（可愛さ・愛着）←G2（生きた反応）←G3（3D/Motion/Runtime）←G4（技術衛生）。下位PASSで上位品質を犠牲にしない。
- **Preserve-first:** Canonical・原本・承認済み資産・他キャラ・ユーザー変更を保護。Identity維持に必要な局所修復や内部構造変更は許容。
- **Evidence-first:** 数値PASS ≠ Human外観PASS ≠ Motion/Runtime PASS。対象に応じた実レンダー、姿勢遷移、保存GLB、PlayCanvas・スマホ実機で確認。UNKNOWNをPASSにせず、Human Gateを自己承認しない。
- **Minimum-sufficient execution:** Geometry／Rig／Weight／Morph／Texture／Runtime等の原因を切り分ける。主要な副作用・後工程の破綻を予測し、最小十分な検証を行う。改善が停滞したら方式を再評価し、過剰実装・重複検証・サブエージェントを避ける。

## 3. 用途 → 読むべき正式資料

以下は`main`上のリポジトリ相対パス。個別ファイルのStatusとHuman承認範囲を優先。

| 目的 | 参照先 |
| --- | --- |
| 製品全体像（安定情報のみ） | `docs/grimo/knowledge/GRIMO_PROJECT_OVERVIEW_STABLE.md` |
| 正本の索引・実装配置 | `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md`、`docs/repo-map.md` |
| North Star／最低成立条件 | `docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md` |
| 相棒の行動・体験 | `docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md` |
| Full 3D／Motion／Runtime | `docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md` |
| Human・ChatGPT・Codex分担 | `docs/grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md`と`AGENTS.md` |
| Task／Calendar／Grimo／Collection、所有・報酬 | `docs/grimo/knowledge/product/GRIMO_PRODUCT_FEATURE_SPEC.md`、`GRIMO_DATA_MODEL_SPEC.md` |
| Blender参考技法（補助） | `docs/grimo/knowledge/character-production/GRIMO_BLENDER_IMPLEMENTATION_GUIDE.md` |

## 4. 4キャラ共通の制作ルート

| キャラクター | Identity・現状・確認対象 |
| --- | --- |
| **Jill** | `assets/grimo/source/jill/`のCanonical、対象Geometry/RigブランチとEvidence。翼・葉・尾の独立動作を確認 |
| **Pino** | `assets/grimo/source/pino/`のCanonical、対象Geometry/RigブランチとEvidence。短腕・太尾・支持/接触を確認 |
| **Shushu** | `assets/grimo/source/shushu/`のCanonical、対象Geometry/RigブランチとEvidence。顔の奥行き、短肢、plushな真の座位を確認 |

`docs/production/motion/GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`と`GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`はDRAFT。後続のHuman判断と個別制作Evidenceを見ずに正式仕様へ格上げしない。完成素材ではない参考画像・生成Pose・候補GLBも同様。

## 5. 個別Codexプロンプト：標準5項目

共通方針は最新の`AGENTS.md`を参照し、個別プロンプトには**今回の差分**を書く。通常1,000文字以内・厳格な上限1,500文字（Markdown・空白含む）。

1. **目的** — 最終GOALと欲しいユーザー体験。
2. **問題** — 現時点の具体的な未達事項。
3. **Authority** — 既存の正式資料・承認済み実物。
4. **制約** — 保護対象、変更範囲、課金/安全境界。
5. **完了条件** — 人間が確認できる成果、必要なEvidence、GO/HOLD、Scoped commit/push・remote HEAD、残課題。

原因調査・設計・実装方法・検証方法は原則Codexに委ねる。固定の修正回数・一律の全工程検証・高推論モデルの固定はしない。Model/Effort、新規/継続セッション、`/compact`はタスク別に判断する。

## 6. 更新境界

- **固定:** Router・Overviewは参照構造や恒久判断が変わったときだけ更新。進捗・コミット・Tripo残数は複製しない。
- **変動:** 重要な進捗・判断・障害・担当変更時のみ`main:docs/production/Handoff.md`を更新。実際のNOWは対象ブランチ・作業ツリー・Evidence。
- **保護:** 進行中の制作ブランチへ一括merge/rebaseしない。原本と他AI/ユーザー差分、秘密情報、過去履歴を維持。無断の課金・生成クレジット消費・破壊的操作は禁止。
- **歴史:** `coord/grimo-ai-handoff`、`docs/project-knowledge-router-20261011`、`docs/archive/`、旧Project Knowledgeルーター、旧Promptは履歴であり、現行の起動指示ではない。

**原則:** WHYはGoal√map、恒久ルールはmain AGENTS、進行先はmain Handoff、真実は現行ブランチの実物とHuman判断。

## 制作知見

[キャラクター3D制作の恒久知見](character-production/GRIMO_CHARACTER_3D_LESSONS.md)を参照。廃止済みキャラクターの制作導線は撤去済み。現役対象はJill / Pino / Shushu。

Body-only選定は `assets/grimo/source/body-only-multiview-manifest.json` と [Asset Register](character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md) を照合。現役3匹各4方向の12枚。画像承認はTripo・3D・Motion承認を意味しない。最新状態は作業branchの実物・Evidence・未コミット差分で確認する。
