from datetime import datetime
from pytz import timezone
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

OnWelcBtn = InlineKeyboardButton(text='Добро пожаловать Вкл ✅', callback_data='welc-on')
OffWelcBtn = InlineKeyboardButton(text='Добро пожаловать Выкл ❌', callback_data='welc-off')
OnLeavBtn = InlineKeyboardButton(text='Пока Вкл ✅', callback_data='leav-on')
OffLeavBtn = InlineKeyboardButton(text='Пока Выкл ❌', callback_data='leav-off')
OnAutoacceptBtn = InlineKeyboardButton(text='Авто подтверждение Вкл ✅', callback_data='autoaccept-on')
OffAutoacceptBtn = InlineKeyboardButton(text='Авто подтверждение Выкл ❌', callback_data='autoaccept-off')

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Новый пользователь начал использовать бота--**\n\nПользователь: {u.mention}\nID: `{u.id}`\nИмя пользователя: @{u.username}\n\nДата: {date}\nВремя: {time}\n\nОт: {b.mention}"
        )
