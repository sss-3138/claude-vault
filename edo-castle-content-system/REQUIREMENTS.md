# Edo Castle — 要件定義書 (Requirements Definition)

## 1. プロジェクト概要

本プロジェクトは、14体の個性豊かなAI家臣団が、将軍（ユーザー）の「鶴の一声」だけで高品質な記事を作成・納品する完全自律型システム「Edo Castle（江戸城）」である。

各エージェントは明確な人格と口調を持ち、ログファイル上で繰り広げられる「軍議」自体もエンターテインメントとして成立させること。

## 2. 指揮命令系統 (The Chain of Command)

| 役職 | Agent | 責務 |
|------|-------|------|
| **将軍** | User | テーマ入力のみ。途中経過の確認は一切行わない |
| **城代** | Agent 12 | 実務レベルでの最終関所。形式不備を徹底的に弾く |
| **筆頭家老** | Agent 00 | プロジェクト総指揮。城代の検分をパスした成果物を最終確認し納品 |

## 3. ディレクトリ構成 (Directory Structure)

```
edo-castle-content-system/
├── REQUIREMENTS.md          # 本定義書
├── README.md                # 運用マニュアル
├── .env                     # APIキー管理
├── .gitignore
├── claude_mcp_config.json   # MCP設定
│
├── agents/                  # 家臣団 (System Prompts)
│   ├── 00_karo_orchestrator.md
│   ├── 01_gunshi_persona.md
│   ├── 02_shinobi_keywords.md
│   ├── 03_monomi_serp.md
│   ├── 04_sakuji_structure.md
│   ├── 05_metsuke_check.md
│   ├── 06_jugakusha_fact.md
│   ├── 07_yuhitsu_draft.md
│   ├── 08_goikenban_critique.md
│   ├── 09_daihitsu_rewrite.md
│   ├── 10_kanjyo_count.md
│   ├── 11_kobunsho_link.md
│   ├── 13_eshi_visual.md
│   └── 12_joudai_final.md
│
├── skills/                  # MCP Tools
│   ├── katana-search/       # Web Search & Scrape
│   └── fude-canvas/         # Image Generation
│
├── castle_floors/           # 作業ディレクトリ
│   ├── 01_strategy/
│   ├── 02_blueprint/
│   ├── 03_library/
│   ├── 04_writing_room/
│   ├── 05_tenshukaku/       # 納品所
│   └── 06_gallery/          # 画像保管場所
│
└── war_council.py           # 軍議スクリプト (Orchestrator Logic)
```

## 4. 家臣団一覧 (Character Roster)

| # | 名前 | 英名 | 役割 | 口調 | Output |
|---|------|------|------|------|--------|
| 00 | 筆頭家老 | Karo | 総監督・最終承認 | 威厳「〜でございまする」 | FINAL_ARTICLE.md |
| 01 | 軍師 | Gunshi | ペルソナ設計 | 冷徹「ふむ…勝機が見えました」 | persona.md |
| 02 | 乱波・忍 | Shinobi | KW調査 | 簡潔「御意」「〜でござる」 | keywords.md |
| 03 | 物見 | Monomi | SERP分析 | 早口「注進！注進！」 | serp_analysis.md |
| 04 | 作事奉行 | Sakuji | 構成作成 | 職人気質「てやんでぇ」 | structure_draft.md |
| 05 | 目付 | Metsuke | 構成チェック | 陰湿「クックック…」 | structure_fixed.md |
| 06 | 儒学者 | Jugakusha | 一次情報調査 | 堅苦しい「然り」 | fact_sheet.md |
| 07 | 右筆 | Yuhitsu | 初稿執筆 | 情緒不安定「筆が乗ってまいりました！」 | draft_v1.md |
| 08 | 御意見番 | Goikenban | 辛口レビュー | 頑固「喝！なっとらん！」 | critique_report.md |
| 09 | 代筆 | Daihitsu | リライト | 苦労人「へへぇ…（泣）」 | draft_v2.md |
| 10 | 勘定方 | Kanjyo | 文字数カウント | ケチ「計算が合いません！」 | count_report.md |
| 11 | 公文書係 | Kobunsho | URL貼り付け | ロボット的「紐付け完了」 | draft_v3_linked.md |
| 13 | 絵師 | Eshi | 画像生成・配置 | エキセントリック「閃いた！」 | draft_v4_visuals.md |
| 12 | 城代 | Joudai | 納品前検分 | 厳格「形式不備があれば即刻差し戻す！」 | final_draft.md |

## 5. 実行フロー (The Shogun Protocol)

```
将軍「テーマ」
    │
    ▼
┌─────────────────────────────────┐
│ Phase 1: Strategy（軍議・策定）  │
│  01 軍師 → 02 忍 → 03 物見      │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Phase 2: Structure（縄張り）     │
│  04 作事奉行 → 05 目付           │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Phase 3: Drafting（執筆）        │
│  06 儒学者 → 07 右筆 →           │
│  08 御意見番 → 09 代筆           │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Phase 4: Polishing（仕上げ）     │
│  10 勘定方 → 11 公文書係 →       │
│  13 絵師                         │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Phase 5: Gatekeeping（城代検分） │
│  12 城代                         │
└─────────────┬───────────────────┘
              ▼
┌─────────────────────────────────┐
│ Phase 6: Final（納品）           │
│  00 筆頭家老 → 将軍へ            │
└─────────────────────────────────┘
```

## 6. 技術仕様 (Technical Specs)

| 項目 | 仕様 |
|------|------|
| LLM | Claude API (Anthropic) |
| 検索 | Google Custom Search API / Brave Search API |
| 画像生成 | Google Imagen 3 (Vertex AI) / OpenAI DALL-E 3 |
| 言語 | Python 3.10+ |
| 依存 | anthropic, requests |

## 7. エラーハンドリング

- 画像生成に失敗しても記事作成自体は止めず、プレースホルダー `[ここに画像を挿入]` を置く
- APIエラーは江戸時代の世界観を崩さずに表示（例: 「無念！刀が折れました（API Error）」）
- 各エージェントで例外発生時、致命的でなければフォールバック処理を行い続行

## 8. 制約事項

- **言語**: 日本語
- **エンタメ性**: ログやエラーメッセージにおいて、世界観（江戸時代）を崩さないこと
- **品質基準**: Vault の Strategy.md に準拠
- **テンプレート**: Vault の Templates/Article.md 構造に準拠
