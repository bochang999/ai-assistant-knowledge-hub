#!/bin/bash
# complete-setup.sh
# Serena完全セットアップスクリプト（全自動）

set -e  # エラーで停止

echo "🤖 Serena MCP Server 完全セットアップ"
echo "=========================================="
echo ""

# プロジェクトパス取得
if [ -n "$1" ]; then
    PROJECT_PATH="$1"
else
    PROJECT_PATH="$(pwd)"
fi

# 絶対パスに変換
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)

echo "📁 セットアップ対象: $PROJECT_PATH"
echo ""

# 確認プロンプト
read -p "このプロジェクトでSerenaセットアップを実行しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ セットアップを中止しました"
    exit 0
fi

echo ""
echo "=========================================="
echo ""

# スクリプトディレクトリ取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Phase 1: Serenaインストール
echo "Phase 1/4: Serena インストール"
echo "----------------------------------------"
bash "$SCRIPT_DIR/install-serena.sh"
echo ""

# Phase 2: プロジェクトインデックス作成
echo "Phase 2/4: プロジェクトインデックス作成"
echo "----------------------------------------"
bash "$SCRIPT_DIR/index-project.sh" "$PROJECT_PATH"
echo ""

# Phase 3: ヘルスチェック
echo "Phase 3/4: ヘルスチェック"
echo "----------------------------------------"
bash "$SCRIPT_DIR/health-check.sh" "$PROJECT_PATH"
echo ""

# Phase 4: Claude Code設定
echo "Phase 4/4: Claude Code設定"
echo "----------------------------------------"
bash "$SCRIPT_DIR/setup-claude-config.sh" "$PROJECT_PATH"
echo ""

# 最終確認
echo "=========================================="
echo "🎉 Serena完全セットアップ完了！"
echo ""
echo "📊 セットアップサマリー:"
echo "   ✅ Serenaインストール"
echo "   ✅ プロジェクトインデックス作成"
echo "   ✅ ヘルスチェック完了"
echo "   ✅ Claude Code設定完了"
echo ""
echo "🚀 次のアクション:"
echo "   1. Claude Codeを完全に再起動してください"
echo "   2. 新しいセッションで以下のコマンドを実行:"
echo "      cd $PROJECT_PATH"
echo "      /mcp list"
echo "   3. 'serena: Connected (26 tools)' が表示されることを確認"
echo ""
echo "🔧 接続テスト（オプション）:"
echo "   ./scripts/serena/test-connection.sh $PROJECT_PATH"
echo ""
echo "📖 詳細ガイド:"
echo "   cat $PROJECT_PATH/SERENA-SETUP-GUIDE.md"
echo ""
