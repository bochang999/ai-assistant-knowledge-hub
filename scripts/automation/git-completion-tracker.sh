#!/bin/bash
# Git完了確認システム
# BOC-83問題の再発防止: コミット・プッシュ完了を確実に追跡

set -e

ensure_git_completion() {
    local issue_id="$1"

    echo "🔍 Git作業完了確認開始"

    # Gitリポジトリ確認
    if [ ! -d ".git" ]; then
        echo "❌ 現在のディレクトリはGitリポジトリではありません"
        return 1
    fi

    local repo_url=$(git remote get-url origin 2>/dev/null || echo "N/A")
    local current_branch=$(git branch --show-current 2>/dev/null || echo "N/A")

    echo "📋 Git情報:"
    echo "   📂 Repository: $repo_url"
    echo "   🌿 Branch: $current_branch"

    # 1. 未コミット変更チェック
    echo "🔍 未コミット変更チェック..."

    local unstaged_changes=$(git diff --name-only | wc -l)
    local staged_changes=$(git diff --cached --name-only | wc -l)

    if [ "$unstaged_changes" -gt 0 ]; then
        echo "⚠️ $unstaged_changes 個の未ステージ変更があります:"
        git diff --name-only | sed 's/^/     📄 /'
        echo ""
        echo "💡 以下のコマンドでステージできます:"
        echo "   git add ."
        echo ""
    fi

    if [ "$staged_changes" -gt 0 ]; then
        echo "⚠️ $staged_changes 個の未コミット変更があります:"
        git diff --cached --name-only | sed 's/^/     📄 /'
        echo ""
        echo "💡 以下のコマンドでコミットできます:"
        echo "   git commit -m \"🔧 $issue_id: [作業内容を記述]\""
        echo ""
    fi

    # 2. プッシュ状況確認
    echo "🔍 プッシュ状況チェック..."

    # リモートブランチとの比較
    git fetch origin "$current_branch" 2>/dev/null || echo "⚠️ リモートフェッチに失敗"

    local unpushed_commits=0
    if git rev-parse "@{u}" >/dev/null 2>&1; then
        unpushed_commits=$(git log "@{u}..HEAD" --oneline | wc -l)
    else
        echo "⚠️ リモートブランチが設定されていません"
        unpushed_commits=$(git log --oneline | wc -l)
    fi

    if [ "$unpushed_commits" -gt 0 ]; then
        echo "⚠️ $unpushed_commits 個のコミットがプッシュされていません:"
        if git rev-parse "@{u}" >/dev/null 2>&1; then
            git log "@{u}..HEAD" --oneline | sed 's/^/     📝 /'
        else
            git log --oneline | head -5 | sed 's/^/     📝 /'
        fi
        echo ""
        echo "💡 以下のコマンドでプッシュできます:"
        echo "   git push origin $current_branch"
        echo ""
    fi

    # 3. 作業状況サマリー
    echo "📊 Git作業状況サマリー:"
    echo "   📄 未ステージ変更: $unstaged_changes"
    echo "   📝 未コミット変更: $staged_changes"
    echo "   🚀 未プッシュコミット: $unpushed_commits"

    # 4. 完了判定
    if [ "$unstaged_changes" -eq 0 ] && [ "$staged_changes" -eq 0 ] && [ "$unpushed_commits" -eq 0 ]; then
        echo "✅ Git作業完了確認: すべて同期済み"

        # 完了情報を保存
        mkdir -p /tmp/claude-automation
        echo "completed" > "/tmp/claude-automation/git-status"
        echo "$(date '+%Y-%m-%d %H:%M:%S')" > "/tmp/claude-automation/git-completion-time"

        return 0
    else
        echo "⚠️ Git作業未完了: 上記の問題を解決してください"
        echo "incomplete" > "/tmp/claude-automation/git-status"
        return 1
    fi
}

# GitHub認証設定確認
check_github_auth() {
    echo "🔑 GitHub認証確認..."

    # GitHub CLI確認
    if command -v gh >/dev/null 2>&1; then
        if gh auth status >/dev/null 2>&1; then
            echo "✅ GitHub CLI認証済み"
            return 0
        else
            echo "⚠️ GitHub CLI未認証"
        fi
    fi

    # Git credentials確認
    if [ -f ~/.git-credentials ]; then
        echo "✅ Git credentials設定済み"
        return 0
    fi

    # GitHub token確認
    if [ -f ~/.github-token ]; then
        echo "✅ GitHub token設定済み"
        return 0
    fi

    echo "❌ GitHub認証が設定されていません"
    echo "💡 以下のいずれかを設定してください:"
    echo "   1. gh auth login"
    echo "   2. ~/.github-token にPersonal Access Tokenを保存"
    echo "   3. git config credential.helper store"

    return 1
}

# 自動プッシュ機能（オプション）
auto_push_if_ready() {
    local issue_id="$1"
    local force_push="$2"

    if [ "$force_push" != "--force" ]; then
        echo "🤔 自動プッシュを実行しますか？ (--forceフラグを付けて実行してください)"
        return 1
    fi

    echo "🚀 自動プッシュ実行..."

    # 認証確認
    if ! check_github_auth; then
        return 1
    fi

    # 未ステージ変更がある場合は自動ステージ
    if [ "$(git diff --name-only | wc -l)" -gt 0 ]; then
        echo "📝 未ステージ変更を自動ステージ中..."
        git add .
    fi

    # 未コミット変更がある場合は自動コミット
    if [ "$(git diff --cached --name-only | wc -l)" -gt 0 ]; then
        echo "💾 未コミット変更を自動コミット中..."
        git commit -m "🔧 $issue_id: 自動完了コミット

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    fi

    # プッシュ実行
    local current_branch=$(git branch --show-current)
    echo "📤 プッシュ実行: $current_branch"

    if git push origin "$current_branch"; then
        echo "✅ プッシュ完了"
        return 0
    else
        echo "❌ プッシュ失敗"
        return 1
    fi
}

# スクリプトが直接実行された場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    case "$1" in
        "--auto-push")
            auto_push_if_ready "$2" "--force"
            ;;
        "--check-auth")
            check_github_auth
            ;;
        *)
            ensure_git_completion "$1"
            ;;
    esac
fi
