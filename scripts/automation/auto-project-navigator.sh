#!/bin/bash
# 自動プロジェクトナビゲーションシステム
# BOC-83問題の再発防止: 正しいプロジェクトディレクトリに自動移動

set -e

auto_navigate_to_project() {
    local project_name="$1"

    if [ -z "$project_name" ]; then
        echo "❌ プロジェクト名が指定されていません"
        return 1
    fi

    echo "🚀 プロジェクト自動ナビゲーション開始: $project_name"

    # プロジェクト名とディレクトリのマッピング
    case "$project_name" in
        "petit recipe")
            local target_dir="$HOME/petit-recipe"
            ;;
        "ai-assistant-knowledge-hub")
            local target_dir="$HOME/ai-assistant-knowledge-hub"
            ;;
        "RecipeBox")
            local target_dir="$HOME/recipebox-web"
            ;;
        "Laminator Dashboard")
            # 複数の可能性をチェック
            if [ -d "$HOME/laminator-dashboard" ]; then
                local target_dir="$HOME/laminator-dashboard"
            elif [ -d "$HOME/pwa-to-apk-template" ]; then
                local target_dir="$HOME/pwa-to-apk-template"
            else
                echo "❌ Laminator Dashboard プロジェクトディレクトリが見つかりません"
                return 1
            fi
            ;;
        *)
            echo "⚠️ 未知のプロジェクト: $project_name"
            echo "🔍 利用可能なディレクトリを検索中..."

            # ホームディレクトリで関連ディレクトリを検索
            local search_result=$(find "$HOME" -maxdepth 1 -type d -name "*$(echo "$project_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')*" | head -1)

            if [ -n "$search_result" ]; then
                local target_dir="$search_result"
                echo "📂 推測ディレクトリ: $target_dir"
            else
                echo "❌ プロジェクトディレクトリが見つかりません"
                echo "💡 使用可能なプロジェクト:"
                echo "   - petit recipe -> ~/petit-recipe"
                echo "   - ai-assistant-knowledge-hub -> ~/ai-assistant-knowledge-hub"
                echo "   - RecipeBox -> ~/recipebox-web"
                echo "   - Laminator Dashboard -> ~/laminator-dashboard"
                return 1
            fi
            ;;
    esac

    # ディレクトリ存在確認
    if [ ! -d "$target_dir" ]; then
        echo "❌ プロジェクトディレクトリが存在しません: $target_dir"
        return 1
    fi

    # ディレクトリに移動
    cd "$target_dir" || {
        echo "❌ ディレクトリ移動に失敗しました: $target_dir"
        return 1
    }

    echo "✅ プロジェクトディレクトリに移動完了"
    echo "📂 現在のディレクトリ: $(pwd)"

    # Gitリポジトリ確認
    if [ -d ".git" ]; then
        echo "🔧 Git情報:"
        echo "   📋 Repository: $(git remote get-url origin 2>/dev/null || echo 'N/A')"
        echo "   🌿 Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')"
        echo "   📊 Status: $(git status --porcelain | wc -l) 未コミット変更"
    else
        echo "⚠️ このディレクトリはGitリポジトリではありません"
    fi

    # プロジェクト情報を保存
    mkdir -p /tmp/claude-automation
    echo "$target_dir" > "/tmp/claude-automation/current-project-dir"

    return 0
}

# 保存されたプロジェクト情報から自動ナビゲーション
auto_navigate_from_cache() {
    local project_file="/tmp/claude-automation/current-project"

    if [ ! -f "$project_file" ]; then
        echo "❌ プロジェクト情報が見つかりません。先にissue-validatorを実行してください"
        return 1
    fi

    local project_name=$(cat "$project_file")
    auto_navigate_to_project "$project_name"
}

# スクリプトが直接実行された場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    if [ -n "$1" ]; then
        auto_navigate_to_project "$1"
    else
        auto_navigate_from_cache
    fi
fi
