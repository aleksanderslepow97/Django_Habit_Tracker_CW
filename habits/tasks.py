from celery import shared_task

from habits.services import message_generator, send_tg_message
from users.models import User


@shared_task
def reminder_of_habits():
    """Задача: напоминание о привычках"""
    users = User.objects.all()
    user_dict = {}
    for user in users:
        if user.tg_chat_id:
            user_dict = message_generator(user=user)
        if user_dict:
            for message, chat_id in user_dict.items():
                send_tg_message(message=message, chat_id=chat_id)
