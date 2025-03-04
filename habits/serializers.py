from rest_framework import serializers
from .validators import (validate_award_and_related_habit, validate_execution_time,
                         validate_related_habit, validate_periodicity, validate_pleasant_habit)
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    execution_time = serializers.IntegerField(default=0, validators=[validate_execution_time])
    periodicity = serializers.IntegerField(default=1, validators=[validate_periodicity])

    def validate(self, attrs):
        validate_award_and_related_habit(attrs, fields=['related_habit', 'award'])
        validate_related_habit(attrs, field_name='related_habit')
        validate_pleasant_habit(attrs)

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
