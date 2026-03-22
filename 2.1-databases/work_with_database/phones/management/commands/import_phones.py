import csv
from django.utils.text import slugify
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            # Создаем объект Phone из данных CSV
            phone_obj = Phone(
                id=int(phone['id']),
                name=phone['name'],
                price=float(phone['price']),
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'].lower() == 'true',
                slug=slugify(phone['name'])
            )
            phone_obj.save()

            self.stdout.write(f'Imported: {phone_obj.name}')

        self.stdout.write(self.style.SUCCESS('Successfully imported all phones'))