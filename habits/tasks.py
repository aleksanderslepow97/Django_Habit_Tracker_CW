from celery import shared_task
from .services import send_telegram_message
from .models import Habit
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone
import json


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания и создание следующей задачи"""
    try:
        habit = Habit.objects.get(pk=habit_id)
        # отправка сообщения в tg
        if habit.user and habit.user.tg_chat_id:
            message = (
                f"Напоминание: {habit.action} в {habit.location} в {habit.time.strftime('%H:%M')}.\n"
                f"Не забудьте про награду: {habit.award}!")
            send_telegram_message(habit.user.tg_chat_id, message)

        # cоздание новой задачи на следующий день
        now = timezone.now()
        next_execution = timezone.datetime.combine(
            now.date() + timezone.timedelta(days=habit.periodicity), habit.time)

        # преобразуем в осведомленное время, если оно наивное
        if timezone.is_naive(next_execution):
            next_execution = timezone.make_aware(next_execution)

        # следующий день
        if next_execution < now:
            next_execution += timezone.timedelta(days=habit.periodicity)

        clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=next_execution)

        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f"Напоминание о привычке {habit.pk} - {next_execution}",
            task="habits.tasks.send_habit_reminder",
            args=json.dumps([habit.pk]),
            one_off=True,)
    except Habit.DoesNotExist:
        pass
