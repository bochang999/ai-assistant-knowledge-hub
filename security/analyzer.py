#!/usr/bin/env python3
"""
Python Security Analyzer
メインのセキュリティ解析エンジン
"""

import ast
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import time

from .models import (
    SecurityIssue,
    SecurityReport,
    FixSuggestion,
    SeverityLevel,
    SecurityCategory,
    DANGEROUS_PATTERNS,
)


class PythonSecurityAnalyzer:
    """Pythonコードのセキュリティ解析メインクラス"""

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.rules_enabled = self.config.get(
            "rules_enabled", list(DANGEROUS_PATTERNS.keys())
        )

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        default_config = {
            "rules_enabled": list(DANGEROUS_PATTERNS.keys()),
            "severity_threshold": SeverityLevel.MEDIUM,
            "exclude_patterns": ["test_*.py", "*_test.py"],
            "max_line_length": 88,
        }

        if config_path and Path(config_path).exists():
            import yaml

            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
            except Exception:
                pass  # デフォルト設定を使用

        return default_config

    def analyze_file(self, file_path: str) -> SecurityReport:
        """ファイル単位でのセキュリティ解析"""
        start_time = time.time()
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            return self._empty_report(
                file_path, f"ファイルが見つかりません: {file_path}"
            )

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
        except Exception as e:
            return self._empty_report(file_path, f"ファイル読み込みエラー: {e}")

        return self.analyze_code(code_content, file_path, time.time() - start_time)

    def analyze_code(
        self, code_content: str, file_path: str = "<string>", scan_duration: float = 0
    ) -> SecurityReport:
        """コード文字列のセキュリティ解析"""
        start_time = time.time()
        issues: List[SecurityIssue] = []
        fix_suggestions: List[FixSuggestion] = []

        try:
            # Python ASTでコード解析
            tree = ast.parse(code_content)
            issues.extend(self._analyze_ast(tree, code_content, file_path))

            # 正規表現ベースの解析
            issues.extend(self._analyze_patterns(code_content, file_path))

            # 修正提案生成
            fix_suggestions = self._generate_fix_suggestions(issues, code_content)

        except SyntaxError as e:
            issues.append(
                SecurityIssue(
                    category=SecurityCategory.DANGEROUS_API,
                    severity=SeverityLevel.HIGH,
                    title="構文エラー",
                    description=f"Pythonコードに構文エラーがあります: {e}",
                    file_path=file_path,
                    line_number=getattr(e, "lineno", 1),
                    code_snippet=getattr(e, "text", "").strip(),
                    fix_suggestion="構文エラーを修正してください",
                )
            )

        # 統計計算
        issues_by_severity = {}
        for severity in SeverityLevel:
            issues_by_severity[severity] = len(
                [i for i in issues if i.severity == severity]
            )

        total_duration = scan_duration or (time.time() - start_time) * 1000

        return SecurityReport(
            scan_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            file_path=file_path,
            total_issues=len(issues),
            issues_by_severity=issues_by_severity,
            issues=issues,
            fix_suggestions=fix_suggestions,
            scan_duration_ms=total_duration,
        )

    def _analyze_ast(
        self, tree: ast.AST, code_content: str, file_path: str
    ) -> List[SecurityIssue]:
        """AST解析ベースのセキュリティチェック"""
        issues = []
        code_lines = code_content.split("\n")

        class SecurityVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                # 危険なAPI呼び出し検出
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    line_no = getattr(node, "lineno", 1)
                    line_content = (
                        code_lines[line_no - 1] if line_no <= len(code_lines) else ""
                    )

                    # eval/exec検出
                    if (
                        func_name in ["eval", "exec"]
                        and "eval_usage" in self.analyzer.rules_enabled
                    ):
                        issues.append(
                            SecurityIssue(
                                category=SecurityCategory.DANGEROUS_API,
                                severity=SeverityLevel.CRITICAL,
                                title=f"危険な{func_name}()使用",
                                description=f"{func_name}()は任意コード実行のリスクがあります",
                                file_path=file_path,
                                line_number=line_no,
                                code_snippet=line_content.strip(),
                                fix_suggestion=f"ast.literal_eval()やjson.loads()を検討してください",
                                cwe_id="CWE-94",
                            )
                        )

                # subprocess.run()のshell=True検出
                elif isinstance(node.func, ast.Attribute):
                    if (
                        getattr(node.func.value, "id", None) == "subprocess"
                        and node.func.attr == "run"
                        and "shell_injection" in self.analyzer.rules_enabled
                    ):

                        for keyword in node.keywords:
                            if (
                                keyword.arg == "shell"
                                and isinstance(keyword.value, ast.Constant)
                                and keyword.value.value is True
                            ):

                                line_no = getattr(node, "lineno", 1)
                                line_content = (
                                    code_lines[line_no - 1]
                                    if line_no <= len(code_lines)
                                    else ""
                                )

                                issues.append(
                                    SecurityIssue(
                                        category=SecurityCategory.INJECTION,
                                        severity=SeverityLevel.HIGH,
                                        title="shell=True使用によるコマンドインジェクションリスク",
                                        description="shell=Trueは危険です。コマンドインジェクションの可能性があります",
                                        file_path=file_path,
                                        line_number=line_no,
                                        code_snippet=line_content.strip(),
                                        fix_suggestion="shell=Falseを使用し、コマンドをリスト形式で渡してください",
                                        cwe_id="CWE-78",
                                    )
                                )

                self.generic_visit(node)

            def visit_ExceptHandler(self, node):
                # 雑なexcept検出
                if node.type is None and "bare_except" in self.analyzer.rules_enabled:
                    line_no = getattr(node, "lineno", 1)
                    line_content = (
                        code_lines[line_no - 1] if line_no <= len(code_lines) else ""
                    )

                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.EXCEPTION_HANDLING,
                            severity=SeverityLevel.MEDIUM,
                            title="bare except使用",
                            description="except:は全ての例外を握りつぶすため危険です",
                            file_path=file_path,
                            line_number=line_no,
                            code_snippet=line_content.strip(),
                            fix_suggestion="具体的な例外クラスを指定してください (except ValueError:など)",
                        )
                    )

                elif (
                    isinstance(node.type, ast.Name)
                    and node.type.id == "Exception"
                    and "broad_except" in self.analyzer.rules_enabled
                ):
                    line_no = getattr(node, "lineno", 1)
                    line_content = (
                        code_lines[line_no - 1] if line_no <= len(code_lines) else ""
                    )

                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.EXCEPTION_HANDLING,
                            severity=SeverityLevel.MEDIUM,
                            title="広範囲except Exception使用",
                            description="except Exceptionは問題を隠す可能性があります",
                            file_path=file_path,
                            line_number=line_no,
                            code_snippet=line_content.strip(),
                            fix_suggestion="より具体的な例外クラスを使用してください",
                        )
                    )

                self.generic_visit(node)

            def visit_FunctionDef(self, node):
                # 可変デフォルト引数検出
                if "mutable_default" in self.analyzer.rules_enabled:
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            line_no = getattr(node, "lineno", 1)
                            line_content = (
                                code_lines[line_no - 1]
                                if line_no <= len(code_lines)
                                else ""
                            )

                            issues.append(
                                SecurityIssue(
                                    category=SecurityCategory.DANGEROUS_API,
                                    severity=SeverityLevel.MEDIUM,
                                    title="可変デフォルト引数使用",
                                    description="可変オブジェクトをデフォルト引数にすると関数呼び出し間で状態が共有されます",
                                    file_path=file_path,
                                    line_number=line_no,
                                    code_snippet=line_content.strip(),
                                    fix_suggestion="デフォルト値にNoneを使用し、関数内で空のオブジェクトを作成してください",
                                )
                            )

                self.generic_visit(node)

        visitor = SecurityVisitor()
        visitor.analyzer = self
        visitor.visit(tree)
        return issues

    def _analyze_patterns(
        self, code_content: str, file_path: str
    ) -> List[SecurityIssue]:
        """正規表現ベースのパターン解析"""
        issues = []
        lines = code_content.split("\n")

        for line_no, line in enumerate(lines, 1):
            line_stripped = line.strip()

            # ハードコードされた秘密情報検出
            if "hardcoded_secrets" in self.rules_enabled:
                secret_patterns = [
                    (
                        r'(?i)(password|secret|key|token)\s*=\s*["\'][^"\']{8,}["\']',
                        "認証情報のハードコード",
                    ),
                    (
                        r'(?i)(api[_-]?key)\s*=\s*["\'][^"\']{16,}["\']',
                        "APIキーのハードコード",
                    ),
                    (
                        r'["\'][A-Za-z0-9+/]{40,}[=]{0,2}["\']',
                        "Base64エンコードされた可能性のある秘密情報",
                    ),
                ]

                for pattern, description in secret_patterns:
                    if re.search(pattern, line):
                        issues.append(
                            SecurityIssue(
                                category=SecurityCategory.SECRETS_EXPOSURE,
                                severity=SeverityLevel.HIGH,
                                title="ハードコードされた秘密情報",
                                description=description,
                                file_path=file_path,
                                line_number=line_no,
                                code_snippet=line_stripped,
                                fix_suggestion="環境変数やシークレット管理システムを使用してください",
                                cwe_id="CWE-798",
                            )
                        )

            # 危険なタイムゾーン未指定datetime
            if "naive_datetime" in self.rules_enabled:
                if re.search(r"datetime\.now\(\)(?!\s*\()", line):
                    issues.append(
                        SecurityIssue(
                            category=SecurityCategory.DATETIME,
                            severity=SeverityLevel.MEDIUM,
                            title="タイムゾーン未指定のdatetime",
                            description="datetime.now()はタイムゾーン情報がないため、国際化で問題になります",
                            file_path=file_path,
                            line_number=line_no,
                            code_snippet=line_stripped,
                            fix_suggestion="datetime.now(timezone.utc)を使用してください",
                        )
                    )

            # ログでの機密情報出力
            if "secrets_in_logs" in self.rules_enabled:
                log_patterns = [
                    r'(?i)log.*["\'].*(?:password|secret|key|token)["\']',
                    r'(?i)print.*["\'].*(?:password|secret|key|token)["\']',
                ]

                for pattern in log_patterns:
                    if re.search(pattern, line):
                        issues.append(
                            SecurityIssue(
                                category=SecurityCategory.SECRETS_EXPOSURE,
                                severity=SeverityLevel.MEDIUM,
                                title="ログでの機密情報出力",
                                description="ログに機密情報が出力される可能性があります",
                                file_path=file_path,
                                line_number=line_no,
                                code_snippet=line_stripped,
                                fix_suggestion="機密情報はログに出力せず、IDや一部のみを記録してください",
                            )
                        )

        return issues

    def _generate_fix_suggestions(
        self, issues: List[SecurityIssue], code_content: str
    ) -> List[FixSuggestion]:
        """修正提案の生成"""
        suggestions = []

        for issue in issues:
            if (
                issue.category == SecurityCategory.DANGEROUS_API
                and "eval" in issue.code_snippet
            ):
                suggestions.append(
                    FixSuggestion(
                        original_code=issue.code_snippet,
                        fixed_code=issue.code_snippet.replace(
                            "eval(", "ast.literal_eval("
                        ),
                        explanation="evalの代わりにast.literal_evalを使用",
                        risk_reduction="任意コード実行リスクを排除",
                    )
                )

        return suggestions

    def _empty_report(self, file_path: str, error_message: str) -> SecurityReport:
        """エラー時の空レポート生成"""
        return SecurityReport(
            scan_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            file_path=file_path,
            total_issues=0,
            issues_by_severity={},
            issues=[],
            fix_suggestions=[],
            scan_duration_ms=0,
        )
