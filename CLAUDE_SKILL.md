# Claude Code 指示書 - sagihantei.com

## プロジェクト概要

このリポジトリはsagihantei.com（投資詐欺防止相談室）のソースコードです。
Cloudflare Pages経由で自動デプロイされます。

## 開発ルール

- 全HTMLファイルのheadにGA4タグ（G-Q23L93PYLM）が必須
- OGP画像には氏名を含めない（og-image.png）
- 特定商取引法ページ（tokushoho.html）は常に最新状態を維持
- 金商法に抵触する表現禁止（「元本保証」「必ず儲かる」等）

## デプロイ手順

```
git add .
git commit -m "変更内容"
git push
```

→ Cloudflare Pagesが自動デプロイ（数分で反映）

## よく使うコマンド

```
https://sagihantei.com
https://sagihantei.com/checker.html
https://sagihantei.com/tokushoho.html
```

## ファイル変更時の注意

- consultation.html：CalendlyリンクをSTORES予約URLに変更予定
- og-image.png：氏名なしバージョンに更新済み
- tokushoho.html：Stripe審査通過済み・変更時は要確認

## Stripe情報

| 項目 | 内容 |
|------|------|
| 決済リンク | https://buy.stripe.com/8x25kC6hXdwG5uiaMH9k401 |
| ビジネス名 | 投資詐欺防止相談室 |
| 審査 | 通過済み |

## STORES予約

| 項目 | 内容 |
|------|------|
| 管理画面 | dashboard.stores.app |
| メニュー | 投資詐欺判定・個別オンライン相談（30分）¥10,000 |
| 支払い | Stripeリンクを手動メール送信する運用 |
