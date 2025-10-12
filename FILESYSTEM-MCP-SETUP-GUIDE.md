# 📁 Filesystem MCP Server セットアップガイド

このガイドでは、Filesystem MCP Serverをai-assistant-knowledge-hubプロジェクト（および他のプロジェクト）で使用するための完全なセットアップ手順を説明します。

## 📋 目次

1. [Filesystem MCP Serverとは](#filesystem-mcp-serverとは)
2. [なぜ必要か](#なぜ必要か)
3. [インストール手順](#インストール手順)
4. [Gemini CLI統合](#gemini-cli統合)
5. [Claude Code統合](#claude-code統合)
6. [使用可能なツール](#使用可能なツール)
7. [トラブルシューティング](#トラブルシューティング)

---

## Filesystem MCP Serverとは

**Filesystem MCP Server**は、Model Context Protocol (MCP)を実装したNode.jsサーバーで、AIアシスタントに安全なファイルシステム操作を提供します。

### 主な機能

- 📄 **ファイル操作**: 読み込み、書き込み、編集
- 📁 **ディレクトリ操作**: 作成、一覧表示、削除
- 🔍 **検索機能**: パターンマッチングによるファイル検索
- 🌳 **ディレクトリツリー**: 再帰的なディレクトリ構造の取得
- 🔒 **アクセス制御**: 指定されたディレクトリのみアクセス可能

**公式リポジトリ**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

---

## なぜ必要か

### 問題

- **Gemini CLIのファイル制限**: Gemini CLIは、セキュリティ上の理由から、デフォルトでファイルシステムへのアクセスが厳しく制限されています
- **Claude Codeとの違い**: Claude Codeは比較的ファイル操作が自由ですが、Geminiは制約が多い

### 解決策

Filesystem MCP Serverを導入することで：
- ✅ Gemini CLIでも安全にファイル操作が可能に
- ✅ 明示的に許可したディレクトリのみアクセス可能（セキュリティ確保）
- ✅ 統一されたファイル操作APIを複数のAIで共有

---

## インストール手順

### Step 1: パッケージのインストール

```bash
# NPMでグローバルインストール
npm install -g @modelcontextprotocol/server-filesystem

# インストール確認
which mcp-server-filesystem
```

**期待される出力**:
```
/data/data/com.termux/files/usr/bin/mcp-server-filesystem
```

### Step 2: インストール確認

```bash
# バージョン確認（エラーメッセージが出るのは正常）
mcp-server-filesystem 2>&1 | head -5
```

サーバーはディレクトリ引数を期待するため、引数なしで実行するとエラーになりますが、これは正常です。

---

## Gemini CLI統合

### 自動セットアップ（推奨）

ai-assistant-knowledge-hubには自動セットアップスクリプトが用意されています：

```bash
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub
./scripts/filesystem/setup-filesystem-gemini.sh
```

### 手動セットアップ

```bash
# プロジェクトディレクトリに移動
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub

# Filesystem MCPサーバーを追加（2つのディレクトリへのアクセスを許可）
gemini mcp add filesystem mcp-server-filesystem /data/data/com.termux/files/home /storage/emulated/0/Download
```

### 接続確認

```bash
gemini mcp list
```

**期待される出力**:
```
Configured MCP servers:

✓ filesystem: mcp-server-filesystem /data/data/com.termux/files/home /storage/emulated/0/Download (stdio) - Connected
```

### 設定ファイル

Gemini CLIは`.gemini/settings.json`に設定を保存します：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": [
        "/data/data/com.termux/files/home",
        "/storage/emulated/0/Download"
      ]
    }
  }
}
```

**重要**: `httpUrl`フィールドは使用しません。`command`と`args`のみで構成します。

---

## Claude Code統合

### 自動セットアップ（推奨）

```bash
cd /data/data/com.termux/files/home/ai-assistant-knowledge-hub
./scripts/filesystem/setup-filesystem-claude.sh
```

### 手動セットアップ

`.claude.json`に以下を追加：

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "mcp-server-filesystem",
      "args": [
        "/data/data/com.termux/files/home",
        "/storage/emulated/0/Download"
      ],
      "env": {}
    }
  }
}
```

### 接続確認

Claude Codeを再起動後、新しいセッションで：

```
/mcp list
```

**期待される出力**:
```
filesystem: Connected
```

---

## 使用可能なツール

Filesystem MCP Serverは以下のツールを提供します：

### 1. **read_text_file** - テキストファイル読み込み

```
入力:
- path: ファイルパス
- head (optional): 最初のN行のみ読み込み
- tail (optional): 最後のN行のみ読み込み
```

### 2. **read_media_file** - 画像・音声ファイル読み込み

```
入力:
- path: ファイルパス

出力: Base64エンコードされたデータ + MIMEタイプ
```

### 3. **read_multiple_files** - 複数ファイル同時読み込み

```
入力:
- paths: ファイルパスの配列
```

### 4. **write_file** - ファイル書き込み

```
入力:
- path: ファイルパス
- content: 書き込む内容

⚠️ 警告: 既存ファイルは上書きされます
```

### 5. **edit_file** - ファイル編集（高度なパターンマッチング）

```
入力:
- path: ファイルパス
- edits: 編集操作の配列
  - oldText: 検索する文字列
  - newText: 置換する文字列
- dryRun: プレビューモード（デフォルト: false）

特徴:
- インデントの自動保持
- 複数箇所の同時編集
- Git風のdiff出力
```

**ベストプラクティス**: 常に`dryRun: true`で変更をプレビューしてから実行

### 6. **create_directory** - ディレクトリ作成

```
入力:
- path: ディレクトリパス

特徴:
- 親ディレクトリも自動作成
- 既存の場合はエラーにならない
```

### 7. **list_directory** - ディレクトリ一覧

```
入力:
- path: ディレクトリパス

出力: [FILE] または [DIR] プレフィックス付きリスト
```

### 8. **list_directory_with_sizes** - サイズ付きディレクトリ一覧

```
入力:
- path: ディレクトリパス
- sortBy (optional): "name" または "size"

出力:
- ファイル/ディレクトリ一覧 + サイズ
- 統計情報（合計ファイル数、ディレクトリ数、合計サイズ）
```

### 9. **move_file** - ファイル移動/リネーム

```
入力:
- source: 元のパス
- destination: 移動先のパス

⚠️ 注意: 移動先が既に存在する場合はエラー
```

### 10. **search_files** - ファイル検索

```
入力:
- path: 検索開始ディレクトリ
- pattern: 検索パターン（glob形式）
- excludePatterns: 除外パターン（配列）

出力: マッチしたファイルのフルパス
```

### 11. **directory_tree** - ディレクトリツリー取得

```
入力:
- path: 開始ディレクトリ
- excludePatterns: 除外パターン（配列）

出力: 再帰的なJSON構造のディレクトリツリー
```

---

## トラブルシューティング

### 問題1: "Disconnected" 状態

**原因1**: `httpUrl`フィールドが誤って設定されている

**解決策**:
```bash
# .gemini/settings.json を確認
cat /data/data/com.termux/files/home/ai-assistant-knowledge-hub/.gemini/settings.json

# httpUrl フィールドがあれば削除
# 正しい構成: command + args のみ
```

**原因2**: パッケージがインストールされていない

**解決策**:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

### 問題2: アクセス拒否エラー

**原因**: 許可されていないディレクトリへのアクセス

**解決策**:
```bash
# 現在の許可ディレクトリを確認
# AIに依頼: 「list_allowed_directories ツールで許可されているディレクトリを表示して」

# ディレクトリを追加する場合は再設定
gemini mcp remove filesystem
gemini mcp add filesystem mcp-server-filesystem /path/to/dir1 /path/to/dir2 /path/to/dir3
```

### 問題3: サーバーが起動しない

**原因**: 少なくとも1つの許可ディレクトリが必要

**解決策**:
```bash
# 引数なしでは起動できない
# 必ず1つ以上のディレクトリを指定
gemini mcp add filesystem mcp-server-filesystem /data/data/com.termux/files/home
```

---

## セキュリティのベストプラクティス

### 1. 最小権限の原則

必要なディレクトリのみを許可：

```bash
# ❌ 悪い例: ルートディレクトリ全体を許可
gemini mcp add filesystem mcp-server-filesystem /

# ✅ 良い例: 必要なディレクトリのみ
gemini mcp add filesystem mcp-server-filesystem /data/data/com.termux/files/home/my-project
```

### 2. 読み取り専用ディレクトリ

重要なディレクトリは他の方法で保護：

```bash
# システムファイルへのアクセスは避ける
# /etc, /sys, /proc などは許可しない
```

### 3. 定期的な設定確認

```bash
# 許可ディレクトリを定期的に確認
gemini mcp list
cat .gemini/settings.json
```

---

## 許可ディレクトリの推奨設定

### Termux環境（Android）

```bash
gemini mcp add filesystem mcp-server-filesystem \
  /data/data/com.termux/files/home \
  /storage/emulated/0/Download \
  /storage/emulated/0/Documents
```

### 標準的な開発環境

```bash
gemini mcp add filesystem mcp-server-filesystem \
  ~/projects \
  ~/Documents \
  ~/Downloads
```

---

## 参考リンク

- **公式リポジトリ**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **MCP仕様**: https://modelcontextprotocol.io/
- **NPMパッケージ**: https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

---

## BOC-XXX: Filesystem MCP統合の教訓

このガイドは、Geminiとの協業で得た経験から作成されました。

### 主要な教訓

1. **httpUrlフィールドは不要**: Gemini CLIでは`command`と`args`のみで設定
2. **最低1つのディレクトリが必須**: 引数なしでは起動できない
3. **stdiモードが推奨**: httpモードよりも安定している
4. **パッケージは事前インストール**: `npx`よりもグローバルインストールが確実

---

**作成日**: 2025-10-12
**最終更新**: Filesystem MCP導入完了時
**メンテナンス**: パッケージ更新時にこのガイドを更新してください
