#!/bin/bash
# test-connection.sh
# Serena MCP接続テストスクリプト

set -e  # エラーで停止

echo "🔌 Serena MCP 接続テスト"
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

# Step 1: 前提条件確認
echo "🔍 Step 1/4: 前提条件確認中..."

# Serenaインストール確認
if ! command -v uv &> /dev/null; then
    echo "❌ uv が見つかりません"
    exit 1
fi
echo "✅ uv: インストール済み"

# プロジェクトインデックス確認
if [ ! -d "$PROJECT_PATH/.serena/cache" ]; then
    echo "❌ プロジェクトインデックスが見つかりません: $PROJECT_PATH/.serena/cache"
    echo "💡 ./scripts/serena/index-project.sh を実行してください"
    exit 1
fi
echo "✅ プロジェクトインデックス: 存在"

# .claude.json確認
if [ ! -f "$PROJECT_PATH/.claude.json" ]; then
    echo "❌ .claude.json が見つかりません: $PROJECT_PATH/.claude.json"
    echo "💡 ./scripts/serena/setup-claude-config.sh を実行してください"
    exit 1
fi
echo "✅ .claude.json: 存在"

# Step 2: ポート使用状況確認
echo ""
echo "🌐 Step 2/4: ポート使用状況確認中..."
DEFAULT_PORT=24283

# ポート確認（lsofまたはnetstatを使用）
if command -v lsof &> /dev/null; then
    PORT_IN_USE=$(lsof -ti:$DEFAULT_PORT 2>/dev/null || echo "")
    if [ -n "$PORT_IN_USE" ]; then
        echo "⚠️  ポート $DEFAULT_PORT は既に使用中です (PID: $PORT_IN_USE)"
        echo "   プロセス詳細:"
        ps -p "$PORT_IN_USE" -o pid,command 2>/dev/null || echo "   (情報取得失敗)"
    else
        echo "✅ ポート $DEFAULT_PORT: 使用可能"
    fi
elif command -v netstat &> /dev/null; then
    PORT_IN_USE=$(netstat -tuln 2>/dev/null | grep ":$DEFAULT_PORT " || echo "")
    if [ -n "$PORT_IN_USE" ]; then
        echo "⚠️  ポート $DEFAULT_PORT は既に使用中です"
    else
        echo "✅ ポート $DEFAULT_PORT: 使用可能"
    fi
else
    echo "⚠️  ポート確認ツール（lsof/netstat）が見つかりません"
fi

# Step 3: Serena起動テスト（stdio mode）
echo ""
echo "🚀 Step 3/4: Serena起動テスト（stdio mode）..."
echo "   コマンド: uv run serena start-mcp-server --project $PROJECT_PATH"
echo ""

# タイムアウト付きでSerenaを起動（10秒後に自動終了）
timeout 10s uv run serena start-mcp-server --project "$PROJECT_PATH" &
SERENA_PID=$!

sleep 3

# プロセス確認
if ps -p $SERENA_PID > /dev/null 2>&1; then
    echo "✅ Serenaプロセス起動成功 (PID: $SERENA_PID)"

    # プロセスを停止
    kill $SERENA_PID 2>/dev/null || true
    wait $SERENA_PID 2>/dev/null || true
    echo "✅ テスト終了（プロセス停止）"
else
    echo "❌ Serenaプロセスが起動しませんでした"
    exit 1
fi

# Step 4: .claude.json検証
echo ""
echo "📋 Step 4/4: .claude.json設定検証..."

# jqがあれば構文チェック
if command -v jq &> /dev/null; then
    if jq . "$PROJECT_PATH/.claude.json" > /dev/null 2>&1; then
        echo "✅ .claude.json: JSON構文正常"

        # Serena設定の確認
        SERENA_CONFIG=$(jq -r '.mcpServers.serena' "$PROJECT_PATH/.claude.json")
        if [ "$SERENA_CONFIG" != "null" ]; then
            echo "✅ Serena設定: 存在"

            # プロジェクトパスの確認
            CONFIGURED_PATH=$(jq -r '.mcpServers.serena.args[-1]' "$PROJECT_PATH/.claude.json")
            if [ "$CONFIGURED_PATH" == "$PROJECT_PATH" ]; then
                echo "✅ プロジェクトパス: 一致 ($CONFIGURED_PATH)"
            else
                echo "⚠️  プロジェクトパス不一致:"
                echo "   設定値: $CONFIGURED_PATH"
                echo "   実際値: $PROJECT_PATH"
            fi
        else
            echo "❌ Serena設定が見つかりません"
        fi
    else
        echo "❌ .claude.json: JSON構文エラー"
        exit 1
    fi
else
    echo "⚠️  jqが見つかりません（構文チェックスキップ）"
fi

echo ""
echo "======================================"
echo "🎉 接続テスト完了！"
echo ""
echo "📋 結果サマリー:"
echo "   ✅ Serenaインストール"
echo "   ✅ プロジェクトインデックス"
echo "   ✅ .claude.json設定"
echo "   ✅ Serena起動確認"
echo ""
echo "🚀 次のステップ:"
echo "   1. Claude Codeを完全に再起動"
echo "   2. プロジェクトディレクトリで新しいセッション開始"
echo "   3. '/mcp list' コマンド実行"
echo "   4. 'serena: Connected (26 tools)' の表示を確認"
echo ""
echo "❓ トラブルシューティング:"
echo "   接続できない場合:"
echo "   - ターミナルを完全に閉じて再度開く"
echo "   - ~/.claude.json ではなく ./.claude.json を使用していることを確認"
echo "   - ./scripts/serena/health-check.sh でプロジェクト状態を再確認"
echo ""
