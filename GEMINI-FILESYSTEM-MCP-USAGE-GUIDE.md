# Gemini CLI - Filesystem MCP Server ツール使用ガイド

## 問題: MCPツールが見つからない

Gemini CLIでは、MCPサーバーのツールは自動的に発見され、グローバルツールレジストリに登録されます。しかし、ツール名の命名規則により、予想と異なる名前になっている可能性があります。

## ツール命名規則

Gemini CLIの公式ドキュメントによると：

### 基本ルール
- MCPサーバーのツールは自動的に発見され、サニタイズ（無害化）される
- ツールはグローバルツールレジストリに登録される

### 名前衝突時の処理
**重要**: 複数のサーバーが同じ名前のツールを提供している場合、後続のサーバーのツールには `serverName__toolName` というプレフィックスが付与されます。

例：
- 最初のサーバーの`list_directory` → `list_directory`
- 2番目のサーバーの`list_directory` → `filesystem__list_directory`

## Filesystem MCP Serverのツール名を確認する方法

以下の方法でFilesystem MCPサーバーが提供するツールの正確な名前を確認できます：

### 方法1: AIアシスタントに直接質問
```
「現在利用可能なツールのリストを表示してください。特に "filesystem" または "directory" を含むツール名を教えてください。」
```

### 方法2: ツールを推測して試行
Filesystem MCP Serverが提供する可能性のあるツール名：

**プレフィックスなし（デフォルトツールと衝突しない場合）**:
- `read_text_file`
- `read_media_file`
- `write_file`
- `edit_file`
- `create_directory`
- `list_directory` ← Geminiの組み込みツールと衝突する可能性が高い
- `move_file`
- `search_files`
- `directory_tree`

**プレフィックスあり（衝突時）**:
- `filesystem__read_text_file`
- `filesystem__list_directory` ← これが正しい可能性が高い
- `filesystem__write_file`
- など

## 推奨される解決手順

### Step 1: 利用可能なツールを確認
Geminiに以下のように依頼：

```
「私が現在利用可能な全てのツールをリストアップしてください。
特に以下のキーワードを含むツールを探しています：
- filesystem
- directory
- read_text
- write_file
- list_」
```

### Step 2: Filesystem MCPツールを特定して使用
正しいツール名が判明したら、以下のように使用：

```
「[正しいツール名]を使って /storage/emulated/0/Download の内容を表示してください」
```

例：
```
「filesystem__list_directory を使って /storage/emulated/0/Download の内容を表示してください」
```

### Step 3: .gemini/settings.jsonでツール名を制御（オプション）

特定のツールのみを有効化したい場合：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": [
        "/data/data/com.termux/files/home",
        "/storage/emulated/0/Download"
      ],
      "includeTools": [
        "read_text_file",
        "list_directory",
        "write_file"
      ]
    }
  }
}
```

または、特定のツールを除外：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": [
        "/data/data/com.termux/files/home",
        "/storage/emulated/0/Download"
      ],
      "excludeTools": [
        "write_file",
        "edit_file"
      ]
    }
  }
}
```

## トラブルシューティング

### 問題: ツールが見つからない
**確認1**: サーバーが接続されているか
```bash
gemini mcp list
```
→ `✓ filesystem: ... - Connected` が表示されることを確認

**確認2**: Gemini CLIを再起動
MCPサーバーの設定変更後は、Gemini CLIを完全に再起動する必要があります。

**確認3**: デバッグモードで起動
```bash
gemini --debug
```
デバッグモードでツール発見プロセスの詳細を確認できます。

### 問題: パスアクセスエラー
エラーメッセージ例：
```
Path must be within one of the workspace directories
```

**原因**: 組み込みの`list_directory`ツールを使用している（Filesystem MCPツールではない）

**解決策**: `filesystem__list_directory`など、プレフィックス付きのツール名を使用

## 参考情報

- **公式ドキュメント**: https://gemini-cli.xyz/docs/en/tools/mcp-server
- **GitHub**: https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md
- **Filesystem MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

---

**作成日**: 2025-10-12
**目的**: Gemini CLIでFilesystem MCP Serverのツールを正しく使用するためのガイド
