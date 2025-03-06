from datetime import datetime, timedelta

import pytz
from celery import shared_task

from config import settings
from habit.models import Habit
from habit.services import send_telegram_message


@shared_task
def send_information_telegram():
    """Отправляет пользователю напоминание о привычке."""
    time_zone = pytz.timezone(settings.TIME_ZONE)
    print(time_zone)
    current_time = datetime.now(time_zone)
    print(current_time)

    # Фильтруем привычки в диапазоне следующего часа
    start_time = current_time.time()
    print(start_time)
    end_time = (datetime.now(time_zone) + timedelta(hours=1)).time()
    print(end_time)
    habits = Habit.objects.filter(time_habit__range=(start_time, end_time))
    print(habits)
    for habit in habits:
        user = habit.owner.tg_chat_id
        message = f"Вам необходимо сделать {habit.action} в {habit.time_habit} в {habit.location}."
        send_telegram_message(user, message)
