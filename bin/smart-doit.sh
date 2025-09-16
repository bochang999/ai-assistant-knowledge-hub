#!/bin/bash
# smart-doit.sh - Enhanced doit command with mandatory workflow verification

ISSUE_NUM=$1
if [ -z "$ISSUE_NUM" ]; then
    echo "Usage: smart-doit.sh BOC-XX"
    exit 1
fi

echo "🔍 BOC-$ISSUE_NUM 解析開始..."

# Linear APIでIssue詳細取得
ISSUE_DATA=$(curl -s -H "Authorization: $(cat ~/.linear-api-key)" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"query{issue(id:\\\"BOC-$ISSUE_NUM\\\"){title description}}\"}" \
  "https://api.linear.app/graphql")

# 問題種別自動判定
TITLE=$(echo $ISSUE_DATA | jq -r '.data.issue.title')
DESC=$(echo $ISSUE_DATA | jq -r '.data.issue.description')

echo "📋 Issue情報:"
echo "Title: $TITLE"
echo "Description: $DESC"
echo ""

# ワークフロー種別判定
if [[ "$TITLE" =~ ビルドエラー|build.*error|workflow.*fail|GitHub.*Actions ]]; then
    WORKFLOW_TYPE="build_error_correction"
    echo "🔧 判定: ビルドエラー系 → build_error_correction workflow"
elif [[ "$TITLE" =~ UI|画面|表示|レイアウト ]]; then
    WORKFLOW_TYPE="ui_problem"
    echo "🎨 判定: UI問題系 → ui_problem workflow"
elif [[ "$TITLE" =~ API|サーバー|データベース ]]; then
    WORKFLOW_TYPE="api_problem"
    echo "🌐 判定: API問題系 → api_problem workflow"
else
    WORKFLOW_TYPE="general"
    echo "⚡判定: 一般問題 → general workflow"
fi

echo ""
echo "📋 該当ワークフローを表示します:"
echo "=================================="

# 該当ワークフロー強制表示
WORKFLOW_PATH="$HOME/ai-assistant-knowledge-hub/workflows/${WORKFLOW_TYPE}.md"
if [ -f "$WORKFLOW_PATH" ]; then
    cat "$WORKFLOW_PATH"
else
    echo "⚠️ ワークフローファイルが見つかりません: $WORKFLOW_PATH"
    echo "利用可能なワークフロー:"
    ls -1 "$HOME/ai-assistant-knowledge-hub/workflows/"*.md 2>/dev/null || echo "ワークフローディレクトリが見つかりません"
fi

echo ""
echo "=================================="
echo "⚠️  上記ワークフローを読んで理解しましたか？"
echo "理解完了後に 'y' を入力してください (n で中止):"
read -r confirmation

if [[ "$confirmation" != "y" ]]; then
    echo "❌ ワークフロー確認が完了していません"
    echo "💡 ワークフローを再度確認してから作業を開始してください"
    exit 1
fi

echo ""
echo "✅ ワークフロー確認完了"
echo ""
echo "🔄 MANDATORY: ai-assistant-knowledge-hubシステム確認を開始します..."
echo "🚫 この確認完了まで Issue作業は開始できません"
echo ""

# 強制的なシステム構造確認
echo "📋 1. プロジェクトマップ確認中..."
PROJECT_MAP="$HOME/ai-assistant-knowledge-hub/project_map.json"
if [ -f "$PROJECT_MAP" ]; then
    echo "✅ project_map.json found:"
    cat "$PROJECT_MAP"
else
    echo "❌ project_map.json not found at $PROJECT_MAP"
    exit 1
fi

echo ""
echo "📋 2. Issue詳細とプロジェクトタグ確認中..."
ISSUE_DETAIL_FILE="$HOME/ai-assistant-knowledge-hub/temp/agent_issue_BOC-$ISSUE_NUM.json"
if [ -f "$ISSUE_DETAIL_FILE" ]; then
    echo "✅ Issue詳細ファイル found:"
    cat "$ISSUE_DETAIL_FILE"

    # プロジェクト名抽出
    PROJECT_NAME=$(cat "$ISSUE_DETAIL_FILE" | jq -r '.data.issue.project.name' 2>/dev/null)
    if [ "$PROJECT_NAME" != "null" ] && [ -n "$PROJECT_NAME" ]; then
        echo ""
        echo "🎯 対象プロジェクト: $PROJECT_NAME"
    else
        echo "❌ プロジェクトタグが見つかりません"
        exit 1
    fi
else
    echo "❌ Issue詳細ファイルが見つかりません: $ISSUE_DETAIL_FILE"
    echo "💡 Linear APIから取得します..."

    # Issue詳細をLinear APIから取得して保存
    mkdir -p "$HOME/ai-assistant-knowledge-hub/temp"
    FULL_ISSUE_DATA=$(curl -s -H "Authorization: $(cat ~/.linear-api-key)" \
      -H "Content-Type: application/json" \
      -d "{\"query\":\"query{issue(id:\\\"BOC-$ISSUE_NUM\\\"){id title description state{name} project{name} labels{nodes{name}}}}\"}" \
      "https://api.linear.app/graphql")

    echo "$FULL_ISSUE_DATA" > "$ISSUE_DETAIL_FILE"
    echo "✅ Issue詳細を取得・保存しました:"
    cat "$ISSUE_DETAIL_FILE"

    PROJECT_NAME=$(echo "$FULL_ISSUE_DATA" | jq -r '.data.issue.project.name' 2>/dev/null)
    if [ "$PROJECT_NAME" != "null" ] && [ -n "$PROJECT_NAME" ]; then
        echo ""
        echo "🎯 対象プロジェクト: $PROJECT_NAME"
    else
        echo "❌ プロジェクトタグが見つかりません"
        exit 1
    fi
fi

echo ""
echo "📋 3. 対象プロジェクトディレクトリ確認中..."
# project_map.jsonからプロジェクトパス取得
PROJECT_PATH=$(cat "$PROJECT_MAP" | jq -r ".\"$PROJECT_NAME\"" 2>/dev/null)
if [ "$PROJECT_PATH" != "null" ] && [ -n "$PROJECT_PATH" ] && [ -d "$PROJECT_PATH" ]; then
    echo "✅ プロジェクトディレクトリ found: $PROJECT_PATH"
    echo "📂 ディレクトリ構造:"
    ls -la "$PROJECT_PATH" | head -10
else
    echo "❌ プロジェクトディレクトリが見つかりません: $PROJECT_PATH"
    exit 1
fi

echo ""
echo "✅ ai-assistant-knowledge-hubシステム確認完了"
echo "🚀 AI作業開始指示:"
echo "   対象プロジェクト: $PROJECT_NAME"
echo "   プロジェクトパス: $PROJECT_PATH"
echo "   Phase 2 (事実収集) から開始してください"
echo "   - 対象プロジェクトのビルドシステム確認"
echo "   - エラー箇所特定"
echo "   - 詳細ログ取得"
echo "   - 関連コード特定"
echo "   - 事実レポート作成"
echo ""
echo "📝 Issue URL: https://linear.app/bochang-lab/issue/BOC-$ISSUE_NUM"