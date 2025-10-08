# 🤖 AI協業ワークフローシステム

BOC-95の経験を体系化した、AI協業による持続可能な開発プロセスを実現するワークフローシステムです。

## ✨ 2つの主要な使い方

このプロジェクトには、目的に応じて2つの主要なワークフローがあります。

### 1. `run_workflow.sh`：課題を自動で解決したい時に
課題の分析から実装、報告までを8つのフェーズで自動処理する、最も包括的なワークフローです。

- **ユースケース**: Issueの内容を元に、一連の解決プロセスを自動で進めたい場合。
- **実行コマンド**: `./run_workflow.sh <Issue-ID>`

### 2. `working-doit.sh`：特定の課題に手動で取り組む時に
Issue番号を元に、関連するプロジェクトのディレクトリへ自動で移動し、すぐに作業を開始できるワークフローです。

- **ユースケース**: 特定のIssueについて、コーディングなど手動での作業をすぐ始めたい場合。
- **実行コマンド**: `~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh <Issue番号>`

## 🛠️ 開発環境のセットアップ

作業を始める前に、以下の設定が必要です。

### 1. Linearとの連携設定
Linear APIを利用するために、APIキーとチームIDをファイルに保存します。

- `~/.linear-api-key`: あなたのLinear APIキーをこのファイルに保存してください。
- `~/.linear-team-id`: あなたのLinearチームIDをこのファイルに保存してください。

**API直接利用（デバッグ用）:**
```bash
curl -X POST "https://api.linear.app/graphql" -H "Authorization: $(cat ~/.linear-api-key)" ...
```

### 2. コード品質ツールの設定 (ESLint)
開発効率を上げるため、ESLintを導入しています。

**インストール:**
```bash
npm install --save-dev eslint eslint_d vscode-langservers-extracted
```

**使い方:**
```bash
# ファイルをチェック
npx eslint <ファイル名>

# 自動で修正
npx eslint <ファイル名> --fix
```

## 思想：ワークベンチ vs ファクトリー

このプロジェクトでは、作業の役割を明確に分けています。

- **ローカル環境（あなたのPC）**: コーディングや簡単なテストを行う「作業台（ワークベンチ）」です。
- **CI/CD環境（GitHub Actionsなど）**: アプリのビルドなど、重い処理を行う「工場（ファクトリー）」です。
