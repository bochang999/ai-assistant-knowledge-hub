# 🤖 Serena MCP Server セットアップガイド

このガイドでは、Serena MCP Serverをai-assistant-knowledge-hubプロジェクト（および他のプロジェクト）で使用するための完全なセットアップ手順を説明します。

## 📋 目次

1. [Serenaとは](#serenaとは)
2. [前提条件](#前提条件)
3. [🚀 クイックスタート（自動セットアップ）](#-クイックスタート自動セットアップ)
4. [インストール手順（手動）](#インストール手順手動)
5. [プロジェクト設定（手動）](#プロジェクト設定手動)
6. [Claude Code統合（手動）](#claude-code統合手動)
7. [他のAIでの使用方法](#他のaiでの使用方法)
8. [トラブルシューティング](#トラブルシューティング)
9. [使用例](#使用例)
10. [自動化スクリプト詳細](#自動化スクリプト詳細)

---

## Serenaとは

**Serena**は、AI-assisted codebaseのためのセマンティックコーディングツールです。MCP (Model Context Protocol)サーバーとして動作し、以下の機能を提供します：

- 📁 **プロジェクト構造解析**: ディレクトリ・ファイル構造のセマンティック理解
- 🔍 **コード検索**: シンボル検索、参照検索、定義ジャンプ
- 📝 **コード編集**: ファイル読み込み、書き込み、編集
- 🧠 **思考支援**: タスク遵守度分析、戦略的思考支援
- ⚡ **Language Server統合**: Pyright (Python LSP) 統合による高度なコード解析

**公式リポジトリ**: https://github.com/ckreiling/serena

---

## 前提条件

### 必須ツール

```bash
# Python 3.10以上
python3 --version

# uv (Pythonパッケージマネージャー)
# インストール方法:
curl -LsSf https://astral.sh/uv/install.sh | sh

# uvのバージョン確認
uv --version
```

### 推奨環境

- **OS**: Linux (Termux), macOS, Windows WSL
- **シェル**: bash, zsh
- **AI環境**: Claude Code, Cline, その他MCP対応AI

---

## 🚀 クイックスタート（自動セットアップ）

**最も簡単な方法**: 1つのコマンドで全セットアップを完了できます。

### 全自動セットアップ

```bash
# ai-assistant-knowledge-hubディレクトリに移動
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub

# 完全自動セットアップ実行
./scripts/serena/complete-setup.sh
```

このスクリプトは以下を自動で実行します：
1. ✅ Serenaインストール
2. ✅ プロジェクトインデックス作成
3. ✅ ヘルスチェック
4. ✅ `.claude.json`設定

**実行後**: Claude Codeを再起動して `/mcp list` を実行

---

### Gemini CLI向けセットアップ

Gemini CLIの場合は異なるコマンドを使用します：

```bash
# ai-assistant-knowledge-hubディレクトリに移動
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub

# Gemini CLI用セットアップ実行
./scripts/serena/setup-gemini.sh
```

このスクリプトは以下を自動で実行します：
1. ✅ Gemini CLI確認
2. ✅ プロジェクトインデックス確認
3. ✅ `gemini mcp add`で登録
4. ✅ 接続確認

**実行後**: `gemini mcp list` で接続を確認

---

### 他のプロジェクトでのセットアップ

```bash
# セットアップしたいプロジェクトに移動
cd /path/to/your/project

# ai-assistant-knowledge-hubのスクリプトを使用
/data/data/com.termux/files/home/ai-assistant-knowledge-hub/scripts/serena/complete-setup.sh $(pwd)
```

---

### 段階的セットアップ（個別スクリプト）

各ステップを個別に実行したい場合：

```bash
# Step 1: Serenaインストール
./scripts/serena/install-serena.sh

# Step 2: プロジェクトインデックス作成
./scripts/serena/index-project.sh

# Step 3: ヘルスチェック
./scripts/serena/health-check.sh

# Step 4: Claude Code設定
./scripts/serena/setup-claude-config.sh

# Step 5: 接続テスト
./scripts/serena/test-connection.sh
```

**各スクリプトの詳細**: [自動化スクリプト詳細](#自動化スクリプト詳細)を参照

---

## インストール手順（手動）

> **注意**: 自動セットアップを使用する場合、このセクションは不要です。

### Step 1: Serenaパッケージのインストール

```bash
# uvでSerenaをインストール
uv pip install serena-agent

# インストール確認
uv run serena --version
```

**期待される出力**:
```
Serena version 0.1.4 (or later)
```

### Step 2: Pyrightのインストール（Pythonプロジェクトの場合）

SerenaはPyrightをLanguage Serverとして使用します。Node.jsがインストールされている場合：

```bash
# Pyrightのインストール
npm install -g pyright

# バージョン確認
pyright --version
```

---

## プロジェクト設定（手動）

> **注意**: 自動セットアップを使用する場合、このセクションは不要です。

### Step 1: プロジェクトのインデックス作成

**これが最も重要なステップです**。Serenaはプロジェクトを事前にインデックス化する必要があります。

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# プロジェクトをインデックス化
uv run serena project index

# 出力例:
# 🔍 Indexing project...
# ✅ Indexed 34 files, 68 symbols
# 💾 Cache saved to .serena/cache/python/document_symbols_cache_v23-06-25.pkl
```

**重要**: インデックスを作成しないと、Serenaはプロジェクトを自動認識できません。

### Step 2: プロジェクト設定の確認

```bash
# プロジェクト設定ファイルの確認
cat .serena/project.yml
```

**出力例**:
```yaml
language: python
read_only: false
use_gitignore: true
```

### Step 3: ヘルスチェック

```bash
# プロジェクトとLanguage Serverの状態確認
uv run serena project health-check
```

**期待される出力**:
```
✅ Pyright version: 1.1.406
✅ Project recognized: 35 source files
✅ Cache exists: .serena/cache/python/document_symbols_cache_v23-06-25.pkl
```

---

## Claude Code統合（手動）

> **注意**: 自動セットアップを使用する場合、このセクションは不要です。

### Step 1: Claude Code設定ファイルの編集

Claude Codeでは、プロジェクトごとに`.claude.json`でMCPサーバーを設定します。

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# .claude.jsonを編集
nano .claude.json
```

### Step 2: Serena設定の追加

`.claude.json`に以下を追加：

```json
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "serena",
        "start-mcp-server",
        "--project",
        "/absolute/path/to/your/project"
      ],
      "env": {}
    }
  }
}
```

**重要ポイント**:
- `--project`フラグで**絶対パス**を指定
- プロジェクトパスは必ずインデックス済みのディレクトリ

#### ai-assistant-knowledge-hubの例

```json
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "serena",
        "start-mcp-server",
        "--project",
        "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
      ],
      "env": {}
    }
  }
}
```

### Step 3: Claude Codeの再起動

```bash
# Claude Codeを完全に終了して再起動
# ターミナルを閉じてから新しいセッションを開始
```

### Step 4: MCP接続確認

Claude Codeの新しいセッションで：

```
/mcp list
```

**期待される出力**:
```
serena: Connected (26 tools)
```

---

## 他のAIでの使用方法

### 1. **Gemini CLI**

Gemini CLIには専用のMCP管理コマンドがあります。

#### セットアップ手順

```bash
# プロジェクトディレクトリに移動
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub

# Serena MCPサーバーを追加
gemini mcp add serena uv run serena start-mcp-server --project $(pwd)
```

**出力例**:
```
MCP server "serena" added to project settings. (stdio)
```

#### 接続確認

```bash
# MCP接続状態を確認
gemini mcp list
```

**期待される出力**:
```
Configured MCP servers:

✓ serena: uv run serena start-mcp-server --project /path/to/project (stdio) - Connected
```

#### 設定ファイルの場所

Gemini CLIは**プロジェクトレベル**で設定を保存します：

```
.gemini/settings.json
```

**内容例**:
```json
{
  "mcpServers": {
    "serena": {
      "command": "uv",
      "args": [
        "run",
        "serena",
        "start-mcp-server",
        "--project",
        "/absolute/path/to/project"
      ]
    }
  }
}
```

#### その他のGemini MCPコマンド

```bash
# MCPサーバーを削除
gemini mcp remove serena

# MCPサーバーのヘルプ
gemini mcp --help
```

#### 重要な違い: Gemini CLI vs Claude Code

| 項目 | Gemini CLI | Claude Code |
|-----|-----------|------------|
| 設定ファイル | `.gemini/settings.json` | `.claude.json` |
| 設定コマンド | `gemini mcp add` | 手動編集 |
| スコープ | プロジェクトレベル | プロジェクトレベル |
| 確認コマンド | `gemini mcp list` | `/mcp list` (CLI内部) |

---

### 2. **Cline（VSCode拡張）**

Clineの設定ファイル（`~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`など）に以下を追加：

```json
{
  "mcpServers": {
    "serena": {
      "command": "uv",
      "args": ["run", "serena", "start-mcp-server", "--project", "/absolute/path/to/project"]
    }
  }
}
```

---

### 3. **スタンドアロンHTTPサーバー**

他のAIツールがHTTP経由でアクセスする場合：

```bash
# HTTPモードでSerenaを起動（ポート24283）
uv run serena start-mcp-server --transport streamable-http --port 24283 --project /path/to/project
```

**使用可能なトランスポート**:
- `stdio`: 標準入出力（Claude Code、Clineなど）
- `streamable-http`: HTTPストリーミング
- `sse`: Server-Sent Events

### 4. **Python APIから直接呼び出し**

Python script内でSerenaを使用：

```python
import requests

# Serenaサーバーの起動が必要
serena_url = "http://localhost:24283/mcp"

# ツール呼び出し例
response = requests.post(
    serena_url,
    headers={"Content-Type": "application/json"},
    json={
        "tool": "list_directory",
        "args": {"path": "/path/to/project"}
    }
)

print(response.json())
```

---

## トラブルシューティング

### 問題1: "Project not recognized"

**原因**: プロジェクトがインデックス化されていない

**解決策**:
```bash
cd /path/to/project
uv run serena project index
```

### 問題2: "Port already in use"

**原因**: 既にSerenaサーバーが起動中

**解決策**:
```bash
# プロセス確認
ps aux | grep serena

# プロセスをkill
kill <PID>

# または別のポートを使用
uv run serena start-mcp-server --port 24284 --project /path/to/project
```

### 問題3: "Pyright not found"

**原因**: Pyrightがインストールされていない、またはPATHに含まれていない

**解決策**:
```bash
# Node.jsとPyrightをインストール
npm install -g pyright

# PATHの確認
which pyright

# 環境変数の設定（必要に応じて）
export PATH="$PATH:/usr/local/bin"
```

### 問題4: Claude CodeでSerenaツールが見えない

**原因**:
- `.claude.json`の設定ミス
- プロジェクトパスが相対パスになっている
- Claude Codeが再起動されていない

**解決策**:
```bash
# 1. .claude.jsonの構文確認
cat .claude.json | jq .

# 2. 絶対パスを確認
pwd  # 現在のディレクトリの絶対パス

# 3. Claude Codeを完全再起動
# ターミナルを閉じて再度開く

# 4. MCP接続確認
/mcp list
```

### 問題5: "Cache is stale"

**原因**: コードが更新されたがキャッシュが古い

**解決策**:
```bash
# キャッシュを削除して再インデックス
rm -rf .serena/cache
uv run serena project index
```

---

## 使用例

### 例1: ディレクトリ構造の取得

```
# AIに以下のように依頼:
「Serenaのlist_directoryツールを使って、このプロジェクトの構造を表示してください」
```

### 例2: シンボル検索

```
# AIに以下のように依頼:
「Serenaを使って、IssueDiscoveryEngineクラスの定義場所を見つけてください」
```

### 例3: ファイル編集

```
# AIに以下のように依頼:
「Serenaを使って、phase1-issue-discovery.pyのdiscover_issue_projectメソッドを読み込んで、どのような処理をしているか説明してください」
```

### 例4: 思考支援

```
# AIに以下のように依頼:
「Serenaのthink_about_task_adherenceツールを使って、BOC-132の実装がプロジェクトのアーキテクチャに適合しているか評価してください」
```

---

## 自動化スクリプト詳細

ai-assistant-knowledge-hubには、Serenaセットアップを自動化する複数のスクリプトが用意されています。

### スクリプト一覧

| スクリプト | 機能 | 使用タイミング |
|----------|------|-------------|
| `complete-setup.sh` | 全自動セットアップ（Claude Code） | 初回セットアップ時 |
| `install-serena.sh` | Serenaインストール | Serenaが未インストールの場合 |
| `index-project.sh` | プロジェクトインデックス作成 | 新規プロジェクトまたはコード更新後 |
| `health-check.sh` | プロジェクト状態確認 | トラブルシューティング時 |
| `setup-claude-config.sh` | `.claude.json`設定 | Claude Code統合時 |
| `setup-gemini.sh` | `.gemini/settings.json`設定 | Gemini CLI統合時 |
| `test-connection.sh` | MCP接続テスト | セットアップ後の確認 |

### 1. complete-setup.sh（全自動）

**場所**: `./scripts/serena/complete-setup.sh`

**機能**:
- Serenaのインストールから`.claude.json`設定まで全自動実行
- Phase 1-4を順次実行
- 確認プロンプト付き

**使用方法**:
```bash
# カレントディレクトリでセットアップ
./scripts/serena/complete-setup.sh

# 他のプロジェクトでセットアップ
./scripts/serena/complete-setup.sh /path/to/other/project
```

**実行内容**:
1. Serenaインストール確認
2. プロジェクトインデックス作成
3. ヘルスチェック実行
4. `.claude.json`設定

---

### 2. install-serena.sh（インストール）

**場所**: `./scripts/serena/install-serena.sh`

**機能**:
- uv確認
- Python確認
- Serenaインストール
- Pyright確認（オプション）

**使用方法**:
```bash
./scripts/serena/install-serena.sh
```

**出力例**:
```
🤖 Serena MCP Server インストール開始
==========================================
📦 Step 1/4: uv 確認中...
✅ uv が見つかりました: uv 0.4.x
🐍 Step 2/4: Python バージョン確認中...
✅ Python が見つかりました: 3.11.x
📥 Step 3/4: Serena Agent インストール中...
✅ Serena インストール完了: 0.1.4
🔍 Step 4/4: Pyright 確認中...
✅ Pyright が見つかりました: 1.1.406
```

---

### 3. index-project.sh（インデックス作成）

**場所**: `./scripts/serena/index-project.sh`

**機能**:
- 既存キャッシュの削除
- プロジェクトインデックス作成
- `.serena/project.yml`確認

**使用方法**:
```bash
# カレントディレクトリをインデックス
./scripts/serena/index-project.sh

# 他のプロジェクトをインデックス
./scripts/serena/index-project.sh /path/to/project
```

**出力例**:
```
🔍 Serena プロジェクトインデックス作成
==========================================
📁 プロジェクトパス: /path/to/project

🗂️  Step 1/3: 既存のキャッシュ確認中...
✅ 既存のキャッシュなし（初回インデックス）

📊 Step 2/3: プロジェクトインデックス作成中...
🔍 Indexing project...
✅ Indexed 34 files, 68 symbols

✅ Step 3/3: インデックス結果確認中...
✅ キャッシュ作成成功: .serena/cache (2.4M)
✅ プロジェクト設定: .serena/project.yml
```

**再インデックスが必要な場合**:
- コードを大幅に変更した後
- 新しいファイルを追加した後
- キャッシュが古くなった時

---

### 4. health-check.sh（ヘルスチェック）

**場所**: `./scripts/serena/health-check.sh`

**機能**:
- Serenaバージョン確認
- Pyrightバージョン確認
- インデックスキャッシュ確認
- プロジェクト設定確認
- 統合ヘルスチェック実行

**使用方法**:
```bash
# カレントディレクトリを確認
./scripts/serena/health-check.sh

# 他のプロジェクトを確認
./scripts/serena/health-check.sh /path/to/project
```

**出力例**:
```
🏥 Serena ヘルスチェック
==========================================
📁 プロジェクトパス: /path/to/project

🤖 Step 1/5: Serena バージョン確認中...
✅ Serena: 0.1.4

🔍 Step 2/5: Pyright 確認中...
✅ Pyright: pyright 1.1.406

📊 Step 3/5: プロジェクトインデックス確認中...
✅ インデックスキャッシュ: .serena/cache (2.4M)
   キャッシュファイル数: 3

⚙️  Step 4/5: プロジェクト設定確認中...
✅ プロジェクト設定: .serena/project.yml
   language: python
   read_only: false
   use_gitignore: true

🏥 Step 5/5: Serena 統合ヘルスチェック実行中...
✅ Pyright version: 1.1.406
✅ Project recognized: 35 source files
✅ Cache exists
```

---

### 5. setup-claude-config.sh（Claude Code設定）

**場所**: `./scripts/serena/setup-claude-config.sh`

**機能**:
- 既存`.claude.json`の確認とバックアップ
- Serena設定の追加/更新
- jqによる安全な設定マージ（jqがある場合）

**使用方法**:
```bash
# カレントディレクトリに.claude.json作成
./scripts/serena/setup-claude-config.sh

# 他のプロジェクトに作成
./scripts/serena/setup-claude-config.sh /path/to/project
```

**出力例**:
```
⚙️  Claude Code 設定 (.claude.json)
==========================================
📁 プロジェクトパス: /path/to/project

🔍 Step 1/3: 既存の.claude.json確認中...
⚠️  既存の.claude.jsonが見つかりました
💾 バックアップ作成: .claude.json.backup.20251012_143022

📝 Step 2/3: .claude.json設定中...
✅ .claude.json を更新しました（jqを使用）

✅ Step 3/3: 設定内容確認
📋 .claude.json の内容:
{
  "mcpServers": {
    "serena": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "serena", "start-mcp-server", "--project", "/path/to/project"],
      "env": {}
    }
  }
}
```

**重要**:
- 既存の`.claude.json`がある場合は自動的にバックアップを作成
- jqがインストールされている場合は既存設定を保持して追加
- jqがない場合はシンプルな設定で上書き

---

### 6. setup-gemini.sh（Gemini CLI設定）

**場所**: `./scripts/serena/setup-gemini.sh`

**機能**:
- Gemini CLI確認
- プロジェクトインデックス確認
- 既存MCP設定の確認と削除（必要に応じて）
- `gemini mcp add`による登録
- 接続確認

**使用方法**:
```bash
# カレントディレクトリでセットアップ
./scripts/serena/setup-gemini.sh

# 他のプロジェクトでセットアップ
./scripts/serena/setup-gemini.sh /path/to/project
```

**出力例**:
```
🤖 Gemini CLI - Serena MCP セットアップ
==========================================
📁 プロジェクトパス: /path/to/project

🔍 Step 1/5: Gemini CLI確認中...
✅ Gemini CLI: インストール済み

📂 Step 2/5: プロジェクトディレクトリに移動中...
✅ カレントディレクトリ: /path/to/project

📊 Step 3/5: プロジェクトインデックス確認中...
✅ プロジェクトインデックス: 存在

🔍 Step 4/5: 既存のMCP設定確認中...
(既存設定がある場合は上書き確認)

➕ Step 5/5: Serena MCPサーバー登録中...
MCP server "serena" added to project settings. (stdio)

✅ 登録確認中...
Configured MCP servers:
✓ serena: uv run serena start-mcp-server --project /path/to/project (stdio) - Connected

🎉 Gemini CLI - Serena MCP セットアップ完了！
```

**重要**:
- Gemini CLIは `.gemini/settings.json` に設定を保存
- `gemini mcp add` コマンドでMCPサーバーを登録
- Claude Codeとは異なる設定ファイル

---

### 7. test-connection.sh（接続テスト）

**場所**: `./scripts/serena/test-connection.sh`

**機能**:
- 前提条件の包括的確認
- ポート使用状況確認
- Serena起動テスト（10秒タイムアウト）
- `.claude.json`設定検証

**使用方法**:
```bash
# カレントディレクトリをテスト
./scripts/serena/test-connection.sh

# 他のプロジェクトをテスト
./scripts/serena/test-connection.sh /path/to/project
```

**出力例**:
```
🔌 Serena MCP 接続テスト
==========================================
📁 プロジェクトパス: /path/to/project

🔍 Step 1/4: 前提条件確認中...
✅ uv: インストール済み
✅ プロジェクトインデックス: 存在
✅ .claude.json: 存在

🌐 Step 2/4: ポート使用状況確認中...
✅ ポート 24283: 使用可能

🚀 Step 3/4: Serena起動テスト（stdio mode）...
✅ Serenaプロセス起動成功 (PID: 12345)
✅ テスト終了（プロセス停止）

📋 Step 4/4: .claude.json設定検証...
✅ .claude.json: JSON構文正常
✅ Serena設定: 存在
✅ プロジェクトパス: 一致 (/path/to/project)

🎉 接続テスト完了！
```

---

### スクリプト使用のベストプラクティス

1. **初回セットアップ**: `complete-setup.sh`を使用
2. **プロジェクト更新後**: `index-project.sh`を実行
3. **問題発生時**: `health-check.sh` → `test-connection.sh`の順で診断
4. **他のプロジェクトへの適用**: 各スクリプトにプロジェクトパスを引数として渡す

### トラブルシューティングワークフロー

```bash
# 1. ヘルスチェック
./scripts/serena/health-check.sh

# 問題が見つかった場合 → 2. 再インデックス
./scripts/serena/index-project.sh

# それでも問題がある場合 → 3. 接続テスト
./scripts/serena/test-connection.sh

# 最終手段 → 4. 完全再セットアップ
./scripts/serena/complete-setup.sh
```

---

## 参考リンク

- **Serena公式リポジトリ**: https://github.com/ckreiling/serena
- **MCP仕様**: https://modelcontextprotocol.io/
- **Pyright**: https://github.com/microsoft/pyright
- **uv**: https://github.com/astral-sh/uv

---

## BOC-132: Serena統合の教訓

このガイドは、BOC-132での実際のトラブルシューティング経験から作成されました。

### 主要な教訓

1. **プロジェクトインデックスが最重要**: `serena project index`を実行しないと、Serenaはプロジェクトを認識できない
2. **絶対パスを使用**: `--project`フラグには必ず絶対パスを指定
3. **AI再起動が必要**: 設定変更後は、AIセッションを完全に再起動
4. **ヘルスチェックで確認**: `serena project health-check`で問題を早期発見

---

**作成日**: 2025-10-12
**最終更新**: BOC-132完了時
**メンテナンス**: Serenaのバージョンアップ時にこのガイドを更新してください
