import os
from django.core.management.base import BaseCommand
from feelingss.models import Feeling


class Command(BaseCommand):
    help = 'Загружает данные из текстового файла в модель Feeling'

    def add_arguments(self, parser):
        # Добавление аргумента для пути к файлу
        parser.add_argument(
            '--file',
            type=str,
            help='Путь к текстовому файлу с данными для загрузки',
            required=True
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл {file_path} не найден"))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Чтение файла построчно
                for line in file:
                    # Убираем символы переноса строк и обрабатываем строку
                    data = line.strip()

                    # Пример: Сохраняем данные в базе (можно адаптировать под свой формат)
                    if data:
                        feeling_instance = Feeling(name=data)
                        feeling_instance.save()
                        self.stdout.write(self.style.SUCCESS(f"Добавлено: {data}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка загрузки данных: {e}"))

