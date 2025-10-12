#!/bin/bash
# setup-filesystem-gemini.sh
# Gemini CLI用Filesystem MCPセットアップスクリプト

set -e  # エラーで停止

echo "📁 Gemini CLI - Filesystem MCP セットアップ"
echo "============================================"

# デフォルトの許可ディレクトリ
DEFAULT_DIRS=(
    "/data/data/com.termux/files/home"
    "/storage/emulated/0/Download"
)

echo ""
echo "📋 このスクリプトは以下のディレクトリへのアクセスを許可します:"
for dir in "${DEFAULT_DIRS[@]}"; do
    echo "   - $dir"
done
echo ""

read -p "これらのディレクトリで続行しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ セットアップを中止しました"
    exit 0
fi

echo ""
echo "======================================"
echo ""

# Step 1: NPMパッケージ確認
echo "📦 Step 1/5: @modelcontextprotocol/server-filesystem 確認中..."
if ! command -v mcp-server-filesystem &> /dev/null; then
    echo "⚠️  mcp-server-filesystem が見つかりません"
    echo "💡 インストール中..."
    npm install -g @modelcontextprotocol/server-filesystem
    echo "✅ インストール完了"
else
    echo "✅ mcp-server-filesystem: インストール済み"
fi

# Step 2: Gemini CLI確認
echo ""
echo "🔍 Step 2/5: Gemini CLI確認中..."
if ! command -v gemini &> /dev/null; then
    echo "❌ Gemini CLIが見つかりません"
    echo "💡 インストール方法: https://ai.google.dev/gemini-api/docs/cli"
    exit 1
fi
echo "✅ Gemini CLI: インストール済み"

# Step 3: プロジェクトディレクトリに移動
echo ""
echo "📂 Step 3/5: プロジェクトディレクトリ確認中..."
if [ ! -f ".gemini/settings.json" ]; then
    echo "⚠️  .gemini/settings.json が見つかりません"
    echo "💡 このスクリプトは ai-assistant-knowledge-hub ディレクトリから実行してください"
    exit 1
fi
echo "✅ プロジェクトディレクトリ: 確認済み"

# Step 4: 既存のFilesystem MCP設定確認
echo ""
echo "🔍 Step 4/5: 既存のMCP設定確認中..."
EXISTING_FS=$(gemini mcp list 2>/dev/null | grep -c "filesystem:" || echo "0")
if [ "$EXISTING_FS" -gt 0 ]; then
    echo "⚠️  Filesystem MCPサーバーが既に登録されています"
    echo ""
    gemini mcp list | grep "filesystem:"
    echo ""
    read -p "上書きしますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  既存のFilesystem設定を削除中..."
        gemini mcp remove filesystem
        echo "✅ 削除完了"
    else
        echo "❌ セットアップを中止しました"
        exit 0
    fi
fi

# Step 5: Filesystem MCP追加
echo ""
echo "➕ Step 5/5: Filesystem MCPサーバー登録中..."

# 引数配列を構築
ARGS_STRING="mcp-server-filesystem"
for dir in "${DEFAULT_DIRS[@]}"; do
    ARGS_STRING="$ARGS_STRING $dir"
done

gemini mcp add filesystem $ARGS_STRING

# 登録確認
echo ""
echo "✅ 登録確認中..."
sleep 1
gemini mcp list

echo ""
echo "======================================"
echo "🎉 Gemini CLI - Filesystem MCP セットアップ完了！"
echo ""
echo "📋 設定ファイル:"
echo "   $(pwd)/.gemini/settings.json"
echo ""
echo "🔍 接続確認:"
echo "   gemini mcp list"
echo ""
echo "🚀 Gemini CLIを起動して使用開始:"
echo "   gemini"
echo ""
echo "💡 Filesystemツールの使用例:"
echo "   AIに 'list_directoryツールでホームディレクトリの内容を表示して' と依頼"
echo ""
echo "📖 詳細ガイド:"
echo "   cat FILESYSTEM-MCP-SETUP-GUIDE.md"
echo ""
