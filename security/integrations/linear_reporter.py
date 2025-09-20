#!/usr/bin/env python3
"""
Linear Security Reporter
セキュリティ問題をLinear Issueシステムに自動報告

ai-assistant-knowledge-hubの既存Linear統合と連携
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..models import SecurityReport, SecurityIssue, SeverityLevel


class LinearSecurityReporter:
    """Linear Issue SystemへのSecurity報告クラス"""

    def __init__(self):
        self.api_key_file = Path.home() / ".linear-api-key"
        self.team_id_file = Path.home() / ".linear-team-id"
        self.api_key = self._load_api_key()
        self.team_id = self._load_team_id()

    def _load_api_key(self) -> Optional[str]:
        """Linear API key読み込み"""
        try:
            if self.api_key_file.exists():
                return self.api_key_file.read_text().strip()
        except Exception:
            pass
        return None

    def _load_team_id(self) -> Optional[str]:
        """Linear Team ID読み込み"""
        try:
            if self.team_id_file.exists():
                return self.team_id_file.read_text().strip()
        except Exception:
            pass
        return None

    def create_security_issue(
        self, security_report: SecurityReport, parent_issue_id: Optional[str] = None
    ) -> bool:
        """セキュリティ問題をLinear Issueとして作成"""
        if not self.api_key or not self.team_id:
            print("⚠️ Linear API設定が見つかりません")
            return False

        # クリティカルな問題のみIssue作成
        critical_issues = [
            i
            for i in security_report.issues
            if i.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]
        ]

        if not critical_issues:
            return True  # 問題なしとして成功

        try:
            issue_title = f"🔒 Security: {len(critical_issues)}個の問題を検出 - {Path(security_report.file_path).name}"
            issue_description = self._format_security_description(
                security_report, critical_issues
            )

            # GraphQL Mutation
            mutation = {
                "query": """
                mutation CreateIssue($input: IssueCreateInput!) {
                    issueCreate(input: $input) {
                        success
                        issue {
                            id
                            identifier
                            title
                        }
                    }
                }
                """,
                "variables": {
                    "input": {
                        "teamId": self.team_id,
                        "title": issue_title,
                        "description": issue_description,
                        "priority": self._get_priority_from_severity(
                            critical_issues[0].severity
                        ),
                        "labelIds": [],  # セキュリティラベルがあれば追加
                        "parentId": parent_issue_id,
                    }
                },
            }

            # GraphQL API呼び出し
            result = subprocess.run(
                [
                    "curl",
                    "-X",
                    "POST",
                    "https://api.linear.app/graphql",
                    "-H",
                    f"Authorization: {self.api_key}",
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    json.dumps(mutation),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            response = json.loads(result.stdout)

            if response.get("data", {}).get("issueCreate", {}).get("success"):
                issue_data = response["data"]["issueCreate"]["issue"]
                print(
                    f"✅ Linear Issue作成成功: {issue_data['identifier']} - {issue_data['title']}"
                )
                return True
            else:
                print(f"❌ Linear Issue作成失敗: {response}")
                return False

        except Exception as e:
            print(f"❌ Linear API呼び出しエラー: {e}")
            return False

    def update_issue_with_security_results(
        self, issue_id: str, security_report: SecurityReport
    ) -> bool:
        """既存Issueにセキュリティ結果を追加"""
        if not self.api_key:
            return False

        try:
            comment_content = self._format_security_comment(security_report)

            mutation = {
                "query": """
                mutation CreateComment($input: CommentCreateInput!) {
                    commentCreate(input: $input) {
                        success
                        comment {
                            id
                        }
                    }
                }
                """,
                "variables": {"input": {"issueId": issue_id, "body": comment_content}},
            }

            result = subprocess.run(
                [
                    "curl",
                    "-X",
                    "POST",
                    "https://api.linear.app/graphql",
                    "-H",
                    f"Authorization: {self.api_key}",
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    json.dumps(mutation),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            response = json.loads(result.stdout)
            return (
                response.get("data", {}).get("commentCreate", {}).get("success", False)
            )

        except Exception as e:
            print(f"❌ Linear Comment追加エラー: {e}")
            return False

    def _format_security_description(
        self, report: SecurityReport, critical_issues: List[SecurityIssue]
    ) -> str:
        """セキュリティ問題の詳細説明フォーマット"""
        description = f"""# 🔒 セキュリティ解析結果

