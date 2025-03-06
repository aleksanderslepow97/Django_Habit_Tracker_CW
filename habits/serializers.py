from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from habit.models import Habit
from habit.validators import (HabitValidator, PleasantHabitValidator,
                              RelatedHabitValidator, ValidatorTime,
                              WeeklyHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    validators = [
        ValidatorTime(field="time_to_complete"),
        WeeklyHabitValidator(),
        HabitValidator(),
        PleasantHabitValidator(),
        RelatedHabitValidator(),
    ]

    class Meta:
        model = Habit
        fields = "__all__"


class HabitpublicitySerializer(ModelSerializer):
    habitpublicity = SerializerMethodField()

    class Meta:
        model = Habit
        fields = "__all__"

    def get_habitpublicity(self, obj):
        """Метод фильтрует привычки пользователя по статусу публикации."""
        user = self.context["request"].user
        return [
            habit.habit
            for habit in Habit.objects.filter(owner=user, publicity="Опубликована")
        ]


class UserHabitSerializer(ModelSerializer):
    habituser = SerializerMethodField()

    def get_habituser(self, obj):
        """Метод фильтрует привычки  ntreotuj пользователя ."""
        user = self.context["request"].user
        return [habit.habit for habit in Habit.objects.filter(owner=user)]

    class Meta:
        model = Habit
        fields = "__all__"
