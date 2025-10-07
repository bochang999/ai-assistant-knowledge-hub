# マニュアル: git push前の機密情報スキャン設定

## 1. 目的

`git push` を実行する前に、リポジトリにAPIキーやパスワードなどの機密情報が含まれていないかを自動的にスキャンします。これにより、意図しない機密情報の漏洩を未然に防ぎます。

この設定は `pre-commit` フレームワークと `detect-secrets` ツールを利用します。

## 2. 前提条件

設定対象のプロジェクトがあるマシンに、以下がインストールされている必要があります。

- Python 3.6+
- pip (Pythonのパッケージインストーラ)

## 3. 設定手順

### ステップ 3.1: ツールのインストール

ターミナルで以下のコマンドを実行し、必要なツールをインストールします。

```bash
pip install pre-commit detect-secrets
```

### ステップ 3.2: pre-commit設定ファイルの作成

プロジェクトのルートディレクトリ（`.git` ディレクトリがある場所）に、`.pre-commit-config.yaml` という名前で以下の内容のファイルを作成します。（既にファイルが存在する場合は、追記・編集してください）

```yaml
# .pre-commit-config.yaml
repos:
  # (ここに既存の他のフック設定があってもOK)

  # Advanced secret scanning for pre-push
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        name: Detect secrets before push
        stages: [push] # git push の時にだけ実行する
        args: ['--baseline', '.secrets.baseline']
```

### ステップ 3.3: フックの有効化

ターミナルで以下のコマンドを実行し、gitの pre-push フックを有効化します。

```bash
pre-commit install --hook-type pre-push
```

### ステップ 3.4: ベースラインの生成

現在のリポジトリの状態を「安全な基準」として記録するためのベースラインファイルを作成します。これにより、意図的にリポジトリに含めている情報（例: ダミーのキー）が、毎回警告されるのを防ぎます。

以下のコマンドを実行してください。

```bash
pre-commit run detect-secrets --all-files
```

これにより、`.secrets.baseline` というファイルが生成されます。
**この `.secrets.baseline` ファイルは、リポジトリにコミットすることが推奨されます。** チームメンバー間で「安全な基準」を共有するためです。

## 4. 使い方

上記の設定が完了すると、`git push` を実行した際に、自動的に機密情報がスキャンされます。

- **機密情報が検知されなかった場合**: 通常通りpushが実行されます。
- **機密情報が検知された場合**: pushは自動的に失敗（ブロック）され、どのファイルに問題があるかが表示されます。コミットから機密情報を削除するか、それが意図したものであればベースラインを更新するなどの対応が必要です。
