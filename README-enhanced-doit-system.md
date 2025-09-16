# Enhanced Doit System - Project Confusion Prevention

## 問題の解決

BOC-89で発生した「どのプロジェクトか分からず、推測で間違ったディレクトリに移動してしまう」問題を完全に解決するシステムを構築しました。

## システム構成

### 1. `working-doit.sh` - メインコマンド
```bash
~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh 89 [--interactive]
```

**機能:**
- Linear APIからIssue情報を完全取得
- project.nameに基づく自動プロジェクト識別
- 正しいディレクトリへの安全な移動
- Linear Issue状態の自動更新（In Progress）
- インタラクティブセッション対応

### 2. プロジェクトマッピング自動化

**Linear Project Name → Directory Mapping:**
```
"petit recipe"           → ~/petit-recipe/
"ai assistant knowledge hub" → ~/ai-assistant-knowledge-hub/
"laminator dashboard"    → ~/laminator-dashboard/
"recipebox web"         → ~/recipebox-web/
"tarot"                 → ~/tarot/
```

### 3. 安全性チェック

**必須検証項目:**
- Issue存在確認
- プロジェクト名の確実な取得
- ターゲットディレクトリの存在確認
- 推測による動作の完全排除

## 使用方法

### 基本実行
```bash
# BOC-89の解決
~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh 89

# 出力例:
# 🚀 Working Enhanced Doit - Issue #89
# 🔍 Analyzing Issue #89...
# 📊 Issue Information:
#   Title: BOC-89ビルドエラー発生
#   Project: petit recipe
#   Team: Bochang's labo
# ✅ Target Project: petit-recipe
# ✅ Target Directory: /data/data/com.termux/files/home/petit-recipe
# ✅ Status updated successfully
# ✅ Current Directory: /data/data/com.termux/files/home/petit-recipe
```

### インタラクティブモード
```bash
~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh 89 --interactive

# プロジェクト特定後、インタラクティブセッション開始
# プロンプト: [Issue #89 | petit-recipe] $
```

## 今回の問題 (BOC-89) での実証

### 問題発生時の状況
- Issue詳細: "ビルドエラーが出ました"
- プロジェクト不明のままlaminator-dashboardに移動
- 実際はpetit-recipeプロジェクトだった

### 解決システムでの動作
1. **完全情報取得**: Linear APIからproject.name="petit recipe"を取得
2. **確実なマッピング**: "petit recipe" → petit-recipe ディレクトリ
3. **安全な移動**: ~/petit-recipe/ に確実に移動
4. **状態管理**: Linear Issue状態を"In Progress"に自動更新

## システムの利点

### 1. 推測の完全排除
- CLAUDE.mdの"Current Project Context"に依存しない
- Linear APIから確実な情報を取得
- プロジェクト不明時は処理停止

### 2. エラー防止の多重チェック
- Issue存在確認
- プロジェクト名取得確認
- ディレクトリ存在確認
- API応答検証

### 3. 作業効率向上
- 自動Issue状態管理
- 正しいプロジェクトディレクトリへの移動
- インタラクティブセッション対応

## インストール・セットアップ

```bash
# 1. 実行権限付与
chmod +x ~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh

# 2. エイリアス設定 (オプション)
echo 'alias edoit="~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh"' >> ~/.bashrc
source ~/.bashrc

# 3. 使用例
edoit 89 --interactive
```

## 拡張・メンテナンス

### 新プロジェクト追加
`working-doit.sh`内のcase文にマッピングを追加:

```bash
case "${project_name,,}" in
    *"new project name"*)
        target_project="new-project"
        target_dir="$HOME/new-project"
        ;;
```

### デバッグモード
スクリプト内でAPI応答を確認:
```bash
echo "$api_response" | jq '.' # API応答の確認
```

---

このシステムにより、BOC-89のような「どのプロジェクトか分からない」問題は完全に解決され、安全で確実なIssue作業が可能になります。
