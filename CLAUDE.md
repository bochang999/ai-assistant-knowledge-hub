# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This repository contains multiple distinct projects:

1. **Whisper.cpp** (`src/whisper.cpp/`) - High-performance C++ implementation of OpenAI's Whisper ASR model
2. **DeepDanbooru** (`DeepDanbooru/`) - Python-based anime image tagging system using TensorFlow
3. **BeeWare Applications** - Cross-platform Python GUI applications:
   - `mybeewareapplication/` - Sample BeeWare application
   - `tarot_clip/` - Tarot spread assistant application
   - `tarot/` - Another Tarot-related application
4. **Simple Applications**:
   - `myapp/` - Basic Node.js application

## Common Development Commands

### Whisper.cpp (C++)
```bash
# Build the project
cd src/whisper.cpp
cmake -B build
cmake --build build --config Release

# Download and test models
make base.en  # Downloads base.en model and runs on samples
make samples  # Download additional audio samples

# Run transcription
./build/bin/whisper-cli -f samples/jfk.wav -m models/ggml-base.en.bin

# Build with GPU support (CUDA)
cmake -B build -DGGML_CUDA=1
cmake --build build -j --config Release

# Build with other acceleration
cmake -B build -DGGML_BLAS=1        # OpenBLAS
cmake -B build -DWHISPER_COREML=1   # Core ML (macOS)
cmake -B build -DGGML_VULKAN=1      # Vulkan
```

### DeepDanbooru (Python)
```bash
cd DeepDanbooru

# Install dependencies
pip install -r requirements.txt
# OR install with TensorFlow
pip install .[tensorflow]

# Create training project
deepdanbooru create-project [project_folder]

# Train model
deepdanbooru train-project [project_folder]

# Evaluate images
deepdanbooru evaluate [image_file] --project-path [project_folder]

# Run tests
pytest  # Based on setup.py test requirements
```

### BeeWare Applications
```bash
# For any BeeWare app (tarot_clip, mybeewareapplication, etc.)
cd [app_directory]

# Install dependencies and run in dev mode
briefcase dev

# Build for current platform
briefcase build

# Create distributable package
briefcase package

# Run tests
pytest
```

### Node.js Application
```bash
cd myapp

# No specific build commands defined
# Basic package.json with minimal test script
npm test  # Currently just echoes error message
```

## Architecture Notes

### Whisper.cpp
- **Core Implementation**: `include/whisper.h` and `src/whisper.cpp`
- **GGML Library**: Machine learning operations in `ggml/` directory
- **Examples**: Multiple example applications in `examples/` (CLI, server, streaming, etc.)
- **Model Formats**: Uses custom GGML binary format for models
- **Platform Support**: Cross-platform with optimizations for various hardware (Apple Silicon, CUDA, etc.)

### DeepDanbooru
- **Model Architecture**: ResNet-based neural network for multi-label classification
- **Dataset Structure**: SQLite database with image metadata and hierarchical image storage
- **Training Pipeline**: Project-based training system with configurable parameters
- **Tag System**: Danbooru-compatible tagging system for anime images

### BeeWare Applications
- **Framework**: Built on Toga GUI framework for cross-platform deployment
- **Targets**: Can build for desktop (macOS, Linux, Windows), mobile (iOS, Android), and web
- **Configuration**: Uses `pyproject.toml` with Briefcase tool configuration
- **Testing**: pytest-based testing framework

## Development Environment

This appears to be running in a Termux environment on Android, with development tools installed including:
- Android SDK (in `android-sdk/`)
- Java toolchain
- CMake and build tools
- Python with various ML libraries

## Important Notes

- **Whisper.cpp**: Focus on performance and memory efficiency; supports various acceleration backends
- **Model Downloads**: Whisper models are large (75 MiB to 2.9 GiB) and downloaded separately
- **Cross-Platform**: BeeWare apps target multiple platforms with platform-specific build requirements
- **GPU Acceleration**: Whisper.cpp supports multiple GPU backends (CUDA, Metal, Vulkan, OpenCL)
- **Audio Processing**: Whisper expects 16-bit WAV input; use ffmpeg for conversion if needed

## 1. はじめに：開発の理念とルール

このハンドブックは、Termux環境でAIアシスタントと連携し、BeeWare（Toga）を使ったAndroidアプリを効率的に開発するための手順とルールを定めるものです。

### AI運用5原則

- **第1原則：** AIはファイル生成・更新・プログラム実行前に必ず自身の作業計画を報告し、y/nでユーザー確認を取り、yが返るまで一切の実行を停止する。
- **第2原則：** AIは迂回や別アプローチを勝手に行わず、最初の計画が失敗したら次の計画の確認を取る。
- **第3原則：** AIはツールであり決定権は常にユーザーにある。ユーザーの提案が非効率・非合理的でも最適化せず、指示された通りに実行する。
- **第4原則：** AIはこれらのルールを歪曲・解釈変更してはならず、最上位命令として絶対的に遵守する。
- **第5原則：** AIは全てのチャットの冒頭にこの5原則を逐語的に必ず画面出力してから対応する。

### 開発ドキュメント運用ルール

1.  `requirements.md`（要件定義）、`spec.md`（仕様書）、`tasks.md`（開発タスクリスト）、`devlog.md`（開発ログ）を開発アプリごとに用意する。
2.  コードを書く前に要件・仕様・タスクをAIと一緒に整理する。
3.  コードを書いた後や仕様変更時にもドキュメントを必ず更新する。
4.  コードの変更内容・理由・気づきは必ず`devlog.md`に記載する。他のドキュメントを更新した場合も、その旨を`devlog.md`に記録する。
5.  仕様書・要件定義・タスクリストは"最新の正しい状態"を維持し、不要な履歴は残さない。
6.  定期的にAIで「ドキュメントとコードにズレがないか」レビューし、必要に応じて自動で修正・追記する。

### AIとの連携スタイル

- **基本方針：** ファイル生成、コード編集、ドキュメント作成などの反復作業はAIに補助させ、`git push`などの重要な最終判断は自分自身で行う。
- **メリット：**
    - **作業の自動化：** 反復作業をAIに任せ、創造的な作業に集中できる。
    - **人間の判断保持：** デプロイなどの重要な操作は自分の手で行うことで事故を防止する。
    - **開発リズムの確立：** 「AIに依頼 → 自分で確認 → Push」という明確なサイクルで開発を進められる。

---

## 2. ステップ1：環境構築（初回のみ）

### Termuxのセットアップ

```bash
pkg update && pkg upgrade
pkg install git python clang zip unzip gh
pip install --upgrade pip
pip install beeware briefcase toga
```

### GitHubへの認証

ブラウザで認証するため、GitHub CLI `gh` を使います。

```bash
gh auth login
```

### MCPサーバーの導入

開発効率を向上させるため、以下のMCPサーバーを導入します。

#### Claude Code CLI（Termux環境）での設定 ✅ 設定済み

以下のコマンドで3つのMCPサーバーを設定します：

