# AI Assistant Knowledge Hub

AIアシスタントへの指示書・ワークフロー・テンプレートを一元管理する中央知識リポジトリ

## 概要

AI Assistant Knowledge Hubは、AIアシスタント（Claude、ChatGPT、Gemini等）への指示を体系的に管理し、一貫性のある高品質な作業を実現するための中央知識リポジトリです。このプロジェクトは、AIとの協業において発生する以下の課題を解決します：

- **指示の分散・不一致**: 複数のプロジェクトで異なるAI指示が使われることによる品質のばらつき
- **知識の属人化**: 効果的なAI活用ノウハウが個人に蓄積され、組織で共有されない問題
- **再利用性の欠如**: 過去に作成した優秀な指示書・ワークフローが再活用されない問題

このリポジトリを通じて、AIへの指示を標準化し、継続的に改善・蓄積することで、AI協業の効率性と品質を向上させます。

## 核心となる概念

AI Assistant Knowledge Hubは、3つの核心的な概念に基づいて設計されています：

### 🏛️ **憲法 (Constitution)**
AIの不変の行動原則を定める基本法。プロジェクトや状況に関係なく、AIが常に遵守すべき基本的なルール・価値観・倫理観を規定します。

### 📋 **マニュアル (Manual)**
再利用可能な作業手順書・ワークフロー・テンプレートを格納します。具体的な作業パターンを標準化し、品質の一貫性を保ちながら効率的な実行を可能にします。

### 📁 **プロジェクト定義書 (Project Definition)**
個別プロジェクトの固有情報・制約・要件を管理します。憲法とマニュアルを基盤として、プロジェクト特有のカスタマイズを行います。

## ディレクトリ構造

```
ai-assistant-knowledge-hub/
├── commons/          # 🏛️ 憲法：AIの不変の行動原則を格納
│   ├── ethics.md     # AI倫理・価値観の基本原則
│   ├── principles.md # 作業品質・アプローチの基本方針
│   └── constraints.md # 技術的制約・安全性の基本ルール
│
├── workflows/        # 📋 マニュアル：再利用可能な作業手順書を格納
│   ├── development/  # 開発関連ワークフロー
│   ├── analysis/     # 分析・調査関連手順
│   └── documentation/ # ドキュメント作成ワークフロー
│
├── templates/        # 📋 マニュアル：報告書・フォーマットの雛形を格納
│   ├── reports/      # 各種報告書テンプレート
│   ├── issues/       # Issue管理テンプレート
│   └── reviews/      # レビュー・評価テンプレート
│
└── projects/         # 📁 プロジェクト定義書：固有情報を管理
    ├── project-a/    # プロジェクトA固有の設定・制約
    ├── project-b/    # プロジェクトB固有の設定・制約
    └── README.md     # プロジェクト管理ガイド
```

### 各ディレクトリの役割

- **commons/**: 全プロジェクト共通の基本原則を格納。AIが常に参照すべき「憲法」的な内容
- **workflows/**: 作業パターンを標準化した手順書。「〇〇の作業をする時はこの流れで」という再利用可能なプロセス
- **templates/**: 報告書や文書の雛形。一貫したフォーマットで品質の標準化を実現
- **projects/**: 個別プロジェクトの固有情報。上記3つの基盤を元に、プロジェクト特有のカスタマイズを管理

## 基本的な使い方

### 1. プロジェクト開始時の準備

```bash
# 1. リポジトリをクローン
git clone https://github.com/bochang999/ai-assistant-knowledge-hub.git

# 2. プロジェクト固有の設定ファイルを確認
cat projects/[your-project]/context.md
```

### 2. AI作業セッションでの活用

```bash
# AIツール（Claude CLI等）でプロジェクトコンテキストを読み込み
claude --context projects/[your-project]/context.md

# または、必要に応じて個別ファイルを参照
claude --context commons/principles.md workflows/development/code-review.md
```

### 3. 新しいワークフローの追加

```bash
# 1. 適切なディレクトリに新しいワークフローファイルを作成
vim workflows/[category]/new-workflow.md

# 2. 変更をコミット
git add workflows/[category]/new-workflow.md
git commit -m "feat: Add new workflow for [specific task]"
git push origin main
```

### 4. プロジェクト固有設定の更新

```bash
# プロジェクトのコンテキストファイルを更新
vim projects/[your-project]/context.md

# 変更を反映
git add projects/[your-project]/context.md
git commit -m "update: Refine project context for [your-project]"
git push origin main
```

## 貢献方法

このプロジェクトへの貢献に興味をお持ちの方は、詳細な貢献ガイドラインについては `CONTRIBUTING.md`（今後作成予定）をご参照ください。

現在は、以下のような貢献を歓迎しています：

- 新しいワークフローや テンプレートの追加
- 既存の手順書の改善・最適化
- プロジェクト固有のベストプラクティスの共有
- バグ報告や機能改善の提案

## ライセンス

このプロジェクトは、AI協業の知識を広く共有することを目的としています。ライセンス詳細については、今後 `LICENSE` ファイルで明確化予定です。

---

**AI Assistant Knowledge Hub** - より良いAI協業のための知識基盤を構築します