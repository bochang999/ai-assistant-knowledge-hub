#!/usr/bin/env python3
"""
Phase 6: AI Review & Decision Engine
BOC-95に基づく段階的問題解決ワークフローシステム

目的: 他AI（Gemini等）からのレビュー受信、技術的合理性判定、代替案生成
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time


class ReviewDecisionEngine:
    def __init__(self, project_path: str = None):
        """Review Decision Engine初期化"""
        self.project_path = Path(project_path or os.getcwd())
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.temp_dir = self.ai_hub_dir / "temp"
        self.home_dir = Path("/data/data/com.termux/files/home")

        # レビュー要求データ読み込み
        self.review_request = self._load_review_request()
        self.strategic_plan = self._load_strategic_plan()

        # レビュー結果
        self.review_result = {
            "review_responses": [],
            "technical_rationality_assessment": {},
            "decision": "",
            "alternative_proposals": [],
            "next_actions": [],
        }

    def _load_review_request(self) -> Optional[Dict]:
        """AIレビュー要求データ読み込み"""
        try:
            review_files = list(self.temp_dir.glob("ai_review_request_*.json"))
            if review_files:
                latest_review_file = max(review_files, key=lambda f: f.stat().st_mtime)
                with open(latest_review_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  レビュー要求データ読み込みエラー: {e}")
        return None

    def _load_strategic_plan(self) -> Optional[Dict]:
        """戦略計画データ読み込み"""
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

    def execute_review_cycle(self) -> Dict:
        """AIレビューサイクル実行"""
        print(f"🔍 AIレビューサイクル開始")

        if not self.review_request:
            raise Exception("❌ レビュー要求データが見つかりません")

        # 1. AIレビュー実行
        review_responses = self._execute_ai_reviews()

        # 2. 技術的合理性判定
        rationality_assessment = self._assess_technical_rationality(review_responses)

        # 3. 決定エンジン実行
        decision = self._make_implementation_decision(rationality_assessment)

        # 4. 代替案生成（必要に応じて）
        if decision == "ALTERNATIVE_REQUIRED":
            alternatives = self._generate_alternative_proposals(review_responses)
        else:
            alternatives = []

        # 5. 次のアクション決定
        next_actions = self._determine_next_actions(decision, alternatives)

        # 6. レビュー結果保存
        self.review_result = {
            "review_responses": review_responses,
            "technical_rationality_assessment": rationality_assessment,
            "decision": decision,
            "alternative_proposals": alternatives,
            "next_actions": next_actions,
        }

        self._save_review_result()

        print(f"✅ AIレビューサイクル完了: {decision}")
        return self.review_result

    def _execute_ai_reviews(self) -> List[Dict]:
        """AIレビュー実行"""
        print("🤖 AIレビュー実行中...")

        review_responses = []

        # Gemini APIレビュー（シミュレーション）
        gemini_review = self._simulate_gemini_review()
        review_responses.append(
            {
                "reviewer": "Gemini",
                "timestamp": datetime.now().isoformat(),
                "response": gemini_review,
            }
        )

        # Claude Second Opinion（シミュレーション）
        claude_review = self._simulate_claude_second_opinion()
        review_responses.append(
            {
                "reviewer": "Claude_Secondary",
                "timestamp": datetime.now().isoformat(),
                "response": claude_review,
            }
        )

        print(f"📊 AIレビュー完了: {len(review_responses)}件のレビュー受信")
        return review_responses

    def _simulate_gemini_review(self) -> Dict:
        """Gemini レビューシミュレーション"""
        # 実際の実装では、Gemini APIを呼び出す
        strategic_approach = self.strategic_plan.get("strategic_analysis", {}).get(
            "recommended_approach", ""
        )
        feasibility = self.strategic_plan.get("strategic_analysis", {}).get(
            "feasibility_assessment", ""
        )

        # アプローチに基づく評価
        if "段階的" in strategic_approach:
            technical_rating = "High"
            rationale = "段階的実装アプローチは技術的リスクを効果的に軽減し、長期的保守性を向上させる"
        elif "最小限" in strategic_approach:
            technical_rating = "Medium-High"
            rationale = "最小限修正は影響範囲を制限するが、根本的解決に不足の可能性"
        else:
            technical_rating = "Medium"
            rationale = "包括的アプローチは効果的だが、実装コストとリスクが高い"

        return {
            "technical_rationality": technical_rating,
            "architectural_alignment": "Good",
            "long_term_impact": "Positive",
            "risk_assessment": "Acceptable",
            "recommendations": [
                "提案された段階的アプローチを支持",
                "テスト戦略の強化を推奨",
                "パフォーマンス監視の追加を提案",
            ],
            "concerns": [
                "複雑なプロジェクトでの予期しない副作用",
                "実装期間中のチーム負荷",
            ],
            "overall_verdict": "APPROVE_WITH_CONDITIONS",
            "rationale": rationale,
        }

    def _simulate_claude_second_opinion(self) -> Dict:
        """Claude Second Opinion シミュレーション"""
        # 実際の実装では、別のClaude instanceまたはGPT-4を呼び出す
        complexity = (
            self.strategic_plan.get("context_summary", {})
            .get("project_overview", {})
            .get("complexity", "")
        )
        issue_type = (
            self.strategic_plan.get("context_summary", {})
            .get("issue_context", {})
            .get("type", "")
        )

        if complexity == "Complex" and issue_type == "Feature Request":
            verdict = "ALTERNATIVE_RECOMMENDED"
            concerns = [
                "複雑なシステムでの新機能追加は慎重さが必要",
                "既存アーキテクチャへの影響をより詳細に評価すべき",
            ]
        else:
            verdict = "APPROVE"
            concerns = ["実装中の品質チェックポイントの明確化が必要"]

        return {
            "technical_rationality": "High",
            "architectural_alignment": "Very Good",
            "long_term_impact": "Very Positive",
            "risk_assessment": "Low-Medium",
            "recommendations": [
                "BOC-95の教訓を活かした体系的アプローチを評価",
                "Sequential Thinking統合による戦略立案を支持",
                "継続的な品質保証の重要性を強調",
            ],
            "concerns": concerns,
            "overall_verdict": verdict,
            "rationale": "提案された戦略は長期的発展を重視し、技術的合理性が高い",
        }

    def _assess_technical_rationality(self, review_responses: List[Dict]) -> Dict:
        """技術的合理性判定"""
        print("⚖️  技術的合理性判定中...")

        assessment = {
            "overall_score": 0,
            "consensus_level": "",
            "key_strengths": [],
            "key_concerns": [],
            "recommendation_summary": [],
        }

        # レビュー結果の集計
        technical_scores = []
        verdicts = []
        all_recommendations = []
        all_concerns = []

        for response in review_responses:
            review_data = response["response"]

            # 技術的合理性スコア変換
            tech_rating = review_data.get("technical_rationality", "")
            if tech_rating == "High":
                technical_scores.append(4)
            elif tech_rating == "Medium-High":
                technical_scores.append(3)
            elif tech_rating == "Medium":
                technical_scores.append(2)
            else:
                technical_scores.append(1)

            verdicts.append(review_data.get("overall_verdict", ""))
            all_recommendations.extend(review_data.get("recommendations", []))
            all_concerns.extend(review_data.get("concerns", []))

        # 総合スコア計算
        assessment["overall_score"] = (
            sum(technical_scores) / len(technical_scores) if technical_scores else 0
        )

        # コンセンサスレベル判定
        approve_count = sum(1 for v in verdicts if "APPROVE" in v)
        if approve_count == len(verdicts):
            assessment["consensus_level"] = "Strong Consensus"
        elif approve_count > len(verdicts) / 2:
            assessment["consensus_level"] = "Majority Approval"
        else:
            assessment["consensus_level"] = "Mixed Views"

        # 主要な強みと懸念事項
        assessment["key_strengths"] = list(set(all_recommendations))[:5]
        assessment["key_concerns"] = list(set(all_concerns))[:3]

        print(
            f"📊 技術的合理性: スコア {assessment['overall_score']:.1f}/4.0, {assessment['consensus_level']}"
        )
        return assessment

    def _make_implementation_decision(self, assessment: Dict) -> str:
        """実装決定エンジン"""
        print("🎯 実装決定判定中...")

        score = assessment["overall_score"]
        consensus = assessment["consensus_level"]

        # 決定ルール
        if score >= 3.5 and consensus == "Strong Consensus":
            decision = "PROCEED_AS_PLANNED"
        elif score >= 3.0 and consensus in ["Strong Consensus", "Majority Approval"]:
            decision = "PROCEED_WITH_MODIFICATIONS"
        elif score >= 2.5:
            decision = "ALTERNATIVE_REQUIRED"
        else:
            decision = "REJECT_AND_REEVALUATE"

        print(f"⚖️  実装決定: {decision}")
        return decision

    def _generate_alternative_proposals(
        self, review_responses: List[Dict]
    ) -> List[Dict]:
        """代替案生成"""
        print("💡 代替案生成中...")

        alternatives = []

        # レビューで指摘された懸念事項から代替案を生成
        all_concerns = []
        for response in review_responses:
            all_concerns.extend(response["response"].get("concerns", []))

        # 代替案1: リスク軽減重視アプローチ
        if any("リスク" in concern or "副作用" in concern for concern in all_concerns):
            alternatives.append(
                {
                    "title": "リスク軽減重視の段階的アプローチ",
                    "description": "より小さな単位での段階的実装により、リスクを最小化",
                    "modifications": [
                        "実装フェーズをより細分化",
                        "各フェーズでの包括的テスト実施",
                        "フェーズ間でのレビューポイント追加",
                    ],
                    "benefits": ["リスク軽減", "品質向上", "早期問題発見"],
                    "drawbacks": ["実装期間の延長", "オーバーヘッドの増加"],
                }
            )

        # 代替案2: 既存機能拡張アプローチ
        if any("新機能" in concern or "複雑" in concern for concern in all_concerns):
            alternatives.append(
                {
                    "title": "既存機能拡張による段階的実現",
                    "description": "新規実装ではなく既存機能の拡張により要件を満たす",
                    "modifications": [
                        "既存コンポーネントの拡張を優先",
                        "新規コンポーネントは最小限に制限",
                        "既存パターンとの一貫性を重視",
                    ],
                    "benefits": [
                        "アーキテクチャ整合性",
                        "実装コスト削減",
                        "保守性向上",
                    ],
                    "drawbacks": ["機能制限の可能性", "技術負債の蓄積リスク"],
                }
            )

        print(f"💭 代替案生成完了: {len(alternatives)}案")
        return alternatives

    def _determine_next_actions(
        self, decision: str, alternatives: List[Dict]
    ) -> List[str]:
        """次のアクション決定"""
        print("📋 次のアクション決定中...")

        if decision == "PROCEED_AS_PLANNED":
            next_actions = [
                "Phase 7: Implementation Execution開始",
                "実装前の最終チェック実施",
                "開発環境準備",
                "実装開始",
            ]
        elif decision == "PROCEED_WITH_MODIFICATIONS":
            next_actions = [
                "レビューフィードバックに基づく戦略修正",
                "修正版実装計画の作成",
                "stakeholder確認",
                "Phase 7: Implementation Execution開始",
            ]
        elif decision == "ALTERNATIVE_REQUIRED":
            next_actions = [
                "代替案のLinear Issue追記",
                "追加AIレビューサイクル実行",
                "stakeholderとの代替案検討",
                "最終決定後のPhase 7開始",
            ]
        else:  # REJECT_AND_REEVALUATE
            next_actions = [
                "根本的な要件再評価",
                "Phase 3からの再実行検討",
                "issue scope見直し",
                "新たなアプローチ検討",
            ]

        print(f"📝 次のアクション: {len(next_actions)}項目")
        return next_actions

    def _save_review_result(self):
        """レビュー結果保存"""
        self.temp_dir.mkdir(exist_ok=True)

        review_file = self.temp_dir / f"phase6_review_{self.project_path.name}.json"
        with open(review_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "phase": "6-review-engine",
                    "timestamp": datetime.now().isoformat(),
                    "project_name": self.project_path.name,
                    "issue_id": (
                        self.review_request.get("issue_id")
                        if self.review_request
                        else None
                    ),
                    "review_result": self.review_result,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 レビュー結果保存: {review_file}")


def main():
    """メイン実行関数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    try:
        # Review Decision Engine初期化
        review_engine = ReviewDecisionEngine(project_path)

        # AIレビューサイクル実行
        review_result = review_engine.execute_review_cycle()

        decision = review_result["decision"]
        next_actions = review_result["next_actions"]

        print(f"🎯 Phase 6 完了: {decision}")
        print("📋 次のアクション:")
        for action in next_actions:
            print(f"  - {action}")

        if decision in ["PROCEED_AS_PLANNED", "PROCEED_WITH_MODIFICATIONS"]:
            print(
                f"💡 次のコマンド: python {review_engine.ai_hub_dir}/workflows/phase7-implementation.py"
            )
        else:
            print("💡 代替案検討またはPhase再実行が必要です")

    except Exception as e:
        print(f"❌ Phase 6 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
