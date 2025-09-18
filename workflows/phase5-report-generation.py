#!/usr/bin/env python3
"""
Phase 5: Report Generation & Linear Integration
BOC-95に基づく段階的問題解決ワークフローシステム

目的: 詳細レポート生成、Linear Issue自動追記、レビュー要求の送信
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ReportGenerationEngine:
    def __init__(self, project_path: str = None):
        """Report Generation Engine初期化"""
        self.project_path = Path(project_path or os.getcwd())
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.temp_dir = self.ai_hub_dir / "temp"
        self.home_dir = Path("/data/data/com.termux/files/home")

        # 全Phaseのデータを読み込み
        self.issue_data = self._load_issue_data()
        self.project_analysis = self._load_project_analysis()
        self.requirements_result = self._load_requirements_analysis()
        self.strategic_plan = self._load_strategic_plan()

        # Linear API設定
        self.linear_api_key = self._get_linear_api_key()

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

    def _load_requirements_analysis(self) -> Optional[Dict]:
        """Phase 3の要件分析データ読み込み"""
        try:
            req_files = list(self.temp_dir.glob("phase3_requirements_*.json"))
            if req_files:
                latest_req_file = max(req_files, key=lambda f: f.stat().st_mtime)
                with open(latest_req_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("requirements_result")
        except Exception as e:
            print(f"⚠️  要件分析データ読み込みエラー: {e}")
        return None

    def _load_strategic_plan(self) -> Optional[Dict]:
        """Phase 4の戦略計画データ読み込み"""
        try:
            strategy_files = list(self.temp_dir.glob("phase4_strategy_*.json"))
            if strategy_files:
                latest_strategy_file = max(
                    strategy_files, key=lambda f: f.stat().st_mtime
                )
                with open(latest_strategy_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("strategic_plan")
        except Exception as e:
            print(f"⚠️  戦略計画データ読み込みエラー: {e}")
        return None

    def _get_linear_api_key(self) -> str:
        """Linear API Key取得"""
        try:
            with open(self.home_dir / ".linear-api-key", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception("❌ Linear API Keyが見つかりません: ~/.linear-api-key")

    def generate_comprehensive_report(self) -> Dict:
        """包括的レポート生成"""
        print(f"📝 包括的レポート生成開始")

        if not all(
            [
                self.issue_data,
                self.project_analysis,
                self.requirements_result,
                self.strategic_plan,
            ]
        ):
            raise Exception("❌ 前のPhaseのデータが不完全です")

        # 1. 分析レポート生成
        analysis_report = self._generate_analysis_report()

        # 2. 実装戦略レポート生成
        strategy_report = self._generate_strategy_report()

        # 3. 技術決定レポート生成
        technical_report = self._generate_technical_report()

        # 4. 統合レポート作成
        comprehensive_report = self._create_comprehensive_report(
            analysis_report, strategy_report, technical_report
        )

        # 5. Linear Issue更新
        self._update_linear_issue(comprehensive_report)

        # 6. レビュー要求送信
        self._request_ai_review(comprehensive_report)

        print("✅ レポート生成・Linear更新完了")
        return comprehensive_report

    def _generate_analysis_report(self) -> str:
        """分析レポート生成"""
        print("📊 分析レポート生成中...")

        project_name = self.project_analysis.get("project_purpose", {}).get("name", "")
        issue_title = self.issue_data.get("title", "")
        issue_type = self.requirements_result.get("issue_analysis", {}).get(
            "issue_type", ""
        )

        analysis_report = f"""
# 📊 プロジェクト分析レポート

## プロジェクト概要
- **プロジェクト名**: {project_name}
- **ドメイン**: {self.project_analysis.get("project_purpose", {}).get("domain", "")}
- **複雑度**: {self.project_analysis.get("architecture_patterns", {}).get("complexity_level", "")}
- **技術スタック**: {', '.join(self.project_analysis.get("tech_stack", {}).get("language", []))}

## Issue分析
- **タイトル**: {issue_title}
- **タイプ**: {issue_type}
- **優先度**: {self.requirements_result.get("issue_analysis", {}).get("priority_level", "")}
- **影響範囲**: {self.requirements_result.get("codebase_impact", {}).get("modification_scope", "")}

