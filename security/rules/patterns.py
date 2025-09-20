#!/usr/bin/env python3
"""
Pattern-based Security Rules
パターンベースセキュリティルール（その他のPDFパターン対応）
"""

from ..models import SeverityLevel, SecurityCategory


class PatternRules:
    """パターンベースセキュリティルール"""

    def get_rules(self):
        return {
            "naive_datetime": {
                "category": SecurityCategory.DATETIME,
                "severity": SeverityLevel.MEDIUM,
                "title": "タイムゾーン未指定のdatetime",
                "description": "datetime.now()はタイムゾーン情報がないため、国際化で問題になります",
                "patterns": [r"datetime\.now\(\)(?!\s*\()"],
                "fix_template": "datetime.now(timezone.utc)を使用してください",
            },
            "logging_format_issue": {
                "category": SecurityCategory.LOGGING,
                "severity": SeverityLevel.LOW,
                "title": "ログでのf文字列使用",
                "description": "ログレベルがoffでも文字列フォーマットが実行される可能性があります",
                "patterns": [r'logger\.(info|debug|warning|error)\s*\(\s*f["\']'],
                "fix_template": "logger.info('%s', value)形式を使用してください",
            },
            "performance_issue": {
                "category": SecurityCategory.PERFORMANCE,
                "severity": SeverityLevel.LOW,
                "title": "パフォーマンス問題",
                "description": "非効率なコードパターンが検出されました",
                "patterns": [
                    r"result\s*\+=\s*str\(",  # 文字列連結
                    r"for.*in.*for.*in",  # 二重ループ
                ],
                "fix_template": "より効率的な実装を検討してください",
            },
        }
