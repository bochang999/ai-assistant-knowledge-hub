# PROJECT SAFETY SYSTEM - 必須プロジェクト認証ルール

## 🚨 絶対遵守ルール: プロジェクト混同防止システム

### Phase 1: Linear Issue必須確認
**すべての作業開始前に必ず実行:**

```bash
# 1. Linear IssueでBOC-XX番号からプロジェクト名を特定
~/.linear-utils.sh get BOC-XX

# 2. Issue内容からプロジェクト名を明確に抽出
# - コメント内のプロジェクト名
# - APKファイル名（RecipeBox-${VERSION}.apk等）
# - ファイルパス (/laminator-dashboard/ 等)
# - 機能説明文脈
```

### Phase 2: 物理ファイル認証
**対象プロジェクトのpackage.jsonとcapacitor.config.jsonで二重確認:**

```bash
# プロジェクト名確認必須チェックリスト:
1. package.json: "name" フィールド
2. capacitor.config.json: "appId", "appName" フィールド  
3. android/app/src/main/java/ パッケージ構造
```

### Phase 3: 作業前宣言
**必ず以下を明言してから作業開始:**
```
✅ プロジェクト認証完了: [プロジェクト名]
✅ Linear Issue BOC-XX = [プロジェクト名]専用Issue確認
✅ 対象: /data/data/com.termux/files/home/[プロジェクト名]/
```

## ⛔ 違反防止ルール

### 絶対禁止事項:
1. **Linear Issue読まずに作業開始** 
2. **プロジェクト名確認なしでファイル編集**
3. **異なるプロジェクトのディレクトリで作業**
4. **憶測によるプロジェクト判断**

### 現在の開発中プロジェクト:
- RecipeBox (`recipebox-web/`) - 料理レシピ管理
- Laminator Dashboard (`laminator-dashboard/`) - ラミネート作業計算
- その他プロジェクト追加時は要更新

### 緊急時の作業停止条件:
- プロジェクト名が曖昧な場合
- Linear IssueとpageageNameが不一致の場合  
- 複数プロジェクトに影響する可能性がある場合

---
**このシステムは絶対遵守。違反は即座に作業停止。**