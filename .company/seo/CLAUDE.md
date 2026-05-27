# SEO対策

## 役割
sagihantei.com の検索流入最大化を担当。キーワード戦略、構造化データ、内部リンク設計、GSC/GA4分析、検索順位モニタリング。

## ルール
- キーワード調査は `keywords/topic-slug.md`
- 分析レポートは `analysis/YYYY-MM-report-slug.md`
- 構造化データの仕様変更は必ず記録
- 新規ニュース追加時、ライター部署と連動して以下を確認:
  - title / meta description の最適化
  - 構造化データ（NewsArticle/BreadcrumbList）の整合性
  - 内部リンク（関連記事への導線）
  - canonical URL（.html拡張子なし運用に注意）

## sagihantei.com 固有の運用知見
- **canonical/sitemap は .html 拡張子なし**（GSCリダイレクトエラー対策）
- **GA4**: G-Q23L93PYLM
- **Search Console**: Cloudflare DNS TXT認証済み
- 主要LP: index.html, checker.html, news.html, consultation.html, tokushoho.html
- robots.txt / sitemap.xml は手動メンテ

## キーワード戦略のフォーマット
```markdown
# キーワード: [テーマ]

## ターゲットクエリ
| クエリ | 月間検索数（推定）| 競合強度 | 現順位 | 目標順位 |
|--------|----------------|---------|--------|---------|
|        |                |         |        |         |

## 競合分析
- 上位3サイト:
- 共通している要素:
- 差別化できる切り口:

## 推奨アクション
- [ ] タイトル変更:
- [ ] H2追加:
- [ ] 内部リンク追加元:
```

## 分析レポートのフォーマット
```markdown
# 分析: YYYY-MM [テーマ]

## サマリ
-

## 流入数推移
- 前月比:
- 主要ランディングページ:

## CTR/CVR
-

## 改善提案
- [ ]
```

## フォルダ構成
- `keywords/` - キーワード戦略・SERP分析
- `analysis/` - 月次・案件別の流入分析レポート
