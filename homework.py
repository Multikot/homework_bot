import logging
import time
from http import HTTPStatus

import requests
import telegram

from utils_bot import (ENDPOINT, HEADERS, HOMEWORK_STATUSES, PRACTICUM_TOKEN,
                       RETRY_TIME, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN,
                       ApiObjectNotFaund, FatalErrorApps, HomeworkStatusError,
                       MessageNotFound, TokenNotFound, logging_messages_box)


def send_message(bot, message):
    """Отправляется сообщение в телеграм.
    Принимает экземпляр класса, где указан чат id и сообщение.
    """
    try:
        logging.info(logging_messages_box['Send_message'])
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except MessageNotFound:
        logging.error(logging_messages_box['Message_not_found'])
        raise MessageNotFound(logging_messages_box['Message_not_found'])


def get_api_answer(current_timestamp):
    """Проверяем запрос к Api, статус код запроса должен быть равен 200."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK.value:
            logging.error(logging_messages_box['Practicum_api_answer_none'])
            raise ApiObjectNotFaund(
                logging_messages_box['Practicum_api_answer_none'])
    except ApiObjectNotFaund(
            logging_messages_box['Practicum_api_answer_none']):
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    return response.json()


def check_response(response):
    """Провермяем, что длина словаря больше 0.
    Проверяем, что в ответ на запрос нам возвращается словарь,
    что ключ homeworks есть в словаре и что по запросу через ключ
    возвращается список.
    """
    if len(response) == 0:
        assert False
    if not isinstance(response, dict):
        logging.error(logging_messages_box['Type_homework_is_not_dict'])
        raise TypeError(logging_messages_box['Type_homework_is_not_dict'])
    if 'homeworks' not in response:
        logging.error(logging_messages_box['Key_homeworks_not_found'])
        raise TypeError(logging_messages_box['Type_homework_is_not_list'])
    if not isinstance(response['homeworks'], list):
        logging.error(logging_messages_box['Type_homework_is_not_list'])
        raise TypeError(logging_messages_box['Type_homework_is_not_list'])
    homework = response['homeworks']
    return homework


def parse_status(homework):
    """Находим имя работы и статус.
    Если статус успешно получен, то формируем сообщение.
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except HomeworkStatusError:
        logging.error(logging_messages_box['Homework_status_error'])
        raise HomeworkStatusError(
            logging_messages_box['Homework_status_error'])
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяем валидность токенов."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        if PRACTICUM_TOKEN is None:
            logging.error(logging_messages_box['Practicum_token_not_found'])
        if TELEGRAM_TOKEN is None:
            logging.error(logging_messages_box['Telegram_token_not_found'])
        if TELEGRAM_CHAT_ID is None:
            logging.error(logging_messages_box['Telegram_chat_id_not_found'])
    return False


def main():
    """Основная логика работы бота.
    Если токены не прошли проверку, сообщаем об этом.
    Получаем запрос, проверяем ответ на коррекность
    Получаем элемент домашнего задания и статус, отправляем сообщение.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) - RETRY_TIME
    if not check_tokens():
        raise TokenNotFound(logging_messages_box['Token_not_found'])
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot=bot, message=message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)
        else:
            logging.error(logging_messages_box['Fatal_error_apps'])
            raise FatalErrorApps(logging_messages_box['Fatal_error_apps'])


if __name__ == '__main__':
    main()
