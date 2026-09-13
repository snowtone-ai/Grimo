# Grimo Technical Architecture & Tooling

## 1. Runtime Architecture

正式方針:

```text
Next.js / React
├─ route
├─ UI / settings
├─ app state
└─ Grimo viewport host
     ↓
PixiJS
├─ layered sprites
├─ limited mesh deformation
├─ transforms
├─ semantic hit areas
├─ secondary motion
├─ particles / visual feedback
└─ render loop

TypeScript domain layer
├─ gesture classification
├─ interaction state
├─ emotion state
├─ affinity (採用時)
├─ repetition memory
├─ cooldown
└─ reaction selection
```

## 2. Why PixiJS 2.5D

- canonical illustration fidelity
- 1画面1キャラ
- fixed/limited camera
- Web/PWA向け
- Codexがコードで調整しやすい
- image layer / pivot / curve / hit zoneを自動生成・修正しやすい
- DCC authoringへの依存が小さい
- 4体へ横展開しやすい

## 3. Not the main path

- Full 3D
- Blender-based production
- Three.js character runtime
- Live2D Cubism
- Spine
- Unity
- Unreal
- Phaser as the character renderer
- `@pixi/react` as a required abstraction

これらは現在の本線を置き換えない。

## 4. Repository boundary

既存Grimoire本体:
- Next.js 16
- React 19
- TypeScript
- Tailwind CSS v4
- pnpm
- IndexedDB / Dexie
- existing Gmail / Calendar / Gemini integrations

Grimo touch featureのために既存の:
- task data
- persistence schema
- backup
- auth
- Google APIs
- Gemini
を不用意に変更しない。

## 5. Expected folders

```text
src/
  components/grimo/
  lib/grimo/
    runtime/
    interaction/
    motion/
    rendering/
    types/

assets/
  grimo/
    source/
    derived/

public/
  grimo/

tests/
  grimo/

docs/
  grimo/

artifacts/ or ignored output/
  grimo-qa/
```

## 6. Tooling policy

### Keep/use
- pnpm
- Playwright
- Chrome DevTools
- Context7
- codegraph
- FFmpeg
- ImageMagick
- Sharp
- pixelmatch
- pngjs
- existing screenshot/browser skills
- Grimo-specific repo skills

### Grimo-specific skills
- `grimo-art-director`
- `grimo-asset-pipeline`
- `grimo-motion-director`
- `grimo-interaction-runtime`
- `grimo-visual-qa`

### New MCP
原則 **0**。既存能力で不足が証明された場合だけ追加。

## 7. Dependency rule

「便利そう」だけでanimation/physics libraryを増やさない。

まず純粋TypeScriptで:
- easing
- spring
- damping
- reaction scoring
- cooldown
- gesture classification
を実装可能か確認。

依存追加は:
- 実測で必要
- maintenanceが妥当
- browser supportが十分
- Codexが再現可能
な場合だけ。

## 8. Environment status

ユーザー確認: **環境導入作業は完了済み。**

ただし、正確なpost-install version/statusはこのsource packでは再検証していない。  
実装時はリポジトリの最新 `environment-inventory.md` / `package.json` / MCP一覧を事実として確認する。

## 9. Legacy 3D warning

repoやProject Sourcesに Carol 3D / Blender 5.2 / Three.js資料が残っていても、それは比較実験・過去知見。

現在の正式決定:  
**PixiJS 2.5D layered runtime**

新しいチャットは旧3D資料だけを読んでarchitectureを巻き戻さない。
