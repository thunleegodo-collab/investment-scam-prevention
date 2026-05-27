---
created: "2026-05-27"
topic: "個別ニュースの静的ページ化"
status: planning
priority: high
owner: seo
related_departments: [writer, web-design]
---

# SEOブリーフ: 個別ニュースの静的ページ化（NewsArticle schema本格対応）

## 現状の課題

`news.html` のニュース一覧は JavaScript の `news` 配列から動的レンダリングしている。

**SEO上の制約:**
- 個別ニュースに固有URLが存在しない（`#anchor` も実装されていない）
- 検索エンジンは個別事案を別ページとしてインデックスできない
- 構造化データの `ItemList` は追加済みだが、各 `ListItem.url` がアンカー扱いで本格的に効いていない
- 大型事案（GIL 870億円、SANAE TOKEN 等）の検索流入が「news.html」一極集中
- Google Discover / Google News 掲載のチャンスを逸している

## 目的

主要事案（特に2026年の `impact: high` 事案）を**独立した静的HTMLページ**として配信し、NewsArticle schema をフルに活かして検索流入を最大化する。

## ターゲット指標

| 指標 | 現状（推定）| 目標（3ヶ月後）|
|------|-------------|----------------|
| news系URLのインデックス数 | 1（news.htmlのみ）| 15+ |
| 個別事案クエリでの平均順位 | 不明（多くは未掲載）| 上位20位以内 |
| news系URLの月間流入 | 〜数百セッション | 5,000+ |
| Google News掲載 | 未確認 | 1事案以上 |

## 推奨アプローチ

### Option A: 完全静的化（推奨）

- `news/` ディレクトリを作成
- 主要事案ごとに `news/{slug}.html` を配置
  - 例: `news/global-investment-lab-2026-05.html`
  - 例: `news/aichi-87-oku-2026-05.html`
  - 例: `news/sanae-token-2026-03.html`
  - 例: `news/prince-group-2026-01.html`
  - 例: `news/pig-butchering-takedown-2026-05.html`
- 各ページに NewsArticle schema（headline / datePublished / author / publisher / mainEntityOfPage）
- パンくず BreadcrumbList を埋め込み
- `news.html` の一覧から各ページへリンク（カードクリックで遷移）
- Article ページから関連事案・有料相談へクロスリンク

**メリット:**
- 個別URLが立つ → NewsArticle schema が完全に機能
- 一次情報・関連リンク・引用元等を本文に展開できる（現在は150-400字制約）
- 内部リンクのハブとして機能
- Google News申請が現実的になる

**デメリット:**
- 初期実装コスト: 5〜10ページ × テンプレート設計＋執筆
- 運用: 新規ニュース追加時に「JS配列＋静的ページ」の二重管理

**対策:** JS配列を「カード生成のメタデータ」、静的ページを「詳細記事」と役割分担。配列に `detailUrl` フィールドを追加し、存在する事案はカードのタイトル/CTAから個別ページへ遷移。

### Option B: SSG（静的サイトジェネレーター）導入

11ty / Astro / Next.js static export 等で全ページをビルド時生成。

**メリット:** 配列1本管理で全ページ自動生成。

**デメリット:** 既存の静的HTML+vanilla JS構成からの逸脱。ビルドパイプライン構築・Cloudflare Pagesビルド設定が必要。学習コスト高。

→ **現時点では Option A を推奨**。事案数が50を超えたら Option B 再検討。

## 実装ステップ（Option A）

- [ ] ライター部署と協議：どの事案を静的化するか優先度づけ（GIL/SANAE/プリンスG/ピッグブッチャリング/愛知8.7億を最初の5本に推奨）
- [ ] Webデザイン部署とテンプレート設計：詳細ページのレイアウト・ナビ・関連事案表示
- [ ] `news/_template.html` を作成（NewsArticle schema・BreadcrumbList・OGP）
- [ ] 主要5事案を執筆・公開
- [ ] `news.html` の `news` 配列に `detailUrl` フィールド追加
- [ ] カード描画ロジックを更新（detailUrl があれば全カードリンク化）
- [ ] sitemap.xml を再生成（並行ブリーフ参照）
- [ ] GSCで新規URLのインデックス申請
- [ ] 1ヶ月後に流入分析

## リスク・注意

- Stripe審査ページ（tokushoho.html）には影響しないが、フッタ・ナビ変更時は要確認
- 個別ページのコンテンツが薄いと逆効果（Thin Content扱い）。各ページ最低1,500文字目安
- 一次情報源URLを必ず複数明記（推測表現は禁止）
- 「sagihantei.com」のEEATを高めるため、サンリー合同会社の運営情報を各ページ末に明示

## 次のアクション

- [ ] ライター部署にて、GIL記事を静的ページ版（1,500-2,000文字）に拡張する原稿起案
- [ ] Webデザイン部署にて、`news/_template.html` のワイヤー＆デザインブリーフ作成

## 参考

- Google News Publisher Center: https://publishercenter.google.com/
- NewsArticle schema 仕様: https://schema.org/NewsArticle
- Google検索セントラル「ニュース」: https://developers.google.com/search/docs/appearance/structured-data/news-article