## 技術的要件
- **影響コンポーネント**: {len(self.requirements_result.get("technical_requirements", {}).get("affected_components", []))}個
- **Breaking Changes リスク**: {self.requirements_result.get("codebase_impact", {}).get("breaking_changes_risk", "")}
- **必要な技術**: {', '.join(self.requirements_result.get("technical_requirements", {}).get("required_technologies", []))}

## リスク評価
- **技術リスク**: {len(self.requirements_result.get("risk_assessment", {}).get("technical_risks", []))}件
- **実装リスク**: {len(self.requirements_result.get("risk_assessment", {}).get("implementation_risks", []))}件
"""
        return analysis_report

    def _generate_strategy_report(self) -> str:
        """実装戦略レポート生成"""
        print("🎯 戦略レポート生成中...")

        strategy_report = f"""
# 🎯 実装戦略レポート

## Sequential Thinking戦略分析
- **実現可能性**: {self.strategic_plan.get("strategic_analysis", {}).get("feasibility_assessment", "")}
- **アーキテクチャ影響**: {self.strategic_plan.get("strategic_analysis", {}).get("architecture_impact", "")}
- **推奨アプローチ**: {self.strategic_plan.get("strategic_analysis", {}).get("recommended_approach", "")}

## 技術戦略
- **実装アプローチ**: {self.strategic_plan.get("technical_strategy", {}).get("implementation_approach", "")}
- **アーキテクチャ決定**: {len(self.strategic_plan.get("technical_strategy", {}).get("architecture_decisions", []))}項目
- **品質基準**: {len(self.strategic_plan.get("technical_strategy", {}).get("quality_standards", []))}項目

## 実装計画
- **フェーズ数**: {len(self.strategic_plan.get("implementation_plan", {}).get("phases", []))}
- **予想期間**: {self.strategic_plan.get("implementation_plan", {}).get("timeline_estimate", "")}
- **マイルストーン**: {len(self.strategic_plan.get("implementation_plan", {}).get("milestones", []))}個

## 品質保証計画
- **テスト要件**: {len(self.strategic_plan.get("quality_assurance", {}).get("testing_requirements", []))}項目
- **レビュープロセス**: {len(self.strategic_plan.get("quality_assurance", {}).get("review_process", []))}ステップ
"""
        return strategy_report

    def _generate_technical_report(self) -> str:
        """技術決定レポート生成"""
        print("🔧 技術レポート生成中...")

        phases = self.strategic_plan.get("implementation_plan", {}).get("phases", [])
        phases_text = "\\n".join([f"- {phase}" for phase in phases])

        technical_report = f"""
# 🔧 技術決定レポート

## 長期的ビジョン
- **アーキテクチャ進化**: {self.strategic_plan.get("long_term_vision", {}).get("architectural_evolution", "")}
- **保守性目標**: {len(self.strategic_plan.get("long_term_vision", {}).get("maintainability_goals", []))}項目
- **拡張性考慮**: {len(self.strategic_plan.get("long_term_vision", {}).get("scalability_considerations", []))}項目

## 段階的実装計画
{phases_text}

## 技術決定の根拠
1. **BOC-95の教訓**: 場当たり的修正を避け、体系的アプローチを採用
2. **長期的発展重視**: 即座の解決よりも持続可能な解決策を優先
3. **アーキテクチャ整合性**: 既存システムとの調和を重視
4. **品質保証**: 包括的テストとレビューによる品質確保

## 次回セッション継続性
- 実装前に必要なAIレビューの完了
- 段階的実装による影響範囲の制限
- 継続的な品質チェックとドキュメント更新
"""
        return technical_report

    def _create_comprehensive_report(
        self, analysis_report: str, strategy_report: str, technical_report: str
    ) -> Dict:
        """統合レポート作成"""
        print("📋 統合レポート作成中...")

        # Linear用統合レポート
        linear_report = f"""
# 🤖 AI協業ワークフロー分析レポート - BOC-95システム

{analysis_report}

{strategy_report}

{technical_report}

---

## 📊 ワークフロー実行サマリー
- **実行日時**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **分析フェーズ**: 4段階完了 (Issue Discovery → Project Analysis → Requirements Analysis → Strategic Planning)
- **Sequential Thinking**: MCP統合による長期的戦略立案完了
- **次のステップ**: AIレビュー待ち → 技術的合理性判定 → 実装開始

