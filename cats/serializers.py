from rest_framework import serializers

import datetime as dt

from .models import CHOICES, Cat, User, Feed, Medication, CarePlanItem, ExecutionLog


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'


class CatSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'age')
        read_only_fields = ('owner',)

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Имя кота должно содержать минимум 2 символа")
        return value.strip()

    def validate_birth_year(self, value):
        current_year = dt.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(f"Год рождения не может быть больше {current_year}")
        if value < 1900:
            raise serializers.ValidationError("Год рождения не может быть меньше 1900")
        return value

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class CarePlanItemSerializer(serializers.ModelSerializer):
    feed_detail = FeedSerializer(source='feed', read_only=True)
    medication_detail = MedicationSerializer(source='medication', read_only=True)

    class Meta:
        model = CarePlanItem
        fields = (
            'id', 'cat', 'action_type', 'feed', 'feed_detail',
            'medication', 'medication_detail', 'scheduled_time',
            'notes', 'is_active', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate_cat(self, value):
        request = self.context.get('request')
        if request and request.user and not request.user.is_anonymous:
            if value.owner != request.user:
                raise serializers.ValidationError("Вы можете создавать пункты плана только для своих котов")
        return value

    def validate_scheduled_time(self, value):
        if value is None:
            raise serializers.ValidationError("Время приёма обязательно")
        return value

    def validate(self, data):
        action_type = data.get('action_type')
        feed = data.get('feed')
        medication = data.get('medication')

        if action_type == 'feed' and not feed:
            raise serializers.ValidationError({"feed": "Для кормления необходимо указать корм"})
        if action_type == 'medicate' and not medication:
            raise serializers.ValidationError({"medication": "Для лекарства необходимо указать препарат"})

        return data


class ExecutionLogSerializer(serializers.ModelSerializer):
    care_plan_item_detail = CarePlanItemSerializer(source='care_plan_item', read_only=True)

    class Meta:
        model = ExecutionLog
        fields = (
            'id', 'care_plan_item', 'care_plan_item_detail',
            'cat', 'executed_at', 'status', 'notes',
        )
        read_only_fields = ('executed_at',)
