from habit_tracker.models import Habit
from habit_tracker.validators import (
    CheckLeadTimeValidator,
    IsPleasantNotRelatedHabitOrRewordValidator,
    RelatedHabitNotPleasantValidator,
    RelatedHabitOrRewordValidator,
)
from rest_framework import serializers


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitOrRewordValidator(field_1="related_habit", field_2="reward"),
            CheckLeadTimeValidator(field="time_to_complete"),
            RelatedHabitNotPleasantValidator(field_1="related_habit"),
            IsPleasantNotRelatedHabitOrRewordValidator(
                field_1="is_pleasant", field_2="related_habit", field_3="reward"
            ),
        ]
