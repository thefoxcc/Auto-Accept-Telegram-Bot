import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
    # Конфигурация клиента Pyrogram
    API_ID = os.environ.get("API_ID", "")  # ⚠️ Обязательно
    API_HASH = os.environ.get("API_HASH", "")  # ⚠️ Обязательно
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")  # ⚠️ Обязательно

    # Конфигурация базы данных
    DB_URL = os.environ.get("DB_URL", "")  # ⚠️ Обязательно
    DB_NAME = os.environ.get("DB_NAME", "AutoAcceptBot")

    # Другие настройки
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/0ceb5f176f3cf877a08b5.jpg")
    ADMIN = int(os.environ.get('ADMIN', ''))  # ⚠️ Обязательно
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))  # ⚠️ Обязательно
    DEFAULT_WELCOME_MSG = os.environ.get("WELCOME_MSG", "Привет {user},\nВаш запрос одобрен ✅,\n\nДобро пожаловать в **{title}**")
    DEFAULT_LEAVE_MSG = os.environ.get("LEAVE_MSG", "Пока {user},\nДо скорой встречи 👋\n\nИз **{title}**")

    # Конфигурация клиента пользователя
    SESSION = os.environ.get("SESSION", "")  # ⚠️ Обязательно @SnowStringGenBot

    # Конфигурация ответа веб
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class TxT(object):

    HELP_MSG = """
<b> Доступные команды для администратора: </b>

➜ /set_welcome - Установить пользовательское приветственное сообщение (поддерживается фото, видео и анимация или gif)
➜ /set_leave - Установить пользовательское сообщение о выходе (поддерживается фото, видео и анимация или gif)
➜ /option - Включить или выключить приветственное и прощальное сообщения, а также авто-принятие (будут ли они отображаться пользователю и будет ли автоматически принят или нет)
➜ /status - Просмотреть статус бота
➜ /restart - Перезапустить бота
➜ /broadcast - Рассылка пользователям (только тем пользователям, которые начали использовать вашего бота)
➜ /acceptall - Принять все ожидающие запросы на присоединение
➜ /declineall - Отклонить все ожидающие запросы на присоединение

⚠️ <b> Поддерживается форматирование HTML и Markdown в приветственном или прощальном сообщениях, для получения дополнительной информации <a href=https://core.telegram.org/api/entities#:~:text=%2C%20MadelineProto.-,Разрешенные%20сущности,-Например%20the> Ссылка </a>. </b>


<b>⦿ Разработчик:</b> <a href=https://t.me/Snowball_Official>ѕησωвαℓℓ ❄️</a>
"""
