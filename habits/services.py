import requests
from django.utils import timezone

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL
from habits.models import Habit


def send_tg_message(message, chat_id):
    """Функция отправки сообщения в Телерамм"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)


def message_generator(user):
    """Функция генерирует сообщения пользователю с напоминаниями о привычках."""
    current_time = timezone.now()

    habits = Habit.objects.filter(user=user, time__gte=current_time)

    user_dict = {}
    for habit in habits:
        if habit.user.tg_chat_id:
            message = (
                f"Напоминание: '{habit.action}' "
                f"в {habit.time.strftime('%H:%M')} "
                f"в месте: '{habit.place}'."
            )

            if habit.reward:
                message += f" Награда: '{habit.reward}'."

            user_dict = {
                "chat_id": habit.user.tg_chat_id,
                "message": message,
            }

    return user_dict
