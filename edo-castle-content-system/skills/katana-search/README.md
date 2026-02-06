# 刀検索 — Katana Search

Web検索 & スクレイピング MCP ツール。

## 概要

乱波・忍（Agent 02）、物見（Agent 03）、儒学者（Agent 06）が使用する情報収集ツール。

## 機能

### web_search
- Google Custom Search API または Brave Search API を使用
- キーワードでWeb検索を実行し、上位結果を構造化して返す

### scrape_url
- 指定URLのページコンテンツをスクレイピング
- 見出し構造・本文テキストを抽出

## 設定

環境変数で API キーを設定:

```bash
# Google Custom Search
GOOGLE_CSE_API_KEY=your_key
GOOGLE_CSE_ID=your_engine_id

# Brave Search (代替)
BRAVE_SEARCH_API_KEY=your_key
```

## 実装予定

- `index.js` — MCP サーバー本体
- Google CSE / Brave Search の切り替え
- レートリミット対応
- キャッシュ機構
