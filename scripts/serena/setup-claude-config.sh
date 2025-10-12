#!/bin/bash
# setup-claude-config.sh
# Claude Code用.claude.json設定スクリプト

set -e  # エラーで停止

echo "⚙️  Claude Code 設定 (.claude.json)"
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

# プロジェクトディレクトリに移動
cd "$PROJECT_PATH"

# Step 1: 既存の.claude.json確認
echo "🔍 Step 1/3: 既存の.claude.json確認中..."
if [ -f ".claude.json" ]; then
    echo "⚠️  既存の.claude.jsonが見つかりました"
    echo ""

    # Serena設定が既に存在するか確認
    if grep -q '"serena"' .claude.json 2>/dev/null; then
        echo "ℹ️  Serena設定が既に存在します"
        echo ""
        echo "現在の設定:"
        cat .claude.json | jq '.mcpServers.serena' 2>/dev/null || cat .claude.json
        echo ""
        read -p "設定を上書きしますか？ (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ 処理を中止しました"
            exit 0
        fi
    fi

    # バックアップ作成
    BACKUP_FILE=".claude.json.backup.$(date +%Y%m%d_%H%M%S)"
    cp .claude.json "$BACKUP_FILE"
    echo "💾 バックアップ作成: $BACKUP_FILE"
fi

# Step 2: .claude.json作成または更新
echo ""
echo "📝 Step 2/3: .claude.json設定中..."

# jqがインストールされているか確認
if command -v jq &> /dev/null; then
    # jqを使って既存の設定を保持しながらSerenaを追加
    if [ -f ".claude.json" ]; then
        # 既存の.claude.jsonがある場合、Serena設定を追加/更新
        jq --arg project_path "$PROJECT_PATH" \
           '.mcpServers.serena = {
              "type": "stdio",
              "command": "uv",
              "args": ["run", "serena", "start-mcp-server", "--project", $project_path],
              "env": {}
            }' .claude.json > .claude.json.tmp && mv .claude.json.tmp .claude.json
    else
        # 新規作成
        jq -n --arg project_path "$PROJECT_PATH" \
           '{
              mcpServers: {
                serena: {
                  type: "stdio",
                  command: "uv",
                  args: ["run", "serena", "start-mcp-server", "--project", $project_path],
                  env: {}
                }
              }
            }' > .claude.json
    fi
    echo "✅ .claude.json を更新しました（jqを使用）"
else
    # jqがない場合はシンプルな設定を作成
    cat > .claude.json <<EOF
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "serena",
        "start-mcp-server",
        "--project",
        "$PROJECT_PATH"
      ],
      "env": {}
    }
  }
}
EOF
    echo "✅ .claude.json を作成しました"
    echo "⚠️  既存の設定は上書きされました（jqがインストールされていないため）"
fi

# Step 3: 設定内容確認
echo ""
echo "✅ Step 3/3: 設定内容確認"
echo ""
echo "📋 .claude.json の内容:"
echo "----------------------------------------"
cat .claude.json
echo "----------------------------------------"

echo ""
echo "======================================"
echo "🎉 Claude Code設定完了！"
echo ""
echo "📋 次のステップ:"
echo "   1. Claude Codeを完全に再起動"
echo "   2. 新しいセッションで '/mcp list' を実行"
echo "   3. 'serena: Connected (26 tools)' が表示されることを確認"
echo ""
echo "💡 トラブルシューティング:"
echo "   接続できない場合は ./scripts/serena/test-connection.sh で診断"
echo ""
