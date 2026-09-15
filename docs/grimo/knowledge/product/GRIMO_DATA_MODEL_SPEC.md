# GRIMO_DATA_MODEL_SPEC.md

**Status:** Authoritative logical data specification  
**Date:** 2026-09-15  
**Purpose:** Grimoの商品仕様を実装するために「何を保存し、何を関連づけ、何を一時的に扱うか」を、技術製品を決める前の段階で固定する。  
**Audience:** CodeX等、過去Contextを一切持たないAI / 開発者。  
**Important:** この資料は「どのデータベースを使うか」を決めない。名前と関係を固定する資料である。

---

# 0. 最重要原則

Grimoは次の4画面を持つ。

```text
Task
Calendar
Grimo
Collection
```

Task / Calendar本体の詳しいデータ構造は別仕様で管理する。

この資料では、Grimo機能が必要とする次の出来事だけ受け取る。

```text
その日の最初のログイン
タスクが登録された
タスクが完了した
Grimoと触れ合った
```

この4つから報酬・Collection・Grimo体験を作る。

---

# 1. データ全体像

最低限、次のまとまりを持つ。

```text
UserGrimoState
CharacterDefinition
ItemDefinition
FoodDefinition
WearDefinition
SpecialDefinition
SecretMotionDefinition
GiftDefinition
InventoryEntry
CollectionEntry
ReactionDiscovery
EquippedWear
RewardEvent
RewardResult
RewardSettings
CharacterRuntimeState
InteractionSession
```

Task / Calendar側からは、

```text
TaskCreatedEvent
TaskCompletedEvent
```

だけ受け取ればよい。

---

# 2. 共通IDルール

すべての重要データには、画面表示名と別に、変更されないIDを持たせる。

例：

```text
characterId = "carol"
itemId      = "food_strawberry_001"
motionId    = "carol_moon_ball_play_001"
```

画面名を後から変えてもIDは変えない。

禁止例：

```text
itemId = "いちご"
```

理由：表示名は翻訳・修正される可能性があるため。

---

# 3. CharacterDefinition — 4匹の固定情報

1キャラクターにつき1件。

## 3.1 必須項目

| 項目 | 意味 |
|---|---|
| `characterId` | `carol`, `jill`, `pino`, `shushu` |
| `displayName` | 画面表示名 |
| `personalityProfile` | 性格の説明 |
| `available` | 現在利用可能か |
| `assetKey` | 3Dキャラクター資産への参照名 |
| `wearAnchors` | Wearを安全に装着できる位置 |
| `supportedFoodActions` | 対応できる食べ方 |
| `supportedTouchZones` | 触れ合い可能な場所 |

## 3.2 初期4件

```text
carol  = attention-seeking + relaxed
jill   = attention-seeking + energetic
pino   = energetic + independent
shushu = relaxed + independent
```

## 3.3 Wear装着位置

キャラクターごとに、自由座標ではなく名前付きの安全な装着位置を持つ。

### Carol

```text
head_top
ear_root_left
ear_root_right
fleece_front
```

### Jill

```text
head_center
neck_front
chest_front
```

### Pino

```text
head_top
neck_front
chest_front
```

### Shushu

```text
ear_outer_left
ear_outer_right
neck_front
chest_front
```

MVPでは1匹につきWear同時装着1個。

---

# 4. ItemDefinition — すべてのCollection報酬の共通親データ

すべての報酬は、まず共通の `ItemDefinition` として扱う。

## 4.1 種類

```text
FOOD
WEAR
SPECIAL
SECRET_MOTION
GIFT
```

将来の☆☆☆分類追加に備え、種類を増やせる作りにする。

## 4.2 必須項目

| 項目 | 型のイメージ | 意味 |
|---|---|---|
| `itemId` | text | 永続ID |
| `displayName` | text | 表示名 |
| `itemType` | enum | FOOD等 |
| `rarity` | 1〜6 | 星 |
| `description` | text | 説明 |
| `thumbnailKey` | text | Collectionカード画像 |
| `frameStyleKey` | text | レア度枠 |
| `discoverable` | true/false | Collection対象か |
| `enabled` | true/false | 現在報酬として出るか |
| `characterScope` | COMMON / CAROL等 | 使用対象 |
| `reactionTrackable` | true/false | 4匹反応収集対象か |
| `createdContentVersion` | text/number | 追加時期 |

