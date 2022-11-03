import argparse
import datetime
import os
import time
from textwrap import dedent
import logging
import telegram
import requests
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

        self.tg_bot.send_message(chat_id=self.chat_id, text='Бот запущен')

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main(tg_bot, chat_id):

    timestamp = datetime.datetime.now().timestamp()
    request_timeout = 60

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

            if not check_polling['new_attempts'][0]['is_negative']:
                tg_bot.send_message(
                    chat_id,
                    text=dedent(f"""\
                        Преподаватель проверил работу и принял её
                        {check_polling["new_attempts"][0]["lesson_title"]}
                        {check_polling["new_attempts"][0]["lesson_url"]}""")
                )
            else:
                tg_bot.send_message(
                    chat_id,
                    text=dedent(f"""\
                        Преподаватель проверил работу и не принял её.
                        {check_polling["new_attempts"][0]["lesson_title"]}
                        {check_polling["new_attempts"][0]["lesson_url"]}
                        Исправь и отправь заново!""")
                )

        except requests.exceptions.ReadTimeout as warn:
            logger.warning(f'{warn}\nRead timeout! Add 5 sec to timeout.')
            request_timeout += 5

        except requests.exceptions.ConnectionError as warn:
            logger.warning(f'{warn}\nConnection error! Try to connect after 5 seconds.')
            time.sleep(5)


if __name__ == '__main__':

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
    bot = telegram.Bot(token=telegram_token)

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, args.chat_id))

    main(bot, args.chat_id)
