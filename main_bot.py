import time

from logic_bot import (check_response, check_tokens, get_api_answer,
                       parse_status, send_message)
from utils_bot import BOT, RETRY_TIME, TokenNotFound, logger, messages_box


def main():
    """Основная логика работы бота.
    Если токены не прошли проверку, сообщаем об этом.
    Получаем запрос, проверяем ответ на коррекность
    Получаем элемент домашнего задания и статус, отправляем сообщение.
    """
    current_timestamp = int(time.time()) - RETRY_TIME
    if not check_tokens():
        logger.error(messages_box['Token_not_found'])
        raise TokenNotFound(messages_box['Token_not_found'])
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)[0]
            message = parse_status(homework)
            send_message(bot=BOT, message=message)
            current_timestamp = int(time.time())
        except IndexError:
            logger.info(messages_box['New_status_is_none'])
            current_timestamp = int(time.time())
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