## 4.3 `rarity`

```text
1 = ☆
2 = ☆☆
3 = ☆☆☆
4 = ☆☆☆☆
5 = ☆☆☆☆☆
6 = ☆☆☆☆☆☆ Gift
```

通常抽選で使うのは1〜5。

6はGift専用。

---

# 5. FoodDefinition

Foodアイテムだけが持つ追加情報。

## 5.1 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | ItemDefinitionと同じID |
| `eatingStyle` | 食べ方 |
| `preferenceByCharacter` | 4匹それぞれの好き度1〜5 |
| `foodSizeClass` | Motion調整用の大きさ区分 |
| `consumeAmount` | 1回で減る数。基本1 |

## 5.2 `eatingStyle`

初期候補：

```text
SMALL_ONE_BITE    小さい物を一口
MULTI_BITE        数回かじる
LICK              なめる
DRINK             飲む
LARGE_EAT         大きい物を食べる
```

Foodごとに専用Motionを作らず、この分類を使う。

## 5.3 好き度

```text
1 = 大嫌い
2 = 苦手
3 = 普通
4 = 好き
5 = 大好物
```

例：

```yaml
itemId: food_strawberry_001
preferenceByCharacter:
  carol: 5
  jill: 4
  pino: 3
  shushu: 5
```

## 5.4 好き度による消費

```text
1 → 食べない → Foodは減らない
2 → 食べる   → 1減る → 苦手反応
3 → 食べる   → 1減る → 普通反応
4 → 食べる   → 1減る → 好き反応
5 → 食べる   → 1減る → 大好物反応
```

## 5.5 Motion決定

Food使用時のMotionは、

```text
characterId
+ eatingStyle
+ preferenceLevel
+ current short-term character state
```

から決める。

Food名そのものをMotion名に直接結びつけない。

---

# 6. WearDefinition

Wearアイテムだけが持つ追加情報。

## 6.1 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | 共通ID |
| `allowedCharacters` | 装着可能Grimo |
| `anchorByCharacter` | 各Grimoの安全な取り付け位置 |
| `wearAssetKeyByCharacter` | 3D表示物への参照 |
| `replacesCanonicalAccessory` | 既存装飾を交換する特別Wearか |

MVPでは、

- 同時装着1個
- Wear側が取り付け位置を決める
- ユーザー自由移動なし

で固定。

---

# 7. SpecialDefinition

Specialは「特定Grimo専用」であることを意味する。

## 7.1 `specialKind`

```text
FOOD
WEAR
SECRET_MOTION
```

Toyは存在しない。

## 7.2 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | 共通ID |
| `targetCharacterId` | 専用Grimo |
| `specialKind` | FOOD / WEAR / SECRET_MOTION |
| `linkedContentId` | 実際のFood / Wear / Motion定義 |

## 7.3 消費

- `specialKind = FOOD` → 消費。
- それ以外 → 永久所有。

「Foodのみ消費」という商品ルールをここでも守る。

---

# 8. SecretMotionDefinition

Secret Motionは「特別な遊び / 特別な動き」を解放する。

## 8.1 必須項目

| 項目 | 意味 |
|---|---|
| `motionId` | Motion固有ID |
| `itemId` | Collection上のアイテムID |
| `characterScope` | 共通Themeか特定Grimoか |
| `activationMode` | USER_ONLY / AUTO_ONLY / BOTH |
| `motionAssetKeyByCharacter` | 各Grimo用Motion |
| `propAssetKey` | 小物が必要な場合 |
| `propSpawnRule` | いつ小物を出すか |
| `propRemoveRule` | いつ小物を消すか |
| `cooldownGroup` | 自発時の連発防止 |

## 8.2 Toy統合

旧ToyはすべてSecret Motionとして表現する。

例：

```yaml
motionId: carol_moon_ball_play_001
itemId: secret_motion_moon_ball_001
activationMode: BOTH
propAssetKey: prop_moon_ball_001
```

つまり「ボールという物を所有」ではなく、

> **Moon Ball Playという遊びを所有**

する。

---

# 9. GiftDefinition

