#!/usr/bin/env python3
"""
Phase 8: Documentation & Continuity
BOC-95に基づく段階的問題解決ワークフローシステム

目的: GitHub自動コミット・プッシュ、詳細作業報告書の自動生成、次回セッション用コンテキスト保存
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DocumentationContinuityEngine:
    def __init__(self, project_path: str = None):
        """Documentation Continuity Engine初期化"""
        self.project_path = Path(project_path or os.getcwd())
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.temp_dir = self.ai_hub_dir / "temp"
        self.home_dir = Path("/data/data/com.termux/files/home")

        # 全Phaseのデータを統合読み込み
        self.workflow_data = self._load_all_workflow_data()

        # Linear API設定
        self.linear_api_key = self._get_linear_api_key()

        # 最終報告書
        self.final_report = {
            "workflow_summary": {},
            "technical_decisions": {},
            "implementation_results": {},
            "continuity_context": {},
            "next_session_guide": {},
        }

    def _load_all_workflow_data(self) -> Dict:
        """全ワークフローデータ統合読み込み"""
        workflow_data = {}

        # Phase 1: Issue Discovery
        try:
            issue_files = list(self.temp_dir.glob("agent_issue_*.json"))
            if issue_files:
                latest_issue_file = max(issue_files, key=lambda f: f.stat().st_mtime)
                with open(latest_issue_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    workflow_data["phase1_issue"] = data
        except Exception as e:
            print(f"⚠️  Phase 1データ読み込みエラー: {e}")

        # Phase 2: Project Analysis
        try:
            analysis_files = list(self.temp_dir.glob("phase2_analysis_*.json"))
            if analysis_files:
                latest_analysis_file = max(
                    analysis_files, key=lambda f: f.stat().st_mtime
                )
                with open(latest_analysis_file, "r", encoding="utf-8") as f:
                    workflow_data["phase2_analysis"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 2データ読み込みエラー: {e}")

        # Phase 3: Requirements Analysis
        try:
            req_files = list(self.temp_dir.glob("phase3_requirements_*.json"))
            if req_files:
                latest_req_file = max(req_files, key=lambda f: f.stat().st_mtime)
                with open(latest_req_file, "r", encoding="utf-8") as f:
                    workflow_data["phase3_requirements"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 3データ読み込みエラー: {e}")

        # Phase 4: Strategic Planning
        try:
            strategy_files = list(self.temp_dir.glob("phase4_strategy_*.json"))
            if strategy_files:
                latest_strategy_file = max(
                    strategy_files, key=lambda f: f.stat().st_mtime
                )
                with open(latest_strategy_file, "r", encoding="utf-8") as f:
                    workflow_data["phase4_strategy"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 4データ読み込みエラー: {e}")

        # Phase 5: Report Generation
        try:
            report_files = list(self.temp_dir.glob("phase5_report_*.json"))
            if report_files:
                latest_report_file = max(report_files, key=lambda f: f.stat().st_mtime)
                with open(latest_report_file, "r", encoding="utf-8") as f:
                    workflow_data["phase5_report"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 5データ読み込みエラー: {e}")

        # Phase 6: Review Engine
        try:
            review_files = list(self.temp_dir.glob("phase6_review_*.json"))
            if review_files:
                latest_review_file = max(review_files, key=lambda f: f.stat().st_mtime)
                with open(latest_review_file, "r", encoding="utf-8") as f:
                    workflow_data["phase6_review"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 6データ読み込みエラー: {e}")

        # Phase 7: Implementation
        try:
            impl_files = list(self.temp_dir.glob("phase7_implementation_*.json"))
            if impl_files:
                latest_impl_file = max(impl_files, key=lambda f: f.stat().st_mtime)
                with open(latest_impl_file, "r", encoding="utf-8") as f:
                    workflow_data["phase7_implementation"] = json.load(f)
        except Exception as e:
            print(f"⚠️  Phase 7データ読み込みエラー: {e}")

        return workflow_data

    def _get_linear_api_key(self) -> str:
        """Linear API Key取得"""
        try:
            with open(self.home_dir / ".linear-api-key", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            print("⚠️  Linear API Keyが見つかりません（継続性レポートのみ生成）")
            return ""

    def finalize_workflow_session(self) -> Dict:
        """ワークフローセッション完了処理"""
        print(f"📋 ワークフローセッション完了処理開始")

        # 1. 包括的レポート生成
        self._generate_comprehensive_final_report()

        # 2. GitHub自動コミット・プッシュ
        self._auto_commit_and_push()

        # 3. Linear最終更新
        self._update_linear_final_status()

        # 4. 次回セッション用コンテキスト生成
        self._generate_next_session_context()

        # 5. 最終報告書保存
        self._save_final_report()

        print("✅ ワークフローセッション完了処理完了")
        return self.final_report

    def _generate_comprehensive_final_report(self):
        """包括的最終報告書生成"""
        print("📝 包括的最終報告書生成中...")

        # ワークフローサマリー
        workflow_summary = self._create_workflow_summary()
        self.final_report["workflow_summary"] = workflow_summary

        # 技術決定サマリー
        technical_decisions = self._create_technical_decisions_summary()
        self.final_report["technical_decisions"] = technical_decisions

        # 実装結果サマリー
        implementation_results = self._create_implementation_results_summary()
        self.final_report["implementation_results"] = implementation_results

        # 継続性コンテキスト
        continuity_context = self._create_continuity_context()
        self.final_report["continuity_context"] = continuity_context

        # 次回セッションガイド
        next_session_guide = self._create_next_session_guide()
        self.final_report["next_session_guide"] = next_session_guide

        print("📊 包括的最終報告書生成完了")

    def _create_workflow_summary(self) -> Dict:
        """ワークフローサマリー作成"""
        summary = {
            "execution_timeline": {},
            "phases_completed": [],
            "overall_success_rate": 0,
            "key_achievements": [],
            "lessons_learned": [],
        }

        # 実行タイムライン
        summary["execution_timeline"] = {
            "start_time": self._get_earliest_timestamp(),
            "end_time": datetime.now().isoformat(),
            "total_duration_hours": self._calculate_total_duration(),
            "phases_executed": len(
                [k for k in self.workflow_data.keys() if "phase" in k]
            ),
        }

        # 完了フェーズ
        for phase_key in self.workflow_data.keys():
            if "phase" in phase_key:
                phase_num = phase_key.split("_")[0]
                phase_name = phase_key.split("_")[1] if "_" in phase_key else "unknown"
                summary["phases_completed"].append(
                    {"phase": phase_num, "name": phase_name, "status": "completed"}
                )

        # 成功率計算
        total_phases = 8
        completed_phases = len(summary["phases_completed"])
        summary["overall_success_rate"] = (completed_phases / total_phases) * 100

        # 主要成果
        if self.workflow_data.get("phase7_implementation"):
            impl_data = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]
            summary["key_achievements"] = [
                f"実装進捗: {impl_data.get('progress_percentage', 0)}%",
                f"品質スコア: {self._get_average_quality_score()}",
                "AI協業ワークフロー体系化完了",
                "長期的アーキテクチャ戦略策定",
            ]

        # 教訓
        summary["lessons_learned"] = [
            "Sequential Thinking MCPによる戦略立案の有効性",
            "段階的実装アプローチによるリスク軽減",
            "AI多段階レビューによる技術的合理性向上",
            "BOC-95の経験を活かした体系的問題解決",
        ]

        return summary

    def _create_technical_decisions_summary(self) -> Dict:
        """技術決定サマリー作成"""
        decisions = {
            "architecture_decisions": [],
            "technology_choices": [],
            "implementation_strategies": [],
            "quality_standards": [],
        }

        # 戦略データから技術決定を抽出
        if self.workflow_data.get("phase4_strategy"):
            strategy_data = self.workflow_data["phase4_strategy"]["strategic_plan"]

            # アーキテクチャ決定
            arch_decisions = strategy_data.get("technical_strategy", {}).get(
                "architecture_decisions", []
            )
            decisions["architecture_decisions"] = arch_decisions

            # 技術選択
            tech_choices = strategy_data.get("technical_strategy", {}).get(
                "technology_choices", []
            )
            decisions["technology_choices"] = tech_choices

            # 実装戦略
            impl_approach = strategy_data.get("technical_strategy", {}).get(
                "implementation_approach", ""
            )
            decisions["implementation_strategies"] = [impl_approach]

            # 品質基準
            quality_standards = strategy_data.get("technical_strategy", {}).get(
                "quality_standards", []
            )
            decisions["quality_standards"] = quality_standards

        return decisions

    def _create_implementation_results_summary(self) -> Dict:
        """実装結果サマリー作成"""
        results = {
            "completion_status": "",
            "quality_metrics": {},
            "performance_indicators": {},
            "issues_resolved": [],
            "remaining_tasks": [],
        }

        if self.workflow_data.get("phase7_implementation"):
            impl_data = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]

            # 完了状況
            progress = impl_data.get("progress_percentage", 0)
            if progress == 100:
                results["completion_status"] = "Fully Completed"
            elif progress >= 75:
                results["completion_status"] = "Nearly Completed"
            else:
                results["completion_status"] = "Partially Completed"

            # 品質メトリクス
            results["quality_metrics"] = impl_data.get("quality_metrics", {})

            # パフォーマンス指標
            results["performance_indicators"] = {
                "phases_completed": len(impl_data.get("completed_phases", [])),
                "total_progress": f"{progress}%",
                "quality_score": self._get_average_quality_score(),
            }

            # 解決された問題
            if self.workflow_data.get("phase1_issue"):
                issue_title = self.workflow_data["phase1_issue"]["issue_data"]["title"]
                results["issues_resolved"] = [issue_title]

            # 残タスク
            results["remaining_tasks"] = impl_data.get("next_steps", [])

        return results

    def _create_continuity_context(self) -> Dict:
        """継続性コンテキスト作成"""
        context = {
            "project_state": {},
            "ongoing_initiatives": [],
            "technical_context": {},
            "knowledge_artifacts": [],
        }

        # プロジェクト状態
        if self.workflow_data.get("phase2_analysis"):
            project_data = self.workflow_data["phase2_analysis"]["analysis_result"]
            context["project_state"] = {
                "project_name": project_data.get("project_purpose", {}).get("name", ""),
                "complexity_level": project_data.get("architecture_patterns", {}).get(
                    "complexity_level", ""
                ),
                "tech_stack": project_data.get("tech_stack", {}),
                "last_analysis": self.workflow_data["phase2_analysis"]["timestamp"],
            }

        # 進行中の取り組み
        if self.workflow_data.get("phase7_implementation"):
            impl_data = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]
            context["ongoing_initiatives"] = impl_data.get("next_steps", [])

        # 技術コンテキスト
        if self.workflow_data.get("phase4_strategy"):
            strategy_data = self.workflow_data["phase4_strategy"]["strategic_plan"]
            context["technical_context"] = {
                "strategic_approach": strategy_data.get("strategic_analysis", {}).get(
                    "recommended_approach", ""
                ),
                "long_term_vision": strategy_data.get("long_term_vision", {}),
                "implementation_plan": strategy_data.get("implementation_plan", {}),
            }

        # 知識アーティファクト
        context["knowledge_artifacts"] = [
            f"{self.temp_dir}/phase*_*.json - ワークフロー実行データ",
            f"{self.project_path}/README.md - プロジェクト概要",
            f"{self.project_path}/CLAUDE.md - AI協業ルール",
            "Linear Issue - 完了した分析・戦略レポート",
        ]

        return context

    def _create_next_session_guide(self) -> Dict:
        """次回セッションガイド作成"""
        guide = {
            "immediate_actions": [],
            "context_restoration": [],
            "continuation_commands": [],
            "key_files_to_review": [],
            "potential_next_steps": [],
        }

        # 即座のアクション
        if self.workflow_data.get("phase7_implementation"):
            impl_data = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]
            progress = impl_data.get("progress_percentage", 0)

            if progress < 100:
                guide["immediate_actions"] = [
                    "実装の継続",
                    "残りフェーズの実行",
                    "品質チェックの完了",
                ]
            else:
                guide["immediate_actions"] = [
                    "最終テストの実行",
                    "デプロイ準備",
                    "プロジェクト完了確認",
                ]

        # コンテキスト復元
        guide["context_restoration"] = [
            f"cd {self.project_path}",
            f"cat {self.temp_dir}/phase8_final_*.json | jq '.final_report.workflow_summary'",
            "Linear Issue確認 - 最新の戦略・実装レポート",
            "git log --oneline -10 で最近のコミット確認",
        ]

        # 継続コマンド
        if self.workflow_data.get("phase7_implementation"):
            impl_data = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]
            progress = impl_data.get("progress_percentage", 0)

            if progress < 100:
                guide["continuation_commands"] = [
                    f"python {self.ai_hub_dir}/workflows/phase7-implementation.py {self.project_path}",
                    "進捗確認とフェーズ継続",
                ]
            else:
                guide["continuation_commands"] = [
                    "最終デプロイとテスト",
                    "プロジェクト完了報告",
                ]

        # 重要ファイル
        guide["key_files_to_review"] = [
            f"{self.temp_dir}/phase4_strategy_*.json - 戦略計画",
            f"{self.temp_dir}/phase6_review_*.json - AIレビュー結果",
            f"{self.temp_dir}/phase7_implementation_*.json - 実装状況",
            f"{self.project_path}/CLAUDE.md - 開発ルール",
        ]

        # 次のステップ候補
        guide["potential_next_steps"] = [
            "新しいIssueでのワークフロー再実行",
            "ワークフローシステム自体の改善",
            "他プロジェクトへのワークフロー適用",
            "AI協業パターンの更なる最適化",
        ]

        return guide

    def _auto_commit_and_push(self):
        """GitHub自動コミット・プッシュ"""
        print("📤 GitHub自動コミット・プッシュ実行中...")

        try:
            # Git status確認
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True,
            )

            if result.stdout.strip():
                # 変更がある場合のみコミット
                # Add all changes
                subprocess.run(["git", "add", "."], cwd=self.project_path, check=True)

                # Commit message生成
                commit_message = self._generate_commit_message()

                # Commit
                subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    cwd=self.project_path,
                    check=True,
                )

                # Push (optional - リモートが設定されている場合)
                try:
                    subprocess.run(["git", "push"], cwd=self.project_path, check=True)
                    print("✅ GitHub Push成功")
                except subprocess.CalledProcessError:
                    print(
                        "⚠️  GitHub Push失敗（リモートリポジトリ未設定またはネットワークエラー）"
                    )

                print("✅ Git commit完了")
            else:
                print("ℹ️  コミットする変更がありません")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git操作エラー: {e}")

    def _generate_commit_message(self) -> str:
        """コミットメッセージ生成"""
        if self.workflow_data.get("phase1_issue"):
            issue_title = self.workflow_data["phase1_issue"]["issue_data"]["title"]
            issue_id = self.workflow_data["phase1_issue"]["issue_data"]["id"]

            # 実装進捗に基づくメッセージ
            if self.workflow_data.get("phase7_implementation"):
                impl_data = self.workflow_data["phase7_implementation"][
                    "implementation_status"
                ]
                progress = impl_data.get("progress_percentage", 0)

                if progress == 100:
                    status = "完了"
                elif progress >= 75:
                    status = "ほぼ完了"
                else:
                    status = f"{progress}%完了"

                return f"""🤖 AI協業ワークフロー {status}: {issue_title}

