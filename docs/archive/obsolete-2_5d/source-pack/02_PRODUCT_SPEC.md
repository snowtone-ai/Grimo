# Grimo Touch Feature — Product Spec

## 1. Goal

4体のグリモを1画面1キャラで表示し、直接触ることで「生き物を触っている」感覚を得られる高品質なWeb/PWA体験を作る。

品質ベンチマークは Pokémon の触れ合い系機能。  
特に:

1. **Let's Go Pikachu / Eevee** — 直接Touchの生命感
2. **Pokémon-Amie / ポケパルレ** — 部位別interaction grammar
3. **Pokémon Refresh / ポケリフレ** — continuous care / interaction後の余韻
4. **Sword/Shield Camp** — idle / attention / self-initiated behavior

S/V Picnic/Wash等は補助reference。

## 2. What “high quality” means

単なる解像度や3D精細さではない。

高品質 =
- identity fidelity
- touch causality
- local body reaction
- expressive gaze/facial
- weight shift
- anticipation
- follow-through
- secondary motion
- reaction timing
- settle / emotional afterglow
- controlled randomness
- character uniqueness
- stable mobile performance

## 3. Core user loop

```text
Observe
→ Grimo notices / idles
→ User touches
→ Body zone detection
→ Gesture classification
→ Internal state update
→ Reaction selection
→ Immediate local acknowledgment
→ Facial response
→ Primary body motion
→ Secondary follow-through
→ SFX / VFX / haptic if enabled
→ Settle / afterglow
→ Return to attention / idle
```

## 4. Interaction inputs

最低限:
- touch start
- tap / poke
- pet / stroke
- hold
- repeated touch
- body-zone differences

必要に応じて:
- gaze / pointer attention
- special zones
- rare reaction
- care
- food
- affinity

具体的な採否は回答済み事前質問リストを正とする。

## 5. Non-negotiables

- canonicalをidentityの唯一の正式基準とする
- AI生成補助画像をcanonicalへ昇格させない
- “generic cute animal”へ寄せない
- 触れた場所以外がいきなり大きく反応しない
- reactionは入力と因果関係が読み取れること
- continuous idle loopだけで生命感を作らない
- particleを常時出して誤魔化さない
- 同じキャラに見えなくなるdeformationは禁止
- reduced motionでも意味のある表情/状態は残す
- pointer cancel / lost captureで誤tapを発生させない
- tests passだけで完成扱いしない
- Human final gateを残す

## 6. Human role

人間はRigやAnimationを手作業する必要はない。

人間の役割:
- Identity判定
- A/B/CのIdle選択
- A/B/CのTouch Reaction選択
- 「速い/遅い/大きい/小さい/怖い/かわいい」など自然文の違和感指摘
- Final approval

AI/Codexはその評価を数値・curve・stateへ変換して修正する。
