#!/usr/bin/env python3
"""
Security Rules Engine
セキュリティルールの管理システム
"""

from .dangerous_apis import DangerousAPIRules
from .secrets import SecretsRules
from .patterns import PatternRules

__all__ = ["SecurityRuleEngine", "DangerousAPIRules", "SecretsRules", "PatternRules"]


class SecurityRuleEngine:
    """セキュリティルールエンジン統合クラス"""

    def __init__(self):
        self.dangerous_api_rules = DangerousAPIRules()
        self.secrets_rules = SecretsRules()
        self.pattern_rules = PatternRules()

    def get_all_rules(self):
        """全ルールを取得"""
        rules = {}
        rules.update(self.dangerous_api_rules.get_rules())
        rules.update(self.secrets_rules.get_rules())
        rules.update(self.pattern_rules.get_rules())
        return rules

    def get_rule_by_category(self, category: str):
        """カテゴリ別ルール取得"""
        all_rules = self.get_all_rules()
        return {k: v for k, v in all_rules.items() if v.get("category") == category}
