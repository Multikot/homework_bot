import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('YANDEX_TOKEN_API')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('MY_CHAT_ID')
RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log',
    maxBytes=50000000,
    backupCount=5)

logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s -  %(levelname)s - %(message)s')
handler.setFormatter(formatter)

messages_box = {
    'Send_message': 'Отправлено сообщение',
    'Practicum_token_not_found': 'Не найден токен Практикума',
    'Telegram_token_not_found': 'Не найден токен Телеграм-бота',
    'Telegram_chat_id_not_found': 'Не найден токен телеграм-чата',
    'Practicum_api_answer_none': 'Ответ API отличный от 200',
    'Type_homework_is_not_list': 'Тип запроса не является списком',
    'Key_homeworks_not_found': 'Не найден ключ homeworks',
    'Key_status_not_found': 'Не найден ключ status',
    'Key_reviewer_comment_not_found': 'не найден ключ reviewer comment',
    'Type_homework_is_not_dict': 'Тип запроса не является словарем',
    'Homework_status_error': 'Статус домашней работы не получен',
    'Message_not_found': 'Не найдено сообщение для отправки',
    'Token_not_found': 'Один или несколько токенов не найдено',
    'Fatal_error_apps': 'Сбой в работе приложения',
    'Api_get_error': 'Ошибка получения Api'
}


class ApiObjectNotFound(Exception):
    pass


class HomeworkStatusError(Exception):
    pass


class MessageNotFound(Exception):
    pass


class TokenNotFound(Exception):
    pass


class FatalErrorApps(Exception):
    pass