Giftは通常抽選ではない。

## 9.1 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | GiftアイテムID |
| `sourceCharacterScope` | 誰からもらえるか |
| `giftMotionId` | 渡す時のMotion |
| `giftTriggerGroup` | 発生条件グループ |
| `enabled` | 現在出るか |

Gift確率は本仕様では数値固定しない。

「ふれあい中に超低確率」という商品仕様のみ固定。

---

# 10. UserGrimoState — ユーザーごとのGrimo全体状態

ユーザーごとに最低限、

| 項目 | 意味 |
|---|---|
| `activeCharacterId` | 現在Grimo画面で表示する相棒 |
| `ownedCharacterIds` | 利用可能Grimo |
| `lastLoginRewardDate` | その日のログイン報酬済み判定 |
| `rewardSettingsId` | 宝箱等の設定 |
| `collectionVersionSeen` | 新規追加表示等に使用可 |

を持つ。

**親密度の項目は作らない。**

禁止フィールド例：

```text
affection
relationshipLevel
relationshipXp
bondScore
hunger
neglectPenalty
```

---

# 11. InventoryEntry — 現在の所持状態

## 11.1 Food

Foodは数量を持つ。

```text
itemId
quantity
```

例：

```yaml
itemId: food_strawberry_001
quantity: 3
```

## 11.2 永久アイテム

Wear / 非Food Special / Secret Motion / Giftは、基本的に `owned=true` だけでよい。

```text
itemId
owned
firstAcquiredAt
```

重複数を増やさない。

---

# 12. CollectionEntry — 一度見つけた記録

InventoryとCollectionは同じではない。

Foodが0個になってもCollectionには残る。

## 12.1 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | アイテム |
| `discovered` | 一度でも発見したか |
| `firstDiscoveredAt` | 初発見 |
| `sourceFirstDiscovered` | 初発見の原因 |
| `timesAcquired` | これまで何回獲得したか |

例：

```yaml
itemId: food_strawberry_001
discovered: true
firstDiscoveredAt: 2026-09-15T10:00:00+09:00
sourceFirstDiscovered: TASK_COMPLETED
timesAcquired: 7
```

Food quantityが0でもこの行は残る。

---

# 13. ReactionDiscovery — 4匹の反応収集

1アイテム × 1キャラクターごとに記録する。

## 13.1 状態

```text
UNKNOWN      まだ反応を見ていない
DISCOVERED   反応を見た
NOT_APPLICABLE そのキャラでは使えない
```

## 13.2 必須項目

| 項目 | 意味 |
|---|---|
| `itemId` | 対象アイテム |
| `characterId` | Carol等 |
| `status` | UNKNOWN等 |
| `firstDiscoveredAt` | 初回反応発見日時 |
| `reactionKey` | 表示用の反応説明 / Motion family参照 |

## 13.3 Food

Foodを与えようとした時、好き度1で拒否して食べなくても、**反応は発見済み**とする。

理由：食べないこと自体がそのFoodへのReactionだから。

## 13.4 キャラ専用Special

対象外の3匹は `NOT_APPLICABLE`。

---

# 14. EquippedWear — 現在装着しているWear

1キャラクターにつきMVPでは最大1件。

```text
characterId
itemId
anchorId
equippedAt
```

Wearを外す場合は行を削除または `itemId = null`。

同時複数Wearを前提にした画面はMVPで作らない。

ただし将来拡張のため、データ上は `slotId` を追加可能な構造にしてよい。

---

# 15. RewardEvent — 報酬が発生した原因

「同じタスク完了から2回報酬を出す」事故を防ぐため、報酬の原因を記録する。

## 15.1 種類

```text
DAILY_LOGIN
TASK_CREATED
TASK_COMPLETED
INTERACTION_GIFT
```

## 15.2 必須項目

| 項目 | 意味 |
|---|---|
| `rewardEventId` | 一意ID |
| `eventType` | 上記4種 |
| `sourceId` | taskId / interactionSessionId等 |
| `occurredAt` | 発生時刻 |
| `processed` | 抽選済みか |
| `rewardResultId` | 結果への参照 |

## 15.3 重要

`TASK_CREATED` はタスク1件ごと。

