# CLAUDE.md - Essential Development Rules

## Mandatory Knowledge Management System

### 🔄 Linear Issue自動管理システム
```bash
# Issue作業フロー (自動実行):
0. 【必須】ai-assistant-knowledge-hubシステム構造確認
1. Issue読み取り開始 → status: "In Progress"
2. 作業実行・コード実装
3. 作業完了 → 内容・コード記録 → status: "In Review"
→ 許可不要の完全自動管理
```

### 🚫 MANDATORY: Issue作業前システム構造確認
**doit実行後、Issue作業開始前に以下を必ず確認：**
```bash
# 自動確認項目（smart-doit.shで強制実行）
1. ai-assistant-knowledge-hub/project_map.json → プロジェクト一覧確認
2. temp/agent_issue_BOC-XX.json → Issue詳細・プロジェクトタグ確認
3. 対象プロジェクトディレクトリ確認 → 構造把握
4. ↑完了後のみPhase 2開始許可
```
**違反時:** 作業停止・システム確認強制実行

### 📋 Linear Status管理ルール
**開始時:** Issue確認と同時に自動的に "In Progress" に変更
**完了時:** 作業内容とコードを記録後 "In Review" に変更

**実装方法:**
```bash
# Status更新 GraphQL
mutation { issueUpdate(id: "$issue_id", input: { stateId: "$state_id" }) }

# State IDs (固定値):
IN_PROGRESS_ID="1cebb56e-524e-4de0-b676-0f574df9012a"
IN_REVIEW_ID="33feb1c9-3276-4e13-863a-0b93db032a0f"
```

### 🤖 自動実行コマンド
```bash
# Issue開始時
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(cat ~/.linear-api-key)" \
  -d '{"query":"mutation{issueUpdate(id:\"$ISSUE_ID\",input:{stateId:\"1cebb56e-524e-4de0-b676-0f574df9012a\"})}"}'

# Issue完了時  
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $(cat ~/.linear-api-key)" \
  -d '{"query":"mutation{issueUpdate(id:\"$ISSUE_ID\",input:{stateId:\"33feb1c9-3276-4e13-863a-0b93db032a0f\"})}"}'
```

### 📊 2層知識管理システム (統合版)
```
CLAUDE.md     - AI協業ルール・技術制約・開発方針のみ (このファイル)
Linear        - プロジェクト管理・タスク・進捗・開発ログ・エラー解決・学習パターンすべて
```

**重要**: devlog.mdは廃止。すべてのプロジェクト管理業務はLinearで統合管理。

### ⚡ Development Commands
```bash
# doit Command - Instant Issue Management
doit BOC-XX --interactive        # AI: 即座に実行、探索不要

# Linear: 常にGraphQL API使用 (CLIは動作しない)
curl -X POST "https://api.linear.app/graphql" -H "Authorization: $(cat ~/.linear-api-key)"
# 固定チームID: $(cat ~/.linear-team-id) = "bochang's lab"
```

### 🔧 ESLint LSP - Termux最適化コード品質管理
**採用理由**: TypeScript LSPはTermux環境でタイムアウト - ESLintで現実的解決

#### 必須インストール
```bash
# ESLint + daemon版 (高速化)
npm install --save-dev eslint eslint_d vscode-langservers-extracted
```

#### 設定ファイル構成
**eslint.config.js**:
```javascript
export default [
    {
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "module",
            globals: {
                window: "readonly", document: "readonly", console: "readonly",
                localStorage: "readonly", history: "readonly", navigator: "readonly"
            }
        },
        rules: {
            "no-unused-vars": ["warn", { "args": "none" }],
            "no-undef": "error",
            "quotes": ["warn", "single", { "allowTemplateLiterals": true }]
        }
    }
];
```

#### 実用コマンド
```bash
# リアルタイムエラーチェック
npx eslint script.js

# 自動修正 (引用符統一、セミコロン等)
npx eslint script.js --fix

# 継続監視モード
npx eslint script.js --watch
```

#### 機能制約の受容
- ✅ **得られる**: 高速エラー検出、自動修正、実用的開発体験
- ❌ **諦める**: find_definition, find_references等の高度LSP機能
- 🎯 **結果**: Termux制約下での最適解、開発効率大幅向上

## Emergency Patterns
- **Boot Failure**: Check file loading order, undefined dependencies
- **APK Signing**: Use proven signing system patterns
- **Build Errors**: Refer to Linear issue history for similar past solutions

---
*このファイルは必要不可欠なルールのみ。詳細情報はすべてLinear統合管理システムに格納。*