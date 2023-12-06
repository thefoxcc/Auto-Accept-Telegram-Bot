import sys
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, ChatJoinRequest
from config import Config
from helper.database import db


@Client.on_chat_join_request(filters.group | filters.channel)
async def handle_autoAccept(bot: Client, message: ChatJoinRequest):
    try:

        chat = message.chat
        user = message.from_user
        await bot.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        await db.add_appro_user(bot, message)
        bool_welcome = await db.get_bool_welc(Config.ADMIN)

        if bool_welcome:
            welcome_messagae = await db.get_welcome(Config.ADMIN)
            if welcome_messagae:
                await bot.send_message(chat_id=user.id, text=welcome_messagae.format(user=user.mention, title=chat.title))

            else:
                await bot.send_message(chat_id=user.id, text=Config.WELCOME_MSG.format(user=user.mention, title=chat.title))
                
    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


@Client.on_chat_member_updated()
async def handle_chat(bot: Client, update: ChatMemberUpdated):
    left_user = update.old_chat_member

    if await db.is_user_exist(left_user.user.id) and left_user:
        try:
            bool_leave = await db.get_bool_leav(Config.ADMIN)

            if bool_leave:
                leave_message = await db.get_leave(Config.ADMIN)
                if leave_message:
                    await bot.send_message(chat_id=left_user.user.id, text=leave_message.format(user=left_user.user.mention, title=update.chat.title))

                else:
                    await bot.send_message(chat_id=left_user.user.id, text=Config.LEAVE_MSG.format(user=left_user.user.mention, title=update.chat.title))

        except Exception as e:
            print('Error on line {}'.format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
