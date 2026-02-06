#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           江 戸 城  —  E D O   C A S T L E                  ║
║        完全自律型記事作成システム  軍議スクリプト              ║
║                  The Shogun Protocol                        ║
╚══════════════════════════════════════════════════════════════╝

14体のAI家臣団が、将軍（ユーザー）の「鶴の一声」だけで
高品質な記事を作成・納品する完全自律型オーケストレーター。

Usage:
    python war_council.py "テーマ"
    python war_council.py "テーマ" --model claude-sonnet-4-20250514
    python war_council.py "テーマ" --dry-run
"""

import os
import sys
import json
import time
import argparse
import datetime
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# ---------------------------------------------------------------------------
# 基本設定
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / "agents"
CASTLE_FLOORS = BASE_DIR / "castle_floors"
VAULT_ROOT = BASE_DIR.parent  # claude-vault のルート

# 作業ディレクトリ
FLOOR_STRATEGY = CASTLE_FLOORS / "01_strategy"
FLOOR_BLUEPRINT = CASTLE_FLOORS / "02_blueprint"
FLOOR_LIBRARY = CASTLE_FLOORS / "03_library"
FLOOR_WRITING = CASTLE_FLOORS / "04_writing_room"
FLOOR_TENSHUKAKU = CASTLE_FLOORS / "05_tenshukaku"
FLOOR_GALLERY = CASTLE_FLOORS / "06_gallery"

# デフォルトモデル
DEFAULT_MODEL = "claude-sonnet-4-20250514"

# ログ用の色（ANSI）
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    DIM = "\033[2m"


# ---------------------------------------------------------------------------
# フェーズ定義
# ---------------------------------------------------------------------------

class Phase(Enum):
    OPENING = "開城"
    STRATEGY = "軍議・策定"
    STRUCTURE = "縄張り・検分"
    DRAFTING = "執筆・批評・改稿"
    POLISHING = "仕上げ・装飾"
    GATEKEEPING = "城代検分"
    FINAL = "納品"


# ---------------------------------------------------------------------------
# エージェント定義
# ---------------------------------------------------------------------------

@dataclass
class Agent:
    """家臣団のメンバー定義"""
    number: int
    name_jp: str
    name_en: str
    role: str
    prompt_file: str
    input_files: list = field(default_factory=list)
    output_file: str = ""
    output_dir: Path = FLOOR_STRATEGY
    phase: Phase = Phase.STRATEGY

    @property
    def prompt_path(self) -> Path:
        return AGENTS_DIR / self.prompt_file

    @property
    def output_path(self) -> Path:
        return self.output_dir / self.output_file

    def load_system_prompt(self) -> str:
        """System Promptファイルを読み込む"""
        if self.prompt_path.exists():
            return self.prompt_path.read_text(encoding="utf-8")
        raise FileNotFoundError(f"無念！{self.name_jp}の指令書が見つかりませぬ: {self.prompt_path}")


# 家臣団の定義（実行順序通り）
RETAINERS = [
    Agent(
        number=1, name_jp="軍師", name_en="Gunshi",
        role="Strategist — ペルソナ設計",
        prompt_file="01_gunshi_persona.md",
        input_files=[],
        output_file="persona.md",
        output_dir=FLOOR_STRATEGY,
        phase=Phase.STRATEGY,
    ),
    Agent(
        number=2, name_jp="乱波・忍", name_en="Shinobi",
        role="Keyword Researcher — KW調査",
        prompt_file="02_shinobi_keywords.md",
        input_files=["01_strategy/persona.md"],
        output_file="keywords.md",
        output_dir=FLOOR_STRATEGY,
        phase=Phase.STRATEGY,
    ),
    Agent(
        number=3, name_jp="物見", name_en="Monomi",
        role="SERP Analyzer — 上位記事分析",
        prompt_file="03_monomi_serp.md",
        input_files=["01_strategy/keywords.md"],
        output_file="serp_analysis.md",
        output_dir=FLOOR_STRATEGY,
        phase=Phase.STRATEGY,
    ),
    Agent(
        number=4, name_jp="作事奉行", name_en="Sakuji",
        role="Architect — 構成作成",
        prompt_file="04_sakuji_structure.md",
        input_files=[
            "01_strategy/persona.md",
            "01_strategy/keywords.md",
            "01_strategy/serp_analysis.md",
        ],
        output_file="structure_draft.md",
        output_dir=FLOOR_BLUEPRINT,
        phase=Phase.STRUCTURE,
    ),
    Agent(
        number=5, name_jp="目付", name_en="Metsuke",
        role="Auditor — 構成チェック",
        prompt_file="05_metsuke_check.md",
        input_files=[
            "02_blueprint/structure_draft.md",
            "01_strategy/persona.md",
        ],
        output_file="structure_fixed.md",
        output_dir=FLOOR_BLUEPRINT,
        phase=Phase.STRUCTURE,
    ),
    Agent(
        number=6, name_jp="儒学者", name_en="Jugakusha",
        role="Researcher — 一次情報調査",
        prompt_file="06_jugakusha_fact.md",
        input_files=["02_blueprint/structure_fixed.md"],
        output_file="fact_sheet.md",
        output_dir=FLOOR_LIBRARY,
        phase=Phase.DRAFTING,
    ),
    Agent(
        number=7, name_jp="右筆", name_en="Yuhitsu",
        role="Writer — 初稿執筆",
        prompt_file="07_yuhitsu_draft.md",
        input_files=[
            "02_blueprint/structure_fixed.md",
            "03_library/fact_sheet.md",
        ],
        output_file="draft_v1.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.DRAFTING,
    ),
    Agent(
        number=8, name_jp="御意見番", name_en="Goikenban",
        role="Critic — 辛口レビュー",
        prompt_file="08_goikenban_critique.md",
        input_files=[
            "04_writing_room/draft_v1.md",
            "03_library/fact_sheet.md",
        ],
        output_file="critique_report.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.DRAFTING,
    ),
    Agent(
        number=9, name_jp="代筆", name_en="Daihitsu",
        role="Rewriter — リライト",
        prompt_file="09_daihitsu_rewrite.md",
        input_files=[
            "04_writing_room/draft_v1.md",
            "04_writing_room/critique_report.md",
        ],
        output_file="draft_v2.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.DRAFTING,
    ),
    Agent(
        number=10, name_jp="勘定方", name_en="Kanjyo",
        role="Counter — 文字数カウント",
        prompt_file="10_kanjyo_count.md",
        input_files=["04_writing_room/draft_v2.md"],
        output_file="count_report.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.POLISHING,
    ),
    Agent(
        number=11, name_jp="公文書係", name_en="Kobunsho",
        role="Linker — URL貼り付け",
        prompt_file="11_kobunsho_link.md",
        input_files=[
            "04_writing_room/draft_v2.md",
            "03_library/fact_sheet.md",
        ],
        output_file="draft_v3_linked.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.POLISHING,
    ),
    Agent(
        number=13, name_jp="絵師", name_en="Eshi",
        role="Visual Artist — 画像生成・配置",
        prompt_file="13_eshi_visual.md",
        input_files=["04_writing_room/draft_v3_linked.md"],
        output_file="draft_v4_visuals.md",
        output_dir=FLOOR_WRITING,
        phase=Phase.POLISHING,
    ),
    Agent(
        number=12, name_jp="城代", name_en="Joudai",
        role="Gatekeeper — 納品前検分",
        prompt_file="12_joudai_final.md",
        input_files=["04_writing_room/draft_v4_visuals.md"],
        output_file="final_draft.md",
        output_dir=FLOOR_TENSHUKAKU,
        phase=Phase.GATEKEEPING,
    ),
]


# ---------------------------------------------------------------------------
# ログ出力
# ---------------------------------------------------------------------------

class WarCouncilLogger:
    """軍議ログ — エンターテインメント性のあるログ出力"""

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or CASTLE_FLOORS
        self.log_lines: list[str] = []
        self.start_time = time.time()

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    def _log(self, msg: str, color: str = Color.WHITE, plain: str = ""):
        """ターミナル出力 + ログバッファ"""
        timestamp = self._timestamp()
        console_msg = f"{Color.DIM}[{timestamp}]{Color.RESET} {color}{msg}{Color.RESET}"
        print(console_msg)
        # ログファイル用（色なし）
        self.log_lines.append(f"[{timestamp}] {plain or msg}")

    def banner(self):
        """開城バナー"""
        banner_text = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ⛩️  江 戸 城  —  E D O   C A S T L E  ⛩️               ║
║                                                              ║
║          完全自律型記事作成システム  Ver.2                     ║
║          ~~ 軍議、これより開始 ~~                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(f"{Color.YELLOW}{banner_text}{Color.RESET}")

    def phase_start(self, phase: Phase):
        """フェーズ開始"""
        divider = "═" * 58
        self._log(f"\n╔{divider}╗", Color.CYAN)
        self._log(f"║  Phase: {phase.value:<50}║", Color.CYAN)
        self._log(f"╚{divider}╝", Color.CYAN)

    def agent_start(self, agent: Agent, message: str):
        """エージェント開始"""
        self._log(
            f"  🏯 [{agent.name_jp}（{agent.name_en}）] {message}",
            Color.GREEN,
            plain=f"  [{agent.name_jp}（{agent.name_en}）] {message}",
        )

    def agent_done(self, agent: Agent, message: str):
        """エージェント完了"""
        self._log(
            f"  ✅ [{agent.name_jp}] {message}",
            Color.GREEN,
            plain=f"  [完了: {agent.name_jp}] {message}",
        )

    def agent_error(self, agent: Agent, message: str):
        """エージェントエラー"""
        self._log(
            f"  ⚠️  [{agent.name_jp}] 無念！{message}",
            Color.RED,
            plain=f"  [失敗: {agent.name_jp}] {message}",
        )

    def karo_speaks(self, message: str):
        """家老の発言"""
        self._log(f"\n  👑 【筆頭家老】 {message}", Color.YELLOW, plain=f"  【筆頭家老】 {message}")

    def shogun_delivery(self, article_path: str):
        """将軍への納品"""
        divider = "═" * 58
        msg = f"""
