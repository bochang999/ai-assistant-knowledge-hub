# FileSystemMCP 徹底攻略ガイド ＆ フォルダ名エイリアス・ワークフロー

## 1. FileSystemMCP とは

FileSystemMCP (Model Context Protocol for File System) は、AIアシスタントがあなたのローカルファイルシステムと安全に対話するための「橋渡し」をするプロトコル（通信ルール）です。

### 主な目的と利点

-   **セキュリティ**: AIは許可されたディレクトリ（サンドボックス）の外にあるファイルには一切アクセスできません。これにより、意図しないファイルの読み書きや削除を防ぎます。
-   **対話的なファイル操作**: AIが `read_file` や `write_file` のようなツールを使って、人間と対話しながらファイル操作を行えるようになります。
-   **OS非依存**: MCPは標準的な入出力で通信するため、Windows, macOS, Linuxなど、さまざまなOSで同じように動作します。

この環境では、クライアントアプリケーション（Claude Desktop）がFileSystemMCPサーバーをバックグラウンドで起動し、AIとの間の通信を仲介しています。

## 2. この環境での権限設定

この環境では、ファイルシステムへのアクセス許可は `~/.claude/settings.local.json` ファイル内の `permissions` ブロックで管理されています。

```json
{
  "permissions": {
    "allow": [
      "Read(//storage/emulated/0/Documents/**)",
      "Read(//storage/emulated/0/Download/**)",
      "Read(//storage/emulated/0/Pictures/Screenshots/**)",
      "Read(//storage/emulated/0/Pictures/**)"
    ],
    "deny": [],
    "ask": []
  }
}
```

-   `Read(...)` という形式で、読み取りを許可するディレクトリを指定します。
-   `**` は、そのディレクトリ以下のすべてのファイルとサブディレクトリを対象とすることを示します。
-   新しいディレクトリへのアクセスを許可したい場合は、この `allow` リストに新しい `Read(...)` の行を追加する必要があります。

## 3. フォルダ名のエイリアス（別名）ワークフロー

現在の設定では、パスに直接「ドキュメントフォルダ」のような分かりやすい名前を付ける（エイリアスする）機能はサポートされていません。

その代わりとして、**分かりやすい名前を実際のフォルダパスに変換する**ためのワークフロー（スクリプト）を導入しました。

### 使い方

`ai-assistant-knowledge-hub/scripts/` にある `get_folder_path.sh` スクリプトを使用します。

このスクリプトに「名前」を渡すと、対応するフルパスを返します。

#### 使用例

```bash
# スクリプトを直接実行してパスを取得する
path=$(/data/data/com.termux/files/home/ai-assistant-knowledge-hub/scripts/get_folder_path.sh ドキュメントフォルダ)
echo $path
# 出力: /storage/emulated/0/Documents/

# lsコマンドと組み合わせて使う
ls "$(/data/data/com.termux/files/home/ai-assistant-knowledge-hub/scripts/get_folder_path.sh ダウンロードフォルダ)"
```

### 現在の対応表

| 名前 | パス |
| :--- | :--- |
| `ドキュメントフォルダ` | `/storage/emulated/0/Documents/` |
| `ダウンロードフォルダ` | `/storage/emulated/0/Download/` |
| `スクリーンショットフォルダ` | `/storage/emulated/0/Pictures/Screenshots/`|
| `ピクチャーフォルダ` | `/storage/emulated/0/Pictures/` |
| `写真フォルダー` | `/storage/emulated/0/Pictures/` |

### 新しい名前（エイリアス）を追加する方法

1.  `ai-assistant-knowledge-hub/scripts/get_folder_path.sh` ファイルを開きます。
2.  `case "$FOLDER_NAME" in` のブロック内にある既存の対応表に、新しい項目を追加します。

    **例：「動画フォルダ」を追加する場合**

    ```bash
    # ... 既存のcase文 ...
        "ピクチャーフォルダ" | "写真フォルダー")
            echo "/storage/emulated/0/Pictures/"
            ;;
        "動画フォルダ") # << 新しい行を追加
            echo "/storage/emulated/0/Movies/" # << 対応するパスを追加
            ;; # << ;; を忘れない
        *)
    # ...
    ```
3.  ファイルを保存すれば、新しい名前が使えるようになります。
