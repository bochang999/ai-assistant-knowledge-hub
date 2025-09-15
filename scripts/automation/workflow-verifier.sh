#!/bin/bash
# GitHub Actions ワークフロー検証システム
# BOC-83問題の再発防止: ワークフロー実行状況を自動確認

set -e

verify_github_actions() {
    local repo="$1"
    local branch="$2"

    echo "🔄 GitHub Actions ワークフロー検証開始"

    # パラメータ自動取得
    if [ -z "$repo" ]; then
        local repo_url=$(git remote get-url origin 2>/dev/null)
        if [ -n "$repo_url" ]; then
            repo=$(echo "$repo_url" | sed 's|.*github.com[/:]||' | sed 's|\.git$||')
        else
            echo "❌ リポジトリ情報が取得できません"
            return 1
        fi
    fi

    if [ -z "$branch" ]; then
        branch=$(git branch --show-current 2>/dev/null || echo "main")
    fi

    echo "📋 ワークフロー情報:"
    echo "   📂 Repository: $repo"
    echo "   🌿 Branch: $branch"

    # GitHub CLI確認
    if ! command -v gh >/dev/null 2>&1; then
        echo "⚠️ GitHub CLI (gh) がインストールされていません"
        echo "💡 curl を使用してAPI直接呼び出しを試みます..."
        verify_with_curl_api "$repo" "$branch"
        return $?
    fi

    # GitHub CLI認証確認
    if ! gh auth status >/dev/null 2>&1; then
        echo "⚠️ GitHub CLI認証が必要です"
        echo "💡 以下のコマンドで認証してください: gh auth login"
        return 1
    fi

    echo "🔍 最新のワークフロー実行を確認中..."

    # 最新のワークフロー実行を取得
    local workflow_data=$(gh api "repos/$repo/actions/runs?branch=$branch&per_page=5" 2>/dev/null)

    if [ $? -ne 0 ]; then
        echo "❌ GitHub Actions API呼び出しに失敗しました"
        return 1
    fi

    # ワークフロー実行の解析
    local total_runs=$(echo "$workflow_data" | jq '.total_count // 0')

    if [ "$total_runs" -eq 0 ]; then
        echo "⚠️ このブランチにはワークフロー実行履歴がありません"
        return 1
    fi

    echo "📊 ワークフロー実行状況 (最新5件):"

    # 最新5件のワークフロー実行を表示
    echo "$workflow_data" | jq -r '.workflow_runs[] | "\(.created_at) | \(.status) | \(.conclusion // "running") | \(.name)"' | while IFS='|' read -r created status conclusion name; do
        local created_formatted=$(date -d "$created" '+%m/%d %H:%M' 2>/dev/null || echo "$created")
        local status_icon="❓"
        local conclusion_icon="❓"

        case "$status" in
            "completed") status_icon="✅" ;;
            "in_progress") status_icon="🔄" ;;
            "queued") status_icon="⏳" ;;
            *) status_icon="❓" ;;
        esac

        case "$conclusion" in
            "success") conclusion_icon="🎉" ;;
            "failure") conclusion_icon="❌" ;;
            "cancelled") conclusion_icon="🚫" ;;
            "running") conclusion_icon="🔄" ;;
            *) conclusion_icon="❓" ;;
        esac

        echo "   $created_formatted $status_icon $conclusion_icon $(echo "$name" | tr -d '[:space:]')"
    done

    # 最新実行の詳細確認
    local latest_run=$(echo "$workflow_data" | jq -r '.workflow_runs[0]')
    local latest_status=$(echo "$latest_run" | jq -r '.status')
    local latest_conclusion=$(echo "$latest_run" | jq -r '.conclusion // "running"')
    local latest_created=$(echo "$latest_run" | jq -r '.created_at')
    local latest_url=$(echo "$latest_run" | jq -r '.html_url')

    echo ""
    echo "🎯 最新ワークフロー実行:"
    echo "   📅 作成日時: $(date -d "$latest_created" '+%Y/%m/%d %H:%M:%S' 2>/dev/null || echo "$latest_created")"
    echo "   📊 Status: $latest_status"
    echo "   🎯 Result: $latest_conclusion"
    echo "   🔗 URL: $latest_url"

    # 結果の判定
    case "$latest_conclusion" in
        "success")
            echo "✅ 最新ワークフローは成功しました"
            echo "completed" > "/tmp/claude-automation/workflow-status"
            return 0
            ;;
        "failure")
            echo "❌ 最新ワークフローが失敗しました"
            echo "🔍 失敗の詳細を確認してください: $latest_url"
            echo "failed" > "/tmp/claude-automation/workflow-status"
            return 1
            ;;
        "cancelled")
            echo "🚫 最新ワークフローがキャンセルされました"
            echo "cancelled" > "/tmp/claude-automation/workflow-status"
            return 1
            ;;
        *)
            if [ "$latest_status" = "in_progress" ]; then
                echo "🔄 ワークフローは実行中です"
                echo "💡 完了まで待機するか、以下のURLで進捗を確認してください:"
                echo "   $latest_url"
                echo "running" > "/tmp/claude-automation/workflow-status"
                return 0
            else
                echo "❓ ワークフロー状況が不明です"
                echo "unknown" > "/tmp/claude-automation/workflow-status"
                return 1
            fi
            ;;
    esac
}

