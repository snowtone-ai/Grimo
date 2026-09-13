# Grimo Interaction & Motion Bible

## 1. Reaction Grammar

原則:

```text
Input
→ contact acknowledgment
→ short anticipation / intent beat
→ local body response
→ facial / gaze response
→ main body motion
→ secondary motion
→ optional VFX/SFX/haptic
→ overshoot
→ settle
→ emotional afterglow
→ idle/attention
```

すべてを毎回大きく出す必要はない。  
重要なのは「触れたことが身体内部で伝わった」ように見える因果性。

## 2. Local-first

Touch reactionの基本:

1. 触れた部位が最初に反応
2. 隣接部位へ伝播
3. 顔 / 視線へ伝播
4. 全身は必要な場合だけ
5. secondaryが一拍遅れる

例:
`ear touch → ear flick → head tilt → eye/smile → fleece/leaf/flower settle`

## 3. Timing principles

- 完全即時反応だけにしない
- 反応遅延をゼロ固定にしない
- 触れた直後の小さいacknowledgmentは速く
- 大きいreactionは少し遅れて始める
- peakで止めずsettleを入れる
- settle後も表情/attentionを少し残す
- 同じ入力の反復では timing / amplitude / reaction variant をわずかに変える

## 4. Idle

良いIdle:
- 呼吸/微細な重心移動
- blink
- gaze shift
- 耳/尾/葉/花/泡の小さな独立動作
- 何もしない時間
- 周囲やplayerへ気づく
- rare self-initiated behavior

悪いIdle:
- 2秒周期で永久に同じ上下運動
- 全部位が同じ位相
- 常時player凝視
- 常時particle
- 常時happy

## 5. Gesture classification

最低限の意味分類:
- `touch`: 接触直後
- `tap/poke`: 短く小移動
- `pet/stroke`: 継続した移動
- `hold`: 小移動のまま一定時間
- `repeat`: 同部位・同gestureの反復
- `special`: touch map special zone

数値thresholdはprototypeで端末実測して調整し、過去のCarol 3D実験値を固定コピーしない。

## 6. Reaction selection

候補を単純完全randomにしない。

入力:
- body zone
- gesture
- current emotion
- recent reactions
- repetition count
- affinity（採用時）
- cooldown
- time since last input
- idle context

出力:
- primary reaction
- amplitude
- face preset
- gaze target
- secondary profile
- VFX/SFX profile
- settle state

## 7. Interruptibility

新入力が来たら長いclipをqueueし続けない。

原則:
- 現在pose/stateから次Reactionへredirect
- peak前後で自然なblend/redirect
- pointer releaseで意味のあるreactionを即消去しない
- `pointercancel`, lost capture, blur, hidden は接触を解除するが誤pokeを生成しない

## 8. Facial / Attention

生命感の優先順:
1. player/入力へのattention
2. gaze
3. blink/eyelid
4. mouth/cheek
5. ear/expressive appendage
6. body response

常に目だけ先に動かす、常に身体だけ先に動かす、という単一規則にはしない。キャラ差を持たせる。

## 9. Secondary Motion

物理正しさより **character readabilityと気持ちよさ** を優先。

- springは補助
- primary motionをphysicsへ丸投げしない
- damping / stiffnessは部位ごと
- root attachmentを崩さない
- secondaryはprimaryより遅れる
- settleで無限振動しない

## 10. Benchmark reference

### Primary
**Let's Go Pikachu/Eevee**
- petting response
- high-density partner attention
- touch→expression→body→afterglow

### Interaction grammar
**Pokémon-Amie**
- body-zone differences
- favorite/dislike/special zones
- repeated petting behavior

### Care / continuity
**Pokémon Refresh**
- continuous interaction
- start→continue→finish
- care as stateful interaction

### Autonomous life
**Sword/Shield Camp**
- self-initiated idle
- attention shift
- approach / wait / look-away

Reference clipを収集する場合:
- Let's Go: 8
- Amie: 5
- Refresh: 4
- Camp: 3
を初期目安にする。

## Imported reference notes

詳細なURL・provenance・timestampは `docs/grimo/references/` に保存する。そこにある
`pokemon-lets-go.md` の user-observation として、以下の事実だけを実装原則へ反映する。

- 00:09–00:18: 鼻への接触から予備動作、くしゃみ、頭振り、通常状態へ戻る。
- 00:30–00:45: ポケモン側からハイタッチを求める自己開始型の誘い。
- 00:30–00:34 / 01:16–01:20 / 02:42–02:45: ♪・♡・☆の感情記号が反応に添えられる。
- 01:18–01:27: 食べ物が一瞬で消えず、概ね3段階で進む。
- 02:31–02:35: 小さな頭振りのマイクロモーション。
- 03:35–03:45: ポケモン側からのプレゼントがアイテム取得へつながる。

`pokemon-amie-refresh.md` は timestamp 付き観察をまだ持たない candidate-only reference として扱い、ここへ具体的な観察を追加しない。
