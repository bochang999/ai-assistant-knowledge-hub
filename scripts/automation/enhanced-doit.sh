#!/bin/bash

# Enhanced doit command with automatic project validation
# Prevents workflow confusion by ensuring correct project identification

SCRIPT_DIR="$(dirname "$0")"
QUERY_SCRIPT="$SCRIPT_DIR/enhanced-linear-query.sh"

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ログ関数
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}🔄 $1${NC}"; }

# ヘルプ表示
show_help() {
    cat << EOF
${CYAN}Enhanced Doit Command System${NC}
BOC-83問題再発防止のための統合Issue処理システム

使用方法:
  $0 <ISSUE-ID> [OPTIONS]

例:
  $0 BOC-83                    # 基本実行
  $0 BOC-83 --interactive      # インタラクティブモード
  $0 BOC-83 --auto-push        # 自動プッシュ有効
  $0 BOC-83 --wait-workflow    # ワークフロー完了待機
  $0 BOC-83 --full-auto        # 全自動モード

オプション:
  --interactive     各ステップで確認を求める
  --auto-push       Git作業完了時に自動プッシュ
  --wait-workflow   ワークフロー完了まで待機
  --full-auto       全自動実行（プッシュ＋ワークフロー待機）
  --dry-run         実際の作業を行わず、プロセスのみ表示
  --help            このヘルプを表示

処理フロー:
  1. 🔍 Issue検証・プロジェクト特定
  2. 📂 正しいプロジェクトディレクトリに移動
  3. 🔧 作業実行 (ユーザーが手動で実行)
  4. 📊 Git作業完了確認
  5. 🚀 GitHub Actions ワークフロー検証
  6. ✅ Linear Issue状態更新

EOF
}

# Linear Issue状態更新
update_linear_status() {
    local issue_id="$1"
    local status="$2"  # "in_progress" または "completed"

    log_step "Linear Issue状態更新: $issue_id → $status"

    if [ ! -f ~/.linear-api-key ]; then
        log_warning "Linear API keyが見つかりません。手動で状態更新してください"
        return 1
    fi

    # Issue情報取得
    if [ ! -f "/tmp/claude-automation/current-issue-id" ]; then
        log_error "Issue情報が見つかりません"
        return 1
    fi

    local linear_issue_id=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"query { issues(filter: { number: { eq: $(echo "$issue_id" | sed 's/.*-//') } }) { nodes { id } }}\"}" | \
        jq -r '.data.issues.nodes[0].id // empty')

    if [ -z "$linear_issue_id" ]; then
        log_error "Linear Issue IDが取得できませんでした"
        return 1
    fi

    # 状態ID設定
    local state_id
    case "$status" in
        "in_progress")
            state_id="1cebb56e-524e-4de0-b676-0f574df9012a"
            ;;
        "completed")
            state_id="33feb1c9-3276-4e13-863a-0b93db032a0f"
            ;;
        *)
            log_error "不正な状態: $status"
            return 1
            ;;
    esac

    # 状態更新
    local update_result=$(curl -s -X POST "https://api.linear.app/graphql" \
        -H "Authorization: $(cat ~/.linear-api-key)" \
        -H "Content-Type: application/json" \
        -d "{\"query\":\"mutation { issueUpdate(id: \\\"$linear_issue_id\\\", input: { stateId: \\\"$state_id\\\" }) { success }}\"}")

    if echo "$update_result" | jq -e '.data.issueUpdate.success' >/dev/null 2>&1; then
        log_success "Linear Issue状態更新完了: $status"
        return 0
    else
        log_error "Linear Issue状態更新失敗"
        echo "$update_result" | jq '.errors // empty' | head -3
        return 1
    fi
}

