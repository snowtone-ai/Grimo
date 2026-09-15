# Grimo — AGENTS.md

**ステータス:** リポジトリ運用の正式規約  
**基準:** smartphone-first PWA / Full 3D / Blender → GLB/glTF → PlayCanvas

## 1. 権威順位

競合時は次を優先する。

1. 現在のユーザー明示指示
2. 承認済みcanonical identity / 3D production reference
3. UI/UX・Audio・Hapticsは `DESIGN.md`
4. 現行Product / Data / Motion / 3D Production仕様
5. `docs/decisions.md` → `docs/state.md` → `tasks.md` → 現在のcode/tests
6. 外部調査
7. archive / legacy

旧PixiJS / 2D / 2.5D architectureは廃止済み。古いfileから復活させない。

## 2. Product固定前提

メイン画面：

```text
Task
Calendar
Grimo
Collection
```

Character基盤：

```text
Blender → GLB/glTF → PlayCanvas → smartphone PWA
```

Carolを最初のvertical sliceとし、合格後にJill / Pino / Shushuへ展開する。

companion viewは原則front-facing。side/backはproduction reference用途。

現在のGrimo app iconは正式採用品。明示指示なしに再生成・recolor・crop・rename・replaceしない。

## 3. 作業前確認

大きな変更前に最低限、`README.md`、`DESIGN.md`、`tasks.md`、`xp.md`、`docs/state.md`、`docs/decisions.md`、関連spec、変更対象fileを読む。archiveから現在仕様を推測しない。

## 4. UI / UX / Audio

`DESIGN.md` を正式規約とする。

アプリ全体は、ポケポケの観察可能なUI/UX grammarを可能な限り高精度で再現する。対象は情報階層、淡いblue-white neumorphism、spacing、typography、icon、button depth、押下感、transition、micro-interaction、sound、haptics、Collection、reward pacing。

ただしname / character / image / icon / audio / effectはGrimo独自とし、Pokémon asset・logo・無許諾font・抽出soundを使用しない。

意味のあるinteractionは一体で設計する。

```text
visual + motion + sound + optional haptic + result/loading feedback
```

## 5. Character Quality

canonical identityを技術都合より優先する。

禁止：

- 1枚絵全体を変形characterとして使う
- whole-body bob / scaleを生命感に使う
- physicsへhero pose決定を任せる
- 弱いactingをVFX / audioで隠す
- 全channel常時motion
- 同じpersonality animationを4体へretarget

Primary actingはsound / VFXなしでも成立させる。最終visual acceptanceはHuman Gate。

## 6. Runtime責務

```text
React / Next.js
  route, DOM UI, app state, settings, accessibility

PlayCanvas
  3D rendering, animation, camera, hit volume

TypeScript behavior
  gesture, state, attention, cooldown, repetition,
  selection, interruption

Data
  Task / Calendar / Collection / reward persistence / migration
```

rendererにroutingやtask persistenceを持たせない。React stateでper-frame 3D transformを駆動しない。

## 7. 既存system保持

専用migrationまでは、Task / Calendar semantics、Dexie migration / backward compatibility、stable source key / idempotency、Google read-only boundary、Gemini server-only secret、PWA / service worker、app icon、4体のidentity canonicalを保持する。

通常のrepo作業でGoogle Cloud / Vercel settingsを変更しない。

## 8. Secret / User Data

`.env.local`、credential、OAuth token、`GEMINI_API_KEY`、private user dataをprint・commit・upload・公開しない。`GEMINI_API_KEY` はserver-only、`.env.local` はGit ignoreを維持する。

## 9. Git

編集前：

```bash
git status
git branch --show-current
```

未commitのユーザー作業を保護する。明示指示なしにdiscard / reset / overwrite / stashしない。専用 `codex/` branchで作業し、許可なしに `main` へauto-mergeしない。


## 10. Engineering / Coding Principles

Grimoは短期prototypeではなく、長期間継続して機能追加・仕様変更・character追加・runtime改善を行うproduction applicationとして設計する。局所的な実装速度より、**変更容易性・拡張性・性能・データ安全性・検証可能性**を優先する。

