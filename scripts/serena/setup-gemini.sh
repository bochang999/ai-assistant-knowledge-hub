#!/bin/bash
# setup-gemini.sh
# Gemini CLI用Serena MCPセットアップスクリプト

set -e  # エラーで停止

echo "🤖 Gemini CLI - Serena MCP セットアップ"
echo "======================================"

# プロジェクトパス取得
if [ -n "$1" ]; then
    PROJECT_PATH="$1"
else
    PROJECT_PATH="$(pwd)"
fi

# 絶対パスに変換
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)

echo "📁 プロジェクトパス: $PROJECT_PATH"
echo ""

# Step 1: Gemini CLI確認
echo "🔍 Step 1/5: Gemini CLI確認中..."
if ! command -v gemini &> /dev/null; then
    echo "❌ Gemini CLIが見つかりません"
    echo "💡 インストール方法: https://ai.google.dev/gemini-api/docs/cli"
    exit 1
fi
echo "✅ Gemini CLI: インストール済み"

# Step 2: プロジェクトディレクトリに移動
echo ""
echo "📂 Step 2/5: プロジェクトディレクトリに移動中..."
cd "$PROJECT_PATH"
echo "✅ カレントディレクトリ: $(pwd)"

# Step 3: プロジェクトインデックス確認
echo ""
echo "📊 Step 3/5: プロジェクトインデックス確認中..."
if [ ! -d ".serena/cache" ]; then
    echo "⚠️  プロジェクトインデックスが見つかりません"
    echo "💡 先に以下のコマンドを実行してください:"
    echo "   ./scripts/serena/index-project.sh $PROJECT_PATH"
    exit 1
fi
echo "✅ プロジェクトインデックス: 存在"

# Step 4: 既存のSerena MCP設定確認
echo ""
echo "🔍 Step 4/5: 既存のMCP設定確認中..."
EXISTING_MCP=$(gemini mcp list 2>/dev/null | grep -c "serena:" || echo "0")
if [ "$EXISTING_MCP" -gt 0 ]; then
    echo "⚠️  Serena MCPサーバーが既に登録されています"
    echo ""
    gemini mcp list | grep "serena:"
    echo ""
    read -p "上書きしますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  既存のSerena設定を削除中..."
        gemini mcp remove serena
        echo "✅ 削除完了"
    else
        echo "❌ セットアップを中止しました"
        exit 0
    fi
fi

# Step 5: Serena MCP追加
echo ""
echo "➕ Step 5/5: Serena MCPサーバー登録中..."
gemini mcp add serena uv run serena start-mcp-server --project "$PROJECT_PATH"

# 登録確認
echo ""
echo "✅ 登録確認中..."
sleep 1
gemini mcp list

echo ""
echo "======================================"
echo "🎉 Gemini CLI - Serena MCP セットアップ完了！"
echo ""
echo "📋 設定ファイル:"
echo "   $PROJECT_PATH/.gemini/settings.json"
echo ""
echo "🔍 接続確認:"
echo "   gemini mcp list"
echo ""
echo "🚀 Gemini CLIを起動して使用開始:"
echo "   gemini"
echo ""
echo "💡 Serenaツールの使用例:"
echo "   AIに 'Serenaのlist_directoryツールでプロジェクト構造を表示して' と依頼"
echo ""
