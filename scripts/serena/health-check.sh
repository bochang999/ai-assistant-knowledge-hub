#!/bin/bash
# health-check.sh
# Serenaプロジェクトのヘルスチェックスクリプト

set -e  # エラーで停止

echo "🏥 Serena ヘルスチェック"
echo "======================================"

# プロジェクトパス取得
if [ -n "$1" ]; then
    PROJECT_PATH="$1"
else
    PROJECT_PATH="$(pwd)"
fi

echo "📁 プロジェクトパス: $PROJECT_PATH"
echo ""

# プロジェクトディレクトリに移動
cd "$PROJECT_PATH"

# Step 1: Serenaバージョン確認
echo "🤖 Step 1/5: Serena バージョン確認中..."
SERENA_VERSION=$(uv run serena --version 2>&1 || echo "unknown")
echo "✅ Serena: $SERENA_VERSION"

# Step 2: Pyright確認
echo ""
echo "🔍 Step 2/5: Pyright (Language Server) 確認中..."
if command -v pyright &> /dev/null; then
    PYRIGHT_VERSION=$(pyright --version 2>&1 | head -n1)
    echo "✅ Pyright: $PYRIGHT_VERSION"
else
    echo "⚠️  Pyright が見つかりません"
fi

# Step 3: プロジェクトインデックス確認
echo ""
echo "📊 Step 3/5: プロジェクトインデックス確認中..."
if [ -d ".serena/cache" ]; then
    CACHE_SIZE=$(du -sh .serena/cache 2>/dev/null | cut -f1)
    echo "✅ インデックスキャッシュ: .serena/cache ($CACHE_SIZE)"

    # キャッシュファイル数
    CACHE_FILES=$(find .serena/cache -type f 2>/dev/null | wc -l)
    echo "   キャッシュファイル数: $CACHE_FILES"
else
    echo "❌ インデックスキャッシュが見つかりません"
    echo "💡 ./scripts/serena/index-project.sh を実行してください"
fi

# Step 4: プロジェクト設定確認
echo ""
echo "⚙️  Step 4/5: プロジェクト設定確認中..."
if [ -f ".serena/project.yml" ]; then
    echo "✅ プロジェクト設定: .serena/project.yml"
    echo ""
    cat .serena/project.yml | sed 's/^/   /'
else
    echo "⚠️  プロジェクト設定ファイルが見つかりません"
fi

# Step 5: Serena health-check実行
echo ""
echo "🏥 Step 5/5: Serena 統合ヘルスチェック実行中..."
echo ""

uv run serena project health-check

echo ""
echo "======================================"
echo "🎉 ヘルスチェック完了！"
echo ""
echo "📋 次のステップ:"
echo "   ./scripts/serena/setup-claude-config.sh を実行してClaude Code設定"
echo ""
