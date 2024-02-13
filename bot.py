import asyncio
import logging
import logging.config
import warnings
from pyrogram import Client
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from pytz import timezone
from datetime import datetime
from plugins.web_support import web_server
from plugins.admin_panel import user

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="AutoAcceptBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"{me.first_name} ✅✅ Бот успешно запущен ✅✅")

        if Config.ADMIN:
            try:
                await self.send_message(Config.ADMIN, f"**__{me.first_name}  Я Запущен.....✨️__**")
            except:
                pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Бот был перезапущен !!**\n\n📅 Дата : `{date}`\n⏰ Время : `{time}`\n🌐 Часовой пояс : `Asia/Kolkata`\n\n🉐 Версия : `v{__version__} (Слой {layer})`</b>")
            except:
                print("Пожалуйста, сделайте это администратором в вашем лог-канале")

    async def stop(self, *args):
        await super().stop()
        logging.info("Бот остановлен 🙄")


bot_instance = Bot()

def main():
    async def start_services():
        if Config.SESSION:
            await asyncio.gather(
                user.start(),        # Запустить клиент Pyrogram
                bot_instance.start()  # Запустить экземпляр бота
            )
        else:
            await asyncio.gather(
                bot_instance.start()
            )
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    loop.run_forever()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    main()
