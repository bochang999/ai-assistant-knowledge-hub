import requests
import os
import argparse
import json
from pathlib import Path

# --- 定数 ---
API_URL = "https://api.linear.app/graphql"
API_KEY_PATH = Path.home() / ".linear-api-key"
# このチームIDは固定です。必要に応じて変更してください。
TEAM_ID = "3dea9cba-30a5-4a25-b6e3-0ec0a2ec3896"

# --- ヘルパー関数 ---


def get_headers():
    """APIキーを読み込み、リクエストヘッダーを生成する"""
    if not API_KEY_PATH.is_file():
        print(f"エラー: APIキーファイルが見つかりません: {API_KEY_PATH}")
        exit(1)
    api_key = API_KEY_PATH.read_text().strip()
    return {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }


def run_graphql_query(query, variables=None):
    """GraphQLクエリを実行し、結果を返す"""
    headers = get_headers()
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生

        data = response.json()
        if "errors" in data:
            print("GraphQLエラーが発生しました:")
            print(json.dumps(data["errors"], indent=2, ensure_ascii=False))
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"HTTPリクエストエラーが発生しました: {e}")
        return None


# --- 各ステップの関数 ---


def create_project(name):
    print(f"1. プロジェクトを作成中: '{name}'...")
    query = """
        mutation CreateProject($name: String!, $teamIds: [String!]!) {
            projectCreate(input: { name: $name, teamIds: $teamIds }) {
                success
                project { id name }
            }
        }
    """
    variables = {"name": name, "teamIds": [TEAM_ID]}
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("projectCreate", {}).get("success"):
        project = data["data"]["projectCreate"]["project"]
        print(f"   ✅ 成功 (ID: {project['id']})")
        return project
    print("   ❌ 失敗")
    return None


def create_milestone(project_id, name):
    print(f"2. マイルストーンを作成中: '{name}'...")
    query = """
        mutation CreateMilestone($projectId: String!, $name: String!) {
            projectMilestoneCreate(input: { projectId: $projectId, name: $name }) {
                success
                projectMilestone { id name }
            }
        }
    """
    variables = {"projectId": project_id, "name": name}
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("projectMilestoneCreate", {}).get("success"):
        milestone = data["data"]["projectMilestoneCreate"]["projectMilestone"]
        print(f"   ✅ 成功 (ID: {milestone['id']})")
        return milestone
    print("   ❌ 失敗")
    return None


def create_label(name):
    print(f"3. ラベルを作成中: '{name}'...")
    query = """
        mutation CreateLabel($name: String!, $teamId: String!) {
            issueLabelCreate(input: { name: $name, teamId: $teamId }) {
                success
                issueLabel { id name }
            }
        }
    """
    variables = {"name": name, "teamId": TEAM_ID}
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("issueLabelCreate", {}).get("success"):
        label = data["data"]["issueLabelCreate"]["issueLabel"]
        print(f"   ✅ 成功 (ID: {label['id']})")
        return label
    print("   ❌ 失敗")
    return None


def create_issue(project_id, milestone_id, label_ids, title):
    print(f"4. Issueを作成中: '{title}'...")
    query = """
        mutation CreateIssue(
            $teamId: String!, $title: String!, $projectId: String!,
            $projectMilestoneId: String!, $labelIds: [String!]!
        ) {
            issueCreate(input: {
                teamId: $teamId,
                title: $title,
                projectId: $projectId,
                projectMilestoneId: $projectMilestoneId,
                labelIds: $labelIds
            }) {
                success
                issue { id identifier }
            }
        }
    """
    variables = {
        "teamId": TEAM_ID,
        "title": title,
        "projectId": project_id,
        "projectMilestoneId": milestone_id,
        "labelIds": label_ids,
    }
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("issueCreate", {}).get("success"):
        issue = data["data"]["issueCreate"]["issue"]
        print(f"   ✅ 成功 (ID: {issue['identifier']})")
        return issue
    print("   ❌ 失敗")
    return None


def update_issue(issue_id, new_title, new_description):
    print(f"5. Issueを編集中: '{new_title}'...")
    query = """
        mutation UpdateIssue($id: String!, $title: String!, $description: String!) {
            issueUpdate(input: { title: $title, description: $description }, id: $id) {
                success
            }
        }
    """
    variables = {"id": issue_id, "title": new_title, "description": new_description}
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("issueUpdate", {}).get("success"):
        print("   ✅ 成功")
        return True
    print("   ❌ 失敗")
    return False


def create_comment(issue_id, body):
    print(f"6. コメントを追加中...")
    query = """
        mutation CreateComment($issueId: String!, $body: String!) {
            commentCreate(input: { issueId: $issueId, body: $body }) {
                success
            }
        }
    """
    variables = {"issueId": issue_id, "body": body}
    data = run_graphql_query(query, variables)
    if data and data.get("data", {}).get("commentCreate", {}).get("success"):
        print("   ✅ 成功")
        return True
    print("   ❌ 失敗")
    return False


# --- メイン処理 ---


def main():
    parser = argparse.ArgumentParser(
        description="Linearのプロジェクト作成からコメント追加までの一連のワークフローを実行します。",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "project_name", help="作成するプロジェクトの基本名。\n例: 'My New Feature'"
    )
    args = parser.parse_args()

    base_name = args.project_name

    print(f"--- Linearフルワークフローを開始します (ベース名: {base_name}) ---")

    # 1. プロジェクト作成
    project = create_project(f"Project: {base_name}")
    if not project:
        return

    # 2. マイルストーン作成
    milestone = create_milestone(project["id"], f"Milestone 1 for {base_name}")
    if not milestone:
        return

    # 3. ラベル作成
    label = create_label(f"Label-{base_name.replace(' ', '-')}")
    if not label:
        return

    # 4. Issue作成
    issue = create_issue(
        project["id"], milestone["id"], [label["id"]], f"Implement {base_name}"
    )
    if not issue:
        return

    # 5. Issue編集
    update_success = update_issue(
        issue["id"],
        f"【実装】{base_name}",
        f"この課題は「{base_name}」の実装を管理します。\n自動スクリプトによって作成されました。",
    )
    if not update_success:
        return

    # 6. コメント追加
    comment_success = create_comment(
        issue["id"], "ワークフローの初期設定が完了しました。実装を開始してください。"
    )
    if not comment_success:
        return

    print(f"--- ワークフローが正常に完了しました ---")


if __name__ == "__main__":
    # このスクリプトはrequestsライブラリが必要です。
    # pip install requests
    main()
