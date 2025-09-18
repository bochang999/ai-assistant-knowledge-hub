# 🤖 AI協業ワークフローシステム - BOC-95ベース段階的問題解決

BOC-95の経験を体系化した、AI協業による持続可能な開発プロセスを実現するワークフローシステムです。

## 🎯 システム概要

このシステムは、Linear IssueからSequential Thinking MCPによる戦略立案、AIレビュー、実装まで、全8フェーズの自動化されたワークフローを提供します。

### 核心理念
- **長期的発展重視**: 即座の解決よりも持続可能な解決策を優先
- **技術的合理性**: Sequential Thinking MCPとAI多段階レビューによる意思決定
- **場当たり的修正の回避**: BOC-95の教訓を活かした体系的アプローチ
- **AI協業最適化**: 人間とAIの効果的な役割分担

## 🏗️ システムアーキテクチャ

### 8フェーズワークフロー

```
Phase 1: Issue Intelligence & Project Discovery
    ↓ (Linear API + project_map.json)
Phase 2: Project Context Analysis
    ↓ (構造スキャン + 技術スタック分析)
Phase 3: Issue Requirements Analysis
    ↓ (要件抽出 + 影響分析)
Phase 4: Strategic Planning (Sequential Thinking MCP統合) ⭐
    ↓ (長期戦略立案 + アーキテクチャ影響評価)
Phase 5: Report Generation & Linear Integration
    ↓ (包括レポート + Linear自動更新)
Phase 6: AI Review & Decision Engine
    ↓ (Gemini+Claude多段階レビュー + 技術的合理性判定)
Phase 7: Implementation Execution
    ↓ (段階的実装 + 品質チェック)
Phase 8: Documentation & Continuity
    ↓ (GitHub自動commit + 次回セッション用コンテキスト保存)
```

## 🚀 使用方法

### 基本実行

```bash
# 完全ワークフロー実行
python lib/workflow_coordinator.py execute BOC-123

# 特定フェーズ範囲実行
python lib/workflow_coordinator.py phase 1 4 /path/to/project

# ワークフロー再開
python lib/workflow_coordinator.py resume session_id_20240919_143000
```

### 個別フェーズ実行

```bash
# Phase 1: Issue Discovery
python workflows/phase1-issue-discovery.py BOC-123

# Phase 4: Strategic Planning (Sequential Thinking MCP)
python workflows/phase4-strategic-planning.py /path/to/project
```

## ⚙️ 設定・要件

### 必要な設定ファイル

```bash
# Linear API設定
~/.linear-api-key       # Linear APIキー
~/.linear-team-id       # Linear チームID

# プロジェクトマッピング
project_map.json        # プロジェクトタグ→ディレクトリマッピング
```

## 🔧 主要機能

### Sequential Thinking MCP統合 (Phase 4)
- **長期的戦略立案**: MCPによる体系的思考プロセス
- **技術的合理性評価**: アーキテクチャ影響分析
- **代替アプローチ検討**: リスク軽減策の立案

### AI多段階レビュー (Phase 6)
- **Gemini + Claude**: 複数AIによるレビュー
- **技術的合理性判定**: 自動判定アルゴリズム
- **代替案生成**: レビュー結果に基づく改善提案

### 品質保証システム
- **品質ゲート**: 各フェーズでの品質チェック
- **自動リカバリ**: エラー時の自動復旧機能
- **進捗追跡**: リアルタイム状況監視

### 継続性保証
- **セッション管理**: 中断・再開対応
- **コンテキスト保存**: 次回セッション用状態保存
- **GitHub統合**: 自動commit・push

---

**生成システム**: BOC-95ベースAI協業ワークフローシステム
**バージョン**: 1.0.0
**最終更新**: 2024-09-19
