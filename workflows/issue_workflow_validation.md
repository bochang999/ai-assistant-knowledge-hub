# Issue Workflow Validation System

## 概要

Linear Issue作業開始時の戸惑いを防ぐため、プロジェクト識別・環境検証を自動化するワークフローシステム。

## システム構成

### 1. Enhanced Linear Query (`enhanced-linear-query.sh`)
- GraphQL APIから完全なIssue情報を取得
- project.key、team.key、labelsを網羅的に収集
- プロジェクト識別の確実性を向上

### 2. Project Mapping (`project-mapping.json`)
- プロジェクトID → 作業環境の対応関係を定義
- basePath、procedures、buildCommand等を管理
- 新プロジェクト追加時の設定標準化

### 3. Environment Validation
- 作業ディレクトリの存在確認
- 必須ファイル・手順書の検証
- 環境不備時の早期エラー検出

## 使用方法

### 基本実行
```bash
# Issue情報の完全分析
~/ai-assistant-knowledge-hub/scripts/automation/enhanced-linear-query.sh 89

# 出力例:
# 🔍 Fetching complete issue information for #89...
# 📊 Project Information:
#   Project Key: ai-assistant-knowledge-hub
#   Project Name: AI Assistant Knowledge Hub
#   Team Key: bochang-labo
#   Team Name: bochang's lab
#   Labels: AI-Task
# ✅ Primary Project Identifier: ai-assistant-knowledge-hub
# 🔍 Validating project environment...
#   Base Path: ~/ai-assistant-knowledge-hub
# ✅ Found procedure file: README.md
# ✅ Found procedure file: workflows/build_error_correction.md
# ✅ Project environment validated
# ✅ Safe to proceed with project: ai-assistant-knowledge-hub
# ✅ Working directory: /data/data/com.termux/files/home/ai-assistant-knowledge-hub
```

### 環境変数エクスポート
```bash
# スクリプト実行結果を環境変数として設定
eval "$(~/ai-assistant-knowledge-hub/scripts/automation/enhanced-linear-query.sh 89 | tail -3)"

echo $ISSUE_PROJECT_ID        # ai-assistant-knowledge-hub
echo $ISSUE_BASE_PATH         # /data/data/com.termux/files/home/ai-assistant-knowledge-hub
```

## エラー防止戦略

### 1. プロジェクト識別の多重チェック
```
優先度1: project.key
優先度2: team.key
優先度3: labels内のプロジェクトタグ
```

### 2. 必須検証項目
- [ ] プロジェクトIDが特定できること
- [ ] project-mapping.jsonに対応エントリが存在すること
- [ ] 作業ディレクトリが実在すること
- [ ] 手順書ファイルが存在すること

### 3. 失敗時の安全停止
```bash
if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Stopping execution to prevent errors."
    exit 1
fi
```

## 今回の問題 (BOC-89) への対応

### 問題
- Issue詳細に「ビルドエラーが出ました」としか記載がない
- プロジェクトタグを確認せずCLAUDE.mdの推測で行動
- 実際はai-assistant-knowledge-hubプロジェクトだった

### 解決策の実装
1. **完全なIssue情報取得**: project、team、labels全てを取得
2. **プロジェクト対応表**: 各プロジェクトの設定を事前定義
3. **環境検証の自動化**: 作業前の必須チェック
4. **推測の排除**: 不明な場合は作業停止

## ワークフロー統合

### doit コマンドとの連携
```bash
# 既存のdoitコマンドを拡張
#!/bin/bash
# enhanced-doit.sh

issue_number=$1

# Step 1: Issue分析・プロジェクト特定
validation_result=$(~/ai-assistant-knowledge-hub/scripts/automation/enhanced-linear-query.sh "$issue_number")

if [ $? -ne 0 ]; then
    echo "❌ Issue validation failed. Cannot proceed safely."
    exit 1
fi

# Step 2: 環境変数設定
eval "$(echo "$validation_result" | tail -3)"

# Step 3: プロジェクト特有の作業開始
cd "$ISSUE_BASE_PATH"
echo "✅ Starting work on Issue #$issue_number in project $ISSUE_PROJECT_ID"

# Step 4: Claude Code起動 (Interactive mode)
if [ "$2" = "--interactive" ]; then
    claude --context README.md
fi
```

## メンテナンス

### 新プロジェクト追加時
```bash
# project-mapping.jsonに新エントリ追加
{
  "new-project-key": {
    "basePath": "~/new-project",
    "procedures": ["README.md"],
    "buildCommand": "npm run build",
    "testCommand": "npm test",
    "description": "New project description",
    "technologies": ["react", "typescript"],
    "validation": {
      "requiredFiles": ["package.json", "src/"],
      "requiredDirs": ["src", "node_modules"]
    }
  }
}
```

### プロジェクト設定の更新
- basePath変更時は全対応プロジェクトを確認
- procedures追加時は実際のファイル存在を検証
- buildCommand変更時は動作確認必須

---

このシステムにより、Issue作業開始時の「どのプロジェクトか分からない」「推測で間違ったディレクトリに移動」といった問題を根本的に解決できます。
