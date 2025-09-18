#!/usr/bin/env python3
"""
Workflow Coordinator - AI協業ワークフローシステム統合制御
BOC-95に基づく段階的問題解決ワークフローシステム

目的: 8つのPhaseを統合管理し、エラーハンドリング、進捗追跡、品質保証を提供
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time


class WorkflowCoordinator:
    def __init__(self, config_path: str = None):
        """Workflow Coordinator初期化"""
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.workflows_dir = self.ai_hub_dir / "workflows"
        self.temp_dir = self.ai_hub_dir / "temp"
        self.lib_dir = self.ai_hub_dir / "lib"

        # 設定読み込み
        self.config = self._load_config(config_path)

        # ワークフロー状態
        self.workflow_state = {
            "session_id": "",
            "current_phase": 0,
            "phases_status": {},
            "errors_encountered": [],
            "quality_gates": {},
            "project_context": {},
        }

        # Phase定義
        self.phases = [
            {
                "number": 1,
                "name": "Issue Intelligence & Project Discovery",
                "script": "phase1-issue-discovery.py",
                "required_inputs": ["issue_id"],
                "outputs": ["issue_data", "project_path"],
                "quality_checks": ["issue_validity", "project_detection"],
            },
            {
                "number": 2,
                "name": "Project Context Analysis",
                "script": "phase2-project-analysis.py",
                "required_inputs": ["project_path"],
                "outputs": ["project_analysis"],
                "quality_checks": ["structure_analysis", "tech_stack_detection"],
            },
            {
                "number": 3,
                "name": "Issue Requirements Analysis",
                "script": "phase3-requirements-analysis.py",
                "required_inputs": ["project_path", "issue_data"],
                "outputs": ["requirements_result"],
                "quality_checks": ["requirements_completeness", "impact_assessment"],
            },
            {
                "number": 4,
                "name": "Strategic Planning (Sequential Thinking MCP)",
                "script": "phase4-strategic-planning.py",
                "required_inputs": ["project_path", "requirements_result"],
                "outputs": ["strategic_plan"],
                "quality_checks": ["strategic_completeness", "mcp_integration"],
            },
            {
                "number": 5,
                "name": "Report Generation & Linear Integration",
                "script": "phase5-report-generation.py",
                "required_inputs": ["strategic_plan"],
                "outputs": ["comprehensive_report"],
                "quality_checks": ["report_quality", "linear_integration"],
            },
            {
                "number": 6,
                "name": "AI Review & Decision Engine",
                "script": "phase6-review-engine.py",
                "required_inputs": ["comprehensive_report"],
                "outputs": ["review_result"],
                "quality_checks": ["review_consensus", "technical_rationality"],
            },
            {
                "number": 7,
                "name": "Implementation Execution",
                "script": "phase7-implementation.py",
                "required_inputs": ["review_result"],
                "outputs": ["implementation_status"],
                "quality_checks": ["implementation_quality", "progress_tracking"],
            },
            {
                "number": 8,
                "name": "Documentation & Continuity",
                "script": "phase8-documentation.py",
                "required_inputs": ["implementation_status"],
                "outputs": ["final_report", "next_session_context"],
                "quality_checks": [
                    "documentation_completeness",
                    "continuity_assurance",
                ],
            },
        ]

    def _load_config(self, config_path: str = None) -> Dict:
        """設定ファイル読み込み"""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  設定ファイル読み込みエラー: {e}")

        # デフォルト設定
        return {
            "max_retries": 3,
            "timeout_minutes": 30,
            "quality_threshold": 0.8,
            "auto_recovery": True,
            "parallel_execution": False,
            "backup_frequency": "per_phase",
            "log_level": "INFO",
        }

    def execute_full_workflow(self, issue_id: str, project_path: str = None) -> Dict:
        """完全ワークフロー実行"""
        print(f"🚀 AI協業ワークフロー開始: Issue {issue_id}")

        # セッション初期化
        self._initialize_session(issue_id, project_path)

        try:
            # Phase 1-8 順次実行
            for phase in self.phases:
                phase_result = self._execute_phase(phase)

                if not phase_result["success"]:
                    if self.config["auto_recovery"]:
                        recovery_result = self._attempt_phase_recovery(phase)
                        if not recovery_result["success"]:
                            return self._handle_workflow_failure(phase, phase_result)
                    else:
                        return self._handle_workflow_failure(phase, phase_result)

                # 品質ゲートチェック
                quality_check = self._perform_quality_gate_check(phase, phase_result)
                if not quality_check["passed"]:
                    print(
                        f"⚠️  Phase {phase['number']} 品質ゲート失敗: {quality_check['issues']}"
                    )

                # 進捗更新
                self._update_workflow_progress(phase, phase_result)

            # ワークフロー完了
            return self._finalize_workflow_success()

        except Exception as e:
            return self._handle_workflow_exception(e)

    def execute_phase_range(
        self, start_phase: int, end_phase: int, context: Dict = None
    ) -> Dict:
        """指定範囲のPhase実行"""
        print(f"🎯 Phase {start_phase}-{end_phase} 部分実行開始")

        # コンテキスト復元
        if context:
            self._restore_workflow_context(context)

        results = {}
        for phase_num in range(start_phase, end_phase + 1):
            if phase_num <= len(self.phases):
                phase = self.phases[phase_num - 1]
                phase_result = self._execute_phase(phase)
                results[f"phase_{phase_num}"] = phase_result

                if not phase_result["success"]:
                    break

        return {
            "success": all(result["success"] for result in results.values()),
            "results": results,
            "summary": f"Phase {start_phase}-{end_phase} execution completed",
        }

    def resume_workflow(self, session_id: str, from_phase: int = None) -> Dict:
        """ワークフロー再開"""
        print(f"🔄 ワークフロー再開: Session {session_id}")

        # セッション状態復元
        session_restored = self._restore_session_state(session_id)
        if not session_restored:
            return {"success": False, "error": "Session state restoration failed"}

        # 再開フェーズ決定
        if from_phase is None:
            from_phase = self._determine_resume_phase()

        # 再開フェーズから実行
        return self.execute_phase_range(
            from_phase, 8, self.workflow_state["project_context"]
        )

    def _initialize_session(self, issue_id: str, project_path: str = None):
        """セッション初期化"""
        session_id = f"{issue_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.workflow_state = {
            "session_id": session_id,
            "issue_id": issue_id,
            "start_time": datetime.now().isoformat(),
            "current_phase": 0,
            "phases_status": {},
            "errors_encountered": [],
            "quality_gates": {},
            "project_context": {"project_path": project_path, "issue_id": issue_id},
        }

        # セッションディレクトリ作成
        session_dir = self.temp_dir / f"session_{session_id}"
        session_dir.mkdir(exist_ok=True)

        print(f"📋 セッション初期化完了: {session_id}")

    def _execute_phase(self, phase: Dict) -> Dict:
        """個別Phase実行"""
        phase_num = phase["number"]
        phase_name = phase["name"]

        print(f"🔄 Phase {phase_num}: {phase_name} 実行開始")

        start_time = time.time()

        try:
            # 必要な入力データ確認
            input_check = self._validate_phase_inputs(phase)
            if not input_check["valid"]:
                return {
                    "success": False,
                    "phase": phase_num,
                    "error": f"Input validation failed: {input_check['missing_inputs']}",
                    "duration": time.time() - start_time,
                }

            # Phase スクリプト実行
            script_path = self.workflows_dir / phase["script"]

            # プロジェクトパスを引数として渡す
            project_path = self.workflow_state["project_context"].get(
                "project_path", os.getcwd()
            )
            cmd = ["python", str(script_path), project_path]

            # Phase 1の場合はissue_idも追加
            if phase_num == 1:
                cmd = ["python", str(script_path), self.workflow_state["issue_id"]]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config["timeout_minutes"] * 60,
            )

            if result.returncode == 0:
                print(f"✅ Phase {phase_num} 完了")
                return {
                    "success": True,
                    "phase": phase_num,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "duration": time.time() - start_time,
                }
            else:
                return {
                    "success": False,
                    "phase": phase_num,
                    "error": f"Script execution failed: {result.stderr}",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "duration": time.time() - start_time,
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "phase": phase_num,
                "error": f"Phase timeout ({self.config['timeout_minutes']} minutes)",
                "duration": time.time() - start_time,
            }
        except Exception as e:
            return {
                "success": False,
                "phase": phase_num,
                "error": f"Unexpected error: {str(e)}",
                "duration": time.time() - start_time,
            }

    def _validate_phase_inputs(self, phase: Dict) -> Dict:
        """Phase入力データ検証"""
        required_inputs = phase.get("required_inputs", [])
        missing_inputs = []

        for input_name in required_inputs:
            if input_name == "issue_id":
                if not self.workflow_state.get("issue_id"):
                    missing_inputs.append(input_name)
            elif input_name == "project_path":
                if not self.workflow_state["project_context"].get("project_path"):
                    missing_inputs.append(input_name)
            else:
                # 前のPhaseの出力ファイル確認
                if not self._check_phase_output_exists(input_name):
                    missing_inputs.append(input_name)

        return {"valid": len(missing_inputs) == 0, "missing_inputs": missing_inputs}

    def _check_phase_output_exists(self, output_name: str) -> bool:
        """Phase出力ファイル存在確認"""
        # 対応するPhaseの出力ファイルを確認
        output_patterns = {
            "issue_data": "agent_issue_*.json",
            "project_analysis": "phase2_analysis_*.json",
            "requirements_result": "phase3_requirements_*.json",
            "strategic_plan": "phase4_strategy_*.json",
            "comprehensive_report": "phase5_report_*.json",
            "review_result": "phase6_review_*.json",
            "implementation_status": "phase7_implementation_*.json",
        }

        pattern = output_patterns.get(output_name)
        if pattern:
            files = list(self.temp_dir.glob(pattern))
            return len(files) > 0

        return False

    def _perform_quality_gate_check(self, phase: Dict, phase_result: Dict) -> Dict:
        """品質ゲートチェック"""
        phase_num = phase["number"]
        quality_checks = phase.get("quality_checks", [])

        passed_checks = []
        failed_checks = []

        for check in quality_checks:
            check_result = self._execute_quality_check(check, phase_num, phase_result)
            if check_result["passed"]:
                passed_checks.append(check)
            else:
                failed_checks.append({"check": check, "reason": check_result["reason"]})

        # 品質スコア計算
        total_checks = len(quality_checks)
        passed_count = len(passed_checks)
        quality_score = passed_count / total_checks if total_checks > 0 else 1.0

        passed = quality_score >= self.config["quality_threshold"]

        self.workflow_state["quality_gates"][f"phase_{phase_num}"] = {
            "score": quality_score,
            "passed": passed,
            "checks": {"passed": passed_checks, "failed": failed_checks},
        }

        return {"passed": passed, "score": quality_score, "issues": failed_checks}

    def _execute_quality_check(
        self, check_name: str, phase_num: int, phase_result: Dict
    ) -> Dict:
        """個別品質チェック実行"""
        # 簡易的な品質チェック実装
        # 実際の運用では、より詳細なチェックロジックを実装

        if check_name == "issue_validity":
            # Issue データの妥当性チェック
            issue_files = list(self.temp_dir.glob("agent_issue_*.json"))
            if issue_files:
                try:
                    with open(issue_files[0], "r", encoding="utf-8") as f:
                        data = json.load(f)
                        issue_data = data.get("issue_data", {})
                        if issue_data.get("title") and issue_data.get("id"):
                            return {"passed": True, "reason": "Issue data valid"}
                except:
                    pass
            return {"passed": False, "reason": "Invalid or missing issue data"}

        elif check_name == "project_detection":
            # プロジェクト検出チェック
            return {
                "passed": phase_result["success"],
                "reason": "Project detection based on script success",
            }

        elif check_name == "strategic_completeness":
            # 戦略計画の完全性チェック
            strategy_files = list(self.temp_dir.glob("phase4_strategy_*.json"))
            if strategy_files:
                try:
                    with open(strategy_files[0], "r", encoding="utf-8") as f:
                        data = json.load(f)
                        strategic_plan = data.get("strategic_plan", {})
                        if strategic_plan.get(
                            "strategic_analysis"
                        ) and strategic_plan.get("implementation_plan"):
                            return {"passed": True, "reason": "Strategic plan complete"}
                except:
                    pass
            return {"passed": False, "reason": "Incomplete strategic plan"}

        else:
            # デフォルト: スクリプト実行成功をベースとする
            return {
                "passed": phase_result["success"],
                "reason": f"Based on {check_name} script execution",
            }

    def _attempt_phase_recovery(self, phase: Dict) -> Dict:
        """Phaseリカバリ試行"""
        phase_num = phase["number"]
        print(f"🔄 Phase {phase_num} リカバリ試行中...")

        for attempt in range(self.config["max_retries"]):
            print(f"  リトライ {attempt + 1}/{self.config['max_retries']}")

            # 少し待機してからリトライ
            time.sleep(5)

            retry_result = self._execute_phase(phase)
            if retry_result["success"]:
                print(f"✅ Phase {phase_num} リカバリ成功")
                return retry_result

        print(f"❌ Phase {phase_num} リカバリ失敗")
        return {"success": False, "error": "Recovery attempts exhausted"}

    def _update_workflow_progress(self, phase: Dict, phase_result: Dict):
        """ワークフロー進捗更新"""
        phase_num = phase["number"]

        self.workflow_state["phases_status"][f"phase_{phase_num}"] = {
            "name": phase["name"],
            "status": "completed" if phase_result["success"] else "failed",
            "duration": phase_result.get("duration", 0),
            "timestamp": datetime.now().isoformat(),
        }

        self.workflow_state["current_phase"] = phase_num

        if not phase_result["success"]:
            self.workflow_state["errors_encountered"].append(
                {
                    "phase": phase_num,
                    "error": phase_result.get("error", "Unknown error"),
                    "timestamp": datetime.now().isoformat(),
                }
            )

    def _finalize_workflow_success(self) -> Dict:
        """ワークフロー成功完了"""
        self.workflow_state["end_time"] = datetime.now().isoformat()
        self.workflow_state["status"] = "completed"

        # 最終セッション状態保存
        self._save_session_state()

        return {
            "success": True,
            "session_id": self.workflow_state["session_id"],
            "phases_completed": len(self.workflow_state["phases_status"]),
            "total_duration": self._calculate_total_duration(),
            "quality_summary": self._generate_quality_summary(),
            "workflow_state": self.workflow_state,
        }

    def _handle_workflow_failure(self, failed_phase: Dict, phase_result: Dict) -> Dict:
        """ワークフロー失敗処理"""
        self.workflow_state["end_time"] = datetime.now().isoformat()
        self.workflow_state["status"] = "failed"
        self.workflow_state["failed_phase"] = failed_phase["number"]

        # セッション状態保存（復旧用）
        self._save_session_state()

        return {
            "success": False,
            "failed_phase": failed_phase["number"],
            "error": phase_result.get("error", "Unknown error"),
            "session_id": self.workflow_state["session_id"],
            "recovery_info": {
                "resume_command": f"python workflow_coordinator.py resume {self.workflow_state['session_id']} {failed_phase['number']}",
                "session_file": f"{self.temp_dir}/session_{self.workflow_state['session_id']}.json",
            },
        }

    def _handle_workflow_exception(self, exception: Exception) -> Dict:
        """ワークフロー例外処理"""
        self.workflow_state["end_time"] = datetime.now().isoformat()
        self.workflow_state["status"] = "exception"

        error_info = {
            "type": type(exception).__name__,
            "message": str(exception),
            "timestamp": datetime.now().isoformat(),
        }

        self.workflow_state["errors_encountered"].append(error_info)
        self._save_session_state()

        return {
            "success": False,
            "error": "Workflow exception occurred",
            "exception": error_info,
            "session_id": self.workflow_state["session_id"],
        }

    def _save_session_state(self):
        """セッション状態保存"""
        session_file = (
            self.temp_dir / f"session_{self.workflow_state['session_id']}.json"
        )

        try:
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(self.workflow_state, f, ensure_ascii=False, indent=2)
            print(f"💾 セッション状態保存: {session_file}")
        except Exception as e:
            print(f"⚠️  セッション状態保存エラー: {e}")

    def _restore_session_state(self, session_id: str) -> bool:
        """セッション状態復元"""
        session_file = self.temp_dir / f"session_{session_id}.json"

        try:
            if session_file.exists():
                with open(session_file, "r", encoding="utf-8") as f:
                    self.workflow_state = json.load(f)
                print(f"📂 セッション状態復元: {session_id}")
                return True
        except Exception as e:
            print(f"⚠️  セッション状態復元エラー: {e}")

        return False

    def _determine_resume_phase(self) -> int:
        """再開フェーズ決定"""
        # 最後に成功したPhaseの次から再開
        completed_phases = [
            int(phase_key.split("_")[1])
            for phase_key, phase_info in self.workflow_state["phases_status"].items()
            if phase_info["status"] == "completed"
        ]

        if completed_phases:
            return max(completed_phases) + 1
        else:
            return 1

    def _calculate_total_duration(self) -> float:
        """総実行時間計算"""
        try:
            start_time = datetime.fromisoformat(self.workflow_state["start_time"])
            end_time = datetime.fromisoformat(self.workflow_state["end_time"])
            duration = end_time - start_time
            return round(duration.total_seconds() / 3600, 2)  # 時間単位
        except:
            return 0.0

    def _generate_quality_summary(self) -> Dict:
        """品質サマリー生成"""
        quality_gates = self.workflow_state["quality_gates"]

        if not quality_gates:
            return {"overall_score": 0, "phases_passed": 0, "total_phases": 0}

        scores = [gate["score"] for gate in quality_gates.values()]
        passed_count = sum(1 for gate in quality_gates.values() if gate["passed"])

        return {
            "overall_score": sum(scores) / len(scores) if scores else 0,
            "phases_passed": passed_count,
            "total_phases": len(quality_gates),
            "pass_rate": passed_count / len(quality_gates) if quality_gates else 0,
        }

    def get_workflow_status(self, session_id: str = None) -> Dict:
        """ワークフロー状況取得"""
        if session_id:
            if not self._restore_session_state(session_id):
                return {"error": "Session not found"}

        return {
            "session_id": self.workflow_state.get("session_id", ""),
            "status": self.workflow_state.get("status", "unknown"),
            "current_phase": self.workflow_state.get("current_phase", 0),
            "phases_status": self.workflow_state.get("phases_status", {}),
            "quality_summary": self._generate_quality_summary(),
            "errors": self.workflow_state.get("errors_encountered", []),
        }


def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python workflow_coordinator.py execute <issue_id> [project_path]")
        print("  python workflow_coordinator.py resume <session_id> [from_phase]")
        print("  python workflow_coordinator.py status [session_id]")
        print(
            "  python workflow_coordinator.py phase <start_phase> <end_phase> [project_path]"
        )
        sys.exit(1)

    command = sys.argv[1]
    coordinator = WorkflowCoordinator()

    try:
        if command == "execute":
            if len(sys.argv) < 3:
                print("❌ issue_id が必要です")
                sys.exit(1)

            issue_id = sys.argv[2]
            project_path = sys.argv[3] if len(sys.argv) > 3 else None

            result = coordinator.execute_full_workflow(issue_id, project_path)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif command == "resume":
            if len(sys.argv) < 3:
                print("❌ session_id が必要です")
                sys.exit(1)

            session_id = sys.argv[2]
            from_phase = int(sys.argv[3]) if len(sys.argv) > 3 else None

            result = coordinator.resume_workflow(session_id, from_phase)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif command == "status":
            session_id = sys.argv[2] if len(sys.argv) > 2 else None

            status = coordinator.get_workflow_status(session_id)
            print(json.dumps(status, ensure_ascii=False, indent=2))

        elif command == "phase":
            if len(sys.argv) < 4:
                print("❌ start_phase と end_phase が必要です")
                sys.exit(1)

            start_phase = int(sys.argv[2])
            end_phase = int(sys.argv[3])
            project_path = sys.argv[4] if len(sys.argv) > 4 else None

            context = {"project_path": project_path} if project_path else None
            result = coordinator.execute_phase_range(start_phase, end_phase, context)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        else:
            print(f"❌ 不明なコマンド: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Workflow Coordinator エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