### 10.1 Modularity — 変更範囲を局所化する

新機能は可能な限り、責務ごとに独立したmodule / domain / service / adapterへ分離する。

原則：

- 1つのmoduleは1つの主要責務を持つ。
- UI、domain rule、persistence、external integration、3D runtimeを混在させない。
- page / componentからdatabase・Google API・PlayCanvas内部実装を直接操作しない。
- feature間の連携は、明示的なinterface / event / repository / serviceを介する。
- 巨大な`utils.ts`、巨大なglobal store、god component、god serviceを作らない。
- copy-pasteで同じbusiness ruleを複製しない。意味を共有するlogicは適切なownerへ集約する。
- ただし、将来使うかもしれないという理由だけで抽象化を増やさない。**実際に存在する変更軸**を見て抽象化する。
- 既存moduleの責務を越える変更になる場合、無理に追記せず新しい境界を作る。

目標：

```text
仕様変更
→ 影響するmoduleが予測できる
→ 変更箇所が局所化される
→ 無関係なfeatureへ副作用を出さない
```

### 10.2 Extensibility — 追加を「既存コードの大量書換え」にしない

将来追加される可能性が高いものは、data / configuration / registry / typed contractとして拡張可能にする。

Grimoで特に拡張を前提とするもの：

- Character
- Motion / behavior family
- touch zone / gesture
- Food / Wear / Special / Secret Motion / Gift
- reward source / reward rule
- Collection filter / sort
- character-specific preference / reaction
- animation channel / runtime state
- Wear anchor
- audio / haptic / VFX cue
- feature flag / content version
- persistence migration

新しいcharacterやitemを追加するために巨大な`switch(characterId)`を複数fileへ増殖させない。

ただしplugin systemやgeneric frameworkを先回りして作りすぎない。**現在確認できる拡張軸には明示的extension pointを作り、未知の未来には単純で変更しやすいcodeを残す。**

### 10.3 Performance is a Product Requirement

ユーザー体験を損なう遅延・カクつき・不要なloadingをtechnical debtとして扱う。

原則：

- smartphone-firstで設計し、desktop性能を基準にしない。
- hot pathでは不要なallocation、serialization、deep clone、full scanを避ける。
- React render loopとPlayCanvas per-frame loopを分離する。
- per-frame 3D stateをReact stateへ流さない。
- animation / touch / pointer move等の高頻度eventで不要なReact rerenderを起こさない。
- expensive calculationは必要に応じてprecompute / cache / index化する。
- independent async workは安全な範囲でparallelizeし、不要なwaterfallを作らない。
- route初期表示に不要なlarge dependency / 3D asset / editor-only codeを読み込ませない。
- dynamic import / lazy loading / streaming / cachingを、実測で効果がある場所へ使う。
- asset size、texture size、GLB size、animation count、memory、draw call等を無制限に増やさない。
- performance改善のためにcanonical identityやinteraction qualityを勝手に下げない。必要ならtrade-offをHuman Gateへ上げる。

性能問題は感覚だけで修正せず、可能な限りprofile / measurementで原因を特定する。

visible feature変更後は、必要に応じて以下を確認する。

```text
startup / route transition
interaction latency
main-thread blocking
unnecessary rerender
network waterfall
bundle growth
memory growth
PlayCanvas frame pacing
real-device thermal / sustained performance
```

性能regressionを新機能の当然の代償として放置しない。

### 10.4 Stable Contracts / Dependency Direction

依存方向を明確にする。

```text
UI
↓
application / use-case
↓
domain
↓
repository / ports
↓
infrastructure / external integration
```

3D runtimeは同様に、

```text
Grimo behavior / interaction contract
↓
PlayCanvas adapter
↓
engine-specific implementation
```

とする。

原則：

- domain logicはNext.js page、browser API、Dexie、Google API、PlayCanvas APIへ直接依存させない。
- external API responseをapp全体へ直接流さず、境界でvalidate / normalizeする。
- public interfaceを変更する時はcallerを列挙し、migration pathを確認する。
- circular dependencyを作らない。
- hidden global mutable stateを避ける。
- module内部実装を別featureからdeep importしない。

