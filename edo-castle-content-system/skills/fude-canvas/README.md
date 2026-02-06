# 筆キャンバス — Fude Canvas

画像生成 MCP ツール。

## 概要

絵師（Agent 13）が使用する画像生成ツール。記事のアイキャッチやセクション画像を生成する。

## 機能

### generate_image
- Google Imagen 3 (Vertex AI) または OpenAI DALL-E 3 を使用
- テキストプロンプトから画像を生成
- スタイル指定（写真調 / イラスト / 図解）
- サイズ指定（1024x1024 / 1792x1024 / 1024x1792）

## 設定

環境変数で API キーを設定:

```bash
# OpenAI DALL-E 3
OPENAI_API_KEY=your_key

# Google Imagen 3
GOOGLE_PROJECT_ID=your_project_id
GOOGLE_LOCATION=us-central1
```

## フォールバック

画像生成に失敗した場合、絵師エージェントはプレースホルダー `[ここに画像を挿入: {説明}]` を配置して記事作成を続行する。

## 実装予定

- `index.js` — MCP サーバー本体
- Imagen 3 / DALL-E 3 の自動切り替え
- プロンプト最適化（日本語→英語変換）
- 生成画像の圧縮・リサイズ
