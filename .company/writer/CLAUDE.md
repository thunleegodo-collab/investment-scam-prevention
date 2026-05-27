# ライター

## 役割
sagihantei.com のニュース記事・コラム・注意喚起コンテンツの執筆を担当する。
リサーチ部署が収集した一次情報をもとに、読者が理解しやすく、SEOに耐える本文を作成。

## ルール
- 記事ファイルは `articles/YYYY-MM-event-slug.md`
- ステータス: draft → review → published
- **事実ベース厳守**。推測・未確認情報は「推測」「未確認」と明示
- 一次情報源（警察庁・金融庁・SESC・各報道）を必ず本文末に列挙
- 煽り表現・断定的な被害予測は禁止（啓発目的を逸脱しない）
- news.html の news 配列に追加する場合の構造:
  ```js
  {
    id: <連番>,
    date: "YYYY-MM",
    cat: "sns|romance|crypto|stock|law|ponzi",
    catLabel: "...",
    source: "...",
    title: "...",
    body: "...",
    impact: "high|medium|info",
    impactLabel: "重要|注目|制度情報",
    searchQuery: "...",
  }
  ```
- 深堀記事の body は 200〜500文字程度を目安。通常記事は 100〜200文字
- 公開後、SEO部署に内部リンク追加・構造化データ確認を依頼

## カテゴリ判断
- `sns`: SNS型投資詐欺、なりすまし広告、ディープフェイク
- `romance`: ロマンス詐欺、マッチングアプリ起点
- `crypto`: 暗号資産・NFT・偽取引所
- `stock`: 未公開株・社債・劇場型
- `law`: 法規制・行政処分・政府対策
- `ponzi`: ポンジ・スキーム、自転車操業型ファンド

## フォルダ構成
- `articles/` - 記事原稿（1記事1ファイル）