**生成システム**: ai-assistant-knowledge-hub/workflows (BOC-95ベース)
"""

        comprehensive_report = {
            "linear_report": linear_report,
            "analysis_section": analysis_report,
            "strategy_section": strategy_report,
            "technical_section": technical_report,
            "timestamp": datetime.now().isoformat(),
            "workflow_status": "Phase 5 - Report Generation Complete",
        }

        # レポートファイル保存
        self._save_comprehensive_report(comprehensive_report)

        return comprehensive_report

    def _save_comprehensive_report(self, report: Dict):
        """包括的レポート保存"""
        self.temp_dir.mkdir(exist_ok=True)

        report_file = self.temp_dir / f"phase5_report_{self.project_path.name}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "phase": "5-report-generation",
                    "timestamp": report["timestamp"],
                    "project_name": self.project_path.name,
                    "issue_id": self.issue_data.get("id") if self.issue_data else None,
                    "comprehensive_report": report,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 包括レポート保存: {report_file}")

    def _update_linear_issue(self, report: Dict):
        """Linear Issue更新"""
        print("🔄 Linear Issue更新中...")

        if not self.issue_data or not self.issue_data.get("id"):
            print("⚠️  Issue IDが見つかりません")
            return

        issue_id = self.issue_data["id"]
        linear_report = report["linear_report"]

        # GraphQL mutation
        graphql_mutation = {
            "query": f'mutation {{ issueUpdate(id: "{issue_id}", input: {{ description: "{linear_report.replace('"', '\\"').replace('\n', '\\n')}" }}) {{ success }} }}'
        }

        curl_command = [
            "curl",
            "-X",
            "POST",
            "https://api.linear.app/graphql",
            "-H",
            f"Authorization: {self.linear_api_key}",
            "-H",
            "Content-Type: application/json",
            "-d",
            json.dumps(graphql_mutation),
        ]

        try:
            result = subprocess.run(
                curl_command, capture_output=True, text=True, check=True
            )
            response_data = json.loads(result.stdout)

            if response_data.get("data", {}).get("issueUpdate", {}).get("success"):
                print(f"✅ Linear Issue更新成功: {issue_id}")
            else:
                print(f"⚠️  Linear Issue更新失敗: {response_data}")

        except Exception as e:
            print(f"❌ Linear API呼び出しエラー: {e}")

    def _request_ai_review(self, report: Dict):
        """AIレビュー要求送信"""
        print("📤 AIレビュー要求準備中...")

        # AIレビュー要求データ作成
        review_request = {
            "project_name": self.project_path.name,
            "issue_id": self.issue_data.get("id") if self.issue_data else None,
            "issue_title": self.issue_data.get("title", "") if self.issue_data else "",
            "strategic_plan": self.strategic_plan,
            "analysis_summary": {
                "feasibility": self.strategic_plan.get("strategic_analysis", {}).get(
                    "feasibility_assessment", ""
                ),
                "approach": self.strategic_plan.get("strategic_analysis", {}).get(
                    "recommended_approach", ""
                ),
                "risks": len(
                    self.requirements_result.get("risk_assessment", {}).get(
                        "technical_risks", []
                    )
                ),
                "timeline": self.strategic_plan.get("implementation_plan", {}).get(
                    "timeline_estimate", ""
                ),
            },
            "review_focus": [
                "技術的合理性の検証",
                "長期的アーキテクチャへの影響評価",
                "実装リスクの妥当性確認",
                "代替アプローチの提案",
            ],
            "timestamp": datetime.now().isoformat(),
        }

        # レビュー要求ファイル保存
        review_file = self.temp_dir / f"ai_review_request_{self.project_path.name}.json"
        with open(review_file, "w", encoding="utf-8") as f:
            json.dump(review_request, f, ensure_ascii=False, indent=2)

        print(f"📋 AIレビュー要求準備完了: {review_file}")
        print(
            "💡 レビュー実行: python phase6-review-engine.py でAIレビューを実行してください"
        )


def main():
    """メイン実行関数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    try:
        # Report Generation Engine初期化
        report_engine = ReportGenerationEngine(project_path)

        # 包括的レポート生成
        comprehensive_report = report_engine.generate_comprehensive_report()

        print(f"🎯 Phase 5 完了: レポート生成・Linear更新・AIレビュー要求完了")
        print(
            f"💡 次のコマンド: python {report_engine.ai_hub_dir}/workflows/phase6-review-engine.py"
        )

    except Exception as e:
        print(f"❌ Phase 5 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
