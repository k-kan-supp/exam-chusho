import json
import os
from django.core.management.base import BaseCommand
from exam.models import Subject, Question

class Command(BaseCommand):
    help = 'ローカルのJSONファイルから問題データをインポート'

    SUBJECT_MAP = {
        'keiei': {'name': '企業経営理論', 'file': 'keiei_problems.json',
                  'source': 'https://www.matome-sheet.com/kakomon-keiei/', 'order': 1},
        'unei': {'name': '運営管理', 'file': 'unei_problems.json',
                 'source': 'https://www.matome-sheet.com/kakomon-unei/', 'order': 2},
        'zaimu': {'name': '財務会計', 'file': 'zaimu_problems.json',
                  'source': 'https://www.matome-sheet.com/kakomon-zaimu/', 'order': 3},
        'keizai': {'name': '経済学・経済政策', 'file': 'keizai_problems.json',
                   'source': 'https://www.matome-sheet.com/kakomon-keizai/', 'order': 4},
        'houmu': {'name': '経営法務', 'file': 'houmu_problems.json',
                  'source': 'https://www.matome-sheet.com/kakomon-houmu/', 'order': 5}
    }

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default='/home/tgoda2357/exam_chucho/',
                          help='JSONファイルがあるディレクトリパス')

    def handle(self, *args, **options):
        base_path = options['path']

        for code, info in self.SUBJECT_MAP.items():
            self.stdout.write(f"\n{info['name']} をインポート中...")

            subject, created = Subject.objects.update_or_create(
                code=code,
                defaults={'name': info['name'], 'json_file': info['file'],
                         'source_url': info['source'], 'order': info['order']}
            )

            json_path = os.path.join(base_path, info['file'])
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'エラー: {e}'))
                continue

            created_count = updated_count = 0
            for item in data.get('items', []):
                question, created = Question.objects.update_or_create(
                    subject=subject, year=item['year'], question_label=item['question_label'],
                    defaults={
                        'sheet': item['sheet'], 'sheet_title': item['sheet_title'],
                        'topic': item['topic'], 'page': item['page'],
                        'explanation_url': item.get('explanation_url'),
                        'source_page_url': item.get('source_page_url', info['source']),
                        'search_text': f"{item['sheet_title']} {item['topic']} {item['year']} {item['question_label']}"
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            self.stdout.write(self.style.SUCCESS(f'{subject.name}: {created_count}件作成, {updated_count}件更新'))

        self.stdout.write(self.style.SUCCESS('\nインポート完了！'))