╔{divider}╗
║                                                              ║
║   将軍様、大変お待たせいたしました。                          ║
║   これが我ら家臣団の総力、完成した記事でございます。          ║
║                                                              ║
║   納品先: {article_path:<47}║
║                                                              ║
╚{divider}╝
"""
        print(f"{Color.YELLOW}{Color.BOLD}{msg}{Color.RESET}")
        self.log_lines.append(msg)

    def summary(self, success: bool, agents_count: int):
        """実行サマリー"""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        status = "大勝利" if success else "撤退"
        self._log(
            f"\n  📊 軍議結果: {status} | 動員家臣: {agents_count}名 | 所要時間: {minutes}分{seconds}秒",
            Color.MAGENTA,
            plain=f"  軍議結果: {status} | 動員家臣: {agents_count}名 | 所要時間: {minutes}分{seconds}秒",
        )

    def save_log(self, theme: str):
        """ログファイルを保存"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = self.log_dir / f"war_council_log_{timestamp}.md"
        header = f"# 軍議記録 — 「{theme}」\n\n"
        header += f"日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        header += "---\n\n"
        content = header + "\n".join(self.log_lines)
        log_path.write_text(content, encoding="utf-8")
        return log_path


# ---------------------------------------------------------------------------
# API クライアント（Claude API呼び出し）
# ---------------------------------------------------------------------------

