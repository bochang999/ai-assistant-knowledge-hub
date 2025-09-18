#!/usr/bin/env python3
"""
Session Management Library
BOC-95ベース AI協業ワークフローシステム

セッション管理、状態保存、復旧機能を提供
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class SessionManager:
    def __init__(
        self,
        ai_hub_dir: str = "/data/data/com.termux/files/home/ai-assistant-knowledge-hub",
    ):
        """Session Manager初期化"""
        self.ai_hub_dir = Path(ai_hub_dir)
        self.temp_dir = self.ai_hub_dir / "temp"
        self.sessions_dir = self.ai_hub_dir / "sessions"
        self.backups_dir = self.ai_hub_dir / "backups"

        # ディレクトリ作成
        self.temp_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)

        self.current_session_id = None
        self.session_data = {}

    def create_session(self, issue_id: str, project_path: str) -> str:
        """新規セッション作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"session_{issue_id}_{timestamp}"

        self.current_session_id = session_id
        self.session_data = {
            "session_id": session_id,
            "issue_id": issue_id,
            "project_path": project_path,
            "created_at": datetime.now().isoformat(),
            "current_phase": 0,
            "completed_phases": [],
            "workflow_status": "CREATED",
            "phase_results": {},
            "quality_metrics": {},
            "error_log": [],
            "context_data": {},
        }

        self._save_session()
        print(f"📝 新規セッション作成: {session_id}")
        return session_id

    def load_session(self, session_id: str) -> bool:
        """既存セッション読み込み"""
        session_file = self.sessions_dir / f"{session_id}.json"

        if not session_file.exists():
            print(f"⚠️  セッションファイルが見つかりません: {session_id}")
            return False

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                self.session_data = json.load(f)
                self.current_session_id = session_id
                print(f"📂 セッション読み込み成功: {session_id}")
                return True
        except Exception as e:
            print(f"❌ セッション読み込みエラー: {e}")
            return False

    def get_latest_session(self) -> Optional[str]:
        """最新のセッション取得"""
        if not self.sessions_dir.exists():
            return None

        session_files = list(self.sessions_dir.glob("session_*.json"))
        if not session_files:
            return None

        latest_session = max(session_files, key=lambda f: f.stat().st_mtime)
        session_id = latest_session.stem

        if self.load_session(session_id):
            return session_id
        return None

    def update_phase_progress(self, phase_number: int, phase_result: Dict):
        """フェーズ進捗更新"""
        if not self.current_session_id:
            print("⚠️  アクティブなセッションがありません")
            return

        self.session_data["current_phase"] = phase_number
        self.session_data["phase_results"][f"phase_{phase_number}"] = phase_result
        self.session_data["last_updated"] = datetime.now().isoformat()

        if phase_result.get("status") == "completed":
            if phase_number not in self.session_data["completed_phases"]:
                self.session_data["completed_phases"].append(phase_number)

        self._save_session()
        print(f"📊 Phase {phase_number} 進捗更新完了")

    def update_workflow_status(self, status: str):
        """ワークフロー状態更新"""
        if not self.current_session_id:
            return

        self.session_data["workflow_status"] = status
        self.session_data["last_updated"] = datetime.now().isoformat()
        self._save_session()

    def add_error(self, error_message: str, phase_number: int = None):
        """エラーログ追加"""
        if not self.current_session_id:
            return

        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": error_message,
            "phase": phase_number,
        }

        self.session_data["error_log"].append(error_entry)
        self._save_session()

    def store_context_data(self, key: str, data: Any):
        """コンテキストデータ保存"""
        if not self.current_session_id:
            return

        self.session_data["context_data"][key] = data
        self._save_session()

    def get_context_data(self, key: str) -> Any:
        """コンテキストデータ取得"""
        if not self.current_session_id:
            return None

        return self.session_data["context_data"].get(key)

    def create_backup(self, project_path: str) -> str:
        """プロジェクトバックアップ作成"""
        if not self.current_session_id:
            raise Exception("アクティブなセッションがありません")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = Path(project_path).name
        backup_name = f"backup_{project_name}_{self.current_session_id}_{timestamp}"
        backup_path = self.backups_dir / backup_name

        try:
            # プロジェクトディレクトリを除外リストに基づいてコピー
            exclude_patterns = [
                "node_modules",
                ".git",
                "dist",
                "build",
                "__pycache__",
                ".cache",
                ".tmp",
                "temp",
                ".vscode",
                ".idea",
            ]

            shutil.copytree(
                project_path,
                backup_path,
                ignore=shutil.ignore_patterns(*exclude_patterns),
            )

            # バックアップ情報をセッションに記録
            self.session_data["backup_path"] = str(backup_path)
            self.session_data["backup_created_at"] = datetime.now().isoformat()
            self._save_session()

            print(f"💾 バックアップ作成完了: {backup_path}")
            return str(backup_path)

        except Exception as e:
            error_msg = f"バックアップ作成エラー: {e}"
            self.add_error(error_msg)
            raise Exception(error_msg)

    def restore_backup(self, backup_path: str, restore_to: str) -> bool:
        """バックアップからリストア"""
        try:
            if Path(restore_to).exists():
                # 既存ディレクトリを一時的に移動
                temp_name = (
                    f"{restore_to}_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                shutil.move(restore_to, temp_name)

            # バックアップからリストア
            shutil.copytree(backup_path, restore_to)

            print(f"🔄 バックアップリストア完了: {restore_to}")
            return True

        except Exception as e:
            print(f"❌ バックアップリストアエラー: {e}")
            return False

    def cleanup_old_sessions(self, days: int = 7):
        """古いセッションのクリーンアップ"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

        # セッションファイルクリーンアップ
        for session_file in self.sessions_dir.glob("session_*.json"):
            if session_file.stat().st_mtime < cutoff_time:
                session_file.unlink()
                print(f"🗑️  古いセッション削除: {session_file.name}")

        # バックアップクリーンアップ
        for backup_dir in self.backups_dir.iterdir():
            if backup_dir.is_dir() and backup_dir.stat().st_mtime < cutoff_time:
                shutil.rmtree(backup_dir)
                print(f"🗑️  古いバックアップ削除: {backup_dir.name}")

    def generate_session_report(self) -> Dict:
        """セッション報告書生成"""
        if not self.current_session_id:
            return {}

        completed_phases = len(self.session_data.get("completed_phases", []))
        total_phases = 8  # 8フェーズワークフロー

        report = {
            "session_info": {
                "session_id": self.current_session_id,
                "issue_id": self.session_data.get("issue_id"),
                "project_path": self.session_data.get("project_path"),
                "created_at": self.session_data.get("created_at"),
                "duration": self._calculate_session_duration(),
            },
            "progress": {
                "current_phase": self.session_data.get("current_phase", 0),
                "completed_phases": completed_phases,
                "total_phases": total_phases,
                "completion_percentage": (completed_phases / total_phases) * 100,
                "workflow_status": self.session_data.get("workflow_status", "UNKNOWN"),
            },
            "quality_metrics": self.session_data.get("quality_metrics", {}),
            "error_summary": {
                "total_errors": len(self.session_data.get("error_log", [])),
                "recent_errors": self.session_data.get("error_log", [])[-3:],  # 最新3件
            },
            "phase_results": self.session_data.get("phase_results", {}),
            "next_steps": self._generate_next_steps(),
        }

        return report

    def _calculate_session_duration(self) -> str:
        """セッション継続時間計算"""
        if not self.session_data.get("created_at"):
            return "不明"

        created_at = datetime.fromisoformat(self.session_data["created_at"])
        duration = datetime.now() - created_at

        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)

        return f"{int(hours)}時間{int(minutes)}分"

    def _generate_next_steps(self) -> List[str]:
        """次のステップ生成"""
        current_phase = self.session_data.get("current_phase", 0)
        workflow_status = self.session_data.get("workflow_status", "")

        if workflow_status == "COMPLETED":
            return ["✅ ワークフロー完了", "📋 最終報告書確認", "🔄 次のIssueに移行"]

        elif workflow_status == "ERROR":
            return ["🔧 エラー解決", "🔄 失敗フェーズから再開", "📞 サポート連絡"]

        else:
            next_phase = current_phase + 1
            if next_phase <= 8:
                return [f"▶️  Phase {next_phase} 実行", "📊 進捗確認", "🔍 品質チェック"]
            else:
                return ["📝 最終フェーズ完了", "🎯 ワークフロー終了準備"]

    def _save_session(self):
        """セッションデータ保存"""
        if not self.current_session_id:
            return

        session_file = self.sessions_dir / f"{self.current_session_id}.json"
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)

    def list_sessions(self) -> List[Dict]:
        """セッション一覧取得"""
        sessions = []

        for session_file in self.sessions_dir.glob("session_*.json"):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    sessions.append(
                        {
                            "session_id": session_data.get("session_id"),
                            "issue_id": session_data.get("issue_id"),
                            "created_at": session_data.get("created_at"),
                            "workflow_status": session_data.get("workflow_status"),
                            "current_phase": session_data.get("current_phase"),
                            "file_path": str(session_file),
                        }
                    )
            except Exception as e:
                print(f"⚠️  セッションファイル読み込みエラー: {session_file.name} - {e}")

        # 作成日時で降順ソート
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions
