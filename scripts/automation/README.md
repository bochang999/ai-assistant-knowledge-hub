# Enhanced Doit System

BOC-83問題の再発防止のための統合Issue処理自動化システム

## 📋 概要

このシステムは、Linear IssueからGitHub Actionsまでの作業フローを自動化し、以下の問題を防止します：

- ❌ 間違ったプロジェクトでの作業
- ❌ 未完了のGit作業（コミット・プッシュ忘れ）
- ❌ GitHub Actionsワークフロー確認不足
- ❌ Linear Issue状態の更新忘れ

## 🚀 クイックスタート

### 1. エイリアス設定

```bash
# エイリアス自動設定
~/ai-assistant-knowledge-hub/scripts/automation/setup-aliases.sh

# シェル再読み込み
source ~/.bashrc  # bashの場合
source ~/.zshrc   # zshの場合
```

### 2. 基本使用方法

```bash
# 基本実行
doit BOC-83

# インタラクティブモード（各ステップで確認）
doit-i BOC-83

# 全自動モード（プッシュ＋ワークフロー待機）
doit-auto BOC-83

# ドライラン（実際の操作なし）
doit-dry BOC-83
```

## 📚 詳細ガイド

### コマンドオプション

| オプション | 説明 |
|------------|------|
| `--interactive` | 各ステップで確認を求める |
| `--auto-push` | Git作業完了時に自動プッシュ |
| `--wait-workflow` | ワークフロー完了まで待機 |
| `--full-auto` | 全自動実行 |
| `--dry-run` | 実際の作業なしでプロセス確認 |

### 処理フロー

1. **🔍 Issue検証・プロジェクト特定**
   - Linear APIでIssue情報を取得
   - プロジェクト名を自動特定

2. **📂 プロジェクトディレクトリ移動**
   - 正しいプロジェクトディレクトリに自動移動
   - Git情報確認

3. **🔧 作業実行**
   - ユーザーが手動で開発作業を実行
   - Linear状態を"In Progress"に更新

4. **📊 Git作業完了確認**
   - 未コミット変更チェック
   - 未プッシュコミットチェック
   - 自動プッシュ（オプション）

5. **🚀 GitHub Actions検証**
   - ワークフロー実行状況確認
   - 完了待機（オプション）

6. **✅ Issue完了処理**
   - Linear状態を"Completed"に更新

## 🔧 個別ツール

システムは以下の独立したツールで構成されています：

```bash
# Issue検証
check-issue BOC-83

# プロジェクト移動
goto-project "petit recipe"

# Git状況確認
check-git BOC-83

# ワークフロー確認
check-workflow
```

## ⚙️ 設定要件

### 必須設定

1. **Linear API Key**
   ```bash
   echo "YOUR_LINEAR_API_KEY" > ~/.linear-api-key
   ```

2. **GitHub認証** (いずれか)
   ```bash
   # GitHub CLI
   gh auth login

   # または Personal Access Token
   echo "YOUR_GITHUB_TOKEN" > ~/.github-token
   ```

### プロジェクトマッピング

`auto-project-navigator.sh` でサポートされているプロジェクト：

| Linear Project | Directory |
|----------------|-----------|
| `petit recipe` | `~/petit-recipe` |
| `ai-assistant-knowledge-hub` | `~/ai-assistant-knowledge-hub` |
| `RecipeBox` | `~/recipebox-web` |
| `Laminator Dashboard` | `~/laminator-dashboard` |

## 🔍 トラブルシューティング

### よくある問題

**Q: "Linear API keyが見つかりません"**
```bash
echo "YOUR_API_KEY" > ~/.linear-api-key
```

**Q: "GitHub認証が設定されていません"**
```bash
gh auth login
# または
echo "YOUR_TOKEN" > ~/.github-token
```

**Q: "プロジェクトディレクトリが見つかりません"**
- `auto-project-navigator.sh` のプロジェクトマッピングを確認
- 手動でディレクトリパスを修正

### ログ確認

作業情報は `/tmp/claude-automation/` に保存されます：

```bash
# 現在のプロジェクト
cat /tmp/claude-automation/current-project

# Git状況
cat /tmp/claude-automation/git-status

# ワークフロー状況
cat /tmp/claude-automation/workflow-status
```

## 📁 ファイル構成

```
scripts/automation/
├── enhanced-doit.sh           # メインシステム
├── issue-validator.sh         # Issue検証
├── auto-project-navigator.sh  # プロジェクト移動
├── git-completion-tracker.sh  # Git作業確認
├── workflow-verifier.sh       # ワークフロー検証
├── setup-aliases.sh          # エイリアス設定
└── README.md                 # このファイル
```

## 🎯 使用例

### 典型的なワークフロー

```bash
# 1. Issueを開始
doit-i BOC-123

# 2. 作業実行（手動）
# ... 開発作業 ...

# 3. 確認・完了
# システムが自動で：
# - Git状況確認
# - プッシュ実行
# - ワークフロー確認
# - Linear状態更新
```

### 全自動実行

```bash
# 作業後、全て自動化
doit-auto BOC-123
```

### テスト実行

```bash
# 実際の操作なしでプロセス確認
doit-dry BOC-123
```

## 🔮 今後の拡張

- [ ] Slack/Discord通知連携
- [ ] 複数Linear Team対応
- [ ] GitLab CI/CD対応
- [ ] カスタムワークフロー定義

---

**作成**: Enhanced Doit System v1.0
**目的**: BOC-83問題再発防止
**更新**: 2025-09-16
