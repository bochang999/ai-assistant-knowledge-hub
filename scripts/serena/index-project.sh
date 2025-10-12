#!/bin/bash
# index-project.sh
# プロジェクトのインデックス作成スクリプト

set -e  # エラーで停止

echo "🔍 Serena プロジェクトインデックス作成"
echo "======================================"

# プロジェクトパス取得
if [ -n "$1" ]; then
    PROJECT_PATH="$1"
else
    PROJECT_PATH="$(pwd)"
fi

echo "📁 プロジェクトパス: $PROJECT_PATH"
echo ""

# プロジェクトディレクトリ存在確認
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ エラー: プロジェクトディレクトリが存在しません: $PROJECT_PATH"
    exit 1
fi

# プロジェクトディレクトリに移動
cd "$PROJECT_PATH"

# Step 1: 既存のキャッシュ確認
echo "🗂️  Step 1/3: 既存のキャッシュ確認中..."
if [ -d ".serena/cache" ]; then
    echo "⚠️  既存のキャッシュが見つかりました: .serena/cache"
    echo "   古いキャッシュを削除してから新しくインデックスを作成します"
    rm -rf .serena/cache
    echo "✅ 古いキャッシュを削除しました"
else
    echo "✅ 既存のキャッシュなし（初回インデックス）"
fi

# Step 2: プロジェクトインデックス作成
echo ""
echo "📊 Step 2/3: プロジェクトインデックス作成中..."
echo "   （プロジェクトサイズによっては時間がかかる場合があります）"
echo ""

uv run serena project index

# Step 3: インデックス結果確認
echo ""
echo "✅ Step 3/3: インデックス結果確認中..."
if [ -d ".serena/cache" ]; then
    CACHE_SIZE=$(du -sh .serena/cache 2>/dev/null | cut -f1)
    echo "✅ キャッシュ作成成功: .serena/cache ($CACHE_SIZE)"

    # プロジェクト設定ファイル確認
    if [ -f ".serena/project.yml" ]; then
        echo "✅ プロジェクト設定: .serena/project.yml"
        echo ""
        echo "📋 プロジェクト設定内容:"
        cat .serena/project.yml | sed 's/^/   /'
    fi
else
    echo "⚠️  キャッシュディレクトリが作成されませんでした"
    echo "   プロジェクトがサポート対象外の可能性があります"
fi

echo ""
echo "======================================"
echo "🎉 プロジェクトインデックス作成完了！"
echo ""
echo "📋 次のステップ:"
echo "   ./scripts/serena/health-check.sh を実行して状態確認"
echo ""
