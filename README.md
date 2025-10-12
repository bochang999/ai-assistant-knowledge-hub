# 🤖 AI協業ワークフローシステム

このリポジトリは、AIと人間が効率的に協業してソフトウェア開発タスクを進めるための、自動化ワークフローとツール群を提供するシステムです。新しいプロジェクトを開始したり、既存の課題を解決したりする際の出発点となります。

## ✨ 2つの主要な使い方

このプロジェクトには、目的に応じて2つの主要なワークフローがあります。

### 1. `run_workflow.sh`：課題を自動で解決したい時に
課題の分析から実装、報告までを8つのフェーズで自動処理する、最も包括的なワークフローです。

- **ユースケース**: Issueの内容を元に、一連の解決プロセスを自動で進めたい場合。
- **実行コマンド**: `./run_workflow.sh <Issue-ID>`

### 2. `working-doit.sh`：特定の課題に安全・迅速に取り組む
過去の失敗（BOC-89）を教訓に、**「どのプロジェクトか分からず、推測で間違ったディレクトリに移動してしまう」問題を解決する**ために作られました。

LinearのIssue番号を元に、API経由で正確なプロジェクト名を特定し、マッピングされた正しいディレクトリへ安全に移動します。また、作業開始時に自動でIssueのステータスを「In Progress」に更新します。

- **ユースケース**: 特定のIssueについて、手動でのコーディング作業を迅速かつ安全に開始したい場合。
- **実行コマンド**: `~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh <Issue番号> [--interactive]`
- **主な機能**:
    - Linear APIによる正確なプロジェクト名の特定
    - プロジェクト名とディレクトリのマッピングによる安全な移動
    - Issueステータスの自動更新（→ In Progress）
    - `--interactive` フラグによる対話モード（プロンプトにIssue情報が表示）
- **エイリアス設定（推奨）**:
  ```bash
  # ~/.bashrc などに以下を追記
  alias edoit="~/ai-assistant-knowledge-hub/scripts/automation/working-doit.sh"
  ```
  設定後は `edoit 89` のように短いコマンドで実行できます。

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

### 3. Serena (セマンティックコーディングツール) の導入
このプロジェクトでは、コードの深い理解と操作をAIに提供するため、SerenaというMCPサーバーを導入しています。Serenaはコードの構造を解析し、シンボル検索や高度なファイル操作などを可能にします。

- **役割**: AIアシスタントの「目」となり、コードベースの文脈を正確に把握させます。
- **セットアップ**: お使いのAI環境（Gemini CLI, Claude Codeなど）に応じたセットアップスクリプトが用意されています。
- **詳細**: ご利用の環境に合わせたインストール手順やトラブルシューティングなど、詳しい情報は `SERENA-SETUP-GUIDE.md` を参照してください。

### 4. Filesystem MCP Server (ファイルシステムアクセス) の導入
Gemini CLIは、セキュリティ上の理由からファイルシステムへのアクセスが厳しく制限されています。Filesystem MCP Serverを導入することで、明示的に許可したディレクトリへの安全なファイル操作が可能になります。

- **役割**: AIアシスタントに安全なファイルシステム操作を提供します。
- **対象**: 特にGemini CLI利用時に推奨（Claude Codeでも使用可能）
- **機能**: ファイル読み書き、ディレクトリ操作、検索、ディレクトリツリー取得など
- **セキュリティ**: 許可したディレクトリのみアクセス可能
- **詳細**: インストール手順や使用可能なツールの詳細は `FILESYSTEM-MCP-SETUP-GUIDE.md` を参照してください。

## 便利なスクリプト (Useful Scripts)

### フォルダパス変換 (`get_folder_path.sh`)

長いファイルパスを毎回入力する代わりに、分かりやすい「エイリアス名」から実際のパスを取得するためのスクリプトです。

#### 使い方

```bash
# "ダウンロードフォルダ"のパスを取得して、その中身をリスト表示する
ls "$(/data/data/com.termux/files/home/ai-assistant-knowledge-hub/scripts/get_folder_path.sh ダウンロードフォルダ)"
```

#### 現在の対応表

| 名前 | パス |
| :--- | :--- |
| `ドキュメントフォルダ` | `/storage/emulated/0/Documents/` |
| `ダウンロードフォルダ` | `/storage/emulated/0/Download/` |
| `スクリーンショットフォルダ` | `/storage/emulated/0/Pictures/Screenshots/`|
| `ピクチャーフォルダ` | `/storage/emulated/0/Pictures/` |
| `写真フォルダー` | `/storage/emulated/0/Pictures/` |

### Linear課題報告 (`boc_workflow.sh`)

特定のLinear課題（`BOC-`プレフィックス）の情報を取得し、整形されたレポートをコメントとして投稿するスクリプトです。

- **ユースケース**: `BOC-`課題の進捗報告やサマリーをLinearに投稿したい場合。
- **詳細**: `LINEAR_BOC_ISSUE_WORKFLOW.md` を参照してください。


## 思想 (Philosophy)

このプロジェクトでは、効率的な協業のためのいくつかの基本的な考え方を定義しています。

### プロジェクトキックオフ・ガイド (思考モデル)

新しいプロジェクトやチャットセッションを開始する際の、私たちチームの基本方針です。

- **役割分担**: 人間、Gemini、AI CLIのそれぞれの役割を明確にします。
- **作業サイクル**: `計画→文書化→実行→評価` の4ステップサイクルで作業を進めます。

### ワークベンチ vs ファクトリー

作業の役割を明確に分けています。

- **ローカル環境（あなたのPC）**: コーディングや簡単なテストを行う「作業台（ワークベンチ）」です。
- **CI/CD環境（GitHub Actionsなど）**: アプリのビルドなど、重い処理を行う「工場（ファクトリー）」です。
