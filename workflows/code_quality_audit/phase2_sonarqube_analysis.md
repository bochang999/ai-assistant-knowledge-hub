# Phase 2: SonarQube静的解析実行

## 目的
対象コードに対してSonarQubeの静的解析を実行し、その結果（Quality GateステータスとIssue一覧）を取得する。

## あなた（AIアシスタント）実行項目

### 1. SonarQube環境確認
- SonarQube Scannerの利用可能性を確認
- プロジェクト設定ファイル (`sonar-project.properties`) の存在確認
- 必要に応じて設定ファイルを作成

### 2. 言語別スキャン設定
対象コードの言語に応じて適切なスキャン設定を適用：

#### JavaScript/TypeScript
```properties
sonar.projectKey=quality-audit-project
sonar.sources=.
sonar.exclusions=**/node_modules/**,**/dist/**,**/*.test.js,**/*.spec.ts
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

#### Python
```properties
sonar.projectKey=quality-audit-project
sonar.sources=.
sonar.exclusions=**/*test*.py,**/venv/**,**/__pycache__/**
sonar.python.coverage.reportPaths=coverage.xml
```

#### Java
```properties
sonar.projectKey=quality-audit-project
sonar.sources=src/main/java
sonar.java.binaries=target/classes
sonar.exclusions=**/test/**
```

### 3. SonarQube解析実行
```bash
# SonarQube Scanner実行
sonar-scanner \
  -Dsonar.projectKey=quality-audit-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=[TOKEN]
```

### 4. 解析結果取得
SonarQube Web APIを使用して結果を取得：

#### Quality Gate ステータス
```bash
curl -u [TOKEN]: \
  "http://localhost:9000/api/qualitygates/project_status?projectKey=quality-audit-project"
```

#### Issues一覧取得
```bash
curl -u [TOKEN]: \
  "http://localhost:9000/api/issues/search?componentKeys=quality-audit-project&severities=BLOCKER,CRITICAL,MAJOR"
```

### 5. SonarQube解析レポート生成
以下の構造でレポートを作成：

```markdown
# SonarQube解析レポート
## プロジェクト情報
- プロジェクトキー: [プロジェクトキー]
- 解析日時: [実行日時]
- SonarQubeバージョン: [バージョン]

## Quality Gate結果
- ステータス: [PASSED/FAILED]
- 条件詳細:
  - バグ数: [数値]
  - 脆弱性数: [数値]
  - コードスメル数: [数値]
  - カバレッジ: [パーセンテージ]
  - 重複度: [パーセンテージ]

## 検出Issues詳細
### BLOCKER (最重要)
- [Issue1]: [ファイルパス]:[行番号] - [説明]
- [Issue2]: [ファイルパス]:[行番号] - [説明]

### CRITICAL (重要)
- [Issue3]: [ファイルパス]:[行番号] - [説明]

### MAJOR (重要)
- [Issue4]: [ファイルパス]:[行番号] - [説明]

## カテゴリ別Issue統計
### セキュリティ
- 脆弱性: [数値]個
- セキュリティホットスポット: [数値]個

### 信頼性
- バグ: [数値]個
- コードスメル: [数値]個

### 保守性
- 保守性課題: [数値]個
- 技術的負債: [時間]

## メトリクス詳細
- 総行数: [数値]
- コード行数: [数値]
- 複雑度: [数値]
- 認知複雑度: [数値]
```

### 6. データ形式標準化
Phase 3での比較分析のため、結果を標準化された形式で出力：

```json
{
  "sonarqube_results": {
    "quality_gate": "PASSED/FAILED",
    "issues": [
      {
        "severity": "BLOCKER/CRITICAL/MAJOR",
        "type": "BUG/VULNERABILITY/CODE_SMELL",
        "rule": "rule_key",
        "component": "file_path",
        "line": 123,
        "message": "issue_description"
      }
    ],
    "metrics": {
      "bugs": 0,
      "vulnerabilities": 0,
      "code_smells": 5,
      "coverage": 85.5,
      "duplicated_lines_density": 2.1
    }
  }
}
```

## 出力ファイル
- `temp/sonarqube_report_[timestamp].md` (レポート)
- `temp/sonarqube_data_[timestamp].json` (構造化データ)

## エラーハンドリング
- SonarQube サーバー接続エラー
- 認証エラー
- プロジェクト設定エラー
- スキャン実行エラー

各エラーに対する代替手段や手動確認手順を提供。

## 次フェーズとの連携
Phase 3 (比較分析) でAIレビュー結果と照合するため、標準化されたデータ形式で結果を出力。

## 成功基準
- SonarQube解析の正常実行
- Quality Gate結果の取得
- 全Issue詳細の構造化された出力
- Phase 3で比較可能な形式でのデータ提供
