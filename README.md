# Чат-бот Урок 1

## Данный скрипт проверяет проверку отправленных работ на Devman и в случае проверки работы, отправляет сообщение в Telegram

### Требования

- Python 3.10

### Установка
- Создать виртуальное окружение командой:
    > `python -m venv env`
- Войти в виртуальное окружение командой:
    > `source env/bin/activate`
- Создать файл `.env`, в который записать `DEVMAN_TOKEN=(TOKEN)`, `TELEGRAM_TOKEN=(TOKEN)`, `CHAT_ID=(chat id)`
- Установить зависимости командой `pip install requirements.txt`

### Использование
- Запустить скрипт командой:
    > `python main.py -c [ваш chat_id]`

### Запуск в контейнере Docker

Для запуска скрипта в контейнере docker необходимо:

1. Создать контейнер командой 
  ```commandline
  docker build chatbot .
  ```
2. После создания контейнера, запустить командой:
```commandline
docker run chatbot
```
В случае если необходимо указать свой `chat_id` запустить командой:
```commandline
docker run -e "CHAT_ID=[ваш chat id]" chatbot
```
