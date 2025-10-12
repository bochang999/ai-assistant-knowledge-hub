#!/bin/bash
# install-serena.sh
# Serena MCPサーバーのインストールスクリプト

set -e  # エラーで停止

echo "🤖 Serena MCP Server インストール開始"
echo "======================================"

# Step 1: uv確認
echo ""
echo "📦 Step 1/4: uv (Pythonパッケージマネージャー) 確認中..."
if ! command -v uv &> /dev/null; then
    echo "❌ uvがインストールされていません"
    echo "💡 インストール方法:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo "✅ uv が見つかりました: $(uv --version)"

# Step 2: Pythonバージョン確認
echo ""
echo "🐍 Step 2/4: Python バージョン確認中..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python が見つかりました: $PYTHON_VERSION"

# Step 3: Serenaインストール
echo ""
echo "📥 Step 3/4: Serena Agent インストール中..."
uv pip install --system serena-agent

# バージョン確認
SERENA_VERSION=$(uv run serena --version 2>&1 || echo "version check failed")
if [[ "$SERENA_VERSION" == *"version check failed"* ]]; then
    echo "⚠️  Serenaのバージョン確認に失敗しましたが、インストールは完了しています"
else
    echo "✅ Serena インストール完了: $SERENA_VERSION"
fi

# Step 4: Pyright確認（オプション）
echo ""
echo "🔍 Step 4/4: Pyright (Language Server) 確認中..."
if command -v pyright &> /dev/null; then
    echo "✅ Pyright が見つかりました: $(pyright --version)"
else
    echo "⚠️  Pyright が見つかりません（Pythonプロジェクトの場合は推奨）"
    echo "💡 インストール方法:"
    echo "   npm install -g pyright"
fi

echo ""
echo "======================================"
echo "🎉 Serena インストール完了！"
echo ""
echo "📋 次のステップ:"
echo "   1. プロジェクトディレクトリに移動"
echo "   2. ./scripts/serena/index-project.sh を実行してプロジェクトをインデックス化"
echo ""
