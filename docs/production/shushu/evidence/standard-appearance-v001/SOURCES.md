# 最小構造調査 — 2026-10-17

以下の一次資料と公式説明を制作前に確認。植物の種をCanonicalに確定する資料ではない。実植物の構成要素を調べ、輪郭・色・配置のAuthorityには原画を使う。

| 出典 | 実物/仕様から採用した点 | Canonical優先の変更・限界 |
|---|---|---|
| [Harvard Arnold Arboretum: Tree of the Month — Cherry (PDF)](https://arboretum.harvard.edu/wp-content/uploads/2021/04/Tree-of-the-Month-Cherry_April-2021.pdf) | 多くのサクラは5花弁。花弁の切れ込み、蕊、花柄、萼/萼片を区別 | 自然の多数の蕊は目立つ放射状にせず小さい黄色中心へ簡略化。主花2輪のサイズ・向きは原画 |
| [Flora of North America / eFloras: Prunus](https://efloras.org/florataxon.aspx?flora_id=1&taxon_id=126865) | 葉身と葉柄、主脈、5萼片と5花弁、花弁の付け根・蕊という構造 | 二次脈数や種固有の比率を計測したとは主張しない。検索で得た一次記述を確認、ページ本文の再取得はtimeout |
| [Royal Botanic Gardens, Kew: Japanese cherry](https://www.kew.org/plants/japanese-cherry) | 緑の鋸歯葉、白/桃系の花のまとまり | 検索で得たKew記述を確認、本文は403。輪郭の細部・葉数/配置は原画優先で柔らかく簡略化 |
| [Blender Manual: glTF 2.0](https://docs.blender.org/manual/en/3.6/addons/import_export/scene_gltf2.html) | Mesh化、三角形、Principled BSDF、vertex color、skin/morph/animationという交換仕様 | 読めた公式検索本文の概念を使用。実際のBlender 5.2.1でexport/importを実行して互換を確認 |
| [Blender Manual: Solidify](https://docs.blender.org/manual/en/5.3/modeling/modifiers/generate/solidify.html) | 面に厚みと閉じた縁を付ける方式 | 風船状の厚みは付けず、曲率のある薄い花弁殻へ適用。5.2実行で結果を確認 |

側面・背面の花床/接続、浅い曲率と厚みは自然な範囲の設計推定。出典から同一のShushu花飾りを復元したとは主張しない。外部画像の転載・AI生成・有料取得・Tripo実行なし。