### 10.5 Type Safety / Data Validation

TypeScriptの型をdocumentationではなくconstraintとして使う。

- `any`は原則禁止。必要な場合は理由を局所コメントで明示する。
- `unknown`からの境界入力はvalidationしてからdomainへ渡す。
- nullable / optional stateを曖昧にしない。
- impossible stateは型で表現しにくくする。
- string literalの乱用を避け、stable ID / enum / discriminated union等を適切に使う。
- API、storage、import、migration、GLB metadata等、外部境界ではruntime validationを行う。
- display nameとstable IDを混同しない。

### 10.6 Data Integrity / Migration First

Grimoは永続利用を前提とするため、ユーザーデータ破損を重大障害として扱う。

- schema変更はmigrationを伴う。
- migrationは可能な限りidempotentかつ再実行可能にする。
- destructive migrationはbackup / recovery pathなしに実行しない。
- existing user dataを「開発中だから」で初期化しない。
- derived dataは可能なら再計算可能にし、source-of-truthを増やしすぎない。
- reward / inventory / task / collection等の重複処理はstable event IDやidempotency keyで防ぐ。
- migration前後のinvariantをtestする。
- version fieldを持つ永続dataは、古いversionの読み込み戦略を明示する。

### 10.7 Error Handling / Resilience

失敗を握りつぶさない。

- expected failureとprogramming bugを区別する。
- user-facing errorは、可能なら再試行・復旧・安全なfallbackを提供する。
- network failureで保存済みデータを失わない。
- offline / reconnect / duplicate requestを考慮する。
- background failureがprimary interactionを不必要にblockしないようにする。
- `catch {}`、無条件fallback、silent data lossは禁止。
- error messageへsecret / token / private dataを含めない。
- recovery不能なinvariant violationは明確にfailし、原因を隠さない。

### 10.8 Testing Strategy

testは実装詳細ではなくcontract / behavior / regressionを守る。

優先順位：

```text
domain rule / data integrity
→ integration boundary
→ critical user flow
→ visual / interaction regression
→ implementation detail
```

原則：

- bug fixには、再発可能ならregression testを追加する。
- pure domain logicは高速なunit testを優先する。
- repository / migration / external adapterはintegration testを持つ。
- Task作成・Task完了・reward・Collection・Grimo interaction等の主要flowはend-to-endまたは同等の検証経路を持つ。
- testを通すためにproduction behaviorを歪めない。
- flaky testを放置しない。
- snapshotだけでbusiness correctnessを保証しない。
- 3D visual / motion qualityはautomated testだけで合格にしない。Human Gateを維持する。

### 10.9 Refactoring Rules

大規模変更では「全部書き直す」より、安全な段階移行を優先する。

- behaviorを変えないrefactorとfeature変更を可能な限り分離する。
- public contractを保ちながら内部を置換できる場合は段階移行する。
- 新旧実装を一時併存させる場合、削除条件とownerを`tasks.md`へ残す。
- dead code / obsolete adapter / temporary compatibility layerは完了後に削除する。
- TODOを恒久仕様の代用にしない。
- 1回のdiffが大きすぎて検証不能になる場合は、atomic milestoneへ分割する。
- ただし単一の仕様変更を不自然に細切れにして、中間状態を長期間壊したままにしない。

### 10.10 Readability / Maintainability

codeは将来のAI agentとhuman engineerの両方が安全に変更できる状態にする。

- 名前は短さより意味を優先する。
- boolean名はtrue/falseの意味が明確な形にする。
- magic number / magic stringは意味のあるconstant / configへ置く。
- commentは「何をしているか」より「なぜこの制約が必要か」を残す。
- algorithm / business rule / workaroundの根拠が将来失われる場合は短い理由を残す。
- generated codeとhand-written codeの境界を明確にする。
- fileを無制限に肥大化させない。複数の独立責務が見えた時点で分割を検討する。
- abstractionを深くしすぎて処理経路を追えなくしない。
- clever codeよりpredictable codeを優先する。

