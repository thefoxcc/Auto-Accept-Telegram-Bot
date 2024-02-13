import asyncio  # Импортируем asyncio для асинхронного программирования
import logging  # Импортируем logging для ведения журнала
import logging.config  # Импортируем конфигурацию logging
import warnings  # Импортируем warnings для управления предупреждениями
from pyrogram import Client  # Импортируем Client из pyrogram
from pyrogram.raw.all import layer  # Импортируем layer из pyrogram.raw
from config import Config  # Импортируем Config из файла config.py
from aiohttp import web  # Импортируем web из aiohttp
from pytz import timezone  # Импортируем timezone из pytz для работы с часовыми поясами
from datetime import datetime  # Импортируем datetime из datetime для работы с датами и временем
from plugins.web_support import web_server  # Импортируем web_server из плагина web_support
from plugins.admin_panel import user  # Импортируем user из плагина admin_panel

logging.config.fileConfig('logging.conf')  # Конфигурируем logging из файла logging.conf
logging.getLogger().setLevel(logging.INFO)  # Устанавливаем уровень логирования INFO
logging.getLogger("pyrogram").setLevel(logging.ERROR)  # Устанавливаем уровень логирования ERROR для pyrogram

class Bot(Client):  # Создаем класс Bot, наследуемый от Client

    def __init__(self):  # Определяем метод инициализации
        super().__init__(  # Вызываем метод инициализации родительского класса
            name="AutoAcceptBot",  # Устанавливаем имя бота
            api_id=Config.API_ID,  # Устанавливаем API ID из Config
            api_hash=Config.API_HASH,  # Устанавливаем API HASH из Config
            bot_token=Config.BOT_TOKEN,  # Устанавливаем токен бота из Config
            workers=200,  # Устанавливаем количество рабочих
            plugins={"root": "plugins"},  # Устанавливаем плагины для бота
            sleep_threshold=15,  # Устанавливаем порог сна
        )

    async def start(self):  # Определяем метод запуска
        await super().start()  # Вызываем метод запуска родительского класса
        me = await self.get_me()  # Получаем информацию о себе
        self.mention = me.mention  # Устанавливаем упоминание себя
        self.username = me.username  # Устанавливаем имя пользователя
        app = web.AppRunner(await web_server())  # Создаем объект приложения
        await app.setup()  # Настраиваем приложение
        bind_address = "0.0.0.0"  # Устанавливаем адрес привязки
        await web.TCPSite(app, bind_address, Config.PORT).start()  # Запускаем веб-сайт
        logging.info(f"{me.first_name} ✅✅ Бот успешно запущен ✅✅")  # Ведем журнал успешного запуска

        if Config.ADMIN:  # Если указан администратор
            try:
                await self.send_message(Config.ADMIN, f"**__{me.first_name}  БОТ ЗАПУЩЕН.....✨️__**")  # Отправляем сообщение администратору
            except:
                pass

        if Config.LOG_CHANNEL:  # Если указан канал для логов
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))  # Получаем текущую дату и время в часовом поясе Asia/Kolkata
                date = curr.strftime('%d %B, %Y')  # Форматируем дату
                time = curr.strftime('%I:%M:%S %p')  # Форматируем время
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} БОТ ПЕРЕЗАПУЩЕН !!**\n\n📅 Дата : `{date}`\n⏰ Время : `{time}`\n🌐 Часовой пояс : `Asia/Kolkata`\n\n🉐 Версия : `v{__version__} (Layer {layer})`</b>")  # Отправляем сообщение в канал для логов
            except:
                print("Пожалуйста, добавьте этого бота в администраторы вашего лог-канала")

    async def stop(self, *args):  # Определяем метод остановки
        await super().stop()  # Вызываем метод остановки родительского класса
        logging.info("Бот остановлен 🙄")  # Ведем журнал остановки бота

bot_instance = Bot()  # Создаем экземпляр бота

def main():  # Основная функция программы
    async def start_services():  # Определяем асинхронную функцию запуска сервисов
        if Config.SESSION:  # Если указана сессия
            await asyncio.gather(
                user.start(),        # Запускаем клиент Pyrogram
                bot_instance.start()  # Запускаем экземпляр бота
            )
        else:
            await asyncio.gather(
                bot_instance.start()
            )
        
    loop = asyncio.get_event_loop()  # Получаем цикл событий
    loop.run_until_complete(start_services())  # Запускаем асинхронные сервисы
    loop.run_forever()  # Запускаем цикл событий

if __name__ == "__main__":  # Если скрипт запущен как основной
    warnings.filterwarnings("ignore", message="There is no current event loop")  # Игнорируем предупреждения
    main()  # Вызываем основную функцию
