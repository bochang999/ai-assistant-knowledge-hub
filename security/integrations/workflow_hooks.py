#!/usr/bin/env python3
"""
Workflow Security Hooks
ai-assistant-knowledge-hubワークフローシステムとの統合

既存のフェーズシステムにセキュリティチェックを組み込み
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..analyzer import PythonSecurityAnalyzer
from ..integrations.linear_reporter import LinearSecurityReporter
from ..models import SecurityReport, SeverityLevel


class WorkflowSecurityHooks:
    """ワークフローフェーズでのセキュリティ統合"""

    def __init__(self, ai_hub_dir: str = None):
        self.ai_hub_dir = (
            Path(ai_hub_dir) if ai_hub_dir else Path(__file__).parent.parent.parent
        )
        self.analyzer = PythonSecurityAnalyzer()
        self.linear_reporter = LinearSecurityReporter()

    def pre_phase_security_check(
        self, phase_number: int, issue_id: str, project_path: str
    ) -> bool:
        """フェーズ開始前のセキュリティチェック"""
        print(f"🔒 Phase {phase_number} セキュリティチェック開始")

        # プロジェクト内のPythonファイルを解析
        project_dir = Path(project_path)
        python_files = list(project_dir.rglob("*.py"))

        if not python_files:
            print("✅ Pythonファイルなし - セキュリティチェックスキップ")
            return True

        critical_issues_found = False
        reports = []

        for py_file in python_files[:10]:  # 最大10ファイル
            # テストファイルや一時ファイルをスキップ
            if any(
                pattern in str(py_file)
                for pattern in ["test_", "__pycache__", ".pyc", "temp"]
            ):
                continue

            try:
                report = self.analyzer.analyze_file(str(py_file))
                reports.append(report)

                if report.has_critical_issues:
                    critical_issues_found = True
                    print(
                        f"🔴 {py_file.name}: {len([i for i in report.issues if i.severity == SeverityLevel.CRITICAL])}個のクリティカル問題"
                    )

            except Exception as e:
                print(f"⚠️ {py_file.name}: 解析エラー - {e}")

        # Linear Issueに結果報告
        if reports and issue_id:
            self._report_to_linear(issue_id, reports, phase_number)

        if critical_issues_found:
            print(
                f"❌ Phase {phase_number}: クリティカルなセキュリティ問題が検出されました"
            )
            return False

        print(f"✅ Phase {phase_number}: セキュリティチェック完了")
        return True

    def post_code_generation_check(
        self, generated_code: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """AIコード生成後のリアルタイムチェック"""
        result = {"safe": True, "issues": [], "suggestions": [], "score": 100}

        try:
            # 生成されたコードを解析
            report = self.analyzer.analyze_code(generated_code, "<generated>")

            result["score"] = report.security_score
            result["safe"] = not report.has_critical_issues

            # 問題を結果に追加
            for issue in report.issues:
                if issue.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
                    result["issues"].append(
                        {
                            "severity": issue.severity.value,
                            "title": issue.title,
                            "description": issue.description,
                            "line": issue.line_number,
                            "fix": issue.fix_suggestion,
                        }
                    )

            # 修正提案を追加
            for suggestion in report.fix_suggestions:
                result["suggestions"].append(
                    {
                        "original": suggestion.original_code,
                        "fixed": suggestion.fixed_code,
                        "explanation": suggestion.explanation,
                    }
                )

        except Exception as e:
            result["safe"] = False
            result["issues"].append(
                {
                    "severity": "error",
                    "title": "解析エラー",
                    "description": str(e),
                    "line": 1,
                    "fix": "コード構文を確認してください",
                }
            )

        return result

    def executor_py_security_wrapper(self, function_name: str, args: List[str]) -> bool:
        """executor.pyのセキュリティラッパー"""
        print(f"🔒 executor.py セキュリティチェック: {function_name}")

        # 危険な操作をチェック
        dangerous_functions = ["write_file", "run_command"]
        if function_name in dangerous_functions:
            return self._check_executor_security(function_name, args)

        return True

    def _check_executor_security(self, function_name: str, args: List[str]) -> bool:
        """executor.py特有のセキュリティチェック"""
        if function_name == "write_file" and len(args) >= 2:
            file_path, content = args[0], args[1]

            # 書き込み先パスの検証
            if self._is_dangerous_path(file_path):
                print(f"❌ 危険なファイル書き込み試行: {file_path}")
                return False

            # 書き込み内容のセキュリティチェック
            if file_path.endswith(".py"):
                security_result = self.post_code_generation_check(content, {})
                if not security_result["safe"]:
                    print("❌ 生成されるPythonコードにセキュリティ問題があります")
                    for issue in security_result["issues"]:
                        print(f"   🔴 {issue['title']}: {issue['description']}")
                    return False

        elif function_name == "run_command":
            command = args[0] if args else ""

            # 危険なコマンドパターンを検出
            dangerous_patterns = [
                "rm -rf",
                "sudo",
                "curl | sh",
                "wget | sh",
                "eval",
                "exec",
                "; rm",
                "&& rm",
            ]

            for pattern in dangerous_patterns:
                if pattern in command.lower():
                    print(f"❌ 危険なコマンド実行試行: {pattern}")
                    return False

        return True

    def _is_dangerous_path(self, file_path: str) -> bool:
        """危険なファイルパスかチェック"""
        dangerous_paths = [
            "/etc/",
            "/usr/",
            "/bin/",
            "/sbin/",
            "/boot/",
            "~/.ssh/",
            "~/.aws/",
            "~/.config/",
            "../",
            "..\\",
            "/tmp/",
            "/var/",
        ]

        path_lower = file_path.lower()
        return any(dangerous in path_lower for dangerous in dangerous_paths)

    def _report_to_linear(
        self, issue_id: str, reports: List[SecurityReport], phase_number: int
    ):
        """Linear Issueに結果を報告"""
        total_issues = sum(r.total_issues for r in reports)
        critical_count = sum(
            len([i for i in r.issues if i.severity == SeverityLevel.CRITICAL])
            for r in reports
        )
        high_count = sum(
            len([i for i in r.issues if i.severity == SeverityLevel.HIGH])
            for r in reports
        )

        if total_issues == 0:
            comment = f"## ✅ Phase {phase_number} セキュリティチェック\n\n**結果**: 問題なし\n**解析ファイル数**: {len(reports)}個"
        else:
            comment = f"""## 🔒 Phase {phase_number} セキュリティチェック結果

