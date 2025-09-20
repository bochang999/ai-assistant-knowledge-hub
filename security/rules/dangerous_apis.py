#!/usr/bin/env python3
"""
Dangerous APIs Security Rules
危険なAPI使用に関するセキュリティルール

PDFで特定された危険パターンの詳細ルール定義
"""

from ..models import SeverityLevel, SecurityCategory


class DangerousAPIRules:
    """危険なAPI使用検出ルール"""

    def get_rules(self):
        return {
            "eval_usage": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.CRITICAL,
                "title": "eval()使用による任意コード実行リスク",
                "description": "eval()は任意のPythonコードを実行するため、非常に危険です",
                "patterns": [r"\beval\s*\("],
                "fix_template": "ast.literal_eval()やjson.loads()を使用してください",
                "cwe_id": "CWE-94",
                "references": [
                    "https://docs.python.org/3/library/ast.html#ast.literal_eval"
                ],
            },
            "exec_usage": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.CRITICAL,
                "title": "exec()使用による任意コード実行リスク",
                "description": "exec()は任意のPythonコードを実行するため、非常に危険です",
                "patterns": [r"\bexec\s*\("],
                "fix_template": "より安全な代替手段を検討してください",
                "cwe_id": "CWE-94",
            },
            "shell_injection": {
                "category": SecurityCategory.INJECTION,
                "severity": SeverityLevel.HIGH,
                "title": "コマンドインジェクションリスク",
                "description": "shell=Trueは外部コマンド実行時に危険です",
                "patterns": [r"shell\s*=\s*True"],
                "fix_template": "shell=Falseを使用し、コマンドをリスト形式で渡してください",
                "cwe_id": "CWE-78",
            },
            "unsafe_yaml": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.HIGH,
                "title": "unsafe YAML loading",
                "description": "yaml.load()は任意オブジェクト実行の可能性があります",
                "patterns": [r"yaml\.load\s*\([^,)]*\)"],
                "fix_template": "yaml.safe_load()を使用してください",
                "cwe_id": "CWE-502",
            },
            "pickle_usage": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.HIGH,
                "title": "Pickle deserialization リスク",
                "description": "pickle.loads()は任意コード実行のリスクがあります",
                "patterns": [r"pickle\.loads?\s*\("],
                "fix_template": "信頼できるデータのみに使用し、JSON等の代替を検討してください",
                "cwe_id": "CWE-502",
            },
            "ssl_disabled": {
                "category": SecurityCategory.AUTHENTICATION,
                "severity": SeverityLevel.HIGH,
                "title": "SSL/TLS証明書検証無効化",
                "description": "verify=Falseは中間者攻撃のリスクがあります",
                "patterns": [r"verify\s*=\s*False"],
                "fix_template": "verify=Trueを使用し、証明書検証を有効にしてください",
                "cwe_id": "CWE-295",
            },
            "weak_random": {
                "category": SecurityCategory.AUTHENTICATION,
                "severity": SeverityLevel.MEDIUM,
                "title": "セキュリティ用途での弱い乱数使用",
                "description": "randomモジュールは暗号学的に安全ではありません",
                "patterns": [r"random\.(choice|randint|random)\s*\("],
                "fix_template": "cryptographically secure randomにはsecretsモジュールを使用してください",
                "cwe_id": "CWE-338",
            },
            "mutable_default": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.MEDIUM,
                "title": "可変デフォルト引数使用",
                "description": "可変オブジェクトがデフォルト引数に使用されています",
                "patterns": [r"def\s+\w+\([^)]*=\s*[\[\{]"],
                "fix_template": "デフォルト値をNoneにし、関数内で空のオブジェクトを作成してください",
                "cwe_id": "CWE-682",
            },
            "float_comparison": {
                "category": SecurityCategory.DANGEROUS_API,
                "severity": SeverityLevel.LOW,
                "title": "浮動小数点の直接比較",
                "description": "浮動小数点数の直接比較は丸め誤差で失敗する可能性があります",
                "patterns": [r"\d+\.\d+\s*[=!]=\s*\d+\.\d+"],
                "fix_template": "math.isclose()を使用してください",
                "references": [
                    "https://docs.python.org/3/library/math.html#math.isclose"
                ],
            },
        }

    def get_critical_rules(self):
        """クリティカルなルールのみ取得"""
        all_rules = self.get_rules()
        return {
            k: v
            for k, v in all_rules.items()
            if v["severity"] == SeverityLevel.CRITICAL
        }

    def get_fix_suggestions(self):
        """修正提案テンプレート集"""
        return {
            "eval_to_literal_eval": {
                "original_pattern": r"eval\s*\(",
                "fixed_pattern": "ast.literal_eval(",
                "description": "evalをast.literal_evalに置換",
                "imports_needed": ["import ast"],
            },
            "shell_true_to_false": {
                "original_pattern": r"shell\s*=\s*True",
                "fixed_pattern": "shell=False",
                "description": "shell=TrueをFalseに変更し、コマンドをリスト形式に",
                "additional_changes": "コマンド文字列をリスト形式に変更が必要",
            },
            "yaml_load_to_safe_load": {
                "original_pattern": r"yaml\.load\s*\(",
                "fixed_pattern": "yaml.safe_load(",
                "description": "yaml.loadをyaml.safe_loadに置換",
            },
        }
