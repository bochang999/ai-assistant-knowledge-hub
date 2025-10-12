#!/bin/bash
# setup-filesystem-claude.sh
# Claude Code用Filesystem MCPセットアップスクリプト

set -e  # エラーで停止

echo "📁 Claude Code - Filesystem MCP セットアップ"
echo "=============================================="

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
echo "📦 Step 1/4: @modelcontextprotocol/server-filesystem 確認中..."
if ! command -v mcp-server-filesystem &> /dev/null; then
    echo "⚠️  mcp-server-filesystem が見つかりません"
    echo "💡 インストール中..."
    npm install -g @modelcontextprotocol/server-filesystem
    echo "✅ インストール完了"
else
    echo "✅ mcp-server-filesystem: インストール済み"
fi

# Step 2: .claude.json確認
echo ""
echo "📂 Step 2/4: .claude.json確認中..."
if [ ! -f ".claude.json" ]; then
    echo "⚠️  .claude.json が見つかりません"
    echo "💡 このスクリプトは ai-assistant-knowledge-hub ディレクトリから実行してください"
    exit 1
fi
echo "✅ .claude.json: 存在"

# Step 3: バックアップ作成
echo ""
echo "💾 Step 3/4: .claude.json バックアップ作成中..."
BACKUP_FILE=".claude.json.backup.$(date +%Y%m%d_%H%M%S)"
cp .claude.json "$BACKUP_FILE"
echo "✅ バックアップ作成: $BACKUP_FILE"

# Step 4: Filesystem MCP設定追加
echo ""
echo "📝 Step 4/4: Filesystem MCP設定追加中..."

# jqがあれば使用、なければ手動編集
if command -v jq &> /dev/null; then
    # args配列を構築
    ARGS_JSON='['
    for i in "${!DEFAULT_DIRS[@]}"; do
        if [ $i -gt 0 ]; then
            ARGS_JSON+=','
        fi
        ARGS_JSON+="\"${DEFAULT_DIRS[$i]}\""
    done
    ARGS_JSON+=']'

    # jqで設定を追加
    jq --argjson args "$ARGS_JSON" \
       '.mcpServers.filesystem = {
          type: "stdio",
          command: "mcp-server-filesystem",
          args: $args,
          env: {}
        }' .claude.json > .claude.json.tmp && mv .claude.json.tmp .claude.json

    echo "✅ .claude.json を更新しました（jqを使用）"
else
    echo "⚠️  jqがインストールされていません"
    echo "💡 手動で .claude.json を編集してください:"
    echo ""
    echo '{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "mcp-server-filesystem",
      "args": [
        "/data/data/com.termux/files/home",
        "/storage/emulated/0/Download"
      ],
      "env": {}
    }
  }
}'
    exit 1
fi

# 設定内容表示
echo ""
echo "📋 .claude.json の内容:"
echo "----------------------------------------"
cat .claude.json
echo "----------------------------------------"

echo ""
echo "======================================"
echo "🎉 Claude Code - Filesystem MCP セットアップ完了！"
echo ""
echo "📋 次のステップ:"
echo "   1. Claude Codeを完全に再起動"
echo "   2. 新しいセッションで '/mcp list' を実行"
echo "   3. 'filesystem: Connected' が表示されることを確認"
echo ""
echo "💡 Filesystemツールの使用例:"
echo "   AIに 'list_directoryツールでホームディレクトリの内容を表示して' と依頼"
echo ""
echo "📖 詳細ガイド:"
echo "   cat FILESYSTEM-MCP-SETUP-GUIDE.md"
echo ""
