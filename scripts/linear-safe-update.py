#!/usr/bin/env python3
"""
Linear JSON-Safe Update Tool
JSONエスケープ問題を回避するLinear更新ツール

使用例:
  # Issue description更新
  ./linear-safe-update.py --issue BOC-100 --description "新しい説明文"

  # ファイルからdescription更新
  ./linear-safe-update.py --issue BOC-100 --description-file ~/content.md

  # Issue descriptionに追記
  ./linear-safe-update.py --issue BOC-100 --append "追記内容"

  # コメント追加
  ./linear-safe-update.py --issue BOC-100 --comment "コメント内容"

  # ファイルからコメント追加
  ./linear-safe-update.py --issue BOC-100 --comment-file ~/comment.md
"""

import argparse
import sys
import os
from pathlib import Path

# ai-assistant-knowledge-hub/lib をパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from linear_integration import create_json_safe_updater


def main():
    parser = argparse.ArgumentParser(
        description="Linear JSON-Safe Update Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument("--issue", required=True, help="Issue ID (例: BOC-100)")

    # 更新タイプ選択
    update_group = parser.add_mutually_exclusive_group(required=True)
    update_group.add_argument("--description", help="Issue description を更新")
    update_group.add_argument(
        "--description-file", help="ファイルから description を読み込んで更新"
    )
    update_group.add_argument("--append", help="Issue description に内容を追記")
    update_group.add_argument("--append-file", help="ファイルから内容を読み込んで追記")
    update_group.add_argument("--comment", help="コメントを追加")
    update_group.add_argument(
        "--comment-file", help="ファイルからコメントを読み込んで追加"
    )

    args = parser.parse_args()

    try:
        # JSON-safe updater 初期化
        updater = create_json_safe_updater()

        # Issue ID を実際のIDに変換 (BOC-XXX → 実際のLinear ID)
        issue_id = resolve_issue_id(args.issue)
        if not issue_id:
            print(f"❌ Issue {args.issue} の解決に失敗")
            return 1

        # 更新タイプに応じて処理
        if args.description:
            success = updater.safe_update_issue_description(issue_id, args.description)

        elif args.description_file:
            content = read_file(args.description_file)
            if content is None:
                return 1
            success = updater.safe_update_issue_description(issue_id, content)

        elif args.append:
            success = updater.append_to_issue_description(issue_id, args.append)

        elif args.append_file:
            content = read_file(args.append_file)
            if content is None:
                return 1
            success = updater.append_to_issue_description(issue_id, content)

        elif args.comment:
            success = updater.safe_add_comment(issue_id, args.comment)

        elif args.comment_file:
            content = read_file(args.comment_file)
            if content is None:
                return 1
            success = updater.safe_add_comment(issue_id, content)

        if success:
            print(f"✅ {args.issue} 更新成功")
            return 0
        else:
            print(f"❌ {args.issue} 更新失敗")
            return 1

    except Exception as e:
        print(f"❌ エラー: {e}")
        return 1


def resolve_issue_id(issue_identifier: str) -> str:
    """
    Issue識別子を実際のLinear IDに変換

    Args:
        issue_identifier: BOC-100 などの識別子

    Returns:
        str: 実際のLinear Issue ID、見つからない場合は空文字
    """
    if issue_identifier.startswith("BOC-"):
        # temp/agent_issue_BOC-XXX.json から Issue ID を取得
        temp_dir = Path(__file__).parent.parent / "temp"
        json_file = temp_dir / f"agent_issue_{issue_identifier}.json"

        if json_file.exists():
            import json

            try:
                with open(json_file) as f:
                    data = json.load(f)
                    return data["data"]["issue"]["id"]
            except:
                pass

        # フォールバック: doit コマンドの結果から取得
        # 実装簡略化のため、ここでは警告のみ
        print(f"⚠️ {issue_identifier} の Issue ID 解決にフォールバック必要")

    # 既にLinear IDの形式の場合はそのまま返す
    if len(issue_identifier) > 20 and "-" in issue_identifier:
        return issue_identifier

    return ""


def read_file(file_path: str) -> str:
    """
    ファイル内容を読み込み

    Args:
        file_path: ファイルパス

    Returns:
        str: ファイル内容、エラーの場合は None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {file_path}")
        return None
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
        return None


if __name__ == "__main__":
    sys.exit(main())
