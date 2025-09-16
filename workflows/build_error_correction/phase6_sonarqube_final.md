# Phase 6: SonarQube統合と最終検証

## 目的
SonarQubeによる客観的コード品質分析を実行し、AIアシスタントが結果を解釈・報告することで最終品質確認を行う

## トリガー
git pushによるCI/CDパイプラインが開始される

## AIアシスタント実行項目
1. **SonarQube分析結果取得**:
   - CI/CDパイプラインの実行完了を確認する
   - SonarQube Web API（`api/qualitygates/project_status`、`api/issues/search`）を使用してQuality Gateステータスと検出されたIssueリストを取得する

2. **AIアシスタント最終報告書作成**:
   - 取得されたSonarQube分析結果を解釈する
   - Phase 4.5の自己レビューで発見できなかった問題がSonarQubeで指摘されたかを比較・分析する
   - 以下の形式で「SonarQube最終検証レポート」を作成する

3. **最終判定とアクション**:
   - **Quality Gate通過の場合**:
     - Linear Issue のステータスを「完了」に変更する
   - **Quality Gate失敗の場合**:
     - **[知識蓄積]**: 「SonarQube最終検証レポート」内容を基に学習ポイントを抽出し、チェックリスト項目を生成する。それらの項目を中央リポジトリ（ai-review-knowledge-base）に追加するPull Requestを作成する
     - **[修正サイクル開始]**: Linear Issue ステータスを「修正必要」に戻す。レポートの「推奨対応」を基に修正指示を作成し、Phase 4（実装）からワークフローを再開する

## 完了条件
- SonarQube分析結果が正常に取得されている
- Quality Gateの結果に基づいて適切なアクションが実行されている
- 必要に応じて知識蓄積または修正サイクルが開始されている

## ワークフロー完了
Quality Gate通過時にこのフェーズが完了し、ビルドエラー修正ワークフローが正常に完了します。
