from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time

from cats.models import Cat, Feed, Medication, CarePlanItem, ExecutionLog

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        admin.set_password('admin')
        admin.save()

        user, _ = User.objects.get_or_create(
            username='user',
            defaults={'first_name': 'Иван', 'last_name': 'Петров'}
        )
        user.set_password('user')
        user.save()

        cat1 = Cat.objects.create(name='Барсик', color='Ginger', birth_year=2020, owner=user)
        cat2 = Cat.objects.create(name='Мурка', color='Black', birth_year=2021, owner=user)
        cat3 = Cat.objects.create(name='Снежок', color='White', birth_year=2022, owner=admin)

        feed1 = Feed.objects.create(name='Куриный', brand='Royal Canin', feed_type='dry')
        feed2 = Feed.objects.create(name='Рыбный', brand='Whiskas', feed_type='wet')
        feed3 = Feed.objects.create(name='Индейка', brand='Pro Plan', feed_type='natural')

        med1 = Medication.objects.create(name='Мильбемакс', dosage='1 таблетка')
        med2 = Medication.objects.create(name='Стронгхолд', dosage='0.5 мл')
        med3 = Medication.objects.create(name='Глистогонное', dosage='1/4 таблетки')

        items_data = [
            (cat1, 'feed', feed1, None, time(8, 0), True),
            (cat1, 'feed', feed2, None, time(19, 0), True),
            (cat1, 'medicate', None, med1, time(9, 0), True),
            (cat2, 'feed', feed3, None, time(8, 30), True),
            (cat2, 'feed', feed1, None, time(18, 30), True),
            (cat2, 'medicate', None, med2, time(10, 0), False),
            (cat3, 'feed', feed2, None, time(7, 0), True),
            (cat3, 'medicate', None, med3, time(11, 0), True),
            (cat3, 'other', None, None, time(15, 0), True),
        ]

        items = []
        for cat, action, feed, med, t, active in items_data:
            item = CarePlanItem.objects.create(
                cat=cat, action_type=action, feed=feed, medication=med,
                scheduled_time=t, notes='', is_active=active
            )
            items.append(item)

        now = timezone.now()
        ExecutionLog.objects.create(care_plan_item=items[0], cat=cat1, status='completed', notes='Съел всё')
        ExecutionLog.objects.create(care_plan_item=items[1], cat=cat1, status='completed', notes='')
        ExecutionLog.objects.create(care_plan_item=items[2], cat=cat1, status='cancelled', notes='Пропущено')
        ExecutionLog.objects.create(care_plan_item=items[3], cat=cat2, status='completed', notes='')
        ExecutionLog.objects.create(care_plan_item=items[6], cat=cat3, status='completed', notes='')
        ExecutionLog.objects.create(care_plan_item=items[7], cat=cat3, status='skipped', notes='Не стали давать')

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены:'))
        self.stdout.write(f'  Пользователи: admin/admin, user/user')
        self.stdout.write(f'  Кошки: {Cat.objects.count()}')
        self.stdout.write(f'  Корма: {Feed.objects.count()}')
        self.stdout.write(f'  Лекарства: {Medication.objects.count()}')
        self.stdout.write(f'  Пункты плана: {CarePlanItem.objects.count()}')
        self.stdout.write(f'  Логи: {ExecutionLog.objects.count()}')
