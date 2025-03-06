from datetime import timedelta

from rest_framework.serializers import ValidationError


class ValidatorTime:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time = dict(value).get(self.field)
        if time is not None and time > timedelta(seconds=120):
            raise ValidationError(
                "Продолжительность выполнения привычки не может быть более 120 секунд."
            )


class WeeklyHabitValidator:
    """Проверяет периодичность выполнения привычки раз в 7 дней."""

    def __call__(self, value):
        if isinstance(value, dict):
            periodicity = value.get("periodicity")
        else:
            periodicity = value.periodicity

        if periodicity is None:
            raise ValidationError(
                "Привычка должна выполняться хотя бы один раз в неделю."
            )

        if periodicity > 7:
            raise ValidationError(
                "Периодичность выполнения привычки не может превышать 7 дней."
            )
        if periodicity < 1:
            raise ValidationError(
                "Привычка должна выполняться хотя бы один раз в неделю."
            )


class HabitValidator:
    """Проверяет, что не заполнены одновременно поля "связанная привычка" и "вознаграждение"."""

    def __call__(self, value):
        related_habit = value.get("related_habit")
        award = value.get("award")
        if related_habit and award:
            raise ValidationError(
                "Вы можете заполнить только одно из полей:'связанная привычка' или 'вознаграждение'."
            )


class PleasantHabitValidator:
    """Проверяет, что связанные привычки могут быть только с признаком "приятной привычки"."""

    def __call__(self, value):
        related_habit = value.get("related_habit")
        if related_habit is not None:
            if not related_habit.get("pleasant_habit"):
                raise ValidationError(
                    "Связанная привычка должна быть с признаком 'приятной привычки'."
                )


class RelatedHabitValidator:
    """Проверяет, что у приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, value):
        if value.get("pleasant_habit"):
            if value.get("award") or value.get("related_habit"):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )
