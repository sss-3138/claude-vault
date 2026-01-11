# Router (Task Category Routing)

**このノートはVault Routerです。ユーザーからの依頼内容を解析し、適切なカテゴリと参照ノートを決定してください。**

まずユーザーのプロンプトを以下のカテゴリ一覧と照合し、該当するものがあれば指示に従ってください。どれにも当てはまらない場合は「General」を参照します。

## Categories:

### 1. **Article_Draft_Request** 
依頼: 「記事を書いて」「ブログを書いて」「～についてのコラムを作成」等、**新規の記事執筆**を要請するもの。

- **Action**: 
  1. `Templates/Article.md` を開き、記事テンプレートの構成を確認する。
  2. `MOC/Writing_MOC.md` を開き、関連する既存記事やノートをチェックする（同じテーマの記事が過去にないか、参考になるアウトラインはないか）。
  3. 必要に応じて `Strategy/Strategy.md`（全体方針）、`Assets/Assets.md`（表現集）も参照する。
  4. 上記を踏まえアウトライン作成→本文執筆。

- **Output**: Draft記事Markdown（Frontmatter付き）。執筆後、記事タイトルとリンクをWriting_MOCに追記し、ChangeLogに「記事公開済・LearningLog記入予定」等記録。

### 2. **SNS_Post_Request**
依頼: 「Twitter(X)で○○について投稿」「LinkedInに～の内容を書いて」等、**SNS投稿（X/Twitterスレ、LinkedIn投稿）**の作成依頼。

- **Action**:
  1. `MOC/SNS_MOC.md` を開き、過去の類似投稿がないか確認する（重複防止、参考）。
  2. SNS種別を判別。Twitter系なら `Templates/XThread.md`、LinkedInなら `Templates/LinkedIn.md` を開く。
  3. `Strategy/Strategy.md` のトーン＆マナー節でSNS向け注意事項があれば再確認する（例えばTwitterは砕けた口調OK等）。
  4. テンプレートに沿って投稿文案を作成。Xの場合はツイートごとに箇条書きで、LinkedInの場合は段落構成。

- **Output**: SNS投稿Markdown。Xなら各行140文字程度に収める。投稿後、SNS_MOCにエントリ追加。バズ狙い要素など学びがあればLearningLogに後日追記。

### 3. **Research_Info_Request**
依頼: 「～を調査して」「～の統計データを集めて」等、**情報収集・調査ノート**の作成依頼。

- **Action**:
  1. `Templates/ResearchNote.md` を開いて調査ノート構成を把握（調査目的・発見・出典 等）。
  2. 可能ならClaude Codeのネット接続をONにして必要情報を検索（※デフォルトOFF：ユーザー許可がある場合のみ）。見つけた情報源URLや要点を適宜記録。
  3. Vault内に関連メモがないか `MOC/Research_MOC.md` や `Assets/Glossary.md` を検索。
  4. 調査結果をResearchNoteフォーマットに整理して記述。

- **Output**: Research/以下に新規調査ノートMDを保存（ファイル名は調査テーマか日付）。Research_MOCにリンク追加。出典は必ず`Assets/Glossary.md`かノート末尾に**【出典】**節を作りURLと日付を明記する。重要データはStrategyやAssetsにも反映検討。

### 4. **Idea_Brainstorm_Request**
依頼: 「ネタ出しして」「○○のアイデアをブレストして」等、**アイデア出し・プロット構想**の依頼。

- **Action**:
  1. `Assets/Assets.md` の「Hook集」「フレームワーク集」を参照。発想の切り口を探す。
  2. `MOC/Writing_MOC.md` や `MOC/SNS_MOC.md` で過去扱った関連トピックがないか見て重複を避ける。
  3. Claude自身の知識も活用しつつ、ユーザー文脈に合うアイデアリストを作成。
  4. 可能ならアイデアごとに一行程度で展開例も補足。

- **Output**: アイデア箇条書きリスト。ユニークでユーザー興味に合致するものを提案。決定したアイデアは次フェーズ（記事化等）に進むので、この段階ではVault更新は不要だが、重要なアイデアは後でStrategyやテーマリストに追加検討。

### 5. **Vault_Improvement_Request**
依頼: 「Vaultを改善して」「文章スタイルを見直して」等、**Vault自体の改善提案**を求めるもの（ユーザーから明示にVault構成や方針の改善指示）。

- **Action**:
  1. `Logs/ChangeLog.md` を開き、過去に似た提案がなかったか確認。
  2. 該当分野のガイドラインファイル（Strategy, Template, Assets等）を開いて現行内容を把握。
  3. 改善点を考察し、`Templates/ImprovementProposal.md` に従って提案文書（背景・提案内容・メリットデメリット）を作成。
  4. ChangeLogに提案要旨を追記し、詳細はImprovementProposalノートとして保存。

- **Output**: 改善提案ノートMD（ImprovementProposal_YYYYMMDD.md等）。Improvement_MOCにリンク追加。ユーザー承認後に実行するため、この時点では他ファイルへは変更加えない。

### 6. **Q&A_Knowledge_Request**
依頼: 「～とは何？」「過去に書いた△△に関連すること教えて」等、Vault内知識を使った**質問への回答**。

- **Action**:
  1. `Assets/Glossary.md` または関連MOCを検索し、質問のキーワード該当箇所を探す。
  2. 該当ノート（記事や調査メモ）があれば開いて内容を確認。
  3. Strategy.mdに沿った口調で、正確かつ簡潔な回答を作成。必要なら引用も用いる（引用元がVault内なら明示の必要なし。外部なら出典を示す）。

- **Output**: 質問への回答文（1～3段落程度）。必要に応じて「詳しくは〇〇参照」とVault内ノートへの参照を促す。回答後、GlossaryやAssetsに該当項目が無ければ追加検討（ChangeLogへ）。

### 7. **General_Request**
上記に当てはまらない、もしくはカテゴリ判断が難しい依頼。

- **Action**:
  1. 汎用方針として `Strategy/Strategy.md` を開き、基本ルールを押さえる。
  2. ユーザーの質問・依頼内容から連想されるVault内ノートをキーワード検索し、関連が高そうなものを読む。
  3. 最適と思われる形で回答または対応策を作成。必要なら上記カテゴリーの手順を組み合わせる。

- **Output**: ユーザーの要望に沿った適切なアウトプット。Vault更新は状況次第。

---

*（Router最終更新: 2026-01-09）*