ユーザーがタスクを100件作れば100回報酬イベントが作られる。これは仕様通りであり、不正扱いしない。

---

# 16. RewardResult — 抽選結果

## 16.1 通常抽選

通常の星確率：

```text
1星 70%
2星 20%
3星  6%
4星  3%
5星  1%
```

3星はMVPで空き枠。

3星が出た場合、ユーザーには見せず、利用可能なレア度が出るまで再抽選する。

## 16.2 報酬候補の制約

### DAILY_LOGIN

候補：

```text
FOODのみ
```

星の全体表をそのまま使う必要はない。ログインはFoodから選ぶ。

### TASK_CREATED

候補：

```text
FOOD
WEAR
```

### TASK_COMPLETED

候補：

```text
FOOD
WEAR
SPECIAL
SECRET_MOTION
```

### INTERACTION_GIFT

通常抽選を使わない。

```text
GIFT
```

のみ。

## 16.3 注意

「星を引く → そのアクションでは該当カテゴリがない」という場合も、空報酬にせず再抽選する。

実装時は、

1. アクションで許可されたアイテム集合を作る。
2. その集合に存在するレア度だけを有効にする。
3. 基本確率を保ちつつ再計算する、または再抽選する。

どちらでもよいが、**ユーザーが空を引かないこと**が必須。

## 16.4 保存項目

| 項目 | 意味 |
|---|---|
| `rewardResultId` | 一意ID |
| `rewardEventId` | 原因 |
| `rolledRarity` | 最終レア度 |
| `itemId` | 獲得物 |
| `wasDuplicate` | 永久アイテム重複か |
| `duplicateExchangePending` | Food交換待ちか |
| `revealedAt` | ユーザーへ表示した時刻 |
| `chestSkipped` | 自動開封だったか |

---

# 17. DuplicateExchange — 永久アイテム重複交換

永久アイテムが重複した場合に使用。

## 17.1 ルール

```text
永久アイテム重複
↓
重複品は増えない
↓
ユーザーへFood選択を出す
↓
発見済みFoodから1種類選ぶ
↓
選んだFood +1
```

## 17.2 保存項目

```text
exchangeId
sourceRewardResultId
sourceDuplicateItemId
selectedFoodItemId
quantityGranted = 1
completedAt
```

Foodの重複ではこの処理を使わない。

---

# 18. RewardSettings — 報酬演出設定

最低限、

```text
autoOpenChest: boolean
```

を持つ。

### false

```text
アクション
→ 宝箱
→ タップ
→ 報酬
```

### true

```text
アクション
→ 短いレア演出
→ 報酬
```

---

# 19. CharacterRuntimeState — 一時的な現在状態

これは親密度ではない。

Grimoが「今どういう感じか」を表す短期状態。

既存Motion Bibleとの整合のため、概念として次を持てる。

```text
valence         今の気分の良し悪し
arousal         落ち着き / 高揚
comfort         安心
curiosity       興味
socialSeeking   構ってほしさ
boundaryPressure 触れられすぎ等の軽い圧
restSeeking     休みたさ
engagement      今ユーザーへ向いている度合い
```

## 19.1 保存方針

MVPではほとんどを「短時間だけの状態」として扱う。

- 画面を開いている間は保持。
- 数秒〜数分で変化。
- 必要なら短いafterglowだけ再起動後へ持ち越してもよい。
- 数日・数週間の関係数値にはしない。

絶対に長期親密度へ変換しない。

---

# 20. InteractionSession — ふれあいの1回分

Gift抽選や反応履歴のまとまりとして、Grimo画面を開いて触れ合う1回を記録できる。

## 20.1 必須候補

```text
interactionSessionId
characterId
startedAt
endedAt
foodUsedCount
secretMotionUsedCount
touchCount
giftCheckPerformed
giftGranted
```

`giftCheckPerformed` を持つことで、同じSession中に不自然な連続Gift抽選を防ぐ。

具体的なGift判定回数は後で調整可能。

---

# 21. Food使用フロー

```text
Collection / Grimo画面でFood選択
↓
Inventory.quantity > 0 を確認
↓
activeCharacterIdを取得
↓
FoodDefinition.preferenceByCharacterを取得
↓
好き度1なら拒否Motion
  → Reaction DISCOVERED
  → quantityは減らさない
↓
好き度2〜5なら
  eatingStyle Motion
  → 好き度Motion
  → quantity - 1
  → Reaction DISCOVERED
```