### 10.11 API / Async / Concurrency Discipline

- async処理の依存関係を明示し、独立処理を無意味に直列化しない。
- race conditionが起こり得るstate mutationにはownership / ordering / cancellationを設計する。
- stale requestが新しいstateを上書きしないようにする。
- user操作連打、二重submit、route change、component unmountを考慮する。
- debounce / throttleは症状隠しとして使わず、interaction semanticsに合わせる。
- optimistic updateはrollback可能な場合だけ使う。
- external API callにはtimeout / cancellation / retry policyを必要に応じて設ける。
- retryで重複副作用が起きないことを確認する。

### 10.12 Dependency Discipline

新規dependency追加前に、

1. 標準API / 現dependencyで十分でないか
2. bundle / runtime / maintenance cost
3. browser compatibility
4. security / update frequency
5. project longevity
6. tree-shaking / client inclusion

を確認する。

小さな処理のために大きなdependencyを追加しない。abandoned / unmaintained packageへcore architectureを依存させない。

lockfileを維持し、理由なくmajor versionをまとめて上げない。

### 10.13 Security / Privacy by Design

- clientへsecretを送らない。
- inputをtrustしない。
- auth / authorizationをUI表示だけで担保しない。
- URL、query、storage、API response、import file等をuntrusted inputとして扱う。
- HTML injection / unsafe URL / arbitrary code executionを避ける。
- dependency / build script変更ではsupply-chain riskも確認する。
- private user dataをanalytics / logへ不用意に送らない。
- permissionは必要最小限にする。

### 10.14 Accessibility / Interaction Robustness

performanceと同様にaccessibilityを後付けにしない。

- touch target、keyboard、focus、screen reader semanticsをDOM UIで維持する。
- colorだけで状態を伝えない。
- reduced motion設定を尊重する。ただしcharacter identityを壊す単純な全停止ではなく、安全な低motion表現へ落とす。
- loading / disabled / error / success stateを明確にする。
- gesture-only操作には必要に応じて代替手段を持つ。
- safe-area / viewport / orientation / mobile keyboardを考慮する。

### 10.15 Observability / Diagnosability

永続運用を前提に、問題を再現できる状態を作る。

- critical flowは、secret / private dataを含めず診断可能なerror contextを残す。
- opaqueな「何か失敗した」だけにしない。
- runtime error、network error、migration failure、asset load failureを区別できるようにする。
- production-only bugを追跡できないarchitectureにしない。
- performance regressionは再計測可能な手順を残す。

### 10.16 Definition of Done for Engineering Changes

codeを書いただけでは完了ではない。

変更内容に応じて最低限確認する。

```text
correct responsibility / module boundary
type safety
backward compatibility
migration safety
error / offline behavior
performance impact
accessibility impact
tests
build / lint / typecheck
browser / mobile behavior
documentation / decision update
dead code removal
```

重要なarchitecture変更では、なぜその構造を採用したかを`docs/decisions.md`へ残す。

---

## 11. 検証

`pnpm` を使用する。適用可能なら以下を実行する。

```text
pnpm typecheck
pnpm test
pnpm lint
pnpm build
pnpm verify
```

visible UI変更ではreal-browser mobile checkも行い、route、console/runtime/network error、safe-area、keyboard、touch target、pressed/released state、audio/mute、reduced motion、必要に応じてPixel 7a級performanceを確認する。

3Dのautomated metricは証拠であり、最終合否はHuman Gate。

## 12. Documentation

- `tasks.md`: 現在地 / 次作業 / acceptance / blocker / branch / verification
- `xp.md`: 再現可能なengineering lessonのみ
- `docs/decisions.md`: 長期decision
- `docs/state.md`: 現在のproduction fact

obsolete historyをcurrent truthとして扱わない。

## 13. 停止条件

canonical identity失敗、Task/Calendar compatibility破壊、user dataを危険にするmigration、browser/PWA regression、secret handling不明、`DESIGN.md`から重大逸脱、未承認quality lossが必要、Human Gate不合格のいずれかでは、問題を隠さず停止して報告する。

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
