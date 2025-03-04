from rest_framework import serializers


def validate_award_and_related_habit(attrs, fields):
    filled_fields = [fields for field in fields if attrs.get(field) not in (None, '')]
    if len(filled_fields) > 1:
        raise serializers.ValidationError(f'Можно заполнить только одно из полей: {", ".join(fields)}.')


def validate_execution_time(value):
    if value not in range(120):
        raise serializers.ValidationError('Время на выполнение должно быть не больше 2 минут')


def validate_periodicity(value):
    if value not in range(1, 8):
        raise serializers.ValidationError('Периодичность должна быть в пределах от 1 до 8 дней')


def validate_related_habit(attrs, field_name='related_habit'):
    related_habit = attrs.get(field_name)
    if related_habit and not related_habit.is_pleasant_habit:
        raise serializers.ValidationError(f'{field_name}: Связанная привычка должна быть отмечена как приятная')


def validate_pleasant_habit(attrs):
    is_pleasant_habit = attrs.get('is_pleasant_habit')
    related_habit = attrs.get('related_habit')
    award = attrs.get('award')
    if is_pleasant_habit and (related_habit or award):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')