## 21.1 重要

数量減少は「食べることが確定した時」に行う。

Motion開始前に先に0へしない。

途中エラー時にFoodだけ減る事故を防ぐ。

---

# 22. Wear使用フロー

```text
Collectionで所有済みWearを選択
↓
activeCharacterIdが装着可能か確認
↓
anchorを取得
↓
現在Wearがあれば外す
↓
新Wearを装着
↓
EquippedWear更新
↓
必要ならReaction DISCOVERED
```

Wear自体は消費しない。

---

# 23. Secret Motion使用フロー

```text
Collection / Grimoから所有済みSecret Motion選択
↓
activeCharacterIdで使用可能か確認
↓
activationModeにUSERが含まれるか確認
↓
必要なら小物を出す
↓
キャラ固有Motion再生
↓
余韻
↓
小物を消す
↓
Reaction DISCOVERED
```

`activationMode = AUTO_ONLY` はユーザーから直接実行不可。

`BOTH` はユーザー実行も自発実行も可能。

---

# 24. Giftフロー

```text
InteractionSession中
↓
Gift判定可能なタイミング
↓
超低確率判定
↓
不成立 → 何も起きない
成立 → Gift behavior開始
↓
GrimoがGiftを渡す
↓
Gift CollectionEntry作成
↓
Inventory owned=true
↓
RewardEvent(INTERACTION_GIFT)記録
```

Giftは通常宝箱に入れず、Grimo本人が渡す体験を優先する。

Collection追加時のカード表示演出は出してよい。

---

# 25. Collectionの並べ替えに必要なデータ

次を検索 / 並べ替え可能にする。

```text
itemType
rarity
displayName
firstDiscoveredAt
quantity
characterScope
reactionCompletionCount
reactionApplicableCount
```

## 25.1 Reaction completion

例：共通Food。

```text
4匹中3匹発見
reactionCompletionCount = 3
reactionApplicableCount = 4
```

Carol専用Specialなら、

```text
reactionCompletionCount = 1
reactionApplicableCount = 1
```

とする。

---

# 26. Collectionの絞り込みに必要な条件

最低限、

```text
itemType
rarity
characterScope
hasUnknownReaction
isReactionComplete
discovered
owned / quantity > 0
```

を使えるようにする。

Foodは「発見済みだが現在0個」もCollectionに表示する。

---

# 27. 同期するもの / 一時的なもの

技術は未選定だが、商品上の優先度を固定する。

## 27.1 端末間で必ず同じにする

- Collection発見状態
- Food数量
- 永久アイテム所有
- Reaction発見状態
- Wear装着状態
- Secret Motion解放
- Gift所有
- reward event / result
- duplicate exchange
- login reward date
- 設定

## 27.2 一時的でよい

- 現在再生中のMotion位置
- 今の目線の細かい位置
- 一時的なまばたき予定
- 触っている指の軌跡
- 数秒の微細な感情

## 27.3 再計算できる

- Collection完成率
- 各分類の所持率
- 反応完成率
- 「新着」バッジ

---

# 28. オフライン時の商品挙動

MVPの望ましい商品動作：

- すでに読み込み済みCarolとの基本触れ合いは可能。
- 所持済みFood / Wear / Secret Motionは、必要資産が端末にあれば使用可能。
- タスク登録 / 完了で報酬イベントを一旦端末へ保存できる。
- 通信復帰後に同じイベントを二重処理しない。
- Collectionは最後に同期した内容を表示。

Food数量等で衝突した場合は、消費・獲得の履歴から正しく再計算できるようにする。

---

# 29. 報酬抽選の疑似ルール

これは特定言語のコードではなく、実装規則。

```text
function rewardFor(eventType):
    allowedItems = enabled items allowed by eventType

    if eventType == INTERACTION_GIFT:
        use separate Gift rule
        return

    repeat:
        rarity = random by [70,20,6,3,1]
    until rarity exists in allowedItems

    candidateItems = allowedItems with that rarity
    item = random one candidate

    if item is consumable Food:
        add quantity
    else if already owned:
        create duplicate exchange
    else:
        mark owned

    mark Collection discovered
    save RewardResult
```

