# Grimo Project — Source Index

更新: 2026-09-13 JST

このファイルは、ChatGPT の `grimo` プロジェクトで新しいチャットを開始したときの **最初の参照先** とする。

## 1. 現在の正式スコープ

対象は以下の3体の「グリモ」だけ。

- Jill — 植物ドラゴン
- Pino — 水・泡モチーフのカワウソ
- Shushu — 桜モチーフのパンダ

## 2. 現在の正式開発方式

**Next.js 16 / React 19 の既存PWA + PixiJS 8系による 2.5D layered character runtime**

- React: route / UI / app state / viewport host
- PixiJS: character rendering / layered sprites / local mesh deformation / pointer hit / secondary motion / particles / render loop
- renderer外のTypeScript: gesture / interaction / emotion / affinity / cooldown / reaction selection
- 1画面1グリモ
- fixed〜limited view
- canonicalイラスト忠実度を最優先
- Human final gateあり
- 完全3D、Live2D、Spineを本線にしない
- `@pixi/react`を前提にしない

## 3. Source of Truth の優先順位

矛盾した場合は上を優先する。

1. 現在のユーザー指示
2. 3体の canonical 画像
3. **回答済みの事前質問リスト**
4. この source pack の `01_CURRENT_STATE.md`
5. `02_PRODUCT_SPEC.md`
6. `03_CHARACTER_BIBLE.md`
7. `04_INTERACTION_MOTION_BIBLE.md`
8. `05_ASSET_MANIFEST.md`
9. `06_TECH_ARCHITECTURE_AND_TOOLING.md`
10. `07_QUALITY_QA_WORKFLOW.md`
11. 実リポジトリの現在コード・現在の `AGENTS.md` / `tasks.md` / `repo-map.md` / `environment-inventory.md`
12. 古い会話・旧実験資料

### 重要
実装時にコードとこのsource packが食い違う場合は、勝手に統合しない。  
**「現在のユーザー決定」と「現在のrepo事実」を分離して差分を報告する。**

## 4. ChatGPT Project に常時置くもの

### 必須テキスト
- `00_SOURCE_INDEX.md`
- `01_CURRENT_STATE.md`
- `02_PRODUCT_SPEC.md`
- `03_CHARACTER_BIBLE.md`
- `04_INTERACTION_MOTION_BIBLE.md`
- `05_ASSET_MANIFEST.md`
- `06_TECH_ARCHITECTURE_AND_TOOLING.md`
- `07_QUALITY_QA_WORKFLOW.md`
- **ユーザーが回答済みの `事前質問リスト.md`**

### 必須画像
- Jill canonical
- Pino canonical
- Shushu canonical

## 5. 常時置かなくてよいもの

コンテキスト汚染を避けるため、以下は repo / File Library に保存し、対象キャラの作業時だけ参照する。

- 3体 × 8 = 32枚の開発補助画像本体
- 画像生成用プロンプト集
- 完了済みの開発前タスクリスト
- 古い環境導入手順
- Muu関連資料
- 長いQAログ
- build output
- `.blend` / `.glb`
- screenshot/videoの全履歴
- 古いDeep Research全文

32枚については `05_ASSET_MANIFEST.md` を常時情報源にし、必要時に該当画像だけ開く。

## 6. 旧資料の扱い

そこから再利用してよいのは思想だけ:
- canonicalを壊さない
- interactionは部位別
- touch / poke / pet / hold を区別する
- reactionはinterruptible
- pointer cancel / lost captureで誤反応しない
- visual QAをtestsより上位の品質判定にする
- 最終判定はユーザー
