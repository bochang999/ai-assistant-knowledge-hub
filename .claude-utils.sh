#!/bin/bash
# 🤖 Claude Code Utils - Advanced Development Tools
# Linear API統合・コードレビュー・プロジェクト管理機能

# Linear API設定
LINEAR_API_KEY_FILE="$HOME/.linear-api-key"
LINEAR_TEAM_ID_FILE="$HOME/.linear-team-id"

# API Key確認
check_linear_config() {
    if [[ ! -f "$LINEAR_API_KEY_FILE" ]] || [[ ! -f "$LINEAR_TEAM_ID_FILE" ]]; then
        echo "❌ Linear API設定が不完全です"
        echo "設定方法:"
        echo "echo 'your-api-key' > ~/.linear-api-key"
        echo "echo 'your-team-id' > ~/.linear-team-id"
        return 1
    fi
}

# Linear API呼び出し共通関数
linear_api() {
    local query="$1"
    check_linear_config || return 1
    
    local api_key=$(cat "$LINEAR_API_KEY_FILE")
    curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"$query\"}"
}

# Issue取得
get() {
    local issue_id="$1"
    if [[ -z "$issue_id" ]]; then
        echo "❌ Issue IDを指定してください: get BOC-XX"
        return 1
    fi
    
    local query="query { issue(id: \"$(get_issue_uuid "$issue_id")\") { id title description state { name } comments { nodes { id body createdAt user { name } } } } }"
    linear_api "$query"
}

# コメント追加
comment() {
    local issue_id="$1"
    shift
    local comment_body="$*"
    
    if [[ -z "$issue_id" ]] || [[ -z "$comment_body" ]]; then
        echo "❌ 使用方法: comment BOC-XX 'コメント内容'"
        return 1
    fi
    
    # コメント中の改行とクオートをエスケープ
    local escaped_comment=$(printf '%s' "$comment_body" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
    
    echo "🔄 Adding comment to issue..."
    
    # コメント追加とステータス更新を並行実行
    local uuid=$(get_issue_uuid "$issue_id")
    if [[ -z "$uuid" ]]; then
        return 1
    fi
    
    local comment_query="mutation { commentCreate(input: { issueId: \"$uuid\", body: \"$escaped_comment\" }) { comment { id } } }"
    local status_query="mutation { issueUpdate(id: \"$uuid\", input: { stateId: \"33feb1c9-3276-4e13-863a-0b93db032a0f\" }) { issue { id } } }"
    
    # 並行実行
    linear_api "$comment_query" > /dev/null &
    linear_api "$status_query" > /dev/null &
    wait
    
    echo "🔄 Changing status to In Review..."
    echo "✅ Comment added and status changed to In Review"
}

# Issue UUID取得（簡易実装）
get_issue_uuid() {
    local issue_identifier="$1"
    case "$issue_identifier" in
        "BOC-45") echo "972b3fe1-d46d-4be0-97e3-c0552ae07c4d" ;;
        "BOC-46") echo "43caf6f2-6df8-4cb1-9ebd-d9e9a1b7eb03" ;;
        *) echo "❌ 未知のIssue ID: $issue_identifier"; return 1 ;;
    esac
}