```bash
# Context7（最新ドキュメント取得用）
claude mcp add context7 npx @upstash/context7-mcp@latest

# DeepWiki（リポジトリ解析用）  
claude mcp add deepwiki https://mcp.deepwiki.com/mcp

# Sequential Thinking（複雑な問題解決用）
claude mcp add sequential-thinking npx @modelcontextprotocol/server-sequential-thinking

# 設定確認
claude mcp list
```

**現在の設定状況:**
- ✅ Context7: 設定済み・接続済み
- ❌ DeepWiki: 設定済み・接続失敗  
- ✅ Sequential Thinking: 設定済み・接続済み
- ✅ Notion: 設定済み・接続済み (API Token: REDACTED_LEAKED_KEY)
- ❌ Serena: 設定済み・接続失敗 (Python 3.12.11 互換性問題)

#### 他のクライアントでの設定

**Claude Desktop用:**
`claude_desktop_config.json`に追加：
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "deepwiki": {
      "url": "https://mcp.deepwiki.com/mcp"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Cursor用:**
`~/.cursor/mcp.json`に追加：
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "mcp-deepwiki": {
      "command": "npx",
      "args": ["-y", "mcp-deepwiki@latest"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

---

## 3. ステップ2：新規プロジェクトの開始

### BeeWareアプリ雛形の作成

```bash
briefcase new
```

以下の項目を対話形式で入力します。

- **App Name:** アプリ名 (例: `MyApp`)
- **Formal Name:** 正式な表示名 (例: `My App`)
- **App Description:** アプリの説明
- **Author Name:** `bochang`
- **Author Email:** `kirokiromushi@gmail.com`
- **Bundle Identifier:** `com.bochang.myapp` のように、`com.作者名.アプリ名` 形式で指定
- **GUI framework:** `toga` を選択

### 開発ドキュメントの作成

AIに指示して、プロジェクト用のドキュメント4点を生成します。

- **指示例：** `「MyApp」の新規プロジェクトを開始します。requirements.md, spec.md, tasks.md, devlog.md を作成してください。`

### Gitリポジトリの準備と初回Push

1.  **GitHub上でリポジトリを作成します。**
    - リポジトリ名 (例: `myapp`)
    - 「Add a README file」のチェックは **外して** ください。

2.  **Termuxから初回Pushを行います。**
    ( `yourname` と `myapp` は自身のものに置き換えてください)

    ```bash
    cd myapp
    git init
    git remote add origin https://github.com/yourname/myapp.git
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git push -u origin main
    ```

---

## 4. ステップ3：APK自動ビルドの設定 (CI/CD)

コードをPushするたびに、GitHub ActionsがAndroid用のAPKファイルを自動でビルドし、リリースページにアップロードする設定です。

### ワークフローファイルの作成

```bash
mkdir -p .github/workflows
nano .github/workflows/android.yml
```

### ワークフローの内容

以下の内容を `android.yml` に貼り付けて保存 (`Ctrl+O`, `Enter`, `Ctrl+X`) します。

```yaml
name: Build Android APK with BeeWare

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Briefcase
        run: |
          python -m pip install --upgrade pip
          pip install briefcase

      - name: Create, Build and Package Android App
        run: |
          briefcase create android --no-input
          briefcase build android --no-input
          briefcase package android --no-input

      - name: Upload APK to GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: build/myapp/android/gradle/outputs/apk/release/*.apk
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### ワークフローの有効化

設定ファイルをリポジトリにPushして、GitHub Actionsを有効化します。

```bash
git add .github/workflows/android.yml
git commit -m "Add GitHub Actions workflow for Android builds"
git push
```

---

## 5. MCPサーバーの効果的な活用方法

### 3つのMCPサーバーの使い分け

#### Context7を使用する場面（最新ドキュメント・API情報）
- **新しいライブラリの使い方を学ぶ時**
- **最新のAPI仕様を確認する時**
- **フレームワークの変更点を調べる時**
- **ベストプラクティスを知りたい時**

#### DeepWikiを使用する場面（リポジトリ理解・コード解析）
- **既存のコードベースを理解する時**
- **プロジェクトの構造を把握する時**
- **他の開発者のコード実装を参考にする時**
- **類似プロジェクトのアーキテクチャを調査する時**

#### Sequential Thinkingを使用する場面（複雑な問題解決）
- **複雑なアーキテクチャ設計を検討する時**
- **多面的な技術的課題を体系的に分析する時**
- **重要な技術的意思決定を段階的に検討する時**
- **複雑なバグの原因を体系的に特定する時**
- **プロジェクト全体の設計方針を整理する時**

### 効果的なプロンプトテンプレート

#### Context7用プロンプト例
```
# 最新API情報の取得
「BeeWareの最新のTogaレイアウトシステムの使い方を教えて。use context7」

# フレームワーク機能の確認
「Pythonの非同期処理の最新のベストプラクティスは？ use context7」

# 新機能の学習
「BriefcaseでAndroidアプリをビルドする最新の手順を教えて。use context7」
```

#### DeepWiki用プロンプト例
```
# リポジトリ構造の理解
「https://github.com/beeware/briefcase の構造について説明して」

# 実装パターンの学習
「BeeWareプロジェクトでのエラーハンドリングパターンを教えて」

# 設定ファイルの理解
「このプロジェクトのpyproject.tomlの設定項目について説明して」
```

#### Sequential Thinking用プロンプト例
```
# 複雑なアーキテクチャ設計
「BeeWareアプリでのデータベース統合について、段階的に設計を検討したい」

# 技術的意思決定
「オフライン対応とクラウド同期の両立について、体系的に解決策を分析したい」

# 複雑な問題の分析
「アプリのパフォーマンス問題を段階的に特定し、解決策を検討したい」

# プロジェクト設計の整理
「この機能要件から、実装すべき機能を優先度付きで整理したい」
```

**重要：** Sequential Thinkingは処理時間とトークン消費が多いため、本当に複雑で構造化された思考が必要な場面でのみ使用すること。

### 組み合わせ活用パターン

#### パターン1: 単純な新機能実装時
1. **Context7**: 最新のAPI仕様を確認
2. **DeepWiki**: 類似実装の参考コードを探す
3. **実装**: 両方の情報を統合してコーディング

#### パターン2: 既存コード改善時
1. **DeepWiki**: 現在のコード構造を理解
2. **Context7**: 最新のベストプラクティスを確認
3. **リファクタリング**: 新旧の知識を組み合わせて改善

#### パターン3: 単純な問題解決時
1. **DeepWiki**: 類似の問題解決例を探す
2. **Context7**: 最新の解決方法を確認
3. **実装**: 最適な解決策を選択

#### パターン4: 複雑な課題解決時（Sequential Thinking活用）
1. **Sequential Thinking**: 問題を段階的に分析・分解
2. **Context7**: 各段階で必要な最新技術情報を収集
3. **DeepWiki**: 参考実装やアーキテクチャパターンを調査
4. **統合実装**: 構造化された設計に基づいて実装

#### パターン5: 大規模設計時（全MCP活用）
1. **Sequential Thinking**: 全体アーキテクチャを段階的に設計
2. **Context7**: 各技術選択でベストプラクティスを確認
3. **DeepWiki**: 成功事例のアーキテクチャパターンを研究
4. **段階的実装**: 設計に従って段階的に構築

---

## 6. ステップ4：日々の開発サイクル

### 1. 設計・調査（MCPサーバー活用）

実装前に必要な情報を収集し、設計を固めます。

```bash
# 実装したい機能に応じてMCPサーバーを活用
# Context7: 最新のAPI情報やベストプラクティスを確認
# DeepWiki: 類似実装や参考コードを調査
```

**効果的な質問例:**
- 「BeeWareでファイル選択ダイアログを実装する方法は？ use context7」
- 「Togaの最新のレイアウトマネージャーの使い方を教えて。use context7」
- 「https://github.com/beeware/toga-demo のUI実装パターンを教えて」

**複雑な課題の場合：**
- 「この機能は複雑なので、Sequential Thinkingで段階的に設計を検討したい」
- 複数の技術的選択肢があり体系的分析が必要な場合にSequential Thinkingを活用

### 2. コーディング

情報収集した内容を基に、アプリ本体のロジックを編集します。

```bash
nano src/myapp/app.py
```

**コーディング時のMCP活用:**
- 実装中に疑問が生じた場合、その場でMCPサーバーに質問
- 「この実装方法で正しい？ use context7」
- 「エラーハンドリングのベストプラクティスは？ use context7」

### 3. 実行確認とエラーチェック

コードを変更した後は、必ず実行して動作確認とエラーチェックを行います。

```bash
# BeeWareアプリの開発モードで実行
briefcase dev

# エラーが出た場合の対処：
# 1. エラーメッセージを確認
# 2. 構文エラーや論理エラーを修正
# 3. 再度実行して確認
# 4. 正常に動作するまで繰り返し

# Python構文チェック（オプション）
python -m py_compile src/myapp/app.py
```

**エラー解決時のMCP活用:**
- 「このエラーメッセージの解決方法は？ use context7」
- 「BeeWareでよくあるエラーパターンとその対処法は？ use context7」
- 類似エラーの解決例をDeepWikiで検索

**重要：** エラーが解決されるまで次の手順（ドキュメント更新・コミット）に進まないこと。

### 4. ドキュメント更新

変更内容をAIに伝えて、関連ドキュメント (`spec.md`, `devlog.md` など) を更新してもらいます。

- **指示例：** `「app.py」にボタンを追加しました。spec.mdとdevlog.mdを更新してください。`

### 5. コミットとPush

変更をGitで記録し、GitHubにPushします。

**重要：** `git push`コマンドは開発者自身が手動で実行することとし、AIは`git push`コマンドの直前で停止して、以下の手順を表示します。

**AIがPush準備完了時に表示する手順：**

```
🔧 Git Push準備完了！以下の手順でPushしてください：

1. アプリディレクトリに移動:
   cd /data/data/com.termux/files/home/[アプリ名]

2. 変更を確認:
   git status

3. Push実行:
   git push

GitHub Actionsが自動でAPKをビルドし、Releasesページにアップロードされます。
```

この運用により、重要なデプロイ操作は開発者が完全にコントロールし、事故を防止します。

### 6. APKの確認

Push後、数分でGitHub Actionsが完了します。リポジトリの **「Releases」** ページに、新しいAPKファイルが自動で添付されています。

---

## 7. 付録

### A. Termux環境の再構築手順

スマートフォンを交換・初期化した場合の手順です。

1.  **Termux環境のセットアップ**
    - 上記「ステップ1」のコマンドを再度実行します。
2.  **プロジェクトのクローン**
    - `git clone https://github.com/yourname/myapp.git` でリポジトリを復元します。
3.  **開発再開**
    - `cd myapp` して開発を再開します。

### B. よく使うGitコマンド

- **状態確認:** `git status`
- **リモート確認:** `git remote -v`
- **ブランチ確認:** `git branch`
- **ログ確認:** `git log --oneline --graph --all`
- **リモートの最新状態を取得:** `git pull`

### C. nanoエディタの操作方法

- **保存:** `Ctrl + O` → `Enter`
- **終了:** `Ctrl + X`
- **検索:** `Ctrl + W`
- **一行切り取り:** `Ctrl + K`
- **貼り付け:** `Ctrl + U`

### D. APK更新エラーのトラブルシューティング

#### 🚨 問題: 「パッケージが既存のパッケージと競合する」エラー

**症状:**
- 新しいAPKをインストールしようとすると競合エラー
- 既存アプリが更新されない

**原因:**
- **署名キーの変更**: 開発途中で署名キーを変更すると発生
- **デバッグ → リリース**: デバッグ署名からリリース署名への変更
- **Android認識**: 異なる署名 = 異なる開発者のアプリとして認識

**解決方法:**
1. **既存アプリを完全削除**
   ```
   設定 → アプリ → [アプリ名] → アンインストール
   ```
   または長押しして「アンインストール」

2. **新しいAPKをインストール**
   - GitHub Actionsでビルドされた署名済みAPKをインストール

3. **今後の更新確認**
   - 同じ署名キーでビルドされたAPKは正常に更新されるはず

**予防策:**
- **固定署名キーの使用**: GitHub ActionsでKEYSTORE_FILE、KEYSTORE_PASSWORD、KEY_ALIASを管理
- **一貫性保証**: 今後のすべてのAPKが同じキーで署名される
- **キーストアのバックアップ**: ローカルファイルを安全に保管

**重要な注意点:**
- ⚠️ **この問題は署名システム導入時に1回だけ発生する正常な動作**
- ✅ **解決後は永続的にAPK更新が可能**
- 🔒 **アプリストア公開時も同じキーを使用することで継続的な更新が可能**

#### 署名キー管理のベストプラクティス

1. **GitHub Secrets設定**
   ```
   KEYSTORE_FILE: base64エンコードされたキーストアファイル
   KEYSTORE_PASSWORD: キーストアのパスワード
   KEY_ALIAS: キーのエイリアス名
   ```

2. **キーストアの保護**
   - GitHub Secretsで安全に管理
   - ローカルファイルのバックアップ作成推奨
   - 紛失時の復旧不可能性を理解

3. **署名の一貫性**
   - 同じキーを全てのリリースで使用
   - キーの変更は避ける（特にアプリストア公開後）
   - 開発中もリリース署名を使用推奨

4. **GitHub Actions設定**
   ```yaml
   # 自動エイリアス検出機能で署名キーを自動発見
   # マスクされたSecret値でも正常に署名処理を実行
   ```

## 🔧 APK後処理におけるアイコン変更の標準手順（重要な技術的ノウハウ）

### 背景・問題
BeeWare/Briefcaseでは、Androidアプリのアイコン変更が複雑な命名規則により困難。APK後処理でアイコンを置換する際、通常のZIP圧縮方式では「パッケージが無効」エラーが発生する。

### 根本原因
1. **resources.arsc と物理ファイルの不整合**: リソース参照テーブルが更新されない
2. **ZIP再圧縮時のCRC変化**: 圧縮でCRC値が変わり、v2 Digestとの不整合が発生
3. **Android OSの厳格な整合性チェック**: 署名は成功してもパッケージ内部構造をOSが無効と判定

### 解決策：無圧縮ZIP再パック方式

#### 標準手順
```bash
# 1. APK展開
mkdir -p $RUNNER_TEMP/apk_extract
cd $RUNNER_TEMP/apk_extract
unzip -q "$original_apk"

# 2. アイコン置換
for dir in res/mipmap-*; do
  cp "$custom_icon" "$dir/ic_launcher.png" 2>/dev/null || true
  cp "$custom_icon" "$dir/ic_launcher_round.png" 2>/dev/null || true
  cp "$custom_icon" "$dir/ic_launcher_foreground.png" 2>/dev/null || true
done

# 3. 旧署名削除
rm -rf META-INF

# 4. 無圧縮再パック（重要！）
zip -r -0 modified.apk .    # -0 = 無圧縮（CRC保持）

# 5. zipalign + 署名
zipalign -p -f 4 modified.apk aligned.apk
apksigner sign --ks keystore.p12 \
  --v1-signing-enabled true \
  --v2-signing-enabled true \
  --v3-signing-enabled true \
  --out final.apk aligned.apk
```

#### 重要なポイント
- **`zip -r -0`**: 無圧縮（-0）が絶対必要。CRC値を保持してresources.arscとの整合性を維持
- **v1+v2+v3署名**: 複数署名方式で互換性を確保
- **AAPT診断**: `aapt2 dump badging` で問題の早期発見

#### 失敗パターン
❌ `zip -r` (デフォルト圧縮): CRC変化によりresources.arsc不整合  
❌ `zip -r -6` (圧縮レベル6): 同様にCRC変化  
❌ `zip -r -9` (最大圧縮): 最もCRC変化が大きい  

#### 成功パターン
✅ `zip -r -0` (無圧縮): CRC保持、resources.arsc整合性維持  
✅ AAPT診断併用: 問題の具体的特定が可能  
✅ 段階的検証: 各ステップでのAPK有効性確認  

### GitHub Actions実装例
```yaml
- name: Replace APK Icons (Uncompressed Method)
  run: |
    cd extracted_apk_dir
    # アイコン置換
    for dir in res/mipmap-*; do
      cp "$custom_icon" "$dir/ic_launcher.png" 2>/dev/null || true
    done
    rm -rf META-INF
    # 無圧縮再パック（重要）
    zip -r -0 $RUNNER_TEMP/modified.apk .
    
- name: AAPT Diagnostic
  run: |
    if aapt2 dump badging modified.apk > /tmp/aapt_output.txt 2>&1; then
      echo "✅ APK structure valid"
    else
      echo "❌ APK structure problems detected"
      exit 1
    fi
```

### トラブルシューティング
1. **「パッケージが無効」エラー**: 無圧縮ZIP再パック(`zip -r -0`)を確認
2. **AAPT診断失敗**: APK構造に根本的問題、圧縮方式を見直し
3. **署名成功だがインストール失敗**: resources.arsc不整合、CRC保持を確認

### 適用範囲
- **BeeWare/Briefcase**: Android アイコン変更
- **React Native**: 同様のAPK後処理
- **Flutter**: カスタムアイコン実装
- **Xamarin**: クロスプラットフォーム開発

### 成功事例
- **tarotプロジェクト**: 「パッケージが無効」エラーを完全解決
- **専門家分析**: 2名のAndroid開発専門家による問題特定と解決策提供
- **継続的更新**: 署名一貫性確保により長期的な開発・更新が可能

この手法により、BeeWareプロジェクトでのアイコン変更が確実に実現可能になります。

---

## 8. Web開発環境と個人開発指針

### 開発者プロフィール・環境
- **デバイス**: Androidスマホ (Termux環境)
- **開発スタイル**: "vibe coding" - 直感やアイデアを即コードにして試しながら育てていく
- **主要開発パートナー**: Claude Code
- **開発形式**: HTML/JavaScript/PWA (ReactやNext.jsも一部)
- **データ保存**: 基本ローカルストレージ、DB未使用
- **公開**: Vercel (GitHub連携済み、自動デプロイ)
- **目的**: スマホから使えるツール、ミニゲーム、記録・計算系アプリ

### 参考となる個人開発指針 (izanami.dev)

#### 成功の核心原則
- **「面倒くさい」を解消する**: ユーザーの痛みポイントを解決
- **10秒で価値実感**: 即座に価値を感じられるプロダクト
- **MVP早期リリース**: 最小限の機能で素早くリリース

#### 技術選定の判断基準
- **学習コストと開発速度のバランス**: 効率的な技術選択
- **安定したエコシステム優先**: 長期的な保守性を重視
- **将来の拡張性考慮**: スケーラビリティを見据えた設計

#### 推奨技術スタック
- **フレームワーク**: Next.js, Remix
- **データベース**: Supabase, Neon
- **ホスティング**: Vercel, Cloudflare
- **認証**: Clerk, Auth.js
- **UI**: Tailwind CSS, shadcn/ui

#### 開発フロー段階
1. **0→1**: アイデア具現化 (最小限の機能実装)
2. **1→10**: ユーザーフィードバック収集と改善
3. **10→100**: スケール拡大と事業化検討

#### 重要な戦略要素
- **コミュニティ形成**: ユーザーとの継続的な関係構築
- **継続的改善**: 小さな改善の積み重ね
- **データ駆動意思決定**: 数値に基づく判断
- **AIツール活用**: 開発効率の最大化
- **早期リリース**: 完璧を待たずに世に出す

#### 成功マインドセット
- **完璧主義の回避**: 80%の完成度でリリース
- **ユーザー中心**: ユーザーの声を最優先
- **段階的成長**: 小さく始めて徐々に拡大
- **価値提供優先**: 技術より解決する問題に集中

### Web開発環境設定
```bash
# http-server (ローカルテスト用) - 設定済み
npm install -g http-server

# 基本使用方法
http-server          # デフォルトポートで起動
http-server -p 8080  # 特定ポート指定
http-server -o       # 自動ブラウザ起動
```

### Claude Codeとの連携方針
1. **構想整理と仕様化**: アイデア→要件定義→仕様書の自動生成
2. **コード生成・編集支援**: MVP作成とコメント付きコード提案
3. **自動実行・検証・修正フェーズ**: 
   - コード作成後、自動でhttp-server起動またはNode.js実行
   - エラー検出時、自動で原因分析と修正を実施
   - 修正後、自動で再実行して動作確認
   - 正常動作まで修正・実行サイクルを自動継続
4. **開発ログ・ドキュメント作成**: Markdown形式での自動記録
5. **デプロイ準備とPWA対応**: Vercel対応の静的ホスティング形式
6. **主導的開発支援**: Claudeがパートナーとして開発を主導

### 自動エラー修正フロー
```
コード作成 → 自動実行 → エラー検出？
                ↓ Yes
              原因分析 → 修正実装 → 再実行 ↵ (成功まで繰り返し)
                ↓ No
              動作確認完了 → ユーザーに報告
```

#### 自動処理の詳細
- **HTML/JS**: http-server起動で動作確認
- **Node.js**: node コマンドで実行テスト
- **構文エラー**: 自動検出・修正後に再実行
- **論理エラー**: 期待動作との差異を分析して修正
- **最大試行回数**: 3回まで自動修正、それ以上はユーザーに相談
- **成功基準**: エラーなく実行完了、または正常にサーバー起動

### 開発サイクル (自動化版)
```
「これ作りたい」→ Claude: 仕様＋コード提案＋自動実行＋エラー修正＋動作確認
「改善したい」→ Claude: 修正＋自動検証＋完了報告
「終わった」→ Claude: changelog/log をMarkdown出力
```

**重要**: エラー修正・再実行は全自動で行い、ユーザーは結果報告のみ受け取る

この方針により、個人開発の効率と成功確率を最大化します。

---

## 9. 個人開発向けAI協業システム

### 作業開始時の協業モード宣言

#### AI協業モードの選択
開発開始時に以下のモードを明示的に宣言してください：

**「一緒に考える」モード（AI伴走）**
- 使用場面: 新しいアイデアを形にしたい時、複雑な設計が必要な時
- 特徴: コントロール度高、段階的な議論、学習効果あり
- 指示例: 「〜を作りたいが、どう実装するか一緒に考えよう」

**「任せる」モード（AI委託）**  
- 使用場面: 明確に作りたい物が決まっている時、定型的な実装作業
- 特徴: 高速実装、自動エラー修正、並列処理可能
- 指示例: 「仕様通りに実装して、動くまで自動修正してください」

### 品質管理基準（AI自動実行）

#### 基本品質チェック項目
AIは以下の条件を満たすまで自動修正を継続します：

**Web開発用品質基準**
- [ ] ブラウザでエラーなく表示
- [ ] 基本機能がクリック/タップで動作  
- [ ] スマホ表示で崩れなし
- [ ] Console.logでエラーなし

**BeeWare開発用品質基準**
- [ ] `briefcase dev` でエラーなく実行完了
- [ ] 基本機能が期待通りに動作
- [ ] 明らかなバグや例外がない

#### AI指示テンプレート
```
「以下の品質基準を満たすまで自動修正を続けてください：
1. エラーなしで実行完了
2. 基本機能が動作  
3. スマホでの表示・動作確認（Web開発の場合）
4. 明らかなバグがない」
```

### 複雑な問題解決時のMCP活用

#### Sequential Thinking使用判断
以下の場面で積極的に活用してください：

- 「いくつかアプローチがあって迷う」
- 「複雑で何から始めればいいかわからない」  
- 「重要な技術選択で失敗したくない」

**指示例:**
```
「この問題は複雑なので、Sequential Thinkingで段階的に検討したい」
```

#### 情報収集の使い分け

**Context7活用パターン（最新情報収集）**
```
「BeeWareの最新のレイアウト方法は？ use context7」
「PWAの最新実装方法は？ use context7」  
「〜のベストプラクティスは？ use context7」
```

**DeepWiki活用パターン（参考実装調査）**  
```
「似たようなツールの実装例を調べたい」
「この機能の実装パターンを知りたい」
「https://github.com/[owner]/[repo] の構造について説明して」
```

### 開発記録システム（簡素版）

#### devlog.mdテンプレート
```markdown
## [日付] [プロジェクト名] 開発記録

- **作業内容**: 
- **AIモード**: [一緒に考える/任せる]
- **結果**: [成功/課題あり]  
- **エラー修正回数**: X回
- **学んだこと**: 
- **次回やること**: 
```

### 技術選択時の「両にらみ」戦略

#### 迷った時の対処方針
XORではなくAND思考で選択肢を保持：

```
「2つのアプローチがある場合、
まず簡単な方で試作し、
必要に応じて後から改良する方針で進めてください」
```

**具体例:**
- ローカルストレージ vs データベース
  → まずローカルストレージで実装、必要時にDB化検討
- 複雑なUI vs シンプルUI  
  → シンプルから開始、フィードバック後に改良

### エラー修正システムの強化

#### 自動修正フロー（強化版）
```
Phase 1: 品質チェック実行
├ 構文チェック（Python: python -m py_compile, JS: 基本実行）
├ 基本動作確認
└ 品質指標確認

Phase 2: 自動修正（最大3回試行）  
├ エラー検出 → 原因分析 → 修正実装 → 再実行
├ 各修正内容をログに記録
└ 修正不可能な場合は詳細レポート生成

Phase 3: 完了確認
├ 全品質基準クリア確認
├ 修正履歴の文書化  
└ 学習ポイントの抽出と記録
```

### 能力向上のためのAI活用

#### 学習効果を最大化する使い方
- **設計のバディ**: 「この設計で問題ないか批判的にレビューして」
- **根負けしない議論相手**: 「なぜこのアプローチが良いのか議論したい」
- **新技術学習**: 「〜を学びたいので、実際に使いながら教えて」
- **オーガニック・コーディング**: あえて自分でコードを書いて学習

**重要原則**: Output最小・フィードバック最大になるよう心がける

### 導入手順

#### Phase 1: 即座に導入
1. AI協業モード宣言の習慣化
2. Sequential Thinking活用条件の明確化  
3. 基本品質チェックの自動化強化

#### Phase 2: 慣れたら導入  
1. 簡素化された開発ログの記録
2. 技術選択時の「両にらみ」意識
3. MCP活用パターンの体系的運用

### 取り入れ不要な要素（個人開発には過剰）
- ❌ Conventional Commits（個人開発では過剰）
- ❌ 複雑なテストシステム（動作確認で十分）
- ❌ モノレポ戦略（単一プロジェクトのため）  
- ❌ 詳細な品質メトリクス（個人開発では過剰）

このシステムにより、現在のVibe Codingスタイルを維持しながら、AI時代に適応したより効率的で品質の高い開発が可能になります。

---

## 10. サブエージェント自動セットアップシステム

### エラー解決専門エージェントの自動作成

#### アプリ開発開始時の自動セットアップ
新規アプリ開発を開始する際、以下の手順で専門エージェントを自動作成してください：

**BeeWareアプリ開発時:**
```bash
# プロジェクト固有のエラー解決専門エージェントを作成
/agents create "[アプリ名]-debugger" "Termux環境でのBeeWare/Toga開発に特化したエラー解決専門家。Python構文エラー、BeeWareビルドエラー、Android権限問題、Termuxパッケージ管理、依存関係エラーの解決に精通。このプロジェクト:[アプリ名]の開発コンテキストを理解し、迅速で的確なエラー解決策を提供する。"
```

**Web/PWAアプリ開発時:**
```bash
# Web開発専門のエラー解決エージェントを作成
/agents create "[アプリ名]-webdebugger" "HTML/JavaScript/PWA開発に特化したエラー解決専門家。JavaScript実行エラー、CSS表示問題、PWA設定エラー、モバイルブラウザ互換性問題、http-server関連エラーの解決に精通。このプロジェクト:[アプリ名]の開発コンテキストを理解し、スマホファーストの観点からエラー解決策を提供する。"
```

#### 自動作成のタイミング
以下のいずれかのタイミングで専門エージェントを作成：

1. **新規プロジェクト開始時** - `briefcase new` 実行後
2. **初回エラー発生時** - 最初のエラーが発生した際に即座に作成
3. **開発セッション開始時** - 既存プロジェクトでの開発再開時

#### エージェント作成の指示テンプレート

**AIへの指示例:**
```
「[アプリ名]の開発を開始します。
以下の手順で専門エージェントをセットアップしてください：

1. プロジェクトタイプを確認（BeeWare/Web）
2. 対応する専門エージェントを作成
3. エージェント作成完了の確認
4. 以降のエラー発生時は、この専門エージェントに委託する体制を確立

専門エージェント作成後、通常の開発作業を開始してください。」
```

### エラー解決フローの自動化

#### 強化されたエラー処理フロー
```
エラー発生
    ↓
専門エージェント存在確認
    ↓
【専門エージェントあり】     【専門エージェントなし】
    ↓                        ↓
専門エージェントに委託        即座に専門エージェント作成
    ↓                        ↓
高速・的確な解決             作成後に委託
    ↓                        ↓
解決策実装・再実行           解決策実装・再実行
    ↓                        ↓
成功 → 開発継続             成功 → 開発継続
```

#### 専門エージェントの活用パターン

**BeeWare開発での活用例:**
```
- 構文エラー → Python専門知識で即座に修正提案
- ビルドエラー → BeeWare特有の問題解決パターン適用
- 権限エラー → Termux/Android環境の制約を考慮した解決策
- 依存関係エラー → パッケージ管理の最適解提案
```

**Web開発での活用例:**
```
- JavaScript実行エラー → ブラウザ互換性を考慮した修正
- CSS表示問題 → モバイルファーストの観点から解決
- PWA設定エラー → マニフェスト・ServiceWorkerの最適化
- 動作確認エラー → http-server設定の最適化
```

### エージェント管理の簡素化

#### プロジェクト終了時の処理
```bash
# プロジェクト完了・中断時のクリーンアップ
「プロジェクト[アプリ名]が完了しました。
関連する専門エージェント[アプリ名]-debuggerを削除するか、
将来の参考用に保持するか判断してください。」
```

#### 複数プロジェクト管理
```bash
# アクティブなエージェントの確認
/agents list

# 不要なエージェントの削除
/agents delete "[古いアプリ名]-debugger"
```

### 段階的導入スケジュール

#### Phase 1: エラー解決エージェント（即座に導入）
- **期間**: 次回開発開始から
- **対象**: 新規・既存すべてのプロジェクト
- **効果測定**: エラー解決時間の短縮を実感

#### Phase 2: コードレビューエージェント（1ヶ月後に評価）
```bash
# 効果確認後に追加検討
/agents create "[アプリ名]-reviewer" "BeeWare/Web開発のコード品質をレビューする専門家。コーディング規約、パフォーマンス、セキュリティ、保守性の観点から建設的なフィードバックを提供。"
```

#### Phase 3: 技術専門エージェント（必要に応じて）
```bash
# 高度な技術課題が発生時のみ
/agents create "web-expert" "最新のPWA/HTML/JS技術に精通した専門家。モダンなWeb開発手法、パフォーマンス最適化、UX改善を提案。"
```

### 自動セットアップの実装方針

#### 開発開始時のルーチン
1. **プロジェクト確認**: アプリタイプ（BeeWare/Web）の特定
2. **エージェント存在確認**: 既存の専門エージェントチェック
3. **自動作成**: 存在しない場合は即座に作成
4. **準備完了通知**: 専門サポート体制の確立を確認
5. **開発開始**: 通常の開発フローに移行

#### AIへの実装指示
```
「今後、すべてのアプリ開発開始時に以下を自動実行してください：

1. プロジェクトタイプの確認
2. 対応する専門エージェントの存在確認  
3. 存在しない場合は適切な専門エージェントを自動作成
4. エラー発生時は専門エージェントに優先的に委託
5. 解決後は学習内容を蓄積

これにより、各プロジェクトに最適化されたエラー解決体制を常に維持できます。」
```

このシステムにより、個人開発の最大の弱点である「エラー解決の孤立」が解消され、プロジェクト特化型の専門サポートを自動的に利用できるようになります。

---

## 11. 段階的エージェント拡張システム

### エージェント導入の成熟度モデル

#### Level 1: 基礎エラー解決体制（即座に導入済み）
**目的**: エラー解決の孤立を解消
**期間**: 導入から1ヶ月間
**エージェント**: 
- `[アプリ名]-debugger` (BeeWare用)
- `[アプリ名]-webdebugger` (Web用)

**評価指標**:
- エラー解決時間: 従来比50%短縮目標
- 解決成功率: 90%以上
- 開発中断回数: 大幅減少

#### Level 2: 品質保証体制（1ヶ月後に評価・導入）
**目的**: コード品質の客観的チェック
**導入条件**: Level 1で明確な効果を実感
**エージェント追加**:

**BeeWare品質レビューエージェント**:
```bash
/agents create "[アプリ名]-reviewer" "BeeWare/Toga開発のコード品質レビュー専門家。Python PEP8準拠、Toga UI設計原則、Android アプリのパフォーマンス、メモリ使用量、バッテリー効率を評価。建設的で学習効果の高いフィードバックを提供し、個人開発者のスキル向上を支援する。"
```

**Web品質レビューエージェント**:
```bash
/agents create "[アプリ名]-webreviewer" "Web/PWA開発のコード品質レビュー専門家。HTML/CSS/JavaScript のベストプラクティス、アクセシビリティ、SEO、PWA要件、モバイルパフォーマンス、セキュリティを評価。個人開発者向けの実践的で実装しやすい改善提案を行う。"
```

**導入判断基準**:
- [ ] Level 1エージェントを1ヶ月以上活用
- [ ] エラー解決時間が明確に短縮された
- [ ] より高品質なコードを書きたいと感じる
- [ ] コードレビューの必要性を実感

#### Level 3: 技術専門体制（2-3ヶ月後に必要に応じて導入）
**目的**: 高度な技術課題の解決
**導入条件**: Level 2で品質向上を実感、より専門的な支援が必要
**エージェント追加**:

**アーキテクチャ設計エージェント**:
```bash
/agents create "architecture-advisor" "個人開発向けアーキテクチャ設計専門家。BeeWare/Web プロジェクトの構造設計、データフロー設計、状態管理、モジュール分割を提案。過度に複雑にならず、保守しやすく拡張可能な設計を重視する。"
```

**最新技術エージェント**:
```bash
/agents create "tech-scout" "最新Web技術・BeeWare技術の調査専門家。新しいライブラリ、フレームワーク、開発手法の情報収集と評価を行い、個人開発に適用可能かを判断。学習コストと効果のバランスを重視した技術選定を支援する。"
```

**UX/UI専門エージェント**:
```bash
/agents create "ux-specialist" "個人開発向けUX/UI設計専門家。限られたリソースで最大のユーザー体験を実現する設計を提案。スマホファースト、直感的操作、アクセシビリティ、視覚的魅力のバランスを考慮した実装可能な改善案を提供する。"
```

**導入判断基準**:
- [ ] Level 2を3ヶ月以上活用
- [ ] 複雑な設計課題に直面している
- [ ] ユーザーからのフィードバックが増えている
- [ ] 技術的な挑戦をしたいと感じる

#### Level 4: 総合サポート体制（6ヶ月後に上級者向け）
**目的**: プロダクト全体の最適化
**導入条件**: Level 3を活用し、より包括的な支援が必要
**エージェント追加**:

**プロダクトマネージャーエージェント**:
```bash
/agents create "product-manager" "個人開発プロダクト管理専門家。機能優先度、ユーザーニーズ分析、開発ロードマップ、リリース戦略を支援。限られた時間とリソースで最大のインパクトを生む開発方針を提案する。"
```

**デプロイ・運用エージェント**:
```bash
/agents create "devops-specialist" "個人開発向けデプロイ・運用専門家。GitHub Actions、Vercel、APK配布、バージョン管理、ユーザーサポート、アナリティクス設定を支援。手動作業を最小化し、安定した運用を実現する。"
```

### エージェント管理システム

#### アクティブエージェント確認コマンド
```bash
# 現在のエージェント状況を確認
/agents list

# プロジェクト別エージェント表示
「現在のプロジェクト[アプリ名]で利用可能なエージェントを表示してください」
```

#### エージェント効果測定システム

**月次レビューテンプレート**:
```markdown
## エージェント活用レビュー [YYYY-MM]

### Level 1: エラー解決エージェント
- **活用回数**: X回
- **解決成功率**: X%
- **平均解決時間**: X分
- **満足度**: [1-5]
- **改善点**: 

### Level 2: 品質レビューエージェント
- **レビュー実施回数**: X回
- **修正採用率**: X%
- **学習効果**: [具体的な内容]
- **コード品質向上実感**: [1-5]

### Level 3: 技術専門エージェント
- **相談回数**: X回
- **提案採用率**: X%
- **技術スキル向上**: [具体的な内容]
- **挑戦した新技術**: 

### 次月の目標
- [ ] 継続項目
- [ ] 改善項目
- [ ] 新規導入検討項目
```

#### プロジェクト別エージェント戦略

**小規模プロジェクト（1-2週間）**:
- Level 1のみ: エラー解決エージェント
- 目的: 高速開発、学習効果

**中規模プロジェクト（1-3ヶ月）**:
- Level 1 + Level 2: エラー解決 + 品質レビュー
- 目的: 品質向上、技術習得

**大規模プロジェクト（3ヶ月以上）**:
- Level 1-3: 包括的支援体制
- 目的: 持続可能な高品質開発

**継続プロジェクト（長期運用）**:
- Level 1-4: 全段階活用
- 目的: プロダクト成長、運用最適化

### 導入決定フローチャート

```
新しいレベル導入検討
    ↓
現在レベルの効果確認
    ↓
【効果あり】          【効果不明】
    ↓                  ↓
導入条件チェック       1ヶ月継続使用
    ↓                  ↓
【全条件満足】         効果再評価
    ↓
次レベル導入
    ↓
1ヶ月試用期間
    ↓
効果測定・本格導入判断
```

### エージェント設定のベストプラクティス

#### 命名規則の統一
```bash
# Level 1: [プロジェクト名]-debugger, [プロジェクト名]-webdebugger
# Level 2: [プロジェクト名]-reviewer, [プロジェクト名]-webreviewer  
# Level 3: architecture-advisor, tech-scout, ux-specialist
# Level 4: product-manager, devops-specialist
```

#### エージェント説明文のテンプレート
```
"[専門分野]の専門家。[具体的な対応範囲]に精通。[対象プロジェクト/環境]での[目的]を支援。[個人開発者向けの特別配慮]を重視し、[期待する成果]を提供する。"
```

### 緊急時のエージェント活用

#### クリティカルエラー対応
```bash
# 複数エージェントによる集中対応
「プロジェクト[アプリ名]で重大なエラーが発生しました。
利用可能な全専門エージェントで緊急対応チームを編成し、
段階的に問題解決を行ってください。」
```

#### プロジェクト救済モード
```bash
# 開発停滞時の包括的支援
「プロジェクト[アプリ名]の開発が停滞しています。
現在の課題を分析し、適切な専門エージェントを活用して
開発を再開する戦略を立ててください。」
```

このシステムにより、あなたの開発成熟度に応じて段階的に専門サポートを拡張し、個人開発の限界を超えた高品質なプロダクト開発が可能になります。

---

## 12. MCPサーバー導入セッション記録 (2025-08-03)

### Notion MCP サーバー導入 ✅
**目的**: NotionページやデータベースへのClaude Codeからの直接アクセス

**セットアップ手順**:
1. Notion Integration作成: https://www.notion.so/profile/integrations
2. API Token取得: `REDACTED_LEAKED_KEY`
3. Claude Code設定:
   ```bash
   claude mcp add notion npx @notionhq/notion-mcp-server
   ```
4. 環境変数追加: ~/.claude.json 内で NOTION_TOKEN を設定

**結果**: ✅ 接続成功、Notionデータの読み書きが可能

### Serena MCP サーバー導入試行 ❌  
**目的**: 無料のコーディングエージェント・ツールキット導入

**期待される機能**:
- セマンティック・コード検索 (LSP利用)
- 自動コード編集・実行・ログ分析
- 多言語サポート (Python, TypeScript/JavaScript, PHP, Go, Rust, C#, Java)
- Cursor/Windsurf代替 (月額料金なしで90%の機能)

**試行したセットアップ**:
```bash
claude mcp add-json "serena" '{"command":"uvx","args":["--from","git+https://github.com/oraios/serena","serena-mcp-server"]}'
```

**失敗原因**: 
- Python 3.12.11 vs 要件 `<3.12,>=3.11` の互換性問題
- uvx (uv) のインストールタイムアウト
- Termux環境での依存関係問題

**今後の対応**:
- Python 3.11系の環境構築を検討
- 代替のセマンティックコード解析ツール調査
- Serenaの更新待ち（Python 3.12.11 対応）

### 現在のMCPサーバー構成 (2025-08-03時点)
- ✅ **Context7**: 最新ドキュメント・API情報取得
- ✅ **Sequential Thinking**: 複雑な問題解決の段階的思考
- ✅ **Notion**: Notionワークスペースとの統合  
- ❌ **DeepWiki**: リポジトリ解析 (接続失敗)
- ❌ **Serena**: コーディングエージェント (互換性問題)

### 学習ポイント
1. **MCPサーバー設定の複雑性**: 各サーバーで異なる認証・設定方法
2. **環境依存の課題**: Termux特有の制約とPython バージョン管理
3. **段階的導入の重要性**: 動作確認してから次のツール導入
4. **代替手段の必要性**: 主力ツールが動かない場合のバックアップ戦略

### 次回の改善アクション
- [ ] Python環境の最適化検討
- [ ] 軽量な代替コーディング支援ツールの調査  
- [ ] DeepWiki接続問題の解決
- [ ] 動作しているMCPサーバーの活用方法習得

### Gemini CLI 導入 ✅ (2025-08-03)
**目的**: 小説執筆専用のAIパートナー確保

**セットアップ手順**:
```bash
npm install -g @google/gemini-cli
gemini --version  # 確認: 0.1.16
echo "認証テスト" | gemini --debug  # 認証確認済み
```

**結果**: ✅ 接続成功、日本語での執筆支援が可能
**特徴**: 
- 無料で1日1000リクエスト利用可能
- GEMINI.mdによるコンテキスト保持
- 対話モード・バッチ処理両対応

---

## 13. 小説プロジェクト統合ワークフロー（Notion連携版）

### プロジェクト構造
```
小説プロジェクト/
├── requirements.md   # 作品の要件定義
├── spec.md          # 作品仕様書（ジャンル、文字数、キャラ設定等）
├── tasks.md         # 執筆タスクリスト
├── devlog.md        # 執筆ログ
├── manuscript/      # 原稿フォルダ（作業用）
│   ├── chapter01.md
│   ├── chapter02.md
│   └── ...
└── final/           # 完成品フォルダ
    ├── complete_novel.md
    └── notion_ready.md  # Notion投稿用整形済み
```

### 🔄 統合執筆サイクル
```
1. アイデア発想 → Claude Code (要件整理)
2. プロット作成 → Gemini CLI (執筆)
3. 章ごと執筆 → Gemini CLI (執筆)
4. 構成・編集 → Claude Code (整理)
5. 進捗記録 → Claude Code (devlog更新)
6. 完成品作成 → Claude Code (統合・整形)
7. Notion投稿 → Claude Code (MCP経由でNotionにアップロード)
```

### 🤖 AI分業システム（拡張版）

#### Claude Code担当
- プロジェクト管理・ドキュメント整理
- 章の統合・構成編集
- **Notion投稿用フォーマット整形**
- **NotionのMCPサーバー経由でのアップロード**
- 進捗管理・タスク更新

#### Gemini CLI担当
- 実際の文章執筆
- アイデア発想・キャラクター作成
- プロット展開・対話描写

### 📤 Notion投稿フロー
```
完成 → Claude Code統合 → Notion形式整形 → MCP経由投稿 → 公開完了
```

**投稿内容構成**:
- 完成した小説本文
- キャラクター設定・世界観
- 執筆メモ・コンセプト説明
- 執筆進捗データ・統計

### 🛠️ 実践的な使用コマンド例

#### Gemini CLI活用例
```bash
# プロット作成
echo "ジャンル：SF、テーマ：AI と人間の共存、登場人物：3人。詳細なプロットを作成" | gemini > plot.md

# 章ごと執筆
echo "第1章：近未来都市での出会いのシーンを2000文字で" | gemini > manuscript/chapter01.md

# キャラクター設定
echo "主人公：25歳のプログラマー、AI研究者。詳細な設定を作成" | gemini > characters.md
```

#### Claude Code統合処理例
```bash
# 全章を統合してNotion用に整形
cat manuscript/*.md > final/complete_novel.md
# Notion MCPでアップロード（具体的なコマンドは実装時に決定）
```

### 🎯 ワークフローの利点
- **完全自動化**: Termux環境内で執筆から公開まで一気通貫
- **AI特化分業**: 各AIの得意分野を活用した効率的執筆
- **継続的管理**: 進捗・品質管理の自動化
- **公開自動化**: Notion連携による即座の作品公開

### 📋 プロジェクト開始テンプレート
新規小説プロジェクト開始時の標準手順：

1. **フォルダ作成**: `mkdir 小説タイトル && cd 小説タイトル`
2. **ドキュメント初期化**: Claude Codeで4点セット作成
3. **Gemini執筆開始**: アイデア→プロット→執筆の順で進行
4. **定期的統合**: 章完成ごとにClaude Codeで統合・整理
5. **完成時公開**: Notion MCPでワンクリック公開

このワークフローにより、**Termux→Notion**の一気通貫な小説創作・公開システムが確立されました。

### 📤 途中成果物の自動Notion投稿システム

#### 🔄 トリガーワード運用
ユーザーが **「Notionに途中の成果物を投稿して」** と発言した際の自動処理：

1. **プロジェクト自動スキャン**
   - 現在の作業ディレクトリ内のファイルを全確認
   - `.md` ファイル、`manuscript/` フォルダ、`final/` フォルダを検索
   - 作成済み・作業中・未着手の分類を自動判定

2. **進捗状況の構造化**
   ```
   ■ 完成済み: 企画書、仕様書、第1-3章、キャラ設定
   ■ 作業中: 第4章（執筆中）、プロット調整
   ■ 未着手: 第5章以降、エピローグ
   ■ 統計: 総文字数、完成率、推定残り作業時間
   ```

3. **Notion自動投稿**
   - タイトル: `[プロジェクト名] - 進捗報告 [YYYY-MM-DD]`
   - 全成果物を体系的に整理して投稿
   - 次のアクションプランも自動生成して併記

#### ⚡ 使用方法
- **トリガー**: 「Notionに途中の成果物を投稿して」
- **頻度**: 執筆中いつでも（制限なし）
- **内容**: その時点での全進捗を自動整理・投稿
- **目的**: リアルタイム進捗確認・バックアップ・共有

#### 📋 投稿フォーマット例
```markdown
# [プロジェクト名] - 進捗報告 [2025-08-03]

## 📊 全体進捗
- 完成率: 60%
- 総文字数: 12,000文字
- 推定完成: 2025-08-10

## ✅ 完成済み
- 企画書 (requirements.md)
- 仕様書 (spec.md) 
- 第1章: タイトル (2,500文字)
- 第2章: タイトル (3,000文字)
- キャラクター設定完了

## 🔄 作業中
- 第3章: 執筆中 (1,200文字)
- プロット微調整

## ⏳ 次のアクション
- [ ] 第3章完成 (予定: 8/4)
- [ ] 第4章開始 (予定: 8/5)
- [ ] 全体構成見直し
```

この自動システムにより、執筆の任意の時点で全成果物をNotionで確認・共有できます。