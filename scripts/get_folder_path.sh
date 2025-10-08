#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <folder_name>" >&2
    exit 1
fi

FOLDER_NAME="$1"

case "$FOLDER_NAME" in
    "ドキュメントフォルダ")
        echo "/storage/emulated/0/Documents/"
        ;;
    "ダウンロードフォルダ")
        echo "/storage/emulated/0/Download/"
        ;;
    "スクリーンショットフォルダ")
        echo "/storage/emulated/0/Pictures/Screenshots/"
        ;;
    "ピクチャーフォルダ" | "写真フォルダー")
        echo "/storage/emulated/0/Pictures/"
        ;;
    *)
        echo "Error: Unknown folder name '$FOLDER_NAME'" >&2
        exit 1
        ;;
esac
