#!/bin/bash

# Django過去問学習システム セットアップスクリプト

echo "========================================="
echo "Django 過去問学習システム セットアップ"
echo "========================================="
echo ""

# 1. データベースのマイグレーション
echo "1. データベースをセットアップ中..."
python manage.py makemigrations
python manage.py migrate

# 2. 管理ユーザーの作成（オプション）
echo ""
echo "2. 管理ユーザーを作成しますか? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    python manage.py createsuperuser
fi

# 3. JSONデータのインポート
echo ""
echo "3. 問題データをインポート中..."
python manage.py import_questions

# 4. 静的ファイルの収集
echo ""
echo "4. 静的ファイルを収集中..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "セットアップ完了！"
echo "========================================="
echo ""
echo "開発サーバーを起動するには:"
echo "  python manage.py runserver"
echo ""
echo "ブラウザで以下にアクセス:"
echo "  http://127.0.0.1:8000/"
echo ""
