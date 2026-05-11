from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Feed(models.Model):
    FEED_TYPE_CHOICES = (
        ('dry', 'Сухой'),
        ('wet', 'Влажный'),
        ('natural', 'Натуральный'),
    )
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    feed_type = models.CharField(max_length=20, choices=FEED_TYPE_CHOICES, default='dry')

    def __str__(self):
        return f'{self.brand} {self.name}'.strip()


class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CarePlanItem(models.Model):
    ACTION_CHOICES = (
        ('feed', 'Кормление'),
        ('medicate', 'Лекарство'),
        ('other', 'Другое'),
    )
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='care_plan_items')
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True, blank=True)
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_time = models.TimeField()
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cat} - {self.get_action_type_display()} at {self.scheduled_time}'


class ExecutionLog(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
        ('skipped', 'Пропущено'),
    )
    care_plan_item = models.ForeignKey(CarePlanItem, on_delete=models.CASCADE, related_name='execution_logs')
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='execution_logs')
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.cat} - {self.care_plan_item} - {self.get_status_display()}'
