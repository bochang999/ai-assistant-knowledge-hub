# Python Security Guard System
ai-assistant-knowledge-hub統合セキュリティシステム

## 概要

PDFで特定された15の危険パターンを検出し、AI生成Pythonコードのセキュリティを「動く」前に「安全」にするシステムです。

## 設計思想

**「動くコード」よりも「セキュアなコード」** - PDFの教訓に基づき、以下の3層防御を実装：

1. **Pre-generation**: Python書く前のガードレール
2. **Post-generation**: AI生成後の即座チェック
3. **Pre-deployment**: 本番反映前の最終検証

## 検出可能な危険パターン（PDF準拠）

### 🔴 クリティカル（即座に修正）
- `eval()`/`exec()` 使用
- `shell=True` コマンドインジェクション
- ハードコード秘密情報

### 🟡 高重要度
- SQLインジェクション脆弱性
- SSL検証無効化 (`verify=False`)
- Pickle deserialization
- unsafe YAML loading

### 🟠 中重要度
- 雑な例外処理 (`except:`, `except Exception:`)
- 可変デフォルト引数
- タイムゾーン未指定datetime
- ログでの機密情報出力

### 🟢 低重要度
- 浮動小数点直接比較
- パフォーマンス問題
- リソース未解放

## 使用方法

### 基本的なチェック
```bash
# 単一ファイルチェック
python -m security.cli check test_dangerous_code.py

# ディレクトリ全体チェック
python -m security.cli check src/

# クリティカル問題のみ表示
python -m security.cli check file.py --severity critical
```

### ai-assistant-knowledge-hubワークフロー統合
```bash
# 既存ワークフローと統合
python -m security.cli workflow --phase 2 --issue-id BOC-123

# Linear Issue自動作成
python -m security.cli check file.py --create-issue --issue-id BOC-123
```

### pre-commitフック設定
```bash
python -m security.cli setup --pre-commit
```

## アーキテクチャ

```
security/
├── analyzer.py              # メインセキュリティ解析エンジン
├── models.py                # データモデル・セキュリティ分類
├── rules/                   # セキュリティルールエンジン
│   ├── dangerous_apis.py    # 危険API検出
│   ├── secrets.py           # 秘密情報検出
│   └── patterns.py          # パターンベース検出
├── integrations/            # 外部システム統合
│   ├── linear_reporter.py   # Linear Issue自動作成
│   └── workflow_hooks.py    # ワークフロー統合
├── config/
│   └── security_config.yaml # 設定ファイル
└── cli.py                   # CLIエントリポイント
```

## Linear Issue統合

セキュリティ問題を自動でLinear Issueとして作成・追跡：

- **自動Issue作成**: クリティカル/高重要度問題を検出時
- **進捗追跡**: セキュリティスコアの改善状況をコメント
- **サマリーレポート**: プロジェクト全体のセキュリティ状況

## 設定カスタマイズ

`security/config/security_config.yaml`で以下をカスタマイズ可能：

```yaml
# 有効にするルール選択
rules_enabled:
  - eval_usage
  - shell_injection
  - hardcoded_secrets

# Linear統合設定
linear_integration:
  auto_create_issues: true
  severity_threshold: "high"

# ワークフロー統合
workflow_integration:
  block_on_critical: true
```

## 実装フェーズ

### ✅ Phase 1 完了: MVP
- 危険API検出（eval, exec, shell=True）
- ハードコード秘密情報検出
- 雑な例外処理検出
- Linear Issue統合

### 🔄 Phase 2 計画: 拡張
- SQLインジェクション検出
- パストラバーサル検出
- 高度なパターン解析

### 🔮 Phase 3 将来: 高度化
- データフロー解析
- AI生成コードリアルタイム監視
- 自動修正提案

## 技術スタック

- **静的解析**: Python AST + 正規表現
- **統合**: Linear GraphQL API
- **設定**: YAML設定ファイル
- **拡張性**: プラガブルルールエンジン

## セキュリティ効果

PDFの15危険パターン対応により：
- **任意コード実行防止**: eval/exec検出で即座にブロック
- **インジェクション防止**: SQL/コマンドインジェクション早期発見
- **情報漏洩防止**: ハードコード秘密情報とログ出力監視
- **運用安全性向上**: タイムゾーン・例外処理の問題解決

## 貢献とフィードバック

このシステムはai-assistant-knowledge-hubの一部として、長期的視野でセキュリティ向上を目指しています。

---
*🤖 Generated with [Claude Code](https://claude.ai/code)*
*🔒 Powered by Python Security Guard System*