## 📊 概要
- **ファイル**: `{report.file_path}`
- **検出時刻**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **セキュリティスコア**: {report.security_score}/100
- **総問題数**: {report.total_issues}個

## 🚨 重要な問題

"""

        for i, issue in enumerate(critical_issues[:5], 1):  # 最大5個まで
            description += f"""### {i}. {issue.title} ({issue.severity.value.upper()})

**説明**: {issue.description}

**位置**: {issue.file_path}:{issue.line_number}

**問題のコード**:
```python
{issue.code_snippet}
```

**修正提案**: {issue.fix_suggestion}

"""

        if len(critical_issues) > 5:
            description += f"\n...他 {len(critical_issues) - 5}個の問題があります。\n"

        description += f"""
## 🛠️ 次のステップ

1. 🔴 **CRITICAL**問題を優先的に修正
2. 🟡 **HIGH**問題を順次対応
3. ✅ 修正後に再スキャン実行

---
*🤖 ai-assistant-knowledge-hub Security System により自動生成*
"""

        return description

    def _format_security_comment(self, report: SecurityReport) -> str:
        """セキュリティ結果のコメントフォーマット"""
        return f"""## 🔒 セキュリティ再スキャン結果

**スキャン時刻**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**セキュリティスコア**: {report.security_score}/100
**問題数**: {report.total_issues}個

- 🔴 CRITICAL: {report.issues_by_severity.get(SeverityLevel.CRITICAL, 0)}個
- 🟡 HIGH: {report.issues_by_severity.get(SeverityLevel.HIGH, 0)}個
- 🟠 MEDIUM: {report.issues_by_severity.get(SeverityLevel.MEDIUM, 0)}個
- 🟢 LOW: {report.issues_by_severity.get(SeverityLevel.LOW, 0)}個

{f"✅ **改善**: セキュリティ問題が解決されました！" if report.total_issues == 0 else "🔧 **要対応**: 引き続きセキュリティ問題があります"}
"""

    def _get_priority_from_severity(self, severity: SeverityLevel) -> int:
        """セキュリティレベルからLinear Priority番号に変換"""
        priority_mapping = {
            SeverityLevel.CRITICAL: 1,  # Urgent
            SeverityLevel.HIGH: 2,  # High
            SeverityLevel.MEDIUM: 3,  # Medium
            SeverityLevel.LOW: 4,  # Low
            SeverityLevel.INFO: 4,  # Low
        }
        return priority_mapping.get(severity, 3)

    def create_security_summary_report(
        self, reports: List[SecurityReport], issue_id: str
    ) -> bool:
        """複数ファイルのセキュリティサマリーレポート作成"""
        if not reports:
            return True

        total_issues = sum(r.total_issues for r in reports)
        total_critical = sum(
            r.issues_by_severity.get(SeverityLevel.CRITICAL, 0) for r in reports
        )
        total_high = sum(
            r.issues_by_severity.get(SeverityLevel.HIGH, 0) for r in reports
        )

        summary_content = f"""## 📋 プロジェクト全体セキュリティサマリー

**解析ファイル数**: {len(reports)}個
**総問題数**: {total_issues}個
- 🔴 CRITICAL: {total_critical}個
- 🟡 HIGH: {total_high}個

### 🎯 優先対応項目
"""

        # 最も重要な問題を抽出
        all_critical_issues = []
        for report in reports:
            all_critical_issues.extend(
                [i for i in report.issues if i.severity == SeverityLevel.CRITICAL]
            )

        for i, issue in enumerate(all_critical_issues[:3], 1):
            summary_content += f"{i}. **{issue.title}** ({Path(issue.file_path).name}:{issue.line_number})\n"

        return self.update_issue_with_security_results(
            issue_id, reports[0]
        )  # 代表的なレポートを使用
