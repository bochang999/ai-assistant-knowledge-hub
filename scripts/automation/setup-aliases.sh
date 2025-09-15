#!/bin/bash
# エイリアス設定スクリプト
# Enhanced Doit Systemを簡単に使用するためのエイリアス設定

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# エイリアス定義
setup_aliases() {
    local shell_rc=""

    # シェル検出
    case "$SHELL" in
        */bash)
            shell_rc="$HOME/.bashrc"
            ;;
        */zsh)
            shell_rc="$HOME/.zshrc"
            ;;
        *)
            echo "⚠️ 不明なシェル: $SHELL"
            echo "手動で以下のエイリアスを追加してください:"
            show_aliases
            return 1
            ;;
    esac

    echo "🔧 Enhanced Doit System エイリアス設定"
    echo "対象ファイル: $shell_rc"

    # バックアップ作成
    if [ -f "$shell_rc" ]; then
        cp "$shell_rc" "${shell_rc}.backup.$(date +%Y%m%d_%H%M%S)"
        echo "✅ 既存設定をバックアップしました"
    fi

    # エイリアス追加
    cat >> "$shell_rc" << 'EOF'

# ========== Enhanced Doit System Aliases ==========
# BOC-83問題再発防止システム

# 基本コマンド
alias doit='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh'
alias doit-help='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --help'

# インタラクティブモード
alias doit-i='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --interactive'

# 自動化モード
alias doit-auto='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --full-auto'

# ドライランモード
alias doit-dry='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --dry-run'

# 個別ツール
alias check-issue='~/ai-assistant-knowledge-hub/scripts/automation/issue-validator.sh'
alias goto-project='~/ai-assistant-knowledge-hub/scripts/automation/auto-project-navigator.sh'
alias check-git='~/ai-assistant-knowledge-hub/scripts/automation/git-completion-tracker.sh'
alias check-workflow='~/ai-assistant-knowledge-hub/scripts/automation/workflow-verifier.sh'

# ========== End Enhanced Doit System ==========
EOF

    echo "✅ エイリアスを追加しました"
    echo ""
    echo "🚀 使用方法:"
    echo "  source $shell_rc    # エイリアスを有効化"
    echo "  doit BOC-123        # 基本実行"
    echo "  doit-i BOC-123      # インタラクティブ"
    echo "  doit-auto BOC-123   # 全自動"
    echo "  doit-help           # ヘルプ表示"

    return 0
}

# エイリアス一覧表示
show_aliases() {
    cat << 'EOF'
# Enhanced Doit System エイリアス
alias doit='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh'
alias doit-help='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --help'
alias doit-i='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --interactive'
alias doit-auto='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --full-auto'
alias doit-dry='~/ai-assistant-knowledge-hub/scripts/automation/enhanced-doit.sh --dry-run'
alias check-issue='~/ai-assistant-knowledge-hub/scripts/automation/issue-validator.sh'
alias goto-project='~/ai-assistant-knowledge-hub/scripts/automation/auto-project-navigator.sh'
alias check-git='~/ai-assistant-knowledge-hub/scripts/automation/git-completion-tracker.sh'
alias check-workflow='~/ai-assistant-knowledge-hub/scripts/automation/workflow-verifier.sh'
EOF
}

# メイン実行
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    case "$1" in
        "--show")
            show_aliases
            ;;
        *)
            setup_aliases
            ;;
    esac
fi
