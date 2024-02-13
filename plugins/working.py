import sys
import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import ChatMemberUpdated, ChatJoinRequest
from config import Config
from helper.database import db
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.ERROR)


async def approve_func(bot, message):
    try:
        chat = message.chat
        user = message.from_user
        await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        await db.add_appro_user(bot, message)
        bool_welcome = await db.get_bool_welc(Config.ADMIN)

        if bool_welcome:
            welcome_messagae = await db.get_welcome(Config.ADMIN)
            photo_or_video_file = await db.get_welc_file(Config.ADMIN)
            if photo_or_video_file:
                try:
                    try:
                        await bot.send_photo(chat_id=user.id, photo=photo_or_video_file, caption=welcome_messagae.format(user=user.mention, title=chat.title) if welcome_messagae else Config.DEFAULT_WELCOME_MSG.format(user=user.mention, title=chat.title))
                    except:
                        await bot.send_animation(chat_id=user.id, animation=photo_or_video_file, caption=welcome_messagae.format(user=user.mention, title=chat.title) if welcome_messagae else Config.DEFAULT_WELCOME_MSG.format(user=user.mention, title=chat.title))
                except:
                    await bot.send_video(chat_id=user.id, video=photo_or_video_file, caption=welcome_messagae.format(user=user.mention, title=chat.title) if welcome_messagae else Config.DEFAULT_WELCOME_MSG.format(user=user.mention, title=chat.title))

            else:
                await bot.send_message(chat_id=user.id, text=welcome_messagae.format(user=user.mention, title=chat.title) if welcome_messagae else Config.DEFAULT_WELCOME_MSG.format(user=user.mention, title=chat.title))
    except Exception as e:
        pass
        # logging.error(str(e))


@Client.on_chat_join_request(filters.group | filters.channel)
async def handle_autoAccept(bot: Client, message: ChatJoinRequest):
    admin_permission = await db.get_bool_auto_accept(Config.ADMIN)
    if admin_permission:
        try:
            await approve_func(bot, message)
        except FloodWait:
            await approve_func(bot, message)


@Client.on_chat_member_updated()
async def handle_chat(bot: Client, update: ChatMemberUpdated):
    left_user = update.old_chat_member

    if left_user:
        try:
            bool_leave = await db.get_bool_leav(Config.ADMIN)
            if bool_leave:
                leave_message = await db.get_leave(Config.ADMIN)
                photo_or_video_file = await db.get_leav_file(Config.ADMIN)
                if photo_or_video_file:
                    try:
                        try:
                            await bot.send_photo(chat_id=left_user.user.id, photo=photo_or_video_file, caption=leave_message.format(user=left_user.user.mention, title=update.title) if leave_message else Config.DEFAULT_LEAVE_MSG.format(user=left_user.user.mention, title=update.chat.title))
                        except:
                            await bot.send_animation(chat_id=left_user.user.id, animation=photo_or_video_file, caption=leave_message.format(user=left_user.user.mention, title=update.chat.title) if leave_message else Config.DEFAULT_LEAVE_MSG.format(user=left_user.user.mention, title=update.chat.title))
                    except:
                        await bot.send_video(chat_id=left_user.user.id, video=photo_or_video_file, caption=leave_message.format(user=left_user.user.mention, title=update.chat.title) if leave_message else Config.DEFAULT_LEAVE_MSG.format(user=left_user.user.mention, title=update.chat.title))

                else:
                    await bot.send_message(chat_id=left_user.user.id, text=leave_message.format(user=left_user.user.mention, title=update.chat.title) if leave_message else Config.DEFAULT_LEAVE_MSG.format(user=left_user.user.mention, title=update.chat.title))

        except:
            # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            pass
        
    try:
        if update.new_chat_member.user.id == bot.me.id:
            # Получаем идентификатор чата
            chat_id = update.chat.id
        
            # Проверяем, был ли бот повышен до администратора
            if update.new_chat_member.status == enums.ChatMemberStatus.ADMINISTRATOR:
                # Добавляем канал в список бота
                await db.set_channel(Config.ADMIN, chat_id)
                print(f"Бот стал администратором в канале: {chat_id}")
            
    except:
        if update.old_chat_member.user.id == bot.me.id:
            # Получаем идентификатор чата
            chat_id = update.chat.id

            # Проверяем, был ли бот понижен или исключен
            if update.old_chat_member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.ADMINISTRATOR]:
                # Удаляем канал из списка бота
                await db.remove_channel(Config.ADMIN, chat_id)
                print(f"Бот был удален из администратора в канале: {chat_id}")
