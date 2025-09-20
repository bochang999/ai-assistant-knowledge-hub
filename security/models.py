#!/usr/bin/env python3
"""
Security Analysis Models
セキュリティ解析結果のデータモデル定義
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


class SeverityLevel(Enum):
    """セキュリティ問題の重要度"""

    CRITICAL = "critical"  # 即座に修正すべき
    HIGH = "high"  # 優先度高
    MEDIUM = "medium"  # 注意が必要
    LOW = "low"  # 改善推奨
    INFO = "info"  # 情報提供


class SecurityCategory(Enum):
    """セキュリティ問題のカテゴリ"""

    DANGEROUS_API = "dangerous_api"  # eval, exec等
    INJECTION = "injection"  # SQLインジェクション等
    SECRETS_EXPOSURE = "secrets_exposure"  # 秘密情報露出
    RESOURCE_LEAK = "resource_leak"  # リソース未解放
    AUTHENTICATION = "authentication"  # 認証関連
    PERFORMANCE = "performance"  # パフォーマンス問題
    CONFIGURATION = "configuration"  # 設定問題
    LOGGING = "logging"  # ログ関連
    EXCEPTION_HANDLING = "exception_handling"  # 例外処理
    DATETIME = "datetime"  # 日時処理


@dataclass
class SecurityIssue:
    """セキュリティ問題の詳細"""

    category: SecurityCategory
    severity: SeverityLevel
    title: str
    description: str
    file_path: str
    line_number: int
    code_snippet: str
    fix_suggestion: str
    reference_url: Optional[str] = None
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID


@dataclass
class FixSuggestion:
    """修正提案"""

    original_code: str
    fixed_code: str
    explanation: str
    risk_reduction: str


@dataclass
class SecurityReport:
    """セキュリティ解析報告書"""

    scan_id: str
    timestamp: datetime
    file_path: str
    total_issues: int
    issues_by_severity: Dict[SeverityLevel, int]
    issues: List[SecurityIssue]
    fix_suggestions: List[FixSuggestion]
    scan_duration_ms: float

    @property
    def has_critical_issues(self) -> bool:
        """クリティカルな問題があるかチェック"""
        return self.issues_by_severity.get(SeverityLevel.CRITICAL, 0) > 0

    @property
    def security_score(self) -> int:
        """セキュリティスコア (0-100, 100が最も安全)"""
        total_weight = 0
        critical_weight = self.issues_by_severity.get(SeverityLevel.CRITICAL, 0) * 50
        high_weight = self.issues_by_severity.get(SeverityLevel.HIGH, 0) * 20
        medium_weight = self.issues_by_severity.get(SeverityLevel.MEDIUM, 0) * 10
        low_weight = self.issues_by_severity.get(SeverityLevel.LOW, 0) * 5

        total_weight = critical_weight + high_weight + medium_weight + low_weight
        return max(0, 100 - total_weight)


# PDFから抽出した危険パターンのマッピング
DANGEROUS_PATTERNS = {
    # 1. 例外の握りつぶし・雑なexcept
    "bare_except": SecurityCategory.EXCEPTION_HANDLING,
    "broad_except": SecurityCategory.EXCEPTION_HANDLING,
    # 2. 可変デフォルト引数
    "mutable_default": SecurityCategory.DANGEROUS_API,
    # 3. セキュリティ危険API
    "eval_usage": SecurityCategory.DANGEROUS_API,
    "exec_usage": SecurityCategory.DANGEROUS_API,
    "shell_injection": SecurityCategory.INJECTION,
    "unsafe_yaml": SecurityCategory.DANGEROUS_API,
    "pickle_usage": SecurityCategory.DANGEROUS_API,
    "ssl_disabled": SecurityCategory.AUTHENTICATION,
    # 4. SQLインジェクション・パス操作
    "sql_injection": SecurityCategory.INJECTION,
    "path_traversal": SecurityCategory.INJECTION,
    # 5. ログに秘密情報
    "secrets_in_logs": SecurityCategory.SECRETS_EXPOSURE,
    # 6. タイムゾーン無自覚
    "naive_datetime": SecurityCategory.DATETIME,
    # 7. 浮動小数点直接比較
    "float_comparison": SecurityCategory.DANGEROUS_API,
    # 8. Pandas警告無視
    "pandas_chain_assignment": SecurityCategory.PERFORMANCE,
    # 9. 非同期処理でブロッキング
    "async_blocking": SecurityCategory.PERFORMANCE,
    # 10. リソース未解放
    "resource_leak": SecurityCategory.RESOURCE_LEAK,
    # 11. ハードコード値
    "hardcoded_secrets": SecurityCategory.SECRETS_EXPOSURE,
    "hardcoded_config": SecurityCategory.CONFIGURATION,
    # 12. 存在しない引数・関数名
    "api_hallucination": SecurityCategory.DANGEROUS_API,
    # 13. パフォーマンス地雷
    "performance_issue": SecurityCategory.PERFORMANCE,
    # 14. セキュリティ用途での一般乱数
    "weak_random": SecurityCategory.AUTHENTICATION,
    # 15. ログでのf文字列使用
    "logging_format_issue": SecurityCategory.LOGGING,
}
