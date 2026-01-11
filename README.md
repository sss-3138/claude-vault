# Claude Vault – Knowledge OS for Writing & Publishing

**Welcome to the Claude Vault!** このリポジトリは、ObsidianライクなMarkdownベースのナレッジ管理環境をClaude AI上で再現し、文章制作と知識蓄積を効率化するためのVaultです。

## Vault概要

- **目的**: 短い指示でもユーザーの執筆スタイルや知見を反映した高品質な文章を生成すること。そのために、文章の書き方ガイド・テンプレート・過去記事・調査メモ・改善ログ等をすべてここで一元管理します。
- **運用**: Anthropic Claude Code WebとGitHubを連携し、AIがこのVault内のMarkdownファイルを参照・更新しながらアウトプットを作成します。人間はAIの提案をレビューして採択し、必要ならVaultにフィードバックを還元します。
- **想定アウトプット**: ブログ記事、Twitter(X)スレッド、LinkedIn投稿、各種レポート、調査メモ、ナレッジQ&A回答など。

## ディレクトリ構成

- **Root直下**: 
  - `CLAUDE.md` – AIエージェント向けの憲法ファイル。Vault運用ルールや参照順序を規定しています。
  - `00_router.md` – AI用ルーター。ユーザー依頼をカテゴリ分類し、読むべきファイルを指示します。
  - `README.md` – この説明書です（人間向け）。

- **MOC/** – Map of Content（索引）ノート集。テーマ別にVault内ノートへのリンク一覧を掲載。

- **Strategy/** – 文体戦略や想定読者など執筆の基本方針ノート。

- **Assets/** – 執筆補助の素材集。フック例文、比喩集、CTA例、用語集など。

- **Templates/** – 各種アウトプットのテンプレート。記事・SNS投稿・調査ノート・改善提案の雛形を収録。

- **Logs/** – ログ記録。LearningLog（学び）、DecisionLog（判断経緯）、ChangeLog（改善要求履歴）があります。

- **Articles/** – 生成された記事コンテンツ群（Markdown）。公開済みの記事を蓄積。

- **SNS/** – SNS投稿コンテンツ群。XスレッドやLinkedIn投稿など。

- **Research/** – 調査ノート群。情報収集の結果メモやソースまとめ。

> **Note:** `Archive/` フォルダはありませんが、今後情報過多になれば古いログや未使用ノートを移す予定です。現時点ではVault内に最新情報のみ保持します。

## 利用方法

1. **Vaultセットアップ**: Claude Code Webで本リポジトリを開きます（GitHub Appインストール済みであること）。Claudeが自動でVaultをクローンし、CLAUDE.mdを読み込むはずです。
2. **依頼する**: チャットで文章作成や質問を投げます。例えば「○○について1500字の記事を書いて」と依頼すると、ClaudeはまずRouterに従って関連ノート類を読み込み、ドラフトを提示します。
3. **レビュー**: AIの生成したドラフトを人間が確認・修正します。問題なければそのブランチのPRをマージし、記事を公開します。
4. **還元**: 公開後、AIに対し「Vaultを更新して」と指示すると、MOCへのリンク追加やログ追記などを行います（Pull Requestで提案されるので確認してマージ）。
5. **改善**: 定期的にLearningLogを見返して、Strategyやテンプレをより良くするPDCAを回します。AIからもChangeLog経由で改善提案が来るので、採否を判断してVaultに反映させます。

## 注意点

- **事実チェック**: AIはVault内の知識に基づきますが、外部新規情報には弱いです。必要に応じて調査依頼し、その結果をVaultに追加してください。出典付きの記述を心がけます。
- **スタイル統一**: Strategy.mdにスタイルガイドがまとまっています。新しい記事を書く前に目を通し、過去との一貫性を維持します。
- **Vault整頓**: ノートが増えすぎないよう、似た内容は統合し古いものはログ化するなど整理します（AIにも適宜提案させます）。リンク切れやタグ乱立に注意し、グロスアップを防ぎます。
- **セキュリティ**: 本Vaultは公開リポジトリです。個人情報や企業秘密は記載せず、引用も適切な範囲に留めます。Claude AIの利用規約も遵守します。

以上がClaude Vaultの全体概要と利用法です。Obsidianを使ったことがない方でも、上記フォルダとノートの役割に沿って操作すれば、AIと協調しながら効率よく文章作成・ナレッジ運用ができるよう設計されています。

> **参考**: Anthropic Claude Code公式Docsより – *"The single most important file in your codebase for using Claude Code effectively is the root `CLAUDE.md`. This file is the agent's "constitution," its primary source of truth for how your specific repository works."* 本VaultではCLAUDE.mdとRouterを要としてAIの挙動を制御しています。
