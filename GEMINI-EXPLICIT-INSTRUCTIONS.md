# Gemini AIエージェント向け：Filesystem MCPツール使用の明示的な指示

## 🎯 目的
`/storage/emulated/0/Download` ディレクトリの内容を表示する

## ✅ 利用可能なツール
あなたは以下のツールを使用できます：
- `filesystem__list_directory` ← **これを使用**
- `filesystem__read_file`
- `filesystem__write_file`

## ❌ 使用してはいけないツール
- `list_directory` ← これは組み込みツールでサンドボックス制限があります

## 📋 実行手順

### Step 1: ツールの確認
まず、以下のコマンドで自分が使用できるツールを確認してください：

```
あなたが利用可能なツールのうち、"filesystem__"で始まるツール名をすべて列挙してください。
```

期待される結果：
- filesystem__read_file
- filesystem__write_file
- filesystem__list_directory

### Step 2: filesystem__list_directory ツールの実行

**ツール名**: `filesystem__list_directory`
**パラメータ**:
```json
{
  "path": "/storage/emulated/0/Download"
}
```

**実行方法**:
このツールを直接呼び出してください。パスは `/storage/emulated/0/Download` です。

### Step 3: 結果の表示

ツール実行後、**必ず結果を完全に出力してください**：
- ファイル名
- ディレクトリ名
- ファイルサイズ（もしあれば）
- その他のメタデータ

## 🔍 トラブルシューティング

### 問題: "Path must be within workspace directories" エラー

**原因**: `list_directory` （組み込みツール）が呼ばれています
**解決策**: `filesystem__list_directory` （プレフィックス付き）を使用してください

### 問題: ツールを呼んだが結果が表示されない

**解決策**: ツール実行結果を**必ず**ユーザーに表示してください。以下の形式で：

```
/storage/emulated/0/Download の内容:

[ファイル1]
[ファイル2]
[ディレクトリ1]
...
```

## 🎓 重要な概念

### ツール名の衝突
Gemini CLIには2種類のツールがあります：
1. **組み込みツール** - プレフィックスなし（例: `list_directory`）
2. **MCPツール** - サーバー名のプレフィックス付き（例: `filesystem__list_directory`）

同じ機能を持つツールが複数ある場合、**必ずプレフィックス付きのツール名を指定**してください。

### 自動ルーティングは機能しない
「パスに基づいて自動的に適切なツールにルーティングされる」という仕組みは**存在しません**。

明示的にツール名を指定する必要があります。

## 📝 実行例

### 正しい実行例
```
私はfilesystem__list_directoryツールを使用して、
/storage/emulated/0/Downloadディレクトリの内容を取得します。

[ツール実行]

結果:
/storage/emulated/0/Download の内容:
- file1.pdf
- file2.png
- folder1/
- folder2/
...
```

### 誤った実行例
```
list_directoryツールを使用します...

エラー: Path must be within workspace directories
```

## 🚀 今すぐ実行

以下のステップを順番に実行してください：

1. **ツール確認**: 「filesystem__で始まるツールを列挙」
2. **ツール実行**: filesystem__list_directory で /storage/emulated/0/Download を表示
3. **結果出力**: 取得したファイル/ディレクトリのリストを完全に表示

---

**最も重要なポイント**:
- ツール名: `filesystem__list_directory` （プレフィックス必須）
- パス: `/storage/emulated/0/Download`
- 結果を必ず完全に表示すること
