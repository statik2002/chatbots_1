import argparse
import datetime
import os
import time
import telegram
import requests
from dotenv import load_dotenv


def get_all_checks_polling(devman_token, params, timeout):
    url = 'https://dvmn.org/api/long_polling/'

    header = {
        'Authorization': f'Token {devman_token}',
    }

    response = requests.get(url, headers=header, data=params, timeout=timeout)
    response.raise_for_status()

    return response.json()


def send_telegram_message(bot, chat_id, message):
    bot.send_message(chat_id, text=message)


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт проверяет работы на проверку'
                    ' в Devman и шлет сообщение при '
                    'проверке в telegram'
    )
    parser.add_argument('-c', '--chat_id', help='chat_id в Telegram')
    args = parser.parse_args()

    load_dotenv()
    devman_token = os.environ['DEVMAN_TOKEN']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = args.chat_id

    timestamp = datetime.datetime.now().timestamp()
    request_timeout = 90

    bot = telegram.Bot(token=telegram_token)

    while True:

        params = {
            'timestamp': timestamp,
        }

        try:
            all_checks_polling = get_all_checks_polling(
                devman_token,
                params,
                request_timeout
            )

            if all_checks_polling['status'] != 'found':
                params['timestamp'] = \
                    all_checks_polling['timestamp_to_request']
                continue

            if not all_checks_polling['new_attempts']['is_negative']:
                send_telegram_message(
                    bot,
                    chat_id,
                    f'Преподаватель проверил работу '
                    f'{all_checks_polling["new_attempts"]["lesson_title"]}'
                    f'{all_checks_polling["new_attempts"]["lesson_url"]}'
                )
            else:
                send_telegram_message(
                    bot,
                    chat_id,
                    f'Преподаватель проверил работу '
                    f'{all_checks_polling["new_attempts"]["lesson_title"]}'
                    f'{all_checks_polling["new_attempts"]["lesson_url"]}'
                    f'К сожалению есть ошибки. Исправь и отправь заново!'
                )

        except requests.exceptions.ReadTimeout:
            print('Requests timeout. Add 5 sec. to timeout')
            request_timeout += 5

        except requests.exceptions.ConnectionError:
            print('No connection. wait 5 sec.')
            time.sleep(5)


if __name__ == '__main__':
    main()
