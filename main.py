import argparse
import datetime
import os
import time
from textwrap import dedent

import telegram
import requests
from dotenv import load_dotenv


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

    url = 'https://dvmn.org/api/long_polling/'

    header = {
        'Authorization': f'Token {devman_token}',
    }

    while True:

        params = {
            'timestamp': timestamp,
        }

        try:
            response = requests.get(
                url,
                headers=header,
                data=params,
                timeout=request_timeout
            )
            response.raise_for_status()

            check_polling = response.json()

            if check_polling['status'] != 'found':
                params['timestamp'] = \
                    check_polling['timestamp_to_request']
                continue

            if not check_polling['new_attempts']['is_negative']:
                bot.send_message(
                    chat_id,
                    text=dedent(f"""\
                        Преподаватель проверил работу и принял её
                        {check_polling["new_attempts"]["lesson_title"]}
                        {check_polling["new_attempts"]["lesson_url"]}""")
                )
            else:
                bot.send_message(
                    chat_id,
                    text=dedent(f"""\
                        Преподаватель проверил работу и не принял её.
                        {check_polling["new_attempts"]["lesson_title"]}
                        {check_polling["new_attempts"]["lesson_url"]}
                        Исправь и отправь заново!""")
                )

        except requests.exceptions.ReadTimeout:
            request_timeout += 5

        except requests.exceptions.ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    main()
