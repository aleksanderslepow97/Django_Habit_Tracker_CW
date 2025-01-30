import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    """Функция отправки сообщения через телеграм бота."""
    params = {"text": message, "chat_id": chat_id}

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.get(url=url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to send telegram message: {response.text}")