class CastleAPIClient:
    """
    Claude API を呼び出すクライアント。
    Anthropic SDK を使用。環境変数 ANTHROPIC_API_KEY が必要。
    """

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._client = None

    def _get_client(self):
        """遅延初期化でAnthropic clientを取得"""
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic()
            except ImportError:
                raise ImportError(
                    "無念！anthropic パッケージが見つかりませぬ。\n"
                    "  pip install anthropic\n"
                    "を実行してくだされ。"
                )
            except Exception as e:
                raise RuntimeError(
                    f"無念！API接続に失敗いたしました: {e}\n"
                    "ANTHROPIC_API_KEY が正しく設定されているかご確認くだされ。"
                )
        return self._client

    def call_agent(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 8192,
        temperature: float = 0.7,
    ) -> str:
        """
        エージェントを呼び出してテキストレスポンスを返す。

        Args:
            system_prompt: System Prompt（エージェントの人格・指示）
            user_message: ユーザーメッセージ（入力データ）
            max_tokens: 最大出力トークン数
            temperature: 温度パラメータ

        Returns:
            レスポンステキスト
        """
        client = self._get_client()

        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
        )

        # テキストブロックを結合して返す
        return "".join(
            block.text for block in response.content if block.type == "text"
        )


# ---------------------------------------------------------------------------
# メインオーケストレーター
# ---------------------------------------------------------------------------

