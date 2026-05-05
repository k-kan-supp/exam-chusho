# 🚀 クイックスタートガイド

## 1. プロジェクトの展開

```bash
unzip kakomon_django.zip
cd kakomon_django
```

## 2. 自動セットアップ（推奨）

```bash
chmod +x setup.sh
./setup.sh
```

これで以下が自動実行されます：
- データベースのマイグレーション
- 管理ユーザーの作成（オプション）
- 問題データのインポート
- 静的ファイルの収集

## 3. 手動セットアップ（詳細制御したい場合）

### 3-1. 依存パッケージのインストール

```bash
pip install -r requirements.txt --break-system-packages
```

### 3-2. データベースの初期化

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3-3. 管理ユーザーの作成

```bash
python manage.py createsuperuser
```

### 3-4. 問題データのインポート

```bash
# 全科目をインポート
python manage.py import_questions

# または特定の科目のみ
python manage.py import_questions --subject keiei
```

利用可能な科目：
- `keiei` - 企業経営理論
- `unei` - 運営管理
- `zaimu` - 財務会計
- `keizai` - 経済学・経済政策
- `houmu` - 経営法務

## 4. 開発サーバーの起動

```bash
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ にアクセス

## 5. 最初のユーザー登録

1. http://127.0.0.1:8000/accounts/register/ にアクセス
2. ユーザー名とパスワードを入力
3. 登録ボタンをクリック
4. 自動的にダッシュボードにリダイレクトされます

## 6. 管理画面（オプション）

http://127.0.0.1:8000/admin/ にアクセスして、
作成した管理ユーザーでログイン

## 主要機能の使い方

### 問題を解く
1. ダッシュボードまたは問題一覧から問題を選択
2. 解答後、○×△ボタンで結果を記録
3. メモを残すことも可能

### 学習目標の設定
1. 「目標設定」メニューをクリック
2. 試験日と1日の目標問題数を入力
3. ダッシュボードに進捗が表示されます

### 復習する
1. ダッシュボードの「復習が必要な問題」リストから選択
2. または問題一覧で「間違えた問題」フィルタを使用

### データの出力
1. 「CSV出力」ボタンをクリック
2. 学習進捗がCSVファイルとしてダウンロードされます

## トラブルシューティング

### データベースエラー
```bash
rm db.sqlite3
python manage.py migrate
python manage.py import_questions
```

### 静的ファイルが表示されない
```bash
python manage.py collectstatic --noinput
```

### 問題データが表示されない
```bash
# データが正しくインポートされているか確認
python manage.py shell
>>> from exam.models import Question
>>> Question.objects.count()

# 0の場合は再インポート
>>> exit()
python manage.py import_questions
```

## PythonAnywhereへのデプロイ

詳細は README.md の「PythonAnywhereへのデプロイ」セクションを参照してください。

基本手順：
1. ファイルをPythonAnywhereにアップロード
2. WSGI設定ファイルを編集
3. `python manage.py migrate`
4. `python manage.py import_questions`
5. `python manage.py collectstatic`
6. settings.pyでDEBUG=False, ALLOWED_HOSTSを設定

## サポート

質問や不具合があれば、GitHubのIssueを作成してください！

---

楽しい学習を！ 📚✨