# メイン処理
enhanced_doit() {
    local issue_id="$1"
    local interactive_mode="$2"
    local auto_push="$3"
    local wait_workflow="$4"
    local dry_run="$5"

    if [ -z "$issue_id" ]; then
        log_error "Issue IDが指定されていません"
        show_help
        return 1
    fi

    log_info "Enhanced Doit System 開始: $issue_id"
    echo "========================================"

    # 作業開始時間記録
    mkdir -p /tmp/claude-automation
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > "/tmp/claude-automation/start-time"

    # 1. Issue検証・プロジェクト特定
    log_step "Step 1: Issue検証・プロジェクト特定"
    if [ "$dry_run" != "true" ]; then
        if ! "$SCRIPT_DIR/issue-validator.sh" "$issue_id"; then
            log_error "Issue検証に失敗しました"
            return 1
        fi
    else
        log_info "[DRY RUN] Issue検証をスキップ"
    fi

    if [ "$interactive_mode" = "true" ]; then
        read -p "🤔 続行しますか？ (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "ユーザーによって中断されました"
            return 1
        fi
    fi

    # 2. プロジェクトディレクトリ移動
    log_step "Step 2: プロジェクトディレクトリ移動"
    local original_dir=$(pwd)
    if [ "$dry_run" != "true" ]; then
        if ! "$SCRIPT_DIR/auto-project-navigator.sh"; then
            log_error "プロジェクトディレクトリ移動に失敗しました"
            return 1
        fi
    else
        log_info "[DRY RUN] プロジェクトディレクトリ移動をスキップ"
    fi

    # Linear状態を"In Progress"に更新
    if [ "$dry_run" != "true" ]; then
        update_linear_status "$issue_id" "in_progress" || log_warning "Linear状態更新に失敗（続行します）"
    fi

    # 3. 作業実行（ユーザー手動）
    log_step "Step 3: 作業実行"
    log_info "💡 ここで実際の開発作業を行ってください"
    log_info "📂 現在のディレクトリ: $(pwd)"

    if [ -f "/tmp/claude-automation/current-issue-title" ]; then
        local issue_title=$(cat "/tmp/claude-automation/current-issue-title")
        log_info "📋 作業内容: $issue_title"
    fi

    if [ "$interactive_mode" = "true" ]; then
        echo ""
        log_warning "作業が完了したらEnterキーを押してください..."
        read -r
    else
        log_info "作業完了後、次のステップに進んでください"
        echo ""
    fi

    # 4. Git作業完了確認
    log_step "Step 4: Git作業完了確認"
    if [ "$dry_run" != "true" ]; then
        if "$SCRIPT_DIR/git-completion-tracker.sh" "$issue_id"; then
            log_success "Git作業確認完了"
        else
            log_warning "Git作業が未完了です"

            if [ "$auto_push" = "true" ]; then
                log_step "自動プッシュを実行中..."
                if "$SCRIPT_DIR/git-completion-tracker.sh" "--auto-push" "$issue_id"; then
                    log_success "自動プッシュ完了"
                else
                    log_error "自動プッシュに失敗しました"
                    return 1
                fi
            else
                log_info "💡 Git作業を完了してから次のステップに進んでください"
                if [ "$interactive_mode" = "true" ]; then
                    read -p "🤔 Git作業完了後、続行しますか？ (y/N): " -n 1 -r
                    echo
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        return 1
                    fi
                fi
            fi
        fi
    else
        log_info "[DRY RUN] Git作業確認をスキップ"
    fi

    # 5. GitHub Actions ワークフロー検証
    log_step "Step 5: GitHub Actions ワークフロー検証"
    if [ "$dry_run" != "true" ]; then
        if "$SCRIPT_DIR/workflow-verifier.sh"; then
            log_success "ワークフロー検証完了"

            if [ "$wait_workflow" = "true" ]; then
                log_step "ワークフロー完了待機中..."
                if "$SCRIPT_DIR/workflow-verifier.sh" "--wait"; then
                    log_success "ワークフロー完了確認"
                else
                    log_warning "ワークフロー完了待機タイムアウト"
                fi
            fi
        else
            log_warning "ワークフロー検証で問題が検出されました"
        fi
    else
        log_info "[DRY RUN] ワークフロー検証をスキップ"
    fi

    # 6. Issue完了
    log_step "Step 6: Issue完了処理"
    if [ "$dry_run" != "true" ]; then
        # Git作業とワークフローが完了している場合のみLinear状態更新
        local git_status=$(cat "/tmp/claude-automation/git-status" 2>/dev/null || echo "unknown")
        if [ "$git_status" = "completed" ]; then
            update_linear_status "$issue_id" "completed" || log_warning "Linear状態更新に失敗"
        else
            log_info "Git作業未完了のため、Linear状態はIn Progressのまま"
        fi
    else
        log_info "[DRY RUN] Issue完了処理をスキップ"
    fi

    # 完了時間記録
    echo "$(date '+%Y-%m-%d %H:%M:%S')" > "/tmp/claude-automation/end-time"

    # サマリー表示
    echo ""
    log_success "========================================"
    log_success "Enhanced Doit System 完了: $issue_id"

    if [ -f "/tmp/claude-automation/start-time" ] && [ -f "/tmp/claude-automation/end-time" ]; then
        local start_time=$(cat "/tmp/claude-automation/start-time")
        local end_time=$(cat "/tmp/claude-automation/end-time")
        log_info "⏱️  実行時間: $start_time ～ $end_time"
    fi

    # 元のディレクトリに戻る
    cd "$original_dir"

    return 0
}

# パラメータ解析
parse_arguments() {
    local issue_id=""
    local interactive_mode="false"
    local auto_push="false"
    local wait_workflow="false"
    local dry_run="false"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_help
                exit 0
                ;;
            --interactive)
                interactive_mode="true"
                shift
                ;;
            --auto-push)
                auto_push="true"
                shift
                ;;
            --wait-workflow)
                wait_workflow="true"
                shift
                ;;
            --full-auto)
                auto_push="true"
                wait_workflow="true"
                shift
                ;;
            --dry-run)
                dry_run="true"
                shift
                ;;
            BOC-*|LIN-*|ISSUE-*|*-[0-9]*)
                issue_id="$1"
                shift
                ;;
            *)
                log_error "不明なオプション: $1"
                show_help
                exit 1
                ;;
        esac
    done

    enhanced_doit "$issue_id" "$interactive_mode" "$auto_push" "$wait_workflow" "$dry_run"
}

# スクリプトが直接実行された場合
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    parse_arguments "$@"
fi
