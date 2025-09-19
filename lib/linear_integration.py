#!/usr/bin/env python3
"""
Linear API Integration Library
BOC-95ベース AI協業ワークフローシステム

Linear APIとの統合機能を提供
"""

import json
import requests
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class LinearIntegration:
    def __init__(self):
        """Linear API integration初期化"""
        self.api_key = self._load_api_key()
        self.team_id = self._load_team_id()
        self.base_url = "https://api.linear.app/graphql"

        # Linear State IDs (固定値)
        self.state_ids = {
            "IN_PROGRESS": "1cebb56e-524e-4de0-b676-0f574df9012a",
            "IN_REVIEW": "33feb1c9-3276-4e13-863a-0b93db032a0f",
            "DONE": "948532e6-d440-4fa8-938f-2d437c17a660",
        }

    def _load_api_key(self) -> str:
        """Linear API key読み込み"""
        api_key_file = Path.home() / ".linear-api-key"
        if api_key_file.exists():
            with open(api_key_file, "r") as f:
                return f.read().strip()
        raise Exception("Linear API key not found. Create ~/.linear-api-key file")

    def _load_team_id(self) -> str:
        """Linear Team ID読み込み"""
        team_id_file = Path.home() / ".linear-team-id"
        if team_id_file.exists():
            with open(team_id_file, "r") as f:
                return f.read().strip()
        raise Exception("Linear Team ID not found. Create ~/.linear-team-id file")

    def _execute_graphql(self, query: str, variables: Dict = None) -> Dict:
        """GraphQL query実行"""
        headers = {"Authorization": self.api_key, "Content-Type": "application/json"}

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(self.base_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Linear API request failed: {response.status_code}")

        data = response.json()
        if "errors" in data:
            raise Exception(f"Linear API GraphQL errors: {data['errors']}")

        return data["data"]

    def get_issue(self, issue_id: str) -> Optional[Dict]:
        """Issue詳細取得"""
        query = """
        query GetIssue($id: String!) {
            issue(id: $id) {
                id
                identifier
                title
                description
                priority
                priorityLabel
                state {
                    id
                    name
                    type
                }
                assignee {
                    id
                    name
                    email
                }
                project {
                    id
                    name
                    key
                }
                labels {
                    nodes {
                        id
                        name
                        color
                    }
                }
                comments {
                    nodes {
                        id
                        body
                        createdAt
                        user {
                            name
                        }
                    }
                }
                createdAt
                updatedAt
                dueDate
                url
            }
        }
        """

        try:
            data = self._execute_graphql(query, {"id": issue_id})
            return data.get("issue")
        except Exception as e:
            print(f"⚠️  Issue取得エラー: {e}")
            return None

    def search_issues_by_identifier(self, identifier: str) -> Optional[Dict]:
        """Issue識別子による検索"""
        query = """
        query SearchIssues($filter: IssueFilter!) {
            issues(filter: $filter, first: 1) {
                nodes {
                    id
                    identifier
                    title
                    description
                    priority
                    priorityLabel
                    state {
                        id
                        name
                        type
                    }
                    assignee {
                        id
                        name
                        email
                    }
                    project {
                        id
                        name
                        key
                    }
                    labels {
                        nodes {
                            id
                            name
                            color
                        }
                    }
                    comments {
                        nodes {
                            id
                            body
                            createdAt
                            user {
                                name
                            }
                        }
                    }
                    createdAt
                    updatedAt
                    dueDate
                    url
                }
            }
        }
        """

        try:
            variables = {
                "filter": {
                    "team": {"id": {"eq": self.team_id}},
                    "number": {"eq": int(identifier.replace("BOC-", ""))},
                }
            }
            data = self._execute_graphql(query, variables)
            issues = data.get("issues", {}).get("nodes", [])
            return issues[0] if issues else None
        except Exception as e:
            print(f"⚠️  Issue検索エラー: {e}")
            return None

    def update_issue_status(self, issue_id: str, status: str) -> bool:
        """Issue状態更新"""
        if status not in self.state_ids:
            print(f"⚠️  無効な状態: {status}")
            return False

        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
            issueUpdate(id: $id, input: $input) {
                success
                issue {
                    id
                    state {
                        name
                    }
                }
            }
        }
        """

        try:
            variables = {"id": issue_id, "input": {"stateId": self.state_ids[status]}}
            data = self._execute_graphql(mutation, variables)

            result = data.get("issueUpdate", {})
            if result.get("success"):
                print(f"✅ Issue状態更新成功: {status}")
                return True
            else:
                print(f"❌ Issue状態更新失敗")
                return False

        except Exception as e:
            print(f"⚠️  Issue状態更新エラー: {e}")
            return False

    def add_comment(self, issue_id: str, comment: str) -> bool:
        """Issueコメント追加"""
        mutation = """
        mutation CreateComment($input: CommentCreateInput!) {
            commentCreate(input: $input) {
                success
                comment {
                    id
                    body
                }
            }
        }
        """

        try:
            variables = {"input": {"issueId": issue_id, "body": comment}}
            data = self._execute_graphql(mutation, variables)

            result = data.get("commentCreate", {})
            if result.get("success"):
                print(f"✅ コメント追加成功")
                return True
            else:
                print(f"❌ コメント追加失敗")
                return False

        except Exception as e:
            print(f"⚠️  コメント追加エラー: {e}")
            return False

    def extract_project_tags(self, issue: Dict) -> List[str]:
        """Issue からプロジェクトタグを抽出"""
        tags = []

        # プロジェクト名をタグとして追加
        if issue.get("project"):
            project_name = issue["project"].get("name", "").lower()
            if project_name:
                tags.append(project_name)

        # ラベルをタグとして追加
        labels = issue.get("labels", {}).get("nodes", [])
        for label in labels:
            label_name = label.get("name", "").lower()
            if label_name and label_name not in tags:
                tags.append(label_name)

        # 説明文やタイトルからプロジェクト名を抽出
        text_content = f"{issue.get('title', '')} {issue.get('description', '')}"
        common_projects = [
            "petit-recipe",
            "recipebox",
            "ai-assistant-knowledge-hub",
            "mcp-linear",
            "laminator",
            "pwa",
        ]

        for project in common_projects:
            if project.lower() in text_content.lower() and project not in tags:
                tags.append(project)

        return tags

    def create_progress_comment(self, work_report: str, phase: str = "") -> str:
        """作業進捗コメント作成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        comment = f"""## 🔄 作業進捗報告 - {timestamp}

{f'**Phase**: {phase}' if phase else ''}

### 実施内容
{work_report}

### システム情報
- **実行時刻**: {timestamp}
- **ワークフロー**: BOC-95ベース AI協業システム
- **生成**: 🤖 AI Assistant (Claude Code)

---
*この報告は自動生成されました*
"""
        return comment

    def create_completion_comment(
        self, work_summary: str, next_steps: List[str] = None
    ) -> str:
        """作業完了コメント作成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        next_steps_text = ""
        if next_steps:
            next_steps_text = "\n### 📋 次のステップ\n" + "\n".join(
                [f"- {step}" for step in next_steps]
            )

        comment = f"""## ✅ 作業完了報告 - {timestamp}

