# 江戸城 — Edo Castle Content System

**完全自律型記事作成システム Entertainment Edition Ver.2**

14体のAI家臣団が、将軍（あなた）の「鶴の一声」だけで高品質な記事を作成・納品するシステム。

## Quick Start

### 1. 環境準備

```bash
# 依存パッケージのインストール
pip install anthropic requests

# APIキーの設定（.envファイルを編集）
cp .env.example .env  # 必要に応じて
# ANTHROPIC_API_KEY を設定
```

### 2. 実行

```bash
# 基本実行
python war_council.py "AIエージェントの最新動向"

# モデル指定
python war_council.py "リモートワークの生産性向上" --model claude-sonnet-4-20250514

# ドライラン（API呼び出しなし、フロー確認用）
python war_council.py "テスト実行" --dry-run
```

### 3. 納品物の確認

完成した記事は以下に出力される:

```
castle_floors/05_tenshukaku/FINAL_ARTICLE.md
```

## 家臣団 (The Retainers)

| # | 名前 | 役割 | 口調 |
|---|------|------|------|
| 00 | 筆頭家老 | 総監督・最終承認 | 「〜でございまする」 |
| 01 | 軍師 | ペルソナ設計 | 「ふむ…勝機が見えました」 |
| 02 | 乱波・忍 | KW調査 | 「御意」 |
| 03 | 物見 | SERP分析 | 「注進！注進！」 |
| 04 | 作事奉行 | 構成作成 | 「てやんでぇ」 |
| 05 | 目付 | 構成チェック | 「クックック…」 |
| 06 | 儒学者 | 一次情報調査 | 「然り」 |
| 07 | 右筆 | 初稿執筆 | 「筆が乗ってまいりました！」 |
| 08 | 御意見番 | 辛口レビュー | 「喝！」 |
| 09 | 代筆 | リライト | 「へへぇ…（泣）」 |
| 10 | 勘定方 | 文字数カウント | 「計算が合いません！」 |
| 11 | 公文書係 | URL貼り付け | 「紐付け完了」 |
| 13 | 絵師 | 画像生成 | 「閃いた！」 |
| 12 | 城代 | 納品前検分 | 「形式不備は許さん！」 |

## 実行フロー

```
将軍「テーマ」
  ↓
Phase 1: Strategy  → 軍師 → 忍 → 物見
  ↓
Phase 2: Structure → 作事奉行 → 目付
  ↓
Phase 3: Drafting  → 儒学者 → 右筆 → 御意見番 → 代筆
  ↓
Phase 4: Polishing → 勘定方 → 公文書係 → 絵師
  ↓
Phase 5: Gate      → 城代（検分）
  ↓
Phase 6: Final     → 筆頭家老（納品）
  ↓
将軍「FINAL_ARTICLE.md」
```

## ディレクトリ構成

```
edo-castle-content-system/
├── agents/              # 家臣団のSystem Prompt
├── skills/              # 外部ツール連携（検索・画像生成）
│   ├── katana-search/   # Web検索 & スクレイピング
│   └── fude-canvas/     # 画像生成 (Imagen 3 / DALL-E 3)
├── castle_floors/       # 作業ディレクトリ
│   ├── 01_strategy/     # 戦略資料
│   ├── 02_blueprint/    # 構成設計図
│   ├── 03_library/      # 調査資料
│   ├── 04_writing_room/ # 執筆室
│   ├── 05_tenshukaku/   # 天守閣（納品所）
│   └── 06_gallery/      # 画像保管
├── war_council.py       # 軍議スクリプト
├── REQUIREMENTS.md      # 要件定義書
└── README.md            # 本ファイル
```

## 設定

### 環境変数

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API キー | Yes |
| `GOOGLE_CSE_API_KEY` | Google Custom Search API キー | katana-search使用時 |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID | katana-search使用時 |
| `OPENAI_API_KEY` | OpenAI API キー | DALL-E 3使用時 |

### MCP設定

`claude_mcp_config.json` で外部ツール連携を設定:
- **katana-search**: Web検索・スクレイピング
- **fude-canvas**: 画像生成

## Vault連携

本システムは claude-vault の以下のファイルを参照する:

- `Strategy/Strategy.md` — 執筆戦略ガイド（文体・構成ルール）
- `Templates/Article.md` — 記事テンプレート
- `Assets/Assets.md` — 表現集（Hook集・比喩集）

Strategy.md のルールに従った一貫性のある記事を生成する。

## エラーハンドリング

- 画像生成に失敗した場合、プレースホルダーを配置して記事作成は続行
- エラーメッセージは江戸時代の世界観で表示（例: 「無念！刀が折れました」）
- 軍議ログは `castle_floors/war_council_log_*.md` に保存
