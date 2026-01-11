#!/usr/bin/env python3
"""
文字数計算スクリプト
Markdownファイルやテキストファイルの文字数を計算します。
"""

import sys
import os
from pathlib import Path


def count_characters(text, count_type='all'):
    """
    文字数を計算する
    
    Args:
        text: 計算対象のテキスト
        count_type: 計算タイプ
            - 'all': すべての文字（スペース・改行含む）
            - 'no_space': スペースを除く
            - 'no_whitespace': 空白文字（スペース・改行・タブ）を除く
            - 'japanese': 日本語文字のみ（ひらがな・カタカナ・漢字）
            - 'alphanumeric': 英数字のみ
    
    Returns:
        int: 文字数
    """
    if count_type == 'all':
        return len(text)
    elif count_type == 'no_space':
        return len(text.replace(' ', ''))
    elif count_type == 'no_whitespace':
        return len(''.join(text.split()))
    elif count_type == 'japanese':
        # ひらがな、カタカナ、漢字、全角記号をカウント
        import re
        japanese_pattern = re.compile(r'[ひらがな-ゖカタカナ-ヺ一-龯々〆〤]', re.UNICODE)
        return len(japanese_pattern.findall(text))
    elif count_type == 'alphanumeric':
        import re
        alphanumeric_pattern = re.compile(r'[a-zA-Z0-9]')
        return len(alphanumeric_pattern.findall(text))
    else:
        return len(text)


def count_words(text):
    """
    単語数を計算する（日本語と英語に対応）
    
    Args:
        text: 計算対象のテキスト
    
    Returns:
        dict: 日本語単語数と英語単語数
    """
    import re
    
    # 日本語の単語（ひらがな・カタカナ・漢字の連続）
    japanese_words = re.findall(r'[ひらがな-ゖカタカナ-ヺ一-龯々〆〤]+', text)
    
    # 英語の単語（アルファベットの連続）
    english_words = re.findall(r'[a-zA-Z]+', text)
    
    return {
        'japanese': len(japanese_words),
        'english': len(english_words),
        'total': len(japanese_words) + len(english_words)
    }


def analyze_file(file_path, count_type='all'):
    """
    ファイルを分析して文字数情報を返す
    
    Args:
        file_path: ファイルパス
        count_type: 文字数計算タイプ
    
    Returns:
        dict: 分析結果
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 各種文字数を計算
        all_chars = count_characters(content, 'all')
        no_space_chars = count_characters(content, 'no_space')
        no_whitespace_chars = count_characters(content, 'no_whitespace')
        japanese_chars = count_characters(content, 'japanese')
        alphanumeric_chars = count_characters(content, 'alphanumeric')
        
        # 単語数
        word_counts = count_words(content)
        
        # 行数
        lines = content.split('\n')
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        return {
            'file': str(file_path),
            'characters': {
                'all': all_chars,
                'no_space': no_space_chars,
                'no_whitespace': no_whitespace_chars,
                'japanese': japanese_chars,
                'alphanumeric': alphanumeric_chars
            },
            'words': word_counts,
            'lines': {
                'total': total_lines,
                'non_empty': non_empty_lines
            },
            'requested_count': count_characters(content, count_type)
        }
    except Exception as e:
        return {'error': str(e)}


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python word_count.py <ファイルパス> [count_type]")
        print("\ncount_type オプション:")
        print("  all            - すべての文字（デフォルト）")
        print("  no_space       - スペースを除く")
        print("  no_whitespace  - 空白文字を除く")
        print("  japanese       - 日本語文字のみ")
        print("  alphanumeric   - 英数字のみ")
        print("\n例:")
        print("  python word_count.py article.md")
        print("  python word_count.py article.md no_whitespace")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    count_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
    
    if not file_path.exists():
        print(f"エラー: ファイルが見つかりません: {file_path}")
        sys.exit(1)
    
    result = analyze_file(file_path, count_type)
    
    if 'error' in result:
        print(f"エラー: {result['error']}")
        sys.exit(1)
    
    # 結果を表示
    print(f"\nファイル: {result['file']}")
    print("\n【文字数】")
    print(f"  すべて: {result['characters']['all']:,} 文字")
    print(f"  スペース除く: {result['characters']['no_space']:,} 文字")
    print(f"  空白文字除く: {result['characters']['no_whitespace']:,} 文字")
    print(f"  日本語のみ: {result['characters']['japanese']:,} 文字")
    print(f"  英数字のみ: {result['characters']['alphanumeric']:,} 文字")
    print(f"\n  指定タイプ ({count_type}): {result['requested_count']:,} 文字")
    
    print("\n【単語数】")
    print(f"  日本語: {result['words']['japanese']:,} 語")
    print(f"  英語: {result['words']['english']:,} 語")
    print(f"  合計: {result['words']['total']:,} 語")
    
    print("\n【行数】")
    print(f"  総行数: {result['lines']['total']:,} 行")
    print(f"  空行除く: {result['lines']['non_empty']:,} 行")


if __name__ == '__main__':
    main()