☆☆☆がMVPで空なので、自動的に再抽選される。

---

# 30. アイテム追加時の必須チェック

新アイテムを追加するAI / 開発者は、最低限次を埋める。

## Food

- itemId
- 名前
- ☆
- サムネイル
- eatingStyle
- Carol好き度1〜5
- Jill好き度1〜5
- Pino好き度1〜5
- Shushu好き度1〜5

## Wear

- itemId
- 名前
- ☆☆
- 使用可能キャラ
- 各キャラのanchor
- 各キャラの3D資産

## Special

- itemId
- 名前
- ☆☆☆☆
- targetCharacterId
- FOOD / WEAR / SECRET_MOTION
- linkedContent

## Secret Motion

- itemId
- motionId
- ☆☆☆☆☆
- characterScope
- activationMode
- 各キャラMotion
- 必要なら小物

## Gift

- itemId
- ☆☆☆☆☆☆
- sourceCharacterScope
- Gift Motion

---

# 31. 将来の拡張を壊さないためのルール

1. `itemType` は追加可能にする。
2. ☆☆☆はMVPで予約。
3. Wearは将来複数装着へ拡張可能だが、MVPは1個。
4. Secret Motionは小物を0個以上持てる形へ拡張可能にする。
5. ReactionDiscoveryは4匹以外の将来キャラ追加にも対応できる作りが望ましい。
6. Environment等を後で追加しても既存ItemDefinitionを壊さない。
7. 新Foodを追加しても新Motionを必須にしない。
8. 親密度フィールドを後付け前提にしない。

---

# 32. 絶対に作ってはいけないデータ

MVP / 現仕様では次を作らない。

```text
affection
bond
relationship_level
relationship_xp
hunger
sickness
neglect
streak_penalty
currency
coins
xp
shop_balance
loot_pack_inventory
```

旧2D / 2.5D版にこれらが存在しても、現仕様へ持ち込まない。

---

# 33. Phase別に必要なデータ

## Phase 1 — Carol 3D Proof

必要：

- CharacterDefinition(Carol)
- wearAnchors
- supportedFoodActions
- supportedTouchZones
- Motion名 / semantic mapping

本格Inventory等は不要。

## Phase 2 — App Foundation

**全データ構造を実装する。実アイテムはテスト用だけでよい。**

必要：

- ItemDefinition
- Food / Wear / Special / SecretMotion / Gift
- Inventory
- Collection
- ReactionDiscovery
- RewardEvent / RewardResult
- DuplicateExchange
- RewardSettings
- EquippedWear

## Phase 3 — Carol MVP

Carol用の本番Contentを追加。

## Phase 4 — Jill / Pino / Shushu

CharacterDefinitionと各キャラ専用資産・反応を追加。

## Phase 5 — Full Content

4匹のContent量を増やす。

---

# 34. Contextを持たないAI向けの最終要約

Grimoの商品データは、次の一文で理解できる。

> **タスク管理の行動からCollection Itemを抽選し、Foodだけ数量を消費し、それ以外は永久解放する。獲得物を4匹へ使うことでReactionDiscoveryを埋める。長期親密度は存在しない。**

通常レア度：

```text
☆      70%
☆☆    20%
☆☆☆   6%  ← MVP空き枠
☆☆☆☆  3%
☆☆☆☆☆ 1%
```

通常分類：

```text
☆      Food
☆☆    Wear
☆☆☆   Reserved
☆☆☆☆  Special
☆☆☆☆☆ Secret Motion
```

Gift：

```text
☆☆☆☆☆☆
通常抽選とは別
Grimoとのふれあい中に超低確率
```

Food好き度：

```text
1 大嫌い → 食べない / 減らない
2 苦手   → 食べる / 減る / 苦手反応
3 普通   → 食べる / 減る
4 好き   → 食べる / 減る / 喜ぶ
5 大好物 → 食べる / 減る / 大喜び
```

重複：

```text
Food重複 → quantity +1
永久アイテム重複 → 発見済みFoodを1個選んで交換
```

このルールを外れる変更をAIが独断で行ってはいけない。
