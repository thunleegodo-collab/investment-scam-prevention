---
created: "2026-05-27"
topic: "RSS / Atomフィード実装"
status: planning
priority: medium
owner: seo
related_departments: [writer]
---

# SEOブリーフ: RSS / Atomフィード実装

## 現状の課題

- `news.html` の HTML head で `<link rel="alternate" type="application/rss+xml">` は宣言したが、実際のフィードファイルは未実装
- Google News / Feedly / 各種RSSリーダーから当サイトを購読できない
- ニュースサイトとしてのシグナルが弱く、Google Newsへの取り込みも阻害される
- 同業の啓発サイト（消費者庁、警察庁等）はRSS提供している

## 目的

RSSフィードを実装することで以下を達成：

1. Google News / Discover への取り込み確率を上げる
2. パワーユーザー（消費生活センター職員・弁護士・記者等）の定期購読獲得
3. 「ニュースサイトとしての継続更新」のシグナル強化
4. 自社の他チャネル（X, メルマガ）への流し込み元として活用

## ターゲット指標

| 指標 | 現状 | 目標（3ヶ月後）|
|------|------|----------------|
| フィードファイル提供 | なし | RSS 2.0 / Atom 提供 |
| フィード経由訪問者 | 0 | 月100セッション以上 |
| Google News 取り込み | 未確認 | 1事案以上掲載 |
| 外部サイトからのフィード参照 | 0 | 5サイト以上 |

## 推奨アプローチ

### フォーマット: RSS 2.0（推奨）

- Google News / Feedly 等の主要リーダーで広くサポート
- `<media:content>` 拡張で OG画像を含められる
- 1ファイル静的配信で済む（Cloudflare Pagesと相性◯）

### 配置

- `https://sagihantei.com/feed.xml`
- HEAD で `<link rel="alternate" type="application/rss+xml" title="..." href="/feed.xml">` を宣言

### 推奨フォーマット

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>投資詐欺ニュース | 詐欺判定.com</title>
    <link>https://sagihantei.com/news</link>
    <atom:link href="https://sagihantei.com/feed.xml" rel="self" type="application/rss+xml" />
    <description>2024〜2026年の投資詐欺最新事案・摘発情報・被害統計・法規制を毎月更新。SNS型投資詐欺・暗号資産詐欺・ロマンス詐欺・ポンジスキーム。</description>
    <language>ja</language>
    <lastBuildDate>Wed, 27 May 2026 00:00:00 +0900</lastBuildDate>
    <copyright>© 投資詐欺防止相談室（サンリー合同会社）</copyright>
    <category>News</category>
    <image>
      <url>https://sagihantei.com/og-image.png</url>
      <title>詐欺判定.com</title>
      <link>https://sagihantei.com/</link>
    </image>

    <item>
      <title>【深堀】Global Investment Lab事件 — 約7,300人から870億円を集金</title>
      <link>https://sagihantei.com/news#gil-2026</link>
      <description><![CDATA[警視庁は2026年5月14日、英領BVI籍「スターリング・ハウス・トラスト」への出資を無登録で勧誘したとして、GIL代表ら6人を逮捕...]]></description>
      <pubDate>Wed, 14 May 2026 00:00:00 +0900</pubDate>
      <guid isPermaLink="false">sagihantei-news-27-2026-05</guid>
      <category>ポンジ・スキーム</category>
      <dc:creator>投資詐欺防止相談室</dc:creator>
    </item>

    <!-- 直近10〜20件をここに繰り返し -->
  </channel>
</rss>
```

### 個別ニュースが静的化された場合（並行ブリーフ参照）

`<link>` を `https://sagihantei.com/news/{slug}.html` に置換。これで本格的なフィードとなり、Google News申請の質が上がる。

## 実装ステップ

- [ ] news.html の `news` 配列から直近20件を抽出して RSS 2.0 形式のXMLを手動生成
- [ ] `feed.xml` をリポジトリルートに配置
- [ ] news.html / index.html の `<head>` にalternate宣言追加（news.htmlは追加済み、URLを実ファイルに）
- [ ] sitemap.xml に `feed.xml` を追記
- [ ] Feedly Cloud に登録（手動申請）
- [ ] X（旧Twitter）の bio に RSS リンクを追加
- [ ] news更新時に feed.xml も同時更新する運用ルール確立

## 静的化との依存関係

- 静的化ブリーフが先に進めば、各 `<item>` の `<link>` を個別URLに昇格できる
- 静的化前は news.html#anchor で代用可能（NewsArticle schemaほどではないが、フィード自体は機能する）

## 運用フロー

```
[新ニュース追加]
  ↓
  1. news.html の news 配列に追記
  2. （静的化済みなら）news/{slug}.html を新規作成
  3. feed.xml の <item> を冒頭に追加（直近20件まで残す）
  4. sitemap.xml の <lastmod> 更新
  5. git commit & push
```

## リスク・注意

- フィード内の `<description>` は CDATA で囲み、HTMLが含まれる場合はescape必須
- pubDate は RFC 822 形式（`Wed, 27 May 2026 00:00:00 +0900`）厳守
- 直近20件以上を保持しない（フィードサイズ肥大化防止）
- フィード経由でも EEAT を担保するため、`<dc:creator>` で運営主体を明示

## 次のアクション

- [ ] 既存の news 配列直近20件から feed.xml の初版を生成
- [ ] Cloudflare Pages デプロイテスト（XMLのMIME type確認）
- [ ] Feedly / Google Reader系での表示確認

## 参考

- RSS 2.0 仕様: https://www.rssboard.org/rss-specification
- Google News フィード推奨: https://support.google.com/news/publisher-center/answer/9545420
- Feedly publisher 登録: https://feedly.com/i/discover
