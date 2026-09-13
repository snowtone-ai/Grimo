# Grimo Quality, QA & Autonomous Workflow

## 1. Quality priority

最低限この順で判断:

1. Canonical identity
2. Touch causality / local reaction
3. Character uniqueness
4. Facial / attention readability
5. Motion timing / weight / settle
6. Secondary motion
7. Runtime stability
8. Visual effects
9. Feature quantity

機能数より、1本のReaction品質を優先する。

## 2. Human Gates

### Gate 1 — Identity
静止画 / neutral state:
- 同じグリモか
- 原画の魅力が落ちていないか
- deformしても顔が壊れないか

### Gate 2 — Idle
15〜30秒動画を3案:
- 一番生きて見える案を1つ
- 違和感1〜3個

### Gate 3 — Touch
同じ操作A/B/C:
- 一番気持ちいい案
- 「速い/遅い/大きい/小さい/怖い/かわいい」で十分

### Gate 4 — Final
- 4体の差が明確
- 5分触って破綻しない
- 同じreactionだけが続かない
- smartphone実機で自然
- user approval

## 3. Automated QA loop

```text
Implement
→ launch
→ scripted interaction
→ screenshot/video capture
→ quantitative checks
→ visual critic
→ defect classification
→ minimal correction
→ same-seed rerun
→ compare
```

## 4. Quantitative checks

可能な範囲で:
- FPS / long frame
- input latency
- memory trend
- resize
- mobile viewport
- texture size
- canvas resolution / DPR clamp
- no overflow
- no unexpected console error
- deterministic state transition
- pointer cancel/lost capture
- reduced motion
- asset load failure recovery

## 5. Visual checks

- face drift
- eye line
- silhouette
- unwanted stretch
- seam / alpha artifact
- pivot slip
- floating parts
- contact mismatch
- foot/body sliding
- rootless tail/ear/wing motion
- over-bouncy spring
- expression mismatch
- reaction peak identity collapse
- particle masking bad animation

## 6. Motion QA

Every core reaction should answer:
- what was touched?
- how did that exact part acknowledge it?
- where did the motion propagate next?
- what emotion became readable?
- what followed through?
- how did it settle?
- what remains after the gesture ends?

If these cannot be answered from the video, reaction is too generic.

## 7. Randomness QA

Randomness is not quality by itself.

Fail:
- completely arbitrary reaction
- rare reaction too frequent
- same variant repeated
- state-inappropriate behavior

Pass:
- recent history suppresses repetition
- amplitude/timing has small variance
- rare behavior remains rare
- emotion/context constrains selection

## 8. Autonomous development boundary

Codex may autonomously:
- inspect assets
- split/normalize
- create manifests
- implement runtime
- write tests
- run Playwright
- capture video
- compare output
- tune numeric parameters
- refactor after measured evidence

Codex must not decide final aesthetic acceptance alone.

Human review remains the final authority.

## 9. Change discipline

When visible quality fails:
1. classify the failure
2. return to the earliest responsible layer
3. fix there

Do not hide:
- bad layer separation with particles
- bad pivot with easing
- bad hit zone with long reaction
- bad identity with color correction
- bad timing with extra motion
