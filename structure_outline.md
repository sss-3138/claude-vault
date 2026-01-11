# Claude Code Vault フォルダ・ファイル構成（骨子）

## ルート構成

```
VaultRoot/
├── CLAUDE.md                    # 会社のビジョン（憲法ファイル）
├── README.md                    # Vault説明書
│
├── 00_rules/                    # 設計ルール
│   ├── 01_GitHub/              # 会社情報（ナレッジ/知識）
│   ├── 02_Skills/              # GPTsのようなカスタムチャットBot
│   └── 03_MCP/                 # 外部技術接続
│
├── MainAgent/                   # 社長（メインエージェント）
│   ├── MainAgent.md             # メインエージェント定義
│   └── context_window.md        # コンテキストウィンドウ管理
│
├── SubAgents/                   # 幹部社員（サブエージェント）
│   ├── SubAgent_A/              # 子Agent_A（検索/リサーチ、Haiku）
│   │   ├── SubAgent_A.md
│   │   ├── search_research.md
│   │   └── haiku.md
│   │
│   ├── SubAgent_B/              # 子Agent_B（ライティング、Sonnet）
│   │   ├── SubAgent_B.md
│   │   ├── writing.md
│   │   └── sonnet.md
│   │
│   └── WritingAgent/            # ライティングAgent（実例）
│       └── WritingAgent.md
│
├── Skills/                      # 平社員が使うマニュアル
│   ├── Skills.md                # Skills定義
│   ├── execution_tasks/         # 実行タスク
│   └── context_guides/          # コンテキストガイド
│
├── Tasks/                       # 平社員（タスク定義）
│   └── Tasks.md
│
├── Tools/                       # 社内共通ツール
│   ├── Tools.md
│   ├── MCP/                     # MCPツール
│   ├── API/                     # APIツール
│   └── Scripts/                 # スクリプト
│
├── Memory/                      # メモリ管理
│   └── Memory.md
│
├── Tours/                       # ツアー/ガイド
│   └── Tours.md
│
└── Plugin_MarketPlace/          # プラグイン/マーケットプレイス
    └── Plugin_MarketPlace.md
```

## 詳細構成

### 00_rules/（設計ルール）

```
00_rules/
├── 01_GitHub/                   # 会社情報（ナレッジ/知識）
│   ├── GitHub.md
│   ├── knowledge_base/          # 知識ベース
│   └── vault_structure/         # Vault構造定義
│
├── 02_Skills/                   # カスタムチャットBot
│   ├── Skills.md
│   ├── execution_tasks/         # 実行タスク種別
│   │   ├── task_type_01.md
│   │   └── task_type_02.md
│   └── context_rules/           # コンテキストルール
│       └── context_guidelines.md
│
└── 03_MCP/                      # 外部技術接続
    ├── MCP.md
    └── external_connections/    # 外部接続設定
        └── connection_config.md
```

### MainAgent/（メインエージェント）

```
MainAgent/
├── MainAgent.md                 # メインエージェント定義
├── context_window.md             # コンテキストウィンドウ管理
├── hybrid_design.md             # ハイブリッド設計（200k制約対応）
└── context_transfer_rules.md    # コンテキスト受け渡し条件設定
```

### SubAgents/（サブエージェント）

```
SubAgents/
├── SubAgent_A/                  # 検索/リサーチ、Haiku
│   ├── SubAgent_A.md
│   ├── search_research.md
│   ├── haiku.md
│   └── context_requirements.md  # 必要なコンテキスト要件
│
├── SubAgent_B/                  # ライティング、Sonnet
│   ├── SubAgent_B.md
│   ├── writing.md
│   ├── sonnet.md
│   └── context_requirements.md
│
└── WritingAgent/                 # ライティングAgent（実例）
    ├── WritingAgent.md
    └── examples/                 # 実例集
        └── example_01.md
```

### Skills/（マニュアル）

```
Skills/
├── Skills.md                    # Skills定義
├── execution_tasks/             # 実行タスク
│   ├── task_manual_01.md
│   └── task_manual_02.md
└── context_guides/              # コンテキストガイド
    ├── context_guide_01.md
    └── context_guide_02.md
```

### Tools/（共通ツール）

```
Tools/
├── Tools.md
├── MCP/                         # MCPツール
│   └── mcp_tools.md
├── API/                         # APIツール
│   └── api_tools.md
└── Scripts/                     # スクリプト
    └── scripts.md
```

### メタ設計関連

```
MetaDesign/                      # メタ設計
├── MetaDesign.md
├── brainstorming/               # 壁打ち（ChatGPT-5.2 Thinking）
│   └── brainstorming.md
├── design_planning/              # 設計やプラン整形（Gemini-3.0 Pro）
│   └── design_planning.md
└── writing_coding/              # 執筆/コーディング（Claude Code-4.5 Opus）
    └── writing_coding.md
```

## 補足

- 各フォルダ内の`.md`ファイルは定義・説明用のプレースホルダー
- 実際のコンテンツは後で追加
- 階層構造は設計図の「会社組織」メタファーに沿って構成
- ハイブリッド設計（200k制約対応）はMainAgent配下で管理
- コンテキスト受け渡しの条件設定は各SubAgentに配置