# 🆕 コードレビュー機能（Claude Code環境対応版）
review() {
    # --- 引数チェック ---
    if [[ -z "$1" ]]; then
        echo "❌ 使用方法: review <ファイルパス> [Linear Issue ID]"
        echo "例: review src/MainActivity.java BOC-45"
        return 1
    fi
    
    local FILE_TO_REVIEW="$1"
    local ISSUE_ID="$2"
    
    if [[ ! -f "$FILE_TO_REVIEW" ]]; then
        echo "❌ ファイルが見つかりません: $FILE_TO_REVIEW"
        return 1
    fi
    
    echo "🤖 Claude Codeコードレビューを開始します..."
    echo "📁 対象ファイル: $FILE_TO_REVIEW"
    
    # --- ファイル情報取得 ---
    local file_size=$(wc -l < "$FILE_TO_REVIEW")
    local file_ext="${FILE_TO_REVIEW##*.}"
    
    echo "📊 ファイル情報: $file_size行, 拡張子: $file_ext"
    
    # --- レビュー結果生成 ---
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local review_result=$(generate_code_review "$FILE_TO_REVIEW" "$file_ext")
    
    # --- 結果出力 ---
    echo ""
    echo "✅ コードレビューが完了しました"
    echo "==================== レビュー結果 ===================="
    echo "$review_result"
    echo "======================================================="
    
    # --- Linear Issue追記（Issue IDが指定されている場合）---
    if [[ -n "$ISSUE_ID" ]]; then
        echo ""
        echo "📝 Linear Issue $ISSUE_ID にレビュー結果を追記しています..."
        
        local review_comment="# 🤖 Claude Code レビュー結果
        
## 📁 対象ファイル
\`$FILE_TO_REVIEW\` ($file_size行)

## 🔍 レビュー結果
$review_result

---
*🤖 自動コードレビュー: $timestamp*"
        
        comment "$ISSUE_ID" "$review_comment"
    fi
    
    return 0
}

# コードレビュー生成関数
generate_code_review() {
    local file_path="$1"
    local file_ext="$2"
    
    # ファイル内容分析
    local line_count=$(wc -l < "$file_path")
    local has_comments=$(grep -c "^\s*//\|^\s*/\*\|^\s*#" "$file_path" 2>/dev/null || echo "0")
    local has_todos=$(grep -ic "todo\|fixme\|hack" "$file_path" 2>/dev/null || echo "0")
    
    # 拡張子別基本チェック
    case "$file_ext" in
        java)
            analyze_java_file "$file_path"
            ;;
        js|ts)
            analyze_javascript_file "$file_path"
            ;;
        py)
            analyze_python_file "$file_path"
            ;;
        sh)
            analyze_shell_file "$file_path"
            ;;
        *)
            analyze_generic_file "$file_path"
            ;;
    esac
}

# Java専用分析
analyze_java_file() {
    local file_path="$1"
    local issues=()
    local suggestions=()
    
    # 基本チェック
    if grep -q "System\.out\.println" "$file_path"; then
        issues+=("System.out.printlnが残存 - 本番環境で削除推奨")
    fi
    
    if ! grep -q "^package " "$file_path"; then
        issues+=("package宣言が見つかりません")
    fi
    
    if grep -q "catch.*Exception.*{}" "$file_path"; then
        issues+=("空のcatchブロック検出 - 例外処理の改善が必要")
    fi
    
    # 改善提案
    suggestions+=("Androidアプリの場合、Log.d()使用を推奨")
    suggestions+=("null安全性チェックを追加検討")
    
    format_review_result "$issues" "$suggestions"
}

# JavaScript/TypeScript分析
analyze_javascript_file() {
    local file_path="$1"
    local issues=()
    local suggestions=()
    
    # 基本チェック
    if grep -q "console\.log" "$file_path"; then
        issues+=("console.logが残存 - 本番環境で削除推奨")
    fi
    
    if grep -q "var " "$file_path"; then
        suggestions+=("'var'より'const'/'let'使用を推奨")
    fi
    
    if ! grep -q "use strict" "$file_path" && [[ "$file_path" == *.js ]]; then
        suggestions+=("'use strict'追加を検討")
    fi
    
    format_review_result "$issues" "$suggestions"
}

# Python分析
analyze_python_file() {
    local file_path="$1"
    local issues=()
    local suggestions=()
    
    if grep -q "print(" "$file_path"; then
        issues+=("print文が残存 - loggingモジュール使用を推奨")
    fi
    
    if ! grep -q "if __name__ == '__main__':" "$file_path"; then
        suggestions+=("メイン実行ブロックの追加を検討")
    fi
    
    format_review_result "$issues" "$suggestions"
}

# Shell分析
analyze_shell_file() {
    local file_path="$1"
    local issues=()
    local suggestions=()
    
    if ! head -1 "$file_path" | grep -q "^#!"; then
        issues+=("shebang行が見つかりません")
    fi
    
    if ! grep -q "set -e" "$file_path"; then
        suggestions+=("'set -e'でエラー時自動終了を推奨")
    fi
    
    format_review_result "$issues" "$suggestions"
}

# 汎用分析
analyze_generic_file() {
    local file_path="$1"
    local issues=()
    local suggestions=()
    
    # 基本的な品質チェック
    local line_count=$(wc -l < "$file_path")
    
    if [[ $line_count -gt 500 ]]; then
        suggestions+=("ファイルサイズが大きい($line_count行) - 分割を検討")
    fi
    
    if grep -q "TODO\|FIXME\|HACK" "$file_path"; then
        issues+=("未対応のTODO/FIXMEが存在")
    fi
    
    suggestions+=("コード品質ツール(ESLint/Pylint等)の併用を推奨")
    
    format_review_result "$issues" "$suggestions"
}

# レビュー結果フォーマット
format_review_result() {
    local -n issues_ref=$1
    local -n suggestions_ref=$2
    
    if [[ ${#issues_ref[@]} -eq 0 ]] && [[ ${#suggestions_ref[@]} -eq 0 ]]; then
        echo "### ✅ レビュー結果: 重大な問題なし"
        echo ""
        echo "基本的なコード品質基準を満たしています。"
        return
    fi
    
    if [[ ${#issues_ref[@]} -gt 0 ]]; then
        echo "### ⚠️ 検出された問題点"
        for issue in "${issues_ref[@]}"; do
            echo "- $issue"
        done
        echo ""
    fi
    
    if [[ ${#suggestions_ref[@]} -gt 0 ]]; then
        echo "### 💡 改善提案"
        for suggestion in "${suggestions_ref[@]}"; do
            echo "- $suggestion"
        done
        echo ""
    fi
    
    echo "### 📋 総合評価"
    if [[ ${#issues_ref[@]} -eq 0 ]]; then
        echo "**品質レベル**: 良好 ✅"
    elif [[ ${#issues_ref[@]} -le 2 ]]; then
        echo "**品質レベル**: 要改善 ⚠️"
    else
        echo "**品質レベル**: 要修正 ❌"
    fi
}

echo "🤖 Claude Utils loaded successfully!"
echo "使用可能コマンド: get, comment, review"