import requests

from config import settings


def send_telegram_message(tg_chat_id, message):
    params = {
        "text": message,
        "chat_id": tg_chat_id,
    }
    response = requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params
    )
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения: {response.text}")
