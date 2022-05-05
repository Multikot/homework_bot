import time
from http import HTTPStatus

import requests

from utils_bot import (ENDPOINT, HEADERS, HOMEWORK_STATUSES, PRACTICUM_TOKEN,
                       TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, ApiObjectNotFound,
                       HomeworkStatusError, MessageNotFound, logger,
                       messages_box)


def send_message(bot, message):
    """Отправляется сообщение в телеграм.
    Принимает экземпляр класса, где указан чат id и сообщение.
    """
    try:
        logger.info(messages_box['Send_message'])
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except MessageNotFound:
        logger.error(messages_box['Message_not_found'])
        raise MessageNotFound(messages_box['Message_not_found'])


def get_api_answer(current_timestamp):
    """Проверяем запрос к Api, статус код запроса должен быть равен 200."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK.value:
            logger.error(messages_box['Practicum_api_answer_none'])
            raise ApiObjectNotFound(messages_box['Practicum_api_answer_none'])
    except Exception as error:
        logger.error((messages_box['Api_get_error'], error))
        raise ((messages_box['Api_get_error'], error))
    return response.json()


def check_response(response):
    """Провермяем, что длина словаря больше 0.
    Проверяем, что в ответ на запрос нам возвращается словарь,
    что ключ homeworks есть в словаре и что по запросу через ключ
    возвращается список.
    """
    assert len(response) != 0, False
    if not isinstance(response, dict):
        logger.error(messages_box['Type_homework_is_not_dict'])
        raise TypeError(messages_box['Type_homework_is_not_dict'])
    if 'homeworks' not in response:
        logger.error(messages_box['Key_homeworks_not_found'])
        raise TypeError(messages_box['Type_homework_is_not_list'])
    if not isinstance(response['homeworks'], list):
        logger.error(messages_box['Type_homework_is_not_list'])
        raise TypeError(messages_box['Type_homework_is_not_list'])
    homework = response['homeworks']
    return homework


def parse_status(homework):
    """Находим имя работы и статус.
    Если статус успешно получен, то формируем сообщение.
    """
    homework_name = homework['homework_name']
    if 'status' not in homework:
        logger.error(messages_box['Key_status_not_found'])
        raise TypeError(messages_box['Key_status_not_found'])
    homework_status = homework['status']
    if 'reviewer_comment' not in homework:
        logger.error(messages_box['Key_reviewer_comment_not_found'])
        raise TypeError(messages_box['Key_reviewer_comment_not_found'])
    reviewer_comment = homework['reviewer_comment']
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except HomeworkStatusError:
        logger.error(messages_box['Homework_status_error'])
        raise HomeworkStatusError(messages_box['Homework_status_error'])
    return (f'Изменился статус проверки работы "{homework_name}". {verdict}',
            f'c комментарием: {reviewer_comment}')


def check_tokens():
    """Проверяем валидность токенов."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        if PRACTICUM_TOKEN is None:
            logger.error(messages_box['Practicum_token_not_found'])
        if TELEGRAM_TOKEN is None:
            logger.error(messages_box['Telegram_token_not_found'])
        if TELEGRAM_CHAT_ID is None:
            logger.error(messages_box['Telegram_chat_id_not_found'])
    return False
