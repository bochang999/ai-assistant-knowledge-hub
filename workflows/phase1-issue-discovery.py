#!/usr/bin/env python3
"""
Phase 1: Issue Intelligence & Project Discovery
BOC-95に基づく段階的問題解決ワークフローシステム

目的: Linear IssueからプロジェクトタグでプロジェクトのAutodetectとプロジェクトディレクトリ移動
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


class IssueDiscoveryEngine:
    def __init__(self, config_path: str = None):
        """Issue Discovery Engine初期化"""
        self.home_dir = Path("/data/data/com.termux/files/home")
        self.ai_hub_dir = self.home_dir / "ai-assistant-knowledge-hub"

        # 設定ファイル読み込み
        if config_path:
            self.config = self._load_config(config_path)
        else:
            self.config = self._load_default_config()

        # Linear API設定
        self.linear_api_key = self._get_linear_api_key()
        self.linear_team_id = self._get_linear_team_id()

    def _load_config(self, config_path: str) -> Dict:
        """設定ファイル読み込み"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  設定ファイルが見つかりません: {config_path}")
            return self._load_default_config()

    def _load_default_config(self) -> Dict:
        """デフォルト設定"""
        return {
            "project_map_path": str(self.ai_hub_dir / "project_map.json"),
            "temp_dir": str(self.ai_hub_dir / "temp"),
            "linear_graphql_endpoint": "https://api.linear.app/graphql",
            "supported_project_types": ["web", "mobile", "api", "tool", "analysis"],
        }

    def _get_linear_api_key(self) -> str:
        """Linear API Key取得"""
        try:
            with open(self.home_dir / ".linear-api-key", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception("❌ Linear API Keyが見つかりません: ~/.linear-api-key")

    def _get_linear_team_id(self) -> str:
        """Linear Team ID取得"""
        try:
            with open(self.home_dir / ".linear-team-id", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception("❌ Linear Team IDが見つかりません: ~/.linear-team-id")

    def discover_issue_project(self, issue_id: str) -> Tuple[Dict, Optional[str]]:
        """
        IssueからプロジェクトタグベースのProject Discovery

        Returns:
            Tuple[issue_data, project_directory]
        """
        print(f"🔍 Issue Discovery開始: {issue_id}")

        # 1. Linear APIからIssue詳細取得
        issue_data = self._fetch_issue_details(issue_id)

        # 2. Issueからプロジェクトタグ抽出
        project_tags = self._extract_project_tags(issue_data)

        # 3. project_map.jsonとの照合
        project_directory = self._map_tags_to_project(project_tags)

        # 4. プロジェクトディレクトリ存在確認
        if project_directory:
            project_path = self._validate_project_directory(project_directory)
            if project_path:
                print(f"✅ プロジェクト特定完了: {project_path}")
                return issue_data, project_path

        print("⚠️  プロジェクトを特定できませんでした")
        return issue_data, None

    def _fetch_issue_details(self, issue_id: str) -> Dict:
        """Linear APIからIssue詳細取得"""
        graphql_query = {
            "query": f"""
            query {{
                issue(id: "{issue_id}") {{
                    id
                    title
                    description
                    state {{ name }}
                    labels {{ nodes {{ name }} }}
                    project {{ name }}
                    team {{ name key }}
                    createdAt
                    updatedAt
                }}
            }}
            """
        }

        curl_command = [
            "curl",
            "-X",
            "POST",
            self.config["linear_graphql_endpoint"],
            "-H",
            f"Authorization: {self.linear_api_key}",
            "-H",
            "Content-Type: application/json",
            "-d",
            json.dumps(graphql_query),
        ]

        try:
            result = subprocess.run(
                curl_command, capture_output=True, text=True, check=True
            )
            response_data = json.loads(result.stdout)

            if "errors" in response_data:
                raise Exception(f"GraphQL エラー: {response_data['errors']}")

            issue_data = response_data["data"]["issue"]
            print(f"📋 Issue取得完了: {issue_data['title']}")

            # Issue詳細をtempディレクトリに保存
            self._save_issue_to_temp(issue_id, issue_data)

            return issue_data

        except subprocess.CalledProcessError as e:
            raise Exception(f"Linear API呼び出し失敗: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON解析失敗: {e}")

    def _extract_project_tags(self, issue_data: Dict) -> list:
        """Issueからプロジェクトタグ抽出"""
        project_tags = []

        # ラベルからプロジェクトタグ抽出
        if issue_data.get("labels", {}).get("nodes"):
            for label in issue_data["labels"]["nodes"]:
                label_name = label["name"].lower()
                # プロジェクトタグの形式: "project-", "proj-", または直接プロジェクト名
                if any(
                    prefix in label_name
                    for prefix in ["project-", "proj-", "petit-", "recipebox", "mcp-"]
                ):
                    project_tags.append(label_name)

        # プロジェクト名からタグ抽出
        if issue_data.get("project", {}).get("name"):
            project_name = issue_data["project"]["name"].lower()
            project_tags.append(project_name)

        # タイトルからプロジェクトタグ抽出
        title = issue_data.get("title", "").lower()
        if "petit-recipe" in title or "petitrecipe" in title:
            project_tags.append("petit-recipe")
        elif "recipebox" in title:
            project_tags.append("recipebox")
        elif "mcp" in title:
            project_tags.append("mcp-servers")

        print(f"🏷️  抽出されたプロジェクトタグ: {project_tags}")
        return project_tags

    def _map_tags_to_project(self, project_tags: list) -> Optional[str]:
        """プロジェクトタグからproject_map.jsonとの照合"""
        try:
            with open(self.config["project_map_path"], "r", encoding="utf-8") as f:
                project_map = json.load(f)
        except FileNotFoundError:
            print(
                f"⚠️  project_map.json が見つかりません: {self.config['project_map_path']}"
            )
            return None

        # タグマッチング
        for tag in project_tags:
            for project_id, project_info in project_map.get("projects", {}).items():
                project_aliases = project_info.get("aliases", [])
                project_name = project_info.get("name", "").lower()

                if tag in project_aliases or tag in project_name:
                    project_directory = project_info.get("directory")
                    print(
                        f"✅ プロジェクトマッチング成功: {tag} -> {project_directory}"
                    )
                    return project_directory

        return None

    def _validate_project_directory(self, project_directory: str) -> Optional[str]:
        """プロジェクトディレクトリ存在確認"""
        project_path = self.home_dir / project_directory

        if project_path.exists() and project_path.is_dir():
            print(f"📁 プロジェクトディレクトリ確認: {project_path}")
            return str(project_path)
        else:
            print(f"❌ プロジェクトディレクトリが存在しません: {project_path}")
            return None

    def _save_issue_to_temp(self, issue_id: str, issue_data: Dict):
        """Issue詳細をtempディレクトリに保存"""
        temp_dir = Path(self.config["temp_dir"])
        temp_dir.mkdir(exist_ok=True)

        temp_file = temp_dir / f"agent_issue_{issue_id}.json"

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "issue_id": issue_id,
                    "issue_data": issue_data,
                    "discovery_timestamp": subprocess.check_output(["date"])
                    .decode()
                    .strip(),
                    "phase": "1-issue-discovery",
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 Issue詳細保存: {temp_file}")

    def change_to_project_directory(self, project_path: str) -> bool:
        """プロジェクトディレクトリに移動"""
        try:
            os.chdir(project_path)
            current_dir = os.getcwd()
            print(f"📂 ディレクトリ移動完了: {current_dir}")
            return True
        except OSError as e:
            print(f"❌ ディレクトリ移動失敗: {e}")
            return False


def main():
    """メイン実行関数"""
    if len(sys.argv) < 2:
        print("使用方法: python phase1-issue-discovery.py <issue_id>")
        sys.exit(1)

    issue_id = sys.argv[1]

    try:
        # Issue Discovery Engine初期化
        discovery_engine = IssueDiscoveryEngine()

        # Issue Discovery実行
        issue_data, project_path = discovery_engine.discover_issue_project(issue_id)

        if project_path:
            # プロジェクトディレクトリに移動
            success = discovery_engine.change_to_project_directory(project_path)
            if success:
                print(f"🎯 Phase 1 完了: {issue_id} -> {project_path}")
                print(
                    f"💡 次のコマンド: python {discovery_engine.ai_hub_dir}/workflows/phase2-project-analysis.py"
                )
            else:
                print("❌ Phase 1 失敗: ディレクトリ移動エラー")
                sys.exit(1)
        else:
            print("❌ Phase 1 失敗: プロジェクト特定エラー")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Phase 1 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
