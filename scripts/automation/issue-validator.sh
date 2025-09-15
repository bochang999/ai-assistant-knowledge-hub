#!/bin/bash
# Issue-Project自動マッピングシステム
# BOC-83問題の再発防止: 正しいプロジェクトを自動特定

set -e

validate_issue_project() {
    local issue_id="$1"

    if [ -z "$issue_id" ]; then
        echo "❌ Issue IDが指定されていません"
        return 1
    fi

    # Linear API keyチェック
    if [ ! -f ~/.linear-api-key ]; then
        echo "❌ Linear API keyが見つかりません (~/.linear-api-key)"
        return 1
    fi

    echo "🔍 Issue検証開始: $issue_id"

    # Issue番号抽出 (BOC-83 → 83)
    local issue_number=$(echo "$issue_id" | sed 's/.*-//')

    # Linear GraphQL クエリ
    local query_json=$(cat << EOF
{
  "query": "query { issues(filter: { number: { eq: $issue_number } }) { nodes { id title description state { id name } project { name } } }}"
}
EOF
)

    # API呼び出し
    local response=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "$query_json")

    # レスポンス確認
    if echo "$response" | jq -e '.errors' > /dev/null 2>&1; then
        echo "❌ Linear API エラー:"
        echo "$response" | jq '.errors'
        return 1
    fi

    # プロジェクト名抽出
    local project_name=$(echo "$response" | jq -r '.data.issues.nodes[0].project.name // "Unknown"')
    local issue_title=$(echo "$response" | jq -r '.data.issues.nodes[0].title // "Unknown"')
    local issue_state=$(echo "$response" | jq -r '.data.issues.nodes[0].state.name // "Unknown"')

    if [ "$project_name" = "Unknown" ] || [ "$project_name" = "null" ]; then
        echo "❌ Issue $issue_id が見つからないか、プロジェクトが設定されていません"
        return 1
    fi

    echo "✅ Issue情報確認完了:"
    echo "   📋 ID: $issue_id"
    echo "   📝 Title: $issue_title"
    echo "   📊 State: $issue_state"
    echo "   📂 Project: $project_name"

    # プロジェクト情報を一時ファイルに保存
    mkdir -p /tmp/claude-automation
    echo "$project_name" > "/tmp/claude-automation/current-project"
    echo "$issue_title" > "/tmp/claude-automation/current-issue-title"
    echo "$issue_state" > "/tmp/claude-automation/current-issue-state"
    echo "$issue_id" > "/tmp/claude-automation/current-issue-id"

    return 0
}

# スクリプトが直接実行された場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    validate_issue_project "$1"
fi
