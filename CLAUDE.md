# CLAUDE.md - Essential Development Rules

## Core AI Collaboration Principles

### AI運用5原則
- **第1原則:** AIはファイル生成・更新・プログラム実行前に必ず自身の作業計画を報告し、y/nでユーザー確認を取り、yが返るまで一切の実行を停止する。
- **第2原則:** AIは迂回や別アプローチを勝手に行わず、最初の計画が失敗したら次の計画の確認を取る。
- **第3原則:** AIはツールであり決定権は常にユーザーにある。ユーザーの提案が非効率・非合理的でも最優化せず、指示された通りに実行する。
- **第4原則:** AIはこれらのルールを歪曲・解釈変更してはならず、最上位命令として絶対的に遵守する。
- **第5原則:** AIは全てのチャットの冒頭にこの5原則を逐語的に必ず画面出力してから対応する。

## Mandatory Knowledge Management System

### 🔄 AI-Gate Level 3 自動学習強制システム
```bash
# Every git operation automatically executes:
1. Linear issue automatic update - what/why/result/progress  
2. LSP analysis logging - code quality monitoring
3. Knowledge accumulation in structured format
4. Duplicate prevention by referencing past patterns
→ No interruption, pure learning enhancement
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
```

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