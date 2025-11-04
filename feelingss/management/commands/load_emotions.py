# management/commands/load_emotions.py
from django.core.management.base import BaseCommand
from feelingss.models import Emotion


class Command(BaseCommand):
    help = 'Load emotions from text files'

    def handle(self, *args, **options):
        emotions_data = []

        # Чтение файлов
        files = ['data.txt', 'data2.txt']

        for file_name in files:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    emotions_data.extend([line.strip() for line in f if line.strip()])
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING(f'Файл {file_name} не найден'))

        # Создание записей
        count = 0
        for emotion_name in emotions_data:
            obj, created = Emotion.objects.get_or_create(name=emotion_name)
            if created:
                count += 1
                self.stdout.write(f'Добавлена эмоция: {emotion_name}')

        self.stdout.write(self.style.SUCCESS(f'Успешно добавлено {count} эмоций'))