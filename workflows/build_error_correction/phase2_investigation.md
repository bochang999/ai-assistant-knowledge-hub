# Phase 2: 調査（事実の収集）

## 目的
エラーに関する客観的な事実をすべて収集し、報告可能な形式にまとめること。このフェーズでは、原因の推測や解決策の提案（Sequential Thinking）は一切行わない

## あなた（AIアシスタント）実行項目

### 1. エラー箇所の特定
GitHub Actions APIまたはCLIを使用し、エラーが発生している具体的なジョブとステップを正確に特定する

```bash
# GitHub Actions実行履歴取得
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/[OWNER]/[REPO]/actions/runs

# 失敗ジョブ詳細取得
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/[OWNER]/[REPO]/actions/runs/[RUN_ID]/jobs
```

### 2. 詳細ログの取得
特定したステップの詳細なエラーログを取得する

```bash
# 実際のログファイル取得 (認証必須)
echo 'YOUR_TOKEN' | gh auth login --with-token
gh run view [RUN_ID] --repo [OWNER]/[REPO] --log
```

### 3. 関連コードの特定
エラーログが指し示している、関連するコード箇所を特定する

### 4. 事実報告書の作成
上記の収集した情報のみを使い、「AI向けエラー報告テンプレート」の項目1〜5を埋める。項目6（根本原因の仮説）と項目7（質問）は空欄のままにすること。これを「事実報告書」とする

## 完了条件
- エラー箇所が正確に特定されている
- 詳細ログが取得されている
- 関連コード箇所が特定されている
- 「事実報告書」が作成されている（項目1-5のみ記入）

## 次のフェーズ
Phase 2.5: 分析（原因の考察と解決策の立案）