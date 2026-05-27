---
created: "2026-05-27"
topic: "sitemap.xml lastmod 自動更新運用"
status: planning
priority: medium
owner: seo
related_departments: [writer]
---

# SEOブリーフ: sitemap.xml の lastmod 自動更新運用

## 現状の課題

- `sitemap.xml` が手動管理で、`<lastmod>` が更新されていない可能性が高い
- ニュース追加・更新時に sitemap が反映されない
- GSCが「最終更新日」を取得できず、クロール頻度が最適化されない
- 個別ニュース静的化（並行ブリーフ）後に URL 数が急増する見込み

## 目的

`sitemap.xml` を常に最新状態に保ち、GSC のクロール頻度と再インデックスを最適化する。

## 現状確認すべき項目

- [ ] 現在の `sitemap.xml` の中身を確認
- [ ] 含まれているURL一覧と `<lastmod>` の値
- [ ] GSC上での sitemap 取得状況・エラー有無
- [ ] `robots.txt` で sitemap が正しく宣言されているか

## 推奨アプローチ

### Phase 1: 即時手動更新

- 主要ページの `<lastmod>` を今日付に更新
- news.html は2026-05-27に更新済みなのでこれを反映
- GSCで再送信

### Phase 2: 半自動化（推奨）

Cloudflare Pages のビルド時に簡易スクリプトで sitemap を生成。
ただし、本プロジェクトは「先回りでスクリプトを作らない」方針なので、**運用パターンの確立**を優先：

**運用ルール案:**
1. news.html を編集したら、即座に sitemap.xml の `news.html` 行の `<lastmod>` を編集日付に更新
2. 個別ニュースページ追加時（静的化ブリーフ実装後）も同様
3. 月末に全URL の `<lastmod>` 監査

### Phase 3: 完全自動化（事案数増加後）

URL 数が30を超えた段階で簡易ジェネレーター導入を再評価。
Cloudflare Pages の Functions または GitHub Actions で sitemap を生成。

## sitemap.xml 推奨フォーマット

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://sagihantei.com/</loc>
    <lastmod>2026-05-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://sagihantei.com/news</loc>
    <lastmod>2026-05-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <news:news>
      <news:publication>
        <news:name>詐欺判定.com</news:name>
        <news:language>ja</news:language>
      </news:publication>
      <news:publication_date>2026-05-27</news:publication_date>
      <news:title>2026年最新の投資詐欺ニュースまとめ</news:title>
    </news:news>
  </url>
  <!-- 静的化したニュース個別ページもここに -->
</urlset>
```

**ポイント:**
- `xmlns:news` 拡張で Google News 向けメタデータを付与
- `<priority>` で優先度を可視化（news.html は 0.9〜1.0 推奨）
- `<changefreq>` は実態に合わせる（毎月更新なら `monthly`、毎週なら `weekly`）

## 実装ステップ

- [ ] 現状の `sitemap.xml` を確認・スクリーンショット保存
- [ ] news 名前空間（news:news タグ）を未導入なら追加
- [ ] 全URL の `<lastmod>` を最新化
- [ ] `<changefreq>` を実態に合わせて調整
- [ ] GSCで sitemap 再送信
- [ ] 運用ルール確立（news.html編集時の同時更新）
- [ ] 1週間後にGSCの「カバレッジ」「sitemap」状況確認

## リスク・注意

- canonical URL は `.html` 拡張子なし運用（feedback_main_site_primary参照）。sitemap も同様に統一すること
- 古いURLが残っていると404扱いされるので、削除済みURLは sitemap からも除外
- GSCで sitemap エラーが出たら即対応

## 次のアクション

- [ ] 現在の sitemap.xml の中身を確認して状況把握（即実施可能）
- [ ] 静的化ブリーフ完了後、新URLを一括追加

## 参考

- Google News用 sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap
- sitemap.xml 仕様: https://www.sitemaps.org/protocol.html