Phase 1-8: BOC-95ベース段階的問題解決完了
- Issue Discovery → Project Analysis → Requirements Analysis
- Sequential Thinking MCP戦略立案 → AIレビュー → 実装
- 進捗: {progress}%
- 品質スコア: {self._get_average_quality_score()}

🤖 Generated with [Claude Code](https://claude.ai/code)
AI Workflow System: ai-assistant-knowledge-hub

Co-Authored-By: Claude <noreply@anthropic.com>"""

        return """🤖 AI協業ワークフロー実行完了

BOC-95ベース段階的問題解決システムによる実装

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

    def _update_linear_final_status(self):
        """Linear最終状況更新"""
        print("🔄 Linear最終状況更新中...")

        if not self.linear_api_key or not self.workflow_data.get("phase1_issue"):
            print("⚠️  Linear更新スキップ（API KeyまたはIssue情報なし）")
            return

        try:
            issue_id = self.workflow_data["phase1_issue"]["issue_data"]["id"]

            # 最終レポート作成
            final_report_text = self._create_linear_final_report()

            # Linear Issue更新
            graphql_mutation = {
                "query": f'mutation {{ issueUpdate(id: "{issue_id}", input: {{ description: "{final_report_text.replace('"', '\\"').replace('\n', '\\n')}" }}) {{ success }} }}'
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

            result = subprocess.run(
                curl_command, capture_output=True, text=True, check=True
            )
            response_data = json.loads(result.stdout)

            if response_data.get("data", {}).get("issueUpdate", {}).get("success"):
                print(f"✅ Linear最終更新成功: {issue_id}")

                # ステータスを"In Review"に変更
                in_review_id = "33feb1c9-3276-4e13-863a-0b93db032a0f"
                status_mutation = {
                    "query": f'mutation {{ issueUpdate(id: "{issue_id}", input: {{ stateId: "{in_review_id}" }}) {{ success }} }}'
                }

                status_curl = [
                    "curl",
                    "-X",
                    "POST",
                    "https://api.linear.app/graphql",
                    "-H",
                    f"Authorization: {self.linear_api_key}",
                    "-H",
                    "Content-Type: application/json",
                    "-d",
                    json.dumps(status_mutation),
                ]

                subprocess.run(status_curl, capture_output=True, text=True, check=True)
                print("✅ Linear Status: 'In Review'に更新")

            else:
                print(f"⚠️  Linear更新失敗: {response_data}")

        except Exception as e:
            print(f"❌ Linear API呼び出しエラー: {e}")

    def _create_linear_final_report(self) -> str:
        """Linear用最終レポート作成"""
        workflow_summary = self.final_report["workflow_summary"]
        implementation_results = self.final_report["implementation_results"]

        return f"""# 🎯 AI協業ワークフロー最終完了報告

## 実行サマリー
- **実行期間**: {workflow_summary.get("execution_timeline", {}).get("total_duration_hours", "N/A")}時間
- **完了フェーズ**: {len(workflow_summary.get("phases_completed", []))}/8
- **成功率**: {workflow_summary.get("overall_success_rate", 0):.1f}%
- **実装進捗**: {implementation_results.get("performance_indicators", {}).get("total_progress", "N/A")}

## 主要成果
{chr(10).join([f"- {achievement}" for achievement in workflow_summary.get("key_achievements", [])])}

## 品質メトリクス
- **コード品質**: {implementation_results.get("quality_metrics", {}).get("code_quality", {}).get("status", "N/A")}
- **テストカバレッジ**: {implementation_results.get("quality_metrics", {}).get("test_coverage", {}).get("status", "N/A")}
- **パフォーマンス**: {implementation_results.get("quality_metrics", {}).get("performance", {}).get("status", "N/A")}
- **セキュリティ**: {implementation_results.get("quality_metrics", {}).get("security", {}).get("status", "N/A")}

## 技術決定記録
{chr(10).join([f"- {decision}" for decision in self.final_report.get("technical_decisions", {}).get("architecture_decisions", [])])}

## 次回セッション継続性
- **プロジェクト状態**: {self.final_report.get("continuity_context", {}).get("project_state", {}).get("project_name", "")}
- **継続コマンド**: ai-assistant-knowledge-hub/workflows システム利用
- **重要ファイル**: temp/phase8_final_*.json

---

**生成システム**: BOC-95ベースAI協業ワークフローシステム
**完了日時**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status**: ワークフロー実行完了 → 継続性確保完了
"""

    def _generate_next_session_context(self):
        """次回セッション用コンテキスト生成"""
        print("📋 次回セッション用コンテキスト生成中...")

        # 次回セッション用の包括的コンテキストファイル作成
        next_session_context = {
            "session_metadata": {
                "previous_session_end": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "workflow_system": "ai-assistant-knowledge-hub/workflows",
                "last_issue_id": self.workflow_data.get("phase1_issue", {})
                .get("issue_data", {})
                .get("id", ""),
            },
            "project_state_snapshot": self.final_report["continuity_context"][
                "project_state"
            ],
            "last_implementation_status": self.final_report["implementation_results"],
            "next_actions": self.final_report["next_session_guide"][
                "immediate_actions"
            ],
            "restoration_commands": self.final_report["next_session_guide"][
                "context_restoration"
            ],
            "knowledge_artifacts": self.final_report["continuity_context"][
                "knowledge_artifacts"
            ],
        }

        # 次回セッション用ファイル保存
        next_session_file = (
            self.ai_hub_dir / f"next_session_context_{self.project_path.name}.json"
        )
        with open(next_session_file, "w", encoding="utf-8") as f:
            json.dump(next_session_context, f, ensure_ascii=False, indent=2)

        print(f"📝 次回セッションコンテキスト保存: {next_session_file}")

    def _save_final_report(self):
        """最終報告書保存"""
        self.temp_dir.mkdir(exist_ok=True)

        final_file = self.temp_dir / f"phase8_final_{self.project_path.name}.json"
        with open(final_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "phase": "8-documentation-continuity",
                    "timestamp": datetime.now().isoformat(),
                    "project_name": self.project_path.name,
                    "workflow_session_id": f"{self.project_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "final_report": self.final_report,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 最終報告書保存: {final_file}")

    # ヘルパーメソッド
    def _get_earliest_timestamp(self) -> str:
        """最早のタイムスタンプ取得"""
        timestamps = []
        for phase_data in self.workflow_data.values():
            if isinstance(phase_data, dict) and "timestamp" in phase_data:
                timestamps.append(phase_data["timestamp"])
        return min(timestamps) if timestamps else datetime.now().isoformat()

    def _calculate_total_duration(self) -> float:
        """総実行時間計算（時間単位）"""
        try:
            start_time = datetime.fromisoformat(self._get_earliest_timestamp())
            end_time = datetime.now()
            duration = end_time - start_time
            return round(duration.total_seconds() / 3600, 2)
        except:
            return 0.0

    def _get_average_quality_score(self) -> str:
        """平均品質スコア取得"""
        if self.workflow_data.get("phase7_implementation"):
            quality_metrics = self.workflow_data["phase7_implementation"][
                "implementation_status"
            ]["quality_metrics"]
            scores = []

            for category, metrics in quality_metrics.items():
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        if isinstance(value, (int, float)) and key.endswith("_score"):
                            scores.append(value)

            if scores:
                return f"{sum(scores) / len(scores):.1f}"

        return "N/A"


def main():
    """メイン実行関数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    try:
        # Documentation Continuity Engine初期化
        doc_engine = DocumentationContinuityEngine(project_path)

        # ワークフローセッション完了処理
        final_report = doc_engine.finalize_workflow_session()

        success_rate = final_report["workflow_summary"]["overall_success_rate"]
        completion_status = final_report["implementation_results"]["completion_status"]

        print(f"🎯 Phase 8 完了: {success_rate:.1f}% success rate")
        print(f"📊 実装状況: {completion_status}")
        print("📋 次回セッション情報:")
        print(
            f"  - コンテキストファイル: {doc_engine.ai_hub_dir}/next_session_context_{doc_engine.project_path.name}.json"
        )
        print(
            f"  - 最終報告書: {doc_engine.temp_dir}/phase8_final_{doc_engine.project_path.name}.json"
        )

        print("\n🎉 AI協業ワークフローシステム実行完了")
        print(
            "💡 次回セッション開始時は next_session_context_*.json を確認してください"
        )

    except Exception as e:
        print(f"❌ Phase 8 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
