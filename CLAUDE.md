# CLAUDE.md - Essential Development Rules

## Mandatory Knowledge Management System

### 🔄 Linear Issue自動管理システム
```bash
# Issue作業フロー (自動実行):
1. Issue読み取り開始 → status: "In Progress"
2. 作業実行・コード実装
3. 作業完了 → 内容・コード記録 → status: "In Review"
→ 許可不要の完全自動管理
```

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
# Current project: Laminator Dashboard
briefcase dev                    # BeeWare development
http-server                      # Web development
git commit → AI-Gate automatic learning cycle

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

## Current Project Context: Laminator Dashboard
- **Type**: Web→APK (HTML/CSS/JS → GitHub Actions → Signed APK)
- **Status**: Unified script.js architecture with CSV/Backup features
- **Recent**: APK file saving system + Linear API integration
- **Features**: Documents/{AppName}/ file saving, Capacitor Filesystem

## Emergency Patterns
- **Boot Failure**: Check file loading order, undefined dependencies
- **APK Signing**: Use RecipeBox proven signing system 
- **Build Errors**: Refer to Linear issue history for similar past solutions

---
*このファイルは必要不可欠なルールのみ。詳細情報はすべてLinear統合管理システムに格納。*