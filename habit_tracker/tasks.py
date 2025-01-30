import datetime

import pytz
from celery import shared_task
from config import settings
from habit_tracker.models import Habit
from habit_tracker.services import send_telegram_message


@shared_task
def check_habits():
    """
    Периодическая задача
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(zone)
    habits = Habit.objects.filter(owner__telegram_id__isnull=False)

    for habit in habits:
        if habit.time <= now:
            telegram_id = habit.owner.telegram_id

            if habit.place:
                message = f"Пришло время {habit.action} в {habit.place}"
            else:
                message = f"Пришло время {habit.action}"
            send_telegram_message(telegram_id, message)
            habit.time += habit.get_periodicity_timedelta()
            print(habit.time)
            habit.save()
