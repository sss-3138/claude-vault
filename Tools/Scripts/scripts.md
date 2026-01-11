# Scripts - スクリプト

このフォルダには、Vault運用に役立つ各種スクリプトを配置します。

## word_count.py - 文字数計算スクリプト

Markdownファイルやテキストファイルの文字数を計算するPythonスクリプトです。

### 使用方法

```bash
# 基本的な使用方法（すべての文字をカウント）
python Tools/Scripts/word_count.py <ファイルパス>

# カウントタイプを指定
python Tools/Scripts/word_count.py <ファイルパス> <count_type>
```

### カウントタイプ

- `all` - すべての文字（スペース・改行含む、デフォルト）
- `no_space` - スペースを除く
- `no_whitespace` - 空白文字（スペース・改行・タブ）を除く
- `japanese` - 日本語文字のみ（ひらがな・カタカナ・漢字）
- `alphanumeric` - 英数字のみ

### 出力内容

- **文字数**: 各種タイプでの文字数
- **単語数**: 日本語単語数、英語単語数、合計
- **行数**: 総行数、空行を除く行数

### 使用例

```bash
# 記事の文字数を確認
python Tools/Scripts/word_count.py Articles/2026-01-10-記事タイトル.md

# 空白文字を除いた文字数を確認
python Tools/Scripts/word_count.py Templates/Article.md no_whitespace

# 日本語文字のみをカウント
python Tools/Scripts/word_count.py Strategy/Strategy.md japanese
```

### Claude Code Webでの参照方法

Claude Code Webで文字数を計算する際は、以下のように参照してください：

```
文字数を計算する際は、Tools/Scripts/word_count.py を実行してください。
例: python Tools/Scripts/word_count.py <対象ファイル>
```
