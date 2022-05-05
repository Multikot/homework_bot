import time

import telegram

from logic_bot import (check_response, check_tokens, get_api_answer,
                       parse_status, send_message)
from utils_bot import (RETRY_TIME, TELEGRAM_TOKEN, TokenNotFound, logger,
                       messages_box)


def main():
    """Основная логика работы бота.
    Если токены не прошли проверку, сообщаем об этом.
    Получаем запрос, проверяем ответ на коррекность
    Получаем элемент домашнего задания и статус, отправляем сообщение.
    """
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) - RETRY_TIME
    if not check_tokens():
        logger.error(messages_box['Token_not_found'])
        raise TokenNotFound(messages_box['Token_not_found'])
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)[0]
            message = parse_status(homework)
            send_message(bot=bot, message=message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        else:
            logger.critical(messages_box['Fatal_error_apps'])
            send_message(bot=bot, message=messages_box['Fatal_error_apps'])
            # raise FatalErrorApps(messages_box['Fatal_error_apps'])
        finally:
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
