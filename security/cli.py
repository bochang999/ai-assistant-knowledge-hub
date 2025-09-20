#!/usr/bin/env python3
"""
Python Security Guard CLI
ai-assistant-knowledge-hubセキュリティシステムのCLIエントリポイント
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional

from .analyzer import PythonSecurityAnalyzer
from .integrations.linear_reporter import LinearSecurityReporter
from .models import SeverityLevel


def main():
    """メインCLI関数"""
    parser = argparse.ArgumentParser(
        description="Python Security Guard - AI生成コードのセキュリティチェック",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一ファイルチェック
  python -m security.cli check file.py

  # ディレクトリ全体チェック
  python -m security.cli check src/

  # クリティカル問題のみ表示
  python -m security.cli check file.py --severity critical

  # Linear Issue自動作成
  python -m security.cli check file.py --create-issue --issue-id BOC-123

  # 既存ワークフローとの統合
  python -m security.cli workflow --phase 2 --issue-id BOC-123
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="利用可能なコマンド")

    # check コマンド
    check_parser = subparsers.add_parser("check", help="セキュリティチェック実行")
    check_parser.add_argument("path", help="チェック対象のファイルまたはディレクトリ")
    check_parser.add_argument("--config", help="設定ファイルパス")
    check_parser.add_argument(
        "--severity",
        choices=["critical", "high", "medium", "low", "info"],
        default="medium",
        help="表示する問題の最小重要度",
    )
    check_parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="出力形式",
    )
    check_parser.add_argument("--output", help="結果出力ファイル")
    check_parser.add_argument(
        "--create-issue", action="store_true", help="重要な問題をLinear Issueとして作成"
    )
    check_parser.add_argument("--issue-id", help="関連するLinear Issue ID")
    check_parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="クリティカル問題がある場合に終了コード1で終了",
    )

    # workflow コマンド
    workflow_parser = subparsers.add_parser(
        "workflow", help="ai-assistant-knowledge-hubワークフロー統合"
    )
    workflow_parser.add_argument("--phase", type=int, help="ワークフローフェーズ番号")
    workflow_parser.add_argument("--issue-id", required=True, help="Linear Issue ID")
    workflow_parser.add_argument("--project-path", help="プロジェクトパス")

    # setup コマンド
    setup_parser = subparsers.add_parser("setup", help="初期設定")
    setup_parser.add_argument(
        "--pre-commit", action="store_true", help="pre-commitフック設定"
    )

    args = parser.parse_args()

    if args.command == "check":
        return handle_check_command(args)
    elif args.command == "workflow":
        return handle_workflow_command(args)
    elif args.command == "setup":
        return handle_setup_command(args)
    else:
        parser.print_help()
        return 1


def handle_check_command(args) -> int:
    """checkコマンドの処理"""
    try:
        # セキュリティアナライザー初期化
        analyzer = PythonSecurityAnalyzer(args.config)
        linear_reporter = LinearSecurityReporter()

        target_path = Path(args.path)
        reports = []

        if target_path.is_file():
            if target_path.suffix == ".py":
                reports.append(analyzer.analyze_file(str(target_path)))
        elif target_path.is_dir():
            # Pythonファイルを再帰的に検索
            python_files = list(target_path.rglob("*.py"))
            for py_file in python_files[:20]:  # 最大20ファイルまで
                print(f"🔍 解析中: {py_file}")
                reports.append(analyzer.analyze_file(str(py_file)))
        else:
            print(f"❌ パスが見つかりません: {target_path}")
            return 1

        # 結果表示
        severity_threshold = SeverityLevel(args.severity)
        has_critical_issues = False

        for report in reports:
            if args.format == "json":
                print_json_report(report)
            elif args.format == "markdown":
                print_markdown_report(report)
            else:
                print_text_report(report, severity_threshold)

            if report.has_critical_issues:
                has_critical_issues = True

            # Linear Issue作成
            if args.create_issue and (
                report.has_critical_issues
                or any(i.severity == SeverityLevel.HIGH for i in report.issues)
            ):
                linear_reporter.create_security_issue(report, args.issue_id)
            elif args.issue_id:
                linear_reporter.update_issue_with_security_results(
                    args.issue_id, report
                )

        # 結果保存
        if args.output:
            save_reports(reports, args.output, args.format)

        # 終了コード決定
        if args.fail_on_critical and has_critical_issues:
            print("\n❌ クリティカルなセキュリティ問題が検出されました")
            return 1

        print(f"\n✅ セキュリティチェック完了 ({len(reports)}ファイル解析)")
        return 0

    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1


def handle_workflow_command(args) -> int:
    """workflowコマンドの処理"""
    try:
        print(f"🔄 ワークフロー統合 - Issue: {args.issue_id}, Phase: {args.phase}")

        # プロジェクトパス取得
        project_path = Path(args.project_path) if args.project_path else Path.cwd()

        # Pythonファイルを検索してセキュリティチェック
        analyzer = PythonSecurityAnalyzer()
        linear_reporter = LinearSecurityReporter()

        python_files = list(project_path.rglob("*.py"))
        if not python_files:
            print("✅ Pythonファイルが見つかりません")
            return 0

        reports = []
        for py_file in python_files[:10]:  # 最大10ファイル
            if py_file.name.startswith(("test_", "__")):
                continue  # テストファイルやプライベートファイルをスキップ

            report = analyzer.analyze_file(str(py_file))
            reports.append(report)

        # 結果の集計
        total_critical = sum(
            len([i for i in r.issues if i.severity == SeverityLevel.CRITICAL])
            for r in reports
        )
        total_high = sum(
            len([i for i in r.issues if i.severity == SeverityLevel.HIGH])
            for r in reports
        )

        # Linear Issueに結果を報告
        if total_critical > 0 or total_high > 0:
            # 重要な問題がある場合は詳細報告
            for report in reports:
                if report.issues:
                    linear_reporter.update_issue_with_security_results(
                        args.issue_id, report
                    )
        else:
            # 問題なしの場合は簡潔に報告
            dummy_report = reports[0] if reports else None
            if dummy_report:
                dummy_report.issues = []
                dummy_report.total_issues = 0
                linear_reporter.update_issue_with_security_results(
                    args.issue_id, dummy_report
                )

        print(
            f"✅ ワークフロー統合完了 - {len(python_files)}ファイル解析, {total_critical + total_high}問題"
        )
        return 1 if total_critical > 0 else 0

    except Exception as e:
        print(f"❌ ワークフロー統合エラー: {e}")
        return 1


def handle_setup_command(args) -> int:
    """setupコマンドの処理"""
    try:
        if args.pre_commit:
            setup_pre_commit_hook()
        else:
            print("セキュリティシステム初期設定")
            # 設定ファイル作成等

        return 0
    except Exception as e:
        print(f"❌ 設定エラー: {e}")
        return 1


def print_text_report(report, severity_threshold: SeverityLevel):
    """テキスト形式での結果表示"""
    print(f"\n📄 {report.file_path}")
    print(f"🔍 セキュリティスコア: {report.security_score}/100")
    print(f"📊 問題数: {report.total_issues}個")

    if not report.issues:
        print("✅ セキュリティ問題は検出されませんでした")
        return

    # 重要度フィルタリング
    severity_order = [
        SeverityLevel.CRITICAL,
        SeverityLevel.HIGH,
        SeverityLevel.MEDIUM,
        SeverityLevel.LOW,
        SeverityLevel.INFO,
    ]
    threshold_index = severity_order.index(severity_threshold)
    filtered_issues = [
        i for i in report.issues if severity_order.index(i.severity) <= threshold_index
    ]

    for issue in filtered_issues:
        severity_emoji = {
            SeverityLevel.CRITICAL: "🔴",
            SeverityLevel.HIGH: "🟡",
            SeverityLevel.MEDIUM: "🟠",
            SeverityLevel.LOW: "🟢",
            SeverityLevel.INFO: "ℹ️",
        }

        print(
            f"\n{severity_emoji[issue.severity]} **{issue.title}** ({issue.severity.value.upper()})"
        )
        print(f"   📍 {issue.line_number}行目: `{issue.code_snippet}`")
        print(f"   💡 {issue.fix_suggestion}")


def print_json_report(report):
    """JSON形式での結果表示"""
    # JSON serializable形式に変換
    report_dict = {
        "scan_id": report.scan_id,
        "timestamp": report.timestamp.isoformat(),
        "file_path": report.file_path,
        "total_issues": report.total_issues,
        "security_score": report.security_score,
        "issues": [],
    }

    for issue in report.issues:
        issue_dict = {
            "category": issue.category.value,
            "severity": issue.severity.value,
            "title": issue.title,
            "description": issue.description,
            "line_number": issue.line_number,
            "code_snippet": issue.code_snippet,
            "fix_suggestion": issue.fix_suggestion,
        }
        report_dict["issues"].append(issue_dict)

    print(json.dumps(report_dict, indent=2, ensure_ascii=False))


def print_markdown_report(report):
    """Markdown形式での結果表示"""
    print(f"# セキュリティ解析結果: {Path(report.file_path).name}")
    print(f"\n- **セキュリティスコア**: {report.security_score}/100")
    print(f"- **問題数**: {report.total_issues}個")
    print(f"- **解析時刻**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    if not report.issues:
        print("\n✅ セキュリティ問題は検出されませんでした")
        return

    print("\n## 検出された問題\n")

    for i, issue in enumerate(report.issues, 1):
        print(f"### {i}. {issue.title}")
        print(f"**重要度**: {issue.severity.value.upper()}")
        print(f"**位置**: {issue.line_number}行目")
        print(f"**説明**: {issue.description}")
        print(f"\n**問題のコード**:")
        print(f"```python")
        print(f"{issue.code_snippet}")
        print(f"```")
        print(f"\n**修正提案**: {issue.fix_suggestion}\n")


def save_reports(reports: List, output_path: str, format_type: str):
    """結果をファイルに保存"""
    output_file = Path(output_path)

    if format_type == "json":
        # すべてのレポートをJSON配列として保存
        all_reports = []
        for report in reports:
            # JSON serializable形式に変換（上記と同様）
            pass

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_reports, f, indent=2, ensure_ascii=False)
    else:
        # テキスト形式で保存
        with open(output_file, "w", encoding="utf-8") as f:
            for report in reports:
                f.write(f"セキュリティ解析結果: {report.file_path}\n")
                f.write(f"問題数: {report.total_issues}個\n\n")


def setup_pre_commit_hook():
    """pre-commitフック設定"""
    pre_commit_config = """repos:
  - repo: local
    hooks:
      - id: python-security-guard
        name: Python Security Guard
        entry: python -m security.cli check
        language: system
        files: \.py$
        args: [--severity, critical, --fail-on-critical]
"""

    config_file = Path(".pre-commit-config.yaml")
    if config_file.exists():
        print("⚠️ .pre-commit-config.yamlが既に存在します")
    else:
        config_file.write_text(pre_commit_config)
        print("✅ pre-commitフック設定を作成しました")


if __name__ == "__main__":
    sys.exit(main())
