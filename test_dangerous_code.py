#!/usr/bin/env python3
"""
危険なPythonコードサンプル（セキュリティシステムテスト用）
PDFで特定された15の危険パターンを意図的に含む
"""

import subprocess
import pickle
import yaml
import random
from datetime import datetime

# 1. 例外の握りつぶし・雑なexcept
try:
    result = eval("1 + 1")
    process_data(result)
except:  # bare except - 危険
    pass

try:
    api_call()
except Exception:  # 広範囲except - 危険
    pass


# 2. 可変デフォルト引数の罠
def add_item(item, bucket=[]):  # 危険なデフォルト引数
    bucket.append(item)
    return bucket


# 3. セキュリティ危険APIの安易な使用
user_input = "print('hello')"
eval(user_input)  # 任意コード実行 - 危険
exec("import os; os.system('ls')")  # 任意コード実行 - 危険

# shell=True使用 - 危険
subprocess.run("ls -la", shell=True)

# unsafe YAML - 危険
yaml_data = yaml.load("key: value", Loader=yaml.Loader)

# Pickle - 危険
untrusted_data = b"some_pickle_data"
pickle.loads(untrusted_data)

# SSL検証無効化 - 危険
import requests

response = requests.get("https://api.example.com", verify=False)

# 4. SQLインジェクション・パス操作
import sqlite3


def get_user(name):
    cur = sqlite3.connect("db.sqlite").cursor()
    cur.execute(f"SELECT * FROM users WHERE name='{name}'")  # SQLインジェクション危険


def read_file(filename):
    return open(f"/uploads/{filename}").read()  # パストラバーサル危険


# 5. ログに秘密情報を出力
import logging

logger = logging.getLogger(__name__)

password = "secret123"
api_key = "sk-1234567890abcdef"
logger.info(f"APIトークン: {api_key}")  # 秘密情報ログ出力 - 危険
print(f"パスワード: {password}")  # 秘密情報出力 - 危険

# 6. 時刻・タイムゾーンの無自覚
now = datetime.now()  # ナイーブなdatetime - 危険
expiry = now + timedelta(days=1)

# 7. 浮動小数点の直接比較
score = 0.1 + 0.1 + 0.1
if score == 0.3:  # 浮動小数点比較 - 危険
    print("正解")


# 8. リソースの未解放
def process_file(path):
    f = open(path)  # closeし忘れ - 危険
    data = f.read()
    return data.upper()


# 9. ハードコードされた値
API_URL = "https://api.example.com"
SECRET_KEY = "abc123"  # ハードコード秘密情報 - 危険
DATABASE_PASSWORD = "admin123"  # ハードコード秘密情報 - 危険

# 10. 存在しない引数・関数名（ハルシネーション例）
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3]})
# df.save_to_csv("output.csv")  # 存在しないメソッド - コメントアウト

# 11. パフォーマンス地雷
result = ""
for item in range(1000):
    result += str(item)  # 文字列結合 - パフォーマンス問題

# 12. セキュリティ用途での一般乱数使用
token = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=32))  # 弱い乱数 - 危険

# 13. ログ出力でのf文字列使用
user_data = {"id": 123}
logger.info(f"ユーザー {user_data['id']} がログインしました")  # f文字列ログ - 非効率


# 14. その他の危険パターン
def dangerous_function():
    # 複数の危険要素を組み合わせ
    cmd = input("実行するコマンド: ")
    subprocess.run(cmd, shell=True)  # ユーザー入力 + shell=True - 非常に危険

    data = input("評価する式: ")
    result = eval(data)  # ユーザー入力 + eval - 非常に危険

    return result


if __name__ == "__main__":
    print("⚠️ この危険なコードサンプルは実行しないでください！")
    print("セキュリティシステムのテスト用です")
