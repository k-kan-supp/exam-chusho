# 中小企業診断士 一次試験 過去問学習システム (Django版)

## 🎯 機能一覧

### ✅ 実装済み機能
1. **ユーザー認証**
   - ユーザー登録
   - ログイン/ログアウト
   - ユーザーごとのデータ管理

2. **学習管理機能**
   - 問題チェック機能（学習済みマーク）
   - メモ機能（各問題にメモを保存）
   - ブックマーク機能
   - 正答率トラッキング (○×△での自己採点)
   - 学習履歴の記録

3. **問題管理**
   - 5科目対応（企業経営理論、運営管理、財務会計、経済学・経済政策、経営法務）
   - 科目・年度・シート・トピック別フィルタ
   - 検索機能
   - 解説URL対応

4. **分析・可視化**
   - ダッシュボード（学習進捗の可視化）
   - 科目別統計
   - 日次学習ログ
   - 弱点分析（不正解の多い問題）

5. **学習サポート**
   - ランダム出題モード
   - 復習リスト
   - 学習目標設定（試験日・1日の目標問題数）
   - CSV出力機能

6. **タグ機能**
   - ユーザー独自タグ作成
   - 問題へのタグ付け

## 📁 プロジェクト構成

```
kakomon_django/
├── config/              # プロジェクト設定
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── exam/                # 試験問題アプリ
│   ├── models.py       # データモデル
│   ├── views.py        # ビュー
│   ├── urls.py         # URL設定
│   ├── admin.py        # 管理画面設定
│   └── management/
│       └── commands/
│           └── import_questions.py  # JSONインポートコマンド
├── accounts/            # 認証アプリ
│   └── urls.py
├── templates/           # テンプレート
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── exam/
│       ├── dashboard.html
│       ├── question_list.html
│       ├── question_detail.html
│       └── study_goal_settings.html
├── static/              # 静的ファイル
├── media/               # メディアファイル
├── manage.py
└── requirements.txt
```

## 🚀 セットアップ手順

### 1. 依存パッケージのインストール

```bash
pip install django requests --break-system-packages
```

### 2. データベースのマイグレーション

```bash
cd kakomon_django
python manage.py makemigrations
python manage.py migrate
```

### 3. 管理ユーザーの作成

```bash
python manage.py createsuperuser
```

### 4. JSONデータのインポート

```bash
# 全科目をインポート
python manage.py import_questions

# 特定の科目のみインポート
python manage.py import_questions --subject keiei
```

### 5. 開発サーバーの起動

```bash
python manage.py runserver
```

http://127.0.0.1:8000/ にアクセス

## 📊 データモデル

### Subject (科目)
- code: 科目コード
- name: 科目名
- json_file: JSONファイル名
- source_url: スクレイピング元URL

### Question (問題)
- subject: 科目（外部キー）
- sheet: シート番号
- sheet_title: シートタイトル
- topic: トピック
- year: 年度
- question_label: 問題番号
- page: PDFページ番号
- explanation_url: 解説URL

### UserProgress (学習進捗)
- user: ユーザー
- question: 問題
- is_checked: 学習済みフラグ
- is_bookmarked: ブックマークフラグ
- last_result: 最後の結果 (correct/incorrect/partial/skip)
- correct_count: 正解数
- incorrect_count: 不正解数
- total_attempts: 挑戦回数
- accuracy_rate: 正答率（プロパティ）

### UserMemo (メモ)
- user: ユーザー
- question: 問題
- content: メモ内容

### StudyGoal (学習目標)
- user: ユーザー
- exam_date: 試験日
- daily_question_target: 1日の目標問題数

### DailyStudyLog (日次ログ)
- user: ユーザー
- date: 日付
- questions_attempted: 挑戦問題数
- correct_count: 正解数

## 🎨 主要画面

### ダッシュボード (/)
- 全体の学習進捗
- 科目別統計
- 過去7日間の学習履歴グラフ
- 復習が必要な問題リスト

### 問題一覧 (/questions/)
- フィルタ機能（科目・年度・シート・学習状況）
- 検索機能
- 学習状況の一覧表示

### 問題詳細 (/questions/<id>/)
- 問題情報の表示
- チェック機能
- メモ機能
- 正答率記録
- タグ付け
- 解説リンク

### 学習目標設定 (/settings/goal/)
- 試験日設定
- 1日の目標問題数設定

## 🔧 カスタマイズ

### テンプレートの追加が必要なファイル

以下のテンプレートファイルは基本構造のみ作成済みです。
詳細な実装が必要な場合は追加してください：

1. `templates/exam/dashboard.html` - ダッシュボード
2. `templates/exam/question_list.html` - 問題一覧
3. `templates/exam/question_detail.html` - 問題詳細
4. `templates/exam/study_goal_settings.html` - 目標設定

### AJAXエンドポイント

JavaScriptから以下のエンドポイントを呼び出せます：

- `/api/toggle-check/<question_id>/` - チェック切り替え
- `/api/toggle-bookmark/<question_id>/` - ブックマーク切り替え
- `/api/save-memo/<question_id>/` - メモ保存
- `/api/record-result/<question_id>/` - 結果記録

すべてPOSTリクエストで、CSRFトークンが必要です。

## 📦 PythonAnywhereへのデプロイ

### 1. ファイルのアップロード
```bash
# ローカルからzipを作成
cd /home/claude
zip -r kakomon_django.zip kakomon_django/

# PythonAnywhereにアップロードして展開
```

### 2. WSGI設定
```python
import sys
import os

path = '/home/tgoda2357/kakomon_django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 3. 静的ファイルの収集
```bash
python manage.py collectstatic --noinput
```

### 4. settings.py の本番設定
```python
DEBUG = False
ALLOWED_HOSTS = ['tgoda2357.pythonanywhere.com']
```

## 🎯 今後の拡張アイデア

1. **モバイル最適化** - レスポンシブデザインの強化
2. **オフライン対応** - PWA化
3. **ソーシャル機能** - 学習仲間との進捗共有
4. **AIによる弱点診断** - 機械学習で苦手分野を分析
5. **模擬試験モード** - 制限時間付きの本番形式テスト
6. **Slack/LINE通知** - 学習リマインダー

## 📝 ライセンス

このプロジェクトは個人学習用です。

## 🙋 サポート

質問や要望があれば、Issueを作成してください！