### 完了内容
{work_summary}

{next_steps_text}

### 品質確認
- ✅ コード品質チェック完了
- ✅ テスト実行完了
- ✅ ドキュメント更新完了

### システム情報
- **完了時刻**: {timestamp}
- **ワークフロー**: BOC-95ベース AI協業システム
- **生成**: 🤖 AI Assistant (Claude Code)

---
*この作業は Review 段階に移行しました*
"""
        return comment


class ProjectMapper:
    """プロジェクトタグとディレクトリのマッピング"""

    def __init__(self, project_map_path: str = "project_map.json"):
        self.project_map_path = Path(project_map_path)
        self.project_map = self._load_project_map()

    def _load_project_map(self) -> Dict:
        """project_map.json読み込み"""
        if self.project_map_path.exists():
            try:
                with open(self.project_map_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  project_map.json読み込みエラー: {e}")

        # デフォルトマッピング
        return {
            "petit-recipe": "/data/data/com.termux/files/home/petit-recipe",
            "recipebox": "/data/data/com.termux/files/home/recipebox-web",
            "ai-assistant-knowledge-hub": "/data/data/com.termux/files/home/ai-assistant-knowledge-hub",
            "mcp-linear": "/data/data/com.termux/files/home/mcp-linear-app",
            "laminator": "/data/data/com.termux/files/home/laminator-dashboard",
        }

    def resolve_project_path(self, tags: List[str]) -> Optional[str]:
        """タグからプロジェクトパス解決"""
        for tag in tags:
            if tag in self.project_map:
                project_path = Path(self.project_map[tag])
                if project_path.exists():
                    return str(project_path)

        # フォールバック: 現在のディレクトリ
        return os.getcwd()

    def detect_project_type(self, project_path: str) -> str:
        """プロジェクトタイプ検出"""
        path = Path(project_path)

        if (path / "package.json").exists():
            package_json = json.loads((path / "package.json").read_text())

            # Capacitor プロジェクト
            if "capacitor" in package_json.get("dependencies", {}):
                return "mobile"

            # React プロジェクト
            if "react" in package_json.get("dependencies", {}):
                return "web"

            # Node.js プロジェクト
            return "api"

        elif (path / "requirements.txt").exists() or (path / "pyproject.toml").exists():
            return "tool"

        elif (path / "Cargo.toml").exists():
            return "rust"

        elif (path / "go.mod").exists():
            return "go"

        else:
            return "unknown"


class LinearJSONSafeUpdater:
    """JSON エスケープ問題を回避するLinear更新ユーティリティ"""

    def __init__(self, linear_integration: LinearIntegration):
        self.linear = linear_integration

        # 正しいGraphQL mutation templates
        self.mutations = {
            "update_issue": """
            mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
                issueUpdate(id: $id, input: $input) {
                    success
                    issue {
                        id
                        title
                        description
                        state {
                            name
                        }
                    }
                }
            }
            """,
            "add_comment": """
            mutation CommentCreate($input: CommentCreateInput!) {
                commentCreate(input: $input) {
                    success
                    comment {
                        id
                        body
                        createdAt
                    }
                }
            }
            """,
            "update_status": """
            mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {
                issueUpdate(id: $id, input: $input) {
                    success
                    issue {
                        id
                        state {
                            name
                            id
                        }
                    }
                }
            }
            """,
        }

        # Linear State IDs (bochang's labチーム)
        self.state_ids = {
            "todo": "34c3b20c-ad8e-4b7f-864c-9e57bc5e0096",
            "in_progress": "1cebb56e-524e-4de0-b676-0f574df9012a",
            "in_review": "33feb1c9-3276-4e13-863a-0b93db032a0f",
            "done": "bb58fd73-3cbf-4b03-ac3c-e1a40db9ad8c",
        }

    def safe_update_issue_description(
        self, issue_id: str, new_description: str
    ) -> bool:
        """
        JSON エスケープ問題を回避してIssue description を安全に更新

        Args:
            issue_id: Linear Issue ID
            new_description: 新しい説明文

        Returns:
            bool: 更新成功の可否
        """
        import tempfile
        import subprocess
        import json

        try:
            # 一時ファイルに説明文を保存
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as f:
                f.write(new_description)
                temp_file = f.name

            # jqを使用してJSON-safe な GraphQL クエリを生成
            query_template = {
                "query": 'mutation($input: IssueUpdateInput!) { issueUpdate(id: "%s", input: $input) { success } }'
                % issue_id,
                "variables": {"input": {"description": None}},  # jq で置換される
            }

            # jqコマンドでJSON-safe に説明文をセット
            jq_command = [
                "jq",
                "-n",
                "--rawfile",
                "desc",
                temp_file,
                json.dumps(query_template).replace(
                    '"description":null', '"description":$desc'
                ),
            ]

            # GraphQLクエリ生成
            result = subprocess.run(jq_command, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ jq処理エラー: {result.stderr}")
                return False

            # Linear APIに送信
            curl_command = [
                "curl",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                f"Authorization: {self.linear.api_key}",
                "-H",
                "Content-Type: application/json",
                "-d",
                result.stdout,
            ]

            api_result = subprocess.run(curl_command, capture_output=True, text=True)
            response_data = json.loads(api_result.stdout)

            # 結果確認
            if (
                "data" in response_data
                and response_data["data"]["issueUpdate"]["success"]
            ):
                print(f"✅ Issue {issue_id} description 更新成功")
                return True
            else:
                print(f"❌ Issue更新失敗: {response_data}")
                return False

        except Exception as e:
            print(f"❌ JSON-safe更新エラー: {e}")
            return False
        finally:
            # 一時ファイル削除
            try:
                import os

                os.unlink(temp_file)
            except:
                pass

    def safe_add_comment(self, issue_id: str, comment_body: str) -> bool:
        """
        JSON エスケープ問題を回避してコメントを安全に追加

        Args:
            issue_id: Linear Issue ID
            comment_body: コメント内容

        Returns:
            bool: 追加成功の可否
        """
        import tempfile
        import subprocess
        import json

        try:
            # 一時ファイルにコメント内容を保存
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as f:
                f.write(comment_body)
                temp_file = f.name

            # jqを使用してJSON-safe な GraphQL クエリを生成
            query_template = {
                "query": 'mutation { commentCreate(input: { issueId: "%s", body: "PLACEHOLDER" }) { comment { id } } }'
                % issue_id,
            }

            # jqコマンドでJSON-safe にコメント内容をセット
            jq_command = [
                "jq",
                "-n",
                "--rawfile",
                "body",
                temp_file,
                "--arg",
                "query",
                query_template["query"],
                '{"query": ($query | gsub("PLACEHOLDER"; $body))}',
            ]

            # GraphQLクエリ生成
            result = subprocess.run(jq_command, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ jq処理エラー: {result.stderr}")
                return False

            # Linear APIに送信
            curl_command = [
                "curl",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                f"Authorization: {self.linear.api_key}",
                "-H",
                "Content-Type: application/json",
                "-d",
                result.stdout,
            ]

            api_result = subprocess.run(curl_command, capture_output=True, text=True)
            response_data = json.loads(api_result.stdout)

            # 結果確認
            if "data" in response_data and "commentCreate" in response_data["data"]:
                comment_id = response_data["data"]["commentCreate"]["comment"]["id"]
                print(f"✅ コメント追加成功: {comment_id}")
                return True
            else:
                print(f"❌ コメント追加失敗: {response_data}")
                return False

        except Exception as e:
            print(f"❌ JSON-safe コメント追加エラー: {e}")
            return False
        finally:
            # 一時ファイル削除
            try:
                import os

                os.unlink(temp_file)
            except:
                pass

    def append_to_issue_description(
        self, issue_id: str, additional_content: str
    ) -> bool:
        """
        既存のIssue descriptionに内容を追記

        Args:
            issue_id: Linear Issue ID
            additional_content: 追記する内容

        Returns:
            bool: 追記成功の可否
        """
        try:
            # 現在の説明文を取得
            current_issue = self.linear.get_issue(issue_id)
            if not current_issue:
                print(f"❌ Issue {issue_id} の取得に失敗")
                return False

            current_description = current_issue.get("description", "")

            # 新しい説明文 = 既存 + 追記内容
            new_description = current_description + "\n" + additional_content

            # JSON-safe 更新
            return self.safe_update_issue_description(issue_id, new_description)

        except Exception as e:
            print(f"❌ Issue description 追記エラー: {e}")
            return False


# 便利なヘルパー関数
def create_json_safe_updater() -> LinearJSONSafeUpdater:
    """JSON-safe updater インスタンス作成"""
    linear = LinearIntegration()
    return LinearJSONSafeUpdater(linear)