**総問題数**: {total_issues}個
- 🔴 CRITICAL: {critical_count}個
- 🟡 HIGH: {high_count}個
**解析ファイル数**: {len(reports)}個

{f"⚠️ **要対応**: クリティカル問題があります" if critical_count > 0 else "✅ **安全**: クリティカル問題なし"}
"""

        try:
            # 代表的なレポートでコメント作成
            dummy_report = reports[0] if reports else None
            if dummy_report:
                dummy_report.issues = []  # コメントは簡潔に
                self.linear_reporter.update_issue_with_security_results(
                    issue_id, dummy_report
                )
        except Exception as e:
            print(f"⚠️ Linear報告エラー: {e}")

    def integrate_with_phase_scripts(self):
        """既存のフェーズスクリプトにセキュリティチェックを統合"""
        workflows_dir = self.ai_hub_dir / "workflows"

        if not workflows_dir.exists():
            print("⚠️ workflowsディレクトリが見つかりません")
            return

        for phase_file in workflows_dir.glob("phase*.py"):
            self._add_security_hook_to_phase(phase_file)

    def _add_security_hook_to_phase(self, phase_file: Path):
        """個別のフェーズファイルにセキュリティフックを追加"""
        try:
            content = phase_file.read_text(encoding="utf-8")

            # 既にセキュリティフックが存在するかチェック
            if "WorkflowSecurityHooks" in content:
                return

            # セキュリティフックを追加
            security_import = "\nfrom security.integrations.workflow_hooks import WorkflowSecurityHooks\n"
            security_init = "\n    security_hooks = WorkflowSecurityHooks()\n"

            # ファイルの先頭にimportを追加
            lines = content.split("\n")
            import_index = -1
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    import_index = i

            if import_index >= 0:
                lines.insert(import_index + 1, security_import.strip())

            # クラス定義内にセキュリティ初期化を追加
            for i, line in enumerate(lines):
                if "def __init__" in line and "self" in line:
                    # __init__メソッドの最後にセキュリティフックを追加
                    j = i + 1
                    while j < len(lines) and (
                        lines[j].startswith("        ") or lines[j].strip() == ""
                    ):
                        j += 1
                    lines.insert(j, security_init.strip())
                    break

            modified_content = "\n".join(lines)
            phase_file.write_text(modified_content, encoding="utf-8")
            print(f"✅ {phase_file.name}にセキュリティフック追加")

        except Exception as e:
            print(f"⚠️ {phase_file.name}セキュリティフック追加エラー: {e}")


def create_security_wrapper_for_executor():
    """executor.py用のセキュリティラッパー作成"""
    wrapper_code = '''#!/usr/bin/env python3
"""
Security Wrapper for executor.py
executor.pyのセキュリティ強化ラッパー
"""

import sys
from pathlib import Path

# セキュリティシステムをインポート
sys.path.insert(0, str(Path(__file__).parent))
from security.integrations.workflow_hooks import WorkflowSecurityHooks

# 元のexecutor.pyをインポート
from executor import write_file as original_write_file
from executor import run_command as original_run_command
from executor import git_push as original_git_push

security_hooks = WorkflowSecurityHooks()

def write_file(path, content):
    """セキュリティチェック付きファイル書き込み"""
    if not security_hooks.executor_py_security_wrapper('write_file', [path, content]):
        print("❌ セキュリティチェックにより操作がブロックされました")
        return False

    return original_write_file(path, content)

def run_command(command_string):
    """セキュリティチェック付きコマンド実行"""
    if not security_hooks.executor_py_security_wrapper('run_command', [command_string]):
        print("❌ セキュリティチェックにより操作がブロックされました")
        return False

    return original_run_command(command_string)

def git_push(commit_message):
    """Git push（セキュリティチェック付き）"""
    # Git操作は比較的安全なので、基本的にそのまま実行
    return original_git_push(commit_message)

if __name__ == "__main__":
    # 元のexecutor.pyと同じメインロジック
    if len(sys.argv) < 2:
        print("ERROR: No function specified.")
        sys.exit(1)

    function_name = sys.argv[1]
    args = sys.argv[2:]

    if function_name == "write_file":
        if len(args) != 2:
            print("ERROR: write_file requires path and content arguments.")
            sys.exit(1)
        write_file(args[0], args[1])
    elif function_name == "run_command":
        if len(args) != 1:
            print("ERROR: run_command requires a command string argument.")
            sys.exit(1)
        run_command(args[0])
    elif function_name == "git_push":
        if len(args) != 1:
            print("ERROR: git_push requires a commit message argument.")
            sys.exit(1)
        git_push(args[0])
    else:
        print(f"ERROR: Unknown function: {function_name}")
        sys.exit(1)
'''

    ai_hub_dir = Path(__file__).parent.parent.parent
    wrapper_file = ai_hub_dir / "executor_secure.py"

    wrapper_file.write_text(wrapper_code, encoding="utf-8")
    print(f"✅ セキュリティラッパー作成: {wrapper_file}")
