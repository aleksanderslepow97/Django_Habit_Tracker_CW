import requests
from config.settings import BOT_TOKEN
import logging

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Сервис для отправки напоминаний в телеграм"""

    params = {"text": message,
              "chat_id": chat_id}

    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params)
        if response.status_code == 200:
            logger.info(f"Сообщение успешно отправлено в чат {chat_id}")
        else:
            logger.error(f"Ошибка отправки сообщения: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