class WarCouncil:
    """
    軍議（War Council）— メインオーケストレーター
    将軍のテーマを受け取り、全家臣を順に動員して記事を完成させる。
    """

    def __init__(
        self,
        theme: str,
        model: str = DEFAULT_MODEL,
        dry_run: bool = False,
        vault_root: Path = VAULT_ROOT,
    ):
        self.theme = theme
        self.model = model
        self.dry_run = dry_run
        self.vault_root = vault_root
        self.logger = WarCouncilLogger()
        self.api = CastleAPIClient(model=model)
        self.results: dict[str, str] = {}  # agent_name -> output content
        self.current_phase: Optional[Phase] = None

    def _ensure_dirs(self):
        """作業ディレクトリを確保"""
        for floor in [
            FLOOR_STRATEGY, FLOOR_BLUEPRINT, FLOOR_LIBRARY,
            FLOOR_WRITING, FLOOR_TENSHUKAKU, FLOOR_GALLERY,
        ]:
            floor.mkdir(parents=True, exist_ok=True)

    def _load_vault_context(self) -> str:
        """Vault内の戦略・テンプレート情報を読み込む"""
        context_parts = []

        # Strategy.md
        strategy_path = self.vault_root / "Strategy" / "Strategy.md"
        if strategy_path.exists():
            context_parts.append(
                f"## Strategy.md（執筆戦略ガイド）\n\n{strategy_path.read_text(encoding='utf-8')}"
            )

        # Article Template
        article_path = self.vault_root / "Templates" / "Article.md"
        if article_path.exists():
            context_parts.append(
                f"## Article Template\n\n{article_path.read_text(encoding='utf-8')}"
            )

        # Assets
        assets_path = self.vault_root / "Assets" / "Assets.md"
        if assets_path.exists():
            context_parts.append(
                f"## Assets（表現集）\n\n{assets_path.read_text(encoding='utf-8')}"
            )

        return "\n\n---\n\n".join(context_parts)

    def _build_user_message(self, agent: Agent) -> str:
        """エージェント用のユーザーメッセージを構築"""
        parts = [f"# 将軍の勅命（テーマ）\n\n「{self.theme}」\n"]

        # 入力ファイルの内容を添付
        for input_rel in agent.input_files:
            input_path = CASTLE_FLOORS / input_rel
            if input_path.exists():
                content = input_path.read_text(encoding="utf-8")
                parts.append(f"## 参照資料: {input_rel}\n\n{content}")
            else:
                parts.append(f"## 参照資料: {input_rel}\n\n（※ファイル未作成）")

        # Vault戦略コンテキスト（最初のエージェントには必ず付与）
        if agent.number <= 4:
            vault_ctx = self._load_vault_context()
            if vault_ctx:
                parts.append(f"## Vault 戦略コンテキスト\n\n{vault_ctx}")

        return "\n\n---\n\n".join(parts)

    def _run_agent(self, agent: Agent) -> bool:
        """単一エージェントを実行"""
        # フェーズ変更時にヘッダー出力
        if agent.phase != self.current_phase:
            self.current_phase = agent.phase
            self.logger.phase_start(agent.phase)

        # 開始ログ
        opening_lines = {
            1: "ふむ…将軍様の仰せ、承りました。戦略を練りましょう。",
            2: "御意。闇に紛れ、情報を掴んで参ります。",
            3: "注進！注進！偵察に出ます！",
            4: "てやんでぃ！設計図を引くぜ！",
            5: "クックック…お手並み拝見といきましょう。",
            6: "然り。出典なき情報は戯言である。調査を開始する。",
            7: "筆が乗ってまいりました！初稿を書き上げます！",
            8: "喝！どれ、読ませてもらおうか。",
            9: "へへぇ…書き直しますです…（泣）",
            10: "やれやれ…一字一字、数えさせていただきますぞ。",
            11: "…処理を開始します。紐付け作業に入ります。",
            13: "閃いた！色が…色が呼んでいる！",
            12: "検分、開始する。家老様のお手を煩わせるな。",
        }
        self.logger.agent_start(agent, opening_lines.get(agent.number, "参上！"))

        if self.dry_run:
            # ドライラン: ダミー出力
            dummy_content = (
                f"# {agent.name_jp}（{agent.name_en}）の出力\n\n"
                f"テーマ: {self.theme}\n\n"
                f"※ドライランのためダミー出力です。\n"
            )
            agent.output_path.write_text(dummy_content, encoding="utf-8")
            self.results[agent.name_en] = dummy_content
            self.logger.agent_done(agent, f"→ {agent.output_file}（ドライラン）")
            return True

        try:
            # System Prompt読み込み
            system_prompt = agent.load_system_prompt()

            # ユーザーメッセージ構築
            user_message = self._build_user_message(agent)

            # API呼び出し
            response = self.api.call_agent(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=8192,
                temperature=0.7,
            )

            # 出力を保存
            agent.output_path.write_text(response, encoding="utf-8")
            self.results[agent.name_en] = response

            # 完了ログ
            closing_lines = {
                1: f"勝機が見えました。→ {agent.output_file}",
                2: f"…見つけました。→ {agent.output_file}",
                3: f"敵影確認！報告完了！→ {agent.output_file}",
                4: f"こいつはいい仕事になるぜ。→ {agent.output_file}",
                5: f"まあ…及第点としましょう。→ {agent.output_file}",
                6: f"調査完了。論拠は万全です。→ {agent.output_file}",
                7: f"初稿、書き上げました！→ {agent.output_file}",
                8: f"ふん、言いたいことは言った。→ {agent.output_file}",
                9: f"書き直し完了です…お許しを…→ {agent.output_file}",
                10: f"計算完了。帳簿は正確です。→ {agent.output_file}",
                11: f"紐付け完了。承認印を押します。→ {agent.output_file}",
                13: f"これが私の魂（ソウル）だ！→ {agent.output_file}",
                12: f"検分完了。家老様へお回しせよ。→ {agent.output_file}",
            }
            self.logger.agent_done(agent, closing_lines.get(agent.number, f"完了 → {agent.output_file}"))
            return True

        except Exception as e:
            error_lines = {
                1: f"情報不足です: {e}",
                2: f"霧が深く情報を掴めませんでした: {e}",
                3: f"偵察続行困難！: {e}",
                4: f"材料が足りねえ！: {e}",
                5: f"構成案が届きませんな: {e}",
                6: f"書庫に火が入りました: {e}",
                7: f"筆が折れました…: {e}",
                8: f"初稿が届いておらん！: {e}",
                9: f"批評レポートが見つかりません…: {e}",
                10: f"帳簿が読めません: {e}",
                11: f"ファイル読み込み失敗: {e}",
                13: f"筆（API）が折れた…: {e}",
                12: f"検分対象が届いておらぬ！: {e}",
            }
            self.logger.agent_error(agent, error_lines.get(agent.number, str(e)))

            # 画像生成エラーの場合は続行（プレースホルダー配置）
            if agent.number == 13:
                # 前工程の出力をそのまま引き継ぐ
                prev_path = CASTLE_FLOORS / "04_writing_room" / "draft_v3_linked.md"
                if prev_path.exists():
                    fallback = prev_path.read_text(encoding="utf-8")
                    fallback += "\n\n<!-- 画像生成に失敗しました。プレースホルダーを配置しています。 -->\n"
                    agent.output_path.write_text(fallback, encoding="utf-8")
                    self.results[agent.name_en] = fallback
                    self.logger.agent_done(agent, "プレースホルダーで続行します。")
                    return True
            return False

    def _run_karo_final(self) -> bool:
        """家老（Agent 00）の最終確認"""
        self.logger.phase_start(Phase.FINAL)
        self.logger.karo_speaks("うむ、城代から上がった記事を検分いたそう。")

        final_draft_path = FLOOR_TENSHUKAKU / "final_draft.md"
        if not final_draft_path.exists():
            self.logger.karo_speaks("なんと…城代からの報告がまだ届いておりませぬ！")
            return False

        if self.dry_run:
            # ドライラン
            content = final_draft_path.read_text(encoding="utf-8")
            final_path = FLOOR_TENSHUKAKU / "FINAL_ARTICLE.md"
            final_path.write_text(content, encoding="utf-8")
            self.logger.shogun_delivery(str(final_path.relative_to(BASE_DIR)))
            return True

        try:
            # 家老のSystem Prompt読み込み
            karo_prompt_path = AGENTS_DIR / "00_karo_orchestrator.md"
            system_prompt = karo_prompt_path.read_text(encoding="utf-8")

            final_draft = final_draft_path.read_text(encoding="utf-8")
            strategy = ""
            strategy_path = self.vault_root / "Strategy" / "Strategy.md"
            if strategy_path.exists():
                strategy = strategy_path.read_text(encoding="utf-8")

            user_message = (
                f"# 城代検分済み記事\n\n{final_draft}\n\n---\n\n"
                f"# Strategy.md（照合用）\n\n{strategy}\n\n---\n\n"
                f"将軍の勅命テーマ: 「{self.theme}」\n\n"
                f"城代の検分を通過した記事です。最終確認を行い、問題がなければ "
                f"FINAL_ARTICLE として出力してください。修正が必要な場合は修正した上で出力してください。"
            )

            response = self.api.call_agent(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=8192,
                temperature=0.3,  # 最終確認は低温度で
            )

            # FINAL_ARTICLE として保存
            final_path = FLOOR_TENSHUKAKU / "FINAL_ARTICLE.md"
            final_path.write_text(response, encoding="utf-8")

            self.logger.karo_speaks("大義である。将軍様への納品の支度が整いました。")
            self.logger.shogun_delivery(str(final_path.relative_to(BASE_DIR)))
            return True

        except Exception as e:
            self.logger.karo_speaks(f"無念…不測の事態です: {e}")
            return False

    def execute(self) -> bool:
        """
        軍議を開始し、全工程を実行する。
        Returns: 成功したかどうか
        """
        self._ensure_dirs()

        # 開城
        self.logger.banner()
        self.logger.karo_speaks(
            f"将軍様より『{self.theme}』との勅命が下った！者ども、支度はよいか！"
        )

        # 家臣団を順に動員
        success_count = 0
        for agent in RETAINERS:
            success = self._run_agent(agent)
            if success:
                success_count += 1
            else:
                # 致命的エラーの場合は中断（画像生成以外）
                if agent.number != 13:
                    self.logger.karo_speaks(
                        f"無念…{agent.name_jp}が倒れました。軍議を一時中断いたします。"
                    )
                    self.logger.summary(False, success_count)
                    log_path = self.logger.save_log(self.theme)
                    print(f"\n  📜 軍議記録: {log_path}")
                    return False

        # 家老の最終確認
        final_success = self._run_karo_final()

        # サマリー
        self.logger.summary(final_success, success_count + (1 if final_success else 0))

        # ログ保存
        log_path = self.logger.save_log(self.theme)
        print(f"\n  📜 軍議記録: {log_path}")

        return final_success


# ---------------------------------------------------------------------------
# CLI エントリポイント
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="江戸城 — 完全自律型記事作成システム (The Shogun Protocol)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python war_council.py "AIエージェントの最新動向"
  python war_council.py "リモートワークの生産性向上" --model claude-sonnet-4-20250514
  python war_council.py "テスト実行" --dry-run
        """,
    )
    parser.add_argument(
        "theme",
        type=str,
        help="将軍の勅命（記事テーマ）",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"使用するClaude モデル（デフォルト: {DEFAULT_MODEL}）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライラン（API呼び出しなし、ダミー出力で流れを確認）",
    )

    args = parser.parse_args()

    council = WarCouncil(
        theme=args.theme,
        model=args.model,
        dry_run=args.dry_run,
    )

    success = council.execute()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
