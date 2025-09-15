# 🏛️ AI Assistant Constitution

## 基本原則 (Core Principles)

このドキュメントは、AI協業システムにおける基本的な動作原則と設定を定義します。

## 🗺️ プロジェクト辞書 (Project Dictionary)

Linear プロジェクト名とローカル作業ディレクトリの対応表:

- "petit recipe": "~/petit-recipe"
- "laminator-dashboard": "~/laminator-dashboard"
- "AI Assistant Knowledge Hub Project": "~/ai-assistant-knowledge-hub"

## 作業ディレクトリ自動移動ルール

1. Linear Issue の project 情報を取得
2. プロジェクト辞書で対応するローカルパスを検索
3. 該当パスが存在する場合、自動的に移動
4. 該当なしの場合、現在ディレクトリで作業継続

---
*このファイルはagent.shによって自動参照されます*