# curl API使用版（GitHub CLI未使用環境用）
verify_with_curl_api() {
    local repo="$1"
    local branch="$2"

    echo "🌐 GitHub API (curl) でワークフロー確認中..."

    # GitHub token確認
    local github_token=""
    if [ -f ~/.github-token ]; then
        github_token=$(cat ~/.github-token)
    elif [ -n "$GITHUB_TOKEN" ]; then
        github_token="$GITHUB_TOKEN"
    else
        echo "❌ GitHub tokenが見つかりません"
        echo "💡 ~/.github-token にPersonal Access Tokenを保存してください"
        return 1
    fi

    # API呼び出し
    local response=$(curl -s -H "Authorization: token $github_token" \
        "https://api.github.com/repos/$repo/actions/runs?branch=$branch&per_page=3")

    # レスポンス確認
    if echo "$response" | jq -e '.message' >/dev/null 2>&1; then
        echo "❌ GitHub API エラー:"
        echo "$response" | jq '.message'
        return 1
    fi

    # 簡易表示
    local total_runs=$(echo "$response" | jq '.total_count // 0')
    if [ "$total_runs" -eq 0 ]; then
        echo "⚠️ ワークフロー実行履歴がありません"
        return 1
    fi

    local latest_status=$(echo "$response" | jq -r '.workflow_runs[0].status')
    local latest_conclusion=$(echo "$response" | jq -r '.workflow_runs[0].conclusion // "running"')

    echo "📊 最新ワークフロー: $latest_status / $latest_conclusion"

    case "$latest_conclusion" in
        "success") echo "✅ 成功"; return 0 ;;
        "failure") echo "❌ 失敗"; return 1 ;;
        *) echo "🔄 実行中または不明"; return 0 ;;
    esac
}

# ワークフロー実行待機機能
wait_for_workflow_completion() {
    local repo="$1"
    local branch="$2"
    local max_wait_minutes="${3:-30}"

    echo "⏳ ワークフロー完了待機開始 (最大${max_wait_minutes}分)"

    local wait_seconds=$((max_wait_minutes * 60))
    local check_interval=60  # 1分間隔でチェック

    for ((i=0; i<wait_seconds; i+=check_interval)); do
        echo "🔍 ワークフロー状況確認中... ($((i/60))分経過)"

        if verify_github_actions "$repo" "$branch" >/dev/null 2>&1; then
            local status=$(cat "/tmp/claude-automation/workflow-status" 2>/dev/null || echo "unknown")

            case "$status" in
                "completed")
                    echo "✅ ワークフロー完了確認"
                    return 0
                    ;;
                "failed"|"cancelled")
                    echo "❌ ワークフロー失敗またはキャンセル"
                    return 1
                    ;;
                "running")
                    echo "🔄 まだ実行中... (${check_interval}秒後に再確認)"
                    sleep $check_interval
                    ;;
                *)
                    echo "❓ 不明な状況"
                    sleep $check_interval
                    ;;
            esac
        else
            echo "⚠️ ワークフロー確認エラー"
            sleep $check_interval
        fi
    done

    echo "⏰ タイムアウト: ${max_wait_minutes}分経過しました"
    return 1
}

# スクリプトが直接実行された場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    case "$1" in
        "--wait")
            wait_for_workflow_completion "$2" "$3" "$4"
            ;;
        *)
            verify_github_actions "$1" "$2"
            ;;
    esac
fi
