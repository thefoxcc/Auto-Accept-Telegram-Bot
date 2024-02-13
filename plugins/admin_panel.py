from config import Config
from helper.database import db
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Получение статистики бота
@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hч %Mм %Sс", time.gmtime(time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Получение данных...**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Статус бота--** \n\n**⌚️ Время работы бота:** {uptime} \n**🐌 Текущий пинг:** `{time_taken_s:.3f} мс` \n**👭 Всего пользователей:** `{total_users}`")


# Перезапуск бота
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Перезапуск.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)


# Рассылка сообщения только тем пользователям, которые начали использовать бота
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} или {m.from_user.id} начал рассылку сообщений...")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Рассылка началась..!")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(f"Прогресс рассылки: \nВсего пользователей {total_users} \nЗавершено: {done} / {total_users}\nУспешно: {success}\nНеудачно: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Рассылка завершена: \nЗавершено за `{completed_in}`.\n\nВсего пользователей {total_users}\nЗавершено: {done} / {total_users}\nУспешно: {success}\nНеудачно: {failed}")


# Отправка сообщения пользователю с обработкой возможных ошибок
async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Деактивирован")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Заблокировал бота")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Неверный идентификатор пользователя")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500


# Обработчик команды для принятия всех ожидающих запросов
@Client.on_message(filters.private & filters.command('acceptall') & filters.user(Config.ADMIN))
async def handle_acceptall(bot: Client, message: Message):
    ms = await message.reply_text("**Пожалуйста, подождите...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)

    if len(list(chat_ids)) == 0:
        return await ms.edit("**Я не являюсь администратором ни в одном канале или группе!**")

    button = []
    for id in chat_ids:
        info = await bot.get_chat(id)
        button.append([InlineKeyboardButton(
            f"{info.title} {str(info.type).split('.')[1]}", callback_data=f'acceptallchat_{id}')])

    await ms.edit("Выберите канал или группу, в которой хотите принять ожидающие запросы на вступление\n\nНиже перечислены каналы или группы, где я являюсь администратором", reply_markup=InlineKeyboardMarkup(button))


# Обработчик команды для отклонения всех ожидающих запросов
@Client.on_message(filters.private & filters.command('declineall') & filters.user(Config.ADMIN))
async def handle_declineall(bot:Client, message: Message):
    ms = await message.reply_text("**Пожалуйста, подождите...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)
    
    if len(list(chat_ids)) == 0:
        return await ms.edit("**Я не являюсь администратором ни в одном канале или группе!**")
        
    button = []
    for id in chat_ids:
        info = await bot.get_chat(id)
        button.append([InlineKeyboardButton(
            f"{info.title} {str(info.type).split('.')[1]}", callback_data=f'declineallchat_{id}')])

    await ms.edit("Выберите канал или группу, в которой хотите отклонить ожидающие запросы на вступление\n\nНиже перечислены каналы или группы, где я являюсь администратором", reply_markup=InlineKeyboardMarkup(button))
    
    
# Обработчик callback-запроса для принятия всех ожидающих запросов
@Client.on_callback_query(filters.regex('^acceptallchat_'))
async def handle_accept_pending_request(bot: Client, update: CallbackQuery):
    await update.message.edit("**Пожалуйста, подождите, принимаются все ожидающие запросы... ♻️**")
    chat_id = update.data.split('_')[1]
    try:
        await user.approve_all_chat_join_requests(chat_id=chat_id)
    except Exception as e:
        return await update.message.edit(f"**Что-то пошло не так 😵\n\n Ошибка ❗ ➜ __{e}__\n\n **ОШИБКА !")

    await update.message.edit("**Задача завершена** ✓ **Приняты ✅ все ожидающие запросы на вступление**")

# Обработчик callback-запроса для отклонения всех ожидающих запросов
@Client.on_callback_query(filters.regex('^declineallchat_'))
async def handle_delcine_pending_request(bot: Client, update: CallbackQuery):
    await update.message.edit("**Пожалуйста, подождите, отклоняются все ожидающие запросы... ♻️**")
    chat_id = update.data.split('_')[1]
    try:
        await user.decline_all_chat_join_requests(chat_id=chat_id)
    except Exception as e:
        return await update.message.edit(f"**Что-то пошло не так 😵\n\n Ошибка ❗ ➜ __{e}__\n\n **ОШИБКА !")

    await update.message.edit("**Задача завершена** ✓ **Отклонены ❌ все ожидающие запросы на вступление**")
