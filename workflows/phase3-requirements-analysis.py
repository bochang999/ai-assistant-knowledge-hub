#!/usr/bin/env python3
"""
Phase 3: Issue Requirements Analysis
BOC-95に基づく段階的問題解決ワークフローシステム

目的: Issue内容の詳細解析、要望の技術的要件抽出、現在のコードベースとの関係性分析
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


class RequirementsAnalysisEngine:
    def __init__(self, project_path: str = None):
        """Requirements Analysis Engine初期化"""
        self.project_path = Path(project_path or os.getcwd())
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.temp_dir = self.ai_hub_dir / "temp"

        # 前のPhaseのデータを読み込み
        self.issue_data = self._load_issue_data()
        self.project_analysis = self._load_project_analysis()

        # 要件分析結果
        self.requirements_result = {
            "issue_analysis": {},
            "technical_requirements": {},
            "codebase_impact": {},
            "implementation_scope": {},
            "risk_assessment": {},
        }

    def _load_issue_data(self) -> Optional[Dict]:
        """Phase 1のIssueデータ読み込み"""
        try:
            issue_files = list(self.temp_dir.glob("agent_issue_*.json"))
            if issue_files:
                latest_issue_file = max(issue_files, key=lambda f: f.stat().st_mtime)
                with open(latest_issue_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("issue_data")
        except Exception as e:
            print(f"⚠️  Issue データ読み込みエラー: {e}")
        return None

    def _load_project_analysis(self) -> Optional[Dict]:
        """Phase 2のプロジェクト分析データ読み込み"""
        try:
            analysis_files = list(self.temp_dir.glob("phase2_analysis_*.json"))
            if analysis_files:
                latest_analysis_file = max(
                    analysis_files, key=lambda f: f.stat().st_mtime
                )
                with open(latest_analysis_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("analysis_result")
        except Exception as e:
            print(f"⚠️  プロジェクト分析データ読み込みエラー: {e}")
        return None

    def analyze_requirements_comprehensive(self) -> Dict:
        """包括的要件分析実行"""
        print(f"🔍 要件分析開始: {self.project_path}")

        if not self.issue_data:
            raise Exception("❌ Issue データが見つかりません")

        # 1. Issue内容の詳細解析
        self._analyze_issue_content()

        # 2. 技術的要件抽出
        self._extract_technical_requirements()

        # 3. コードベース影響分析
        self._analyze_codebase_impact()

        # 4. 実装範囲定義
        self._define_implementation_scope()

        # 5. リスク評価
        self._assess_risks()

        # 6. 要件分析結果保存
        self._save_requirements_result()

        print("✅ 要件分析完了")
        return self.requirements_result

    def _analyze_issue_content(self):
        """Issue内容の詳細解析"""
        print("📋 Issue内容分析中...")

        issue_analysis = {
            "title": self.issue_data.get("title", ""),
            "description": self.issue_data.get("description", ""),
            "issue_type": "",
            "priority_level": "",
            "user_requests": [],
            "problem_statements": [],
            "expected_outcomes": [],
        }

        # Issue typeの推定
        title = issue_analysis["title"].lower()
        description = issue_analysis["description"].lower()

        if any(
            keyword in title + description
            for keyword in ["bug", "エラー", "問題", "不具合"]
        ):
            issue_analysis["issue_type"] = "Bug Fix"
        elif any(
            keyword in title + description
            for keyword in ["feature", "機能", "追加", "新規"]
        ):
            issue_analysis["issue_type"] = "Feature Request"
        elif any(
            keyword in title + description
            for keyword in ["改善", "最適化", "performance", "リファクタ"]
        ):
            issue_analysis["issue_type"] = "Enhancement"
        elif any(
            keyword in title + description
            for keyword in ["アーキテクチャ", "分析", "architecture"]
        ):
            issue_analysis["issue_type"] = "Architecture Analysis"
        else:
            issue_analysis["issue_type"] = "General Task"

        # 優先度推定
        if any(
            keyword in title + description
            for keyword in ["urgent", "緊急", "critical", "クリティカル"]
        ):
            issue_analysis["priority_level"] = "High"
        elif any(
            keyword in title + description for keyword in ["minor", "軽微", "small"]
        ):
            issue_analysis["priority_level"] = "Low"
        else:
            issue_analysis["priority_level"] = "Medium"

        # ユーザー要求抽出
        issue_analysis["user_requests"] = self._extract_user_requests(
            issue_analysis["description"]
        )

        # 問題文抽出
        issue_analysis["problem_statements"] = self._extract_problem_statements(
            issue_analysis["description"]
        )

        # 期待される結果抽出
        issue_analysis["expected_outcomes"] = self._extract_expected_outcomes(
            issue_analysis["description"]
        )

        self.requirements_result["issue_analysis"] = issue_analysis
        print(
            f"📝 Issue分析: {issue_analysis['issue_type']} ({issue_analysis['priority_level']})"
        )

    def _extract_user_requests(self, description: str) -> List[str]:
        """ユーザー要求抽出"""
        requests = []

        # パターンマッチングでユーザー要求を抽出
        request_patterns = [
            r"ユーザー.*?(?:要求|要望|希望).*?[。.]",
            r"(?:求める|必要な|欲しい).*?[。.]",
            r"(?:実装|追加|修正).*?してください",
            r"(?:したい|できるように).*?[。.]",
        ]

        for pattern in request_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            requests.extend(matches)

        return requests[:5]  # 最大5個

    def _extract_problem_statements(self, description: str) -> List[str]:
        """問題文抽出"""
        problems = []

        # 問題を示すパターン
        problem_patterns = [
            r"問題.*?[。.]",
            r"エラー.*?[。.]",
            r"(?:動かない|機能しない|できない).*?[。.]",
            r"(?:バグ|不具合).*?[。.]",
        ]

        for pattern in problem_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            problems.extend(matches)

        return problems[:3]  # 最大3個

    def _extract_expected_outcomes(self, description: str) -> List[str]:
        """期待される結果抽出"""
        outcomes = []

        # 期待される結果のパターン
        outcome_patterns = [
            r"期待.*?[。.]",
            r"(?:結果|効果).*?[。.]",
            r"(?:完了|成功).*?[。.]",
            r"(?:動作|機能)する.*?[。.]",
        ]

        for pattern in outcome_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            outcomes.extend(matches)

        return outcomes[:3]  # 最大3個

    def _extract_technical_requirements(self):
        """技術的要件抽出"""
        print("⚙️  技術的要件抽出中...")

        tech_requirements = {
            "affected_components": [],
            "required_technologies": [],
            "api_requirements": [],
            "database_changes": [],
            "ui_requirements": [],
            "performance_requirements": [],
            "compatibility_requirements": [],
        }

        issue_content = (
            self.issue_data.get("title", "")
            + " "
            + self.issue_data.get("description", "")
        ).lower()

        # 影響を受けるコンポーネント特定
        tech_requirements["affected_components"] = self._identify_affected_components(
            issue_content
        )

        # 必要な技術特定
        tech_requirements["required_technologies"] = (
            self._identify_required_technologies(issue_content)
        )

        # API要件
        if any(
            keyword in issue_content
            for keyword in ["api", "endpoint", "rest", "graphql"]
        ):
            tech_requirements["api_requirements"].append("API modifications required")

        # データベース変更
        if any(
            keyword in issue_content
            for keyword in ["database", "db", "データベース", "storage"]
        ):
            tech_requirements["database_changes"].append("Database schema changes")

        # UI要件
        if any(
            keyword in issue_content
            for keyword in ["ui", "画面", "ページ", "ボタン", "表示"]
        ):
            tech_requirements["ui_requirements"].append("UI/UX modifications")

        # パフォーマンス要件
        if any(
            keyword in issue_content
            for keyword in ["performance", "パフォーマンス", "速度", "最適化"]
        ):
            tech_requirements["performance_requirements"].append(
                "Performance optimization"
            )

        # 互換性要件
        if any(
            keyword in issue_content
            for keyword in ["browser", "ブラウザ", "mobile", "モバイル"]
        ):
            tech_requirements["compatibility_requirements"].append(
                "Cross-platform compatibility"
            )

        self.requirements_result["technical_requirements"] = tech_requirements
        print(
            f"🔧 技術要件: {len(tech_requirements['affected_components'])} components affected"
        )

    def _identify_affected_components(self, issue_content: str) -> List[str]:
        """影響を受けるコンポーネント特定"""
        components = []

        # プロジェクトファイルから主要コンポーネントを特定
        if self.project_analysis:
            key_files = self.project_analysis.get("project_structure", {}).get(
                "key_files", {}
            )

            # 重要ファイルの存在確認とIssue内容との関連性
            if "package.json" in key_files and any(
                keyword in issue_content for keyword in ["npm", "node", "javascript"]
            ):
                components.append("Node.js/NPM Dependencies")

            if "capacitor.config.json" in key_files and any(
                keyword in issue_content for keyword in ["mobile", "app", "android"]
            ):
                components.append("Capacitor Mobile Platform")

        # ファイル名やパスの直接言及をチェック
        file_mentions = re.findall(r"[\w\-]+\.(js|ts|html|css|json|py)", issue_content)
        components.extend([f"File: {mention}" for mention in file_mentions[:3]])

        return components

    def _identify_required_technologies(self, issue_content: str) -> List[str]:
        """必要な技術特定"""
        technologies = []

        # 技術キーワードマッピング
        tech_keywords = {
            "capacitor": "Capacitor Framework",
            "react": "React",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "html": "HTML/CSS",
            "api": "API Integration",
            "database": "Database",
            "mobile": "Mobile Development",
        }

        for keyword, tech_name in tech_keywords.items():
            if keyword in issue_content:
                technologies.append(tech_name)

        return technologies

    def _analyze_codebase_impact(self):
        """コードベース影響分析"""
        print("🏗️  コードベース影響分析中...")

        impact_analysis = {
            "modification_scope": "",
            "affected_files": [],
            "breaking_changes_risk": "",
            "dependency_changes": [],
            "architecture_impact": "",
        }

        # プロジェクト分析結果を基に影響範囲を推定
        if self.project_analysis:
            total_files = self.project_analysis.get("project_structure", {}).get(
                "total_files", 0
            )
            complexity = self.project_analysis.get("architecture_patterns", {}).get(
                "complexity_level", ""
            )

            # 修正スコープ推定
            issue_type = self.requirements_result["issue_analysis"]["issue_type"]

            if issue_type == "Bug Fix":
                impact_analysis["modification_scope"] = "Localized"
            elif issue_type == "Feature Request":
                impact_analysis["modification_scope"] = "Medium"
            elif issue_type == "Architecture Analysis":
                impact_analysis["modification_scope"] = "Extensive"
            else:
                impact_analysis["modification_scope"] = "Small"

            # Breaking changes リスク
            if complexity == "Complex" and issue_type in [
                "Feature Request",
                "Architecture Analysis",
            ]:
                impact_analysis["breaking_changes_risk"] = "High"
            elif complexity == "Medium":
                impact_analysis["breaking_changes_risk"] = "Medium"
            else:
                impact_analysis["breaking_changes_risk"] = "Low"

            # アーキテクチャ影響
            structure_type = self.project_analysis.get("architecture_patterns", {}).get(
                "structure_type", ""
            )
            if "workflow" in structure_type.lower():
                impact_analysis["architecture_impact"] = "Workflow System Impact"
            elif "mobile" in structure_type.lower():
                impact_analysis["architecture_impact"] = "Mobile Platform Impact"
            else:
                impact_analysis["architecture_impact"] = "Standard Impact"

        self.requirements_result["codebase_impact"] = impact_analysis
        print(
            f"📊 影響分析: {impact_analysis['modification_scope']} scope, {impact_analysis['breaking_changes_risk']} risk"
        )

    def _define_implementation_scope(self):
        """実装範囲定義"""
        print("📋 実装範囲定義中...")

        scope = {
            "primary_tasks": [],
            "secondary_tasks": [],
            "deliverables": [],
            "testing_requirements": [],
            "documentation_needs": [],
        }

        issue_type = self.requirements_result["issue_analysis"]["issue_type"]
        tech_requirements = self.requirements_result["technical_requirements"]

        # Issue typeに基づく主要タスク
        if issue_type == "Bug Fix":
            scope["primary_tasks"] = [
                "問題の根本原因特定",
                "修正の実装",
                "テストによる検証",
            ]
        elif issue_type == "Feature Request":
            scope["primary_tasks"] = [
                "機能仕様の詳細化",
                "実装計画の策定",
                "機能の実装",
                "テスト実装",
            ]
        elif issue_type == "Architecture Analysis":
            scope["primary_tasks"] = [
                "現在のアーキテクチャ分析",
                "問題点の特定",
                "改善案の提案",
                "実装戦略の策定",
            ]

        # 技術要件に基づく副次タスク
        if tech_requirements["ui_requirements"]:
            scope["secondary_tasks"].append("UI/UX改善")
        if tech_requirements["api_requirements"]:
            scope["secondary_tasks"].append("API修正・テスト")
        if tech_requirements["database_changes"]:
            scope["secondary_tasks"].append("データベース変更")

        # 成果物定義
        scope["deliverables"] = ["実装されたコード", "テスト結果", "変更内容の文書化"]

        # テスト要件
        scope["testing_requirements"] = ["機能テスト", "回帰テスト"]

        if self.project_analysis and self.project_analysis.get("tech_stack", {}).get(
            "mobile_platform"
        ):
            scope["testing_requirements"].append("クロスプラットフォームテスト")

        # ドキュメント要件
        scope["documentation_needs"] = [
            "変更内容の記録",
            "技術決定の根拠",
            "今後の保守ガイド",
        ]

        self.requirements_result["implementation_scope"] = scope
        print(f"📝 実装範囲: {len(scope['primary_tasks'])} primary tasks")

    def _assess_risks(self):
        """リスク評価"""
        print("⚠️  リスク評価中...")

        risks = {
            "technical_risks": [],
            "implementation_risks": [],
            "business_risks": [],
            "mitigation_strategies": [],
        }

        # 技術リスク
        complexity = ""
        if self.project_analysis:
            complexity = self.project_analysis.get("architecture_patterns", {}).get(
                "complexity_level", ""
            )

        if complexity == "Complex":
            risks["technical_risks"].append("複雑なコードベースでの予期しない副作用")
        if (
            self.requirements_result["codebase_impact"]["breaking_changes_risk"]
            == "High"
        ):
            risks["technical_risks"].append("既存機能への破壊的変更リスク")

        # 実装リスク
        affected_components = len(
            self.requirements_result["technical_requirements"]["affected_components"]
        )
        if affected_components > 3:
            risks["implementation_risks"].append(
                "複数コンポーネント変更による統合リスク"
            )

        # ビジネスリスク
        priority = self.requirements_result["issue_analysis"]["priority_level"]
        if priority == "High":
            risks["business_risks"].append("緊急要件による品質リスク")

        # 軽減策
        risks["mitigation_strategies"] = [
            "段階的実装による影響範囲の制限",
            "包括的テストによる品質確保",
            "コードレビューによる品質管理",
            "バックアップ・ロールバック計画",
        ]

        self.requirements_result["risk_assessment"] = risks
        print(
            f"🚨 リスク評価: {len(risks['technical_risks']) + len(risks['implementation_risks'])} major risks"
        )

    def _save_requirements_result(self):
        """要件分析結果保存"""
        self.temp_dir.mkdir(exist_ok=True)

        # Phase 3の結果ファイル
        requirements_file = (
            self.temp_dir / f"phase3_requirements_{self.project_path.name}.json"
        )

        with open(requirements_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "phase": "3-requirements-analysis",
                    "timestamp": subprocess.check_output(["date"]).decode().strip(),
                    "project_name": self.project_path.name,
                    "issue_id": self.issue_data.get("id") if self.issue_data else None,
                    "requirements_result": self.requirements_result,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 要件分析結果保存: {requirements_file}")


def main():
    """メイン実行関数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    try:
        # Requirements Analysis Engine初期化
        requirements_engine = RequirementsAnalysisEngine(project_path)

        # 要件分析実行
        requirements_result = requirements_engine.analyze_requirements_comprehensive()

        print(f"🎯 Phase 3 完了: {requirements_result['issue_analysis']['issue_type']}")
        print(
            f"💡 次のコマンド: python {requirements_engine.ai_hub_dir}/workflows/phase4-strategic-planning.py"
        )

    except Exception as e:
        print(f"❌ Phase 3 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
