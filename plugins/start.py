from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from helper.database import db
from config import Config, TxT
from helper.utils import (
    OnWelcBtn,
    OnLeavBtn,
    OffWelcBtn,
    OffLeavBtn,
    OnAutoacceptBtn,
    OffAutoacceptBtn,
)


@Client.on_message(filters.private & filters.command("start"))
async def handle_start(bot: Client, message: Message):
    SnowDev = await message.reply_text(text="**Подождите, пожалуйста...**", reply_to_message_id=message.id)
    await db.add_user(b=bot, m=message)
    text = f"Привет, {message.from_user.mention}\n\n Я Auto Accept Bot, я могу принимать пользователей из любого канала или группы, просто сделайте меня администратором там."
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Разработчик 👨‍💻", url="https://t.me/Snowball_Official")],
            [InlineKeyboardButton("Помощь", callback_data="help")],
        ]
    )
    if Config.START_PIC:
        if message.from_user.id == Config.ADMIN:
            await SnowDev.delete()
            await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=reply_markup)
        else:
            await SnowDev.delete()
            await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Разработчик 👨‍💻", url="https://t.me/Snowball_Official")]]))
    else:
        if message.from_user.id == Config.ADMIN:
            await SnowDev.edit(text=text, reply_markup=reply_markup)
        else:
            await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Разработчик 👨‍💻", url="https://t.me/Snowball_Official")]]))


@Client.on_message(filters.private & filters.command("set_welcome") & filters.user(Config.ADMIN))
async def set_welcome_msg(bot: Client, message: Message):
    welcome_msg = message.reply_to_message
    if welcome_msg:
        SnowDev = await message.reply_text("**Пожалуйста, подождите...**", reply_to_message_id=message.id)
        try:
            if welcome_msg.photo or welcome_msg.video or welcome_msg.animation:
                await db.set_welcome(message.from_user.id, welcome_msg.caption)
                await db.set_welc_file(message.from_user.id, welcome_msg.photo.file_id if welcome_msg.photo else welcome_msg.video.file_id if welcome_msg.video else welcome_msg.animation.file_id)
            else:
                await db.set_welcome(message.from_user.id, welcome_msg.text)
                await db.set_welc_file(message.from_user.id, None)
        except Exception as e:
            return await SnowDev.edit(e)
        await SnowDev.edit("Сообщение приветствия успешно установлено ✅")
    else:
        await message.reply_text("Недействительная команда !\n⚠️ Формат ➜ `Привет, {пользователь} Добро пожаловать в {название}` \n\n **Ответьте на сообщение**")


@Client.on_message(filters.private & filters.command("set_leave") & filters.user(Config.ADMIN))
async def set_leave_msg(bot: Client, message: Message):
    leave_msg = message.reply_to_message
    if leave_msg:
        SnowDev = await message.reply_text("**Пожалуйста, подождите...**", reply_to_message_id=message.id)
        try:
            if leave_msg.photo or leave_msg.video or leave_msg.animation:
                await db.set_leave(message.from_user.id, leave_msg.caption)
                await db.set_leav_file(message.from_user.id, leave_msg.photo.file_id if leave_msg.photo else leave_msg.video.file_id if leave_msg.video else leave_msg.animation.file_id)
            else:
                await db.set_leave(message.from_user.id, leave_msg.text)
                await db.set_leav_file(message.from_user.id, None)
        except Exception as e:
            return await SnowDev.edit(e)
        await SnowDev.edit("Сообщение об уходе успешно установлено ✅")
    else:
        await message.reply_text("Недействительная команда !\n⚠️ Формат ➜ `Привет, {пользователь} До свидания от {название}` \n\n **Ответьте на сообщение**")


@Client.on_message(filters.private & filters.command('option') & filters.user(Config.ADMIN))
async def set_bool_welc(bot: Client, message: Message):
    SnowDev = await message.reply_text("**Пожалуйста, подождите...**", reply_to_message_id=message.id)

    user_id = message.from_user.id
    bool_welc = await db.get_bool_welc(user_id)
    bool_leav = await db.get_bool_leav(user_id)
    bool_auto_accept = await db.get_bool_auto_accept(user_id)

    welc_buttons = [OnWelcBtn, OffWelcBtn]
    leav_buttons = [OnLeavBtn, OffLeavBtn]
    autoaccept_buttons = [OnAutoacceptBtn, OffAutoacceptBtn]

    # Определение конфигураций кнопок на основе настроек пользователя
    welc_button_row = [welc_buttons[0] if bool_welc else welc_buttons[1],
                       leav_buttons[0] if bool_leav else leav_buttons[1]]
    autoaccept_button_row = [autoaccept_buttons[0]
                             if bool_auto_accept else autoaccept_buttons[1]]

    # Обновление текста и кнопок на основе настроек пользователя
    text = "Нажмите кнопку ниже, чтобы переключить приветственные и прощальные сообщения, а также авто-принятие."
    reply_markup = InlineKeyboardMarkup(
        [welc_button_row, autoaccept_button_row])

    # Редактирование сообщения с обновленным текстом и кнопками
    await SnowDev.edit(text=text, reply_markup=reply_markup)


@Client.on_callback_query()
async def handle_CallbackQuery(bot: Client, query: CallbackQuery):

    data = query.data

    if data.startswith('welc'):
        text = "Нажмите кнопку ниже, чтобы переключить приветственные и прощальные сообщения, а также авто-принятие."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_welc(query.from_user.id, False)
            if await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

        elif boolean == 'off':
            await db.set_bool_welc(query.from_user.id, True)
            if await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

    elif data.startswith('leav'):
        text = "Нажмите кнопку ниже, чтобы переключить приветственные и прощальные сообщения, а также авто-принятие."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_leav(query.from_user.id, False)
            if await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

        elif boolean == 'off':
            await db.set_bool_leav(query.from_user.id, True)
            if await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

    elif data.startswith('autoaccept'):
        text = "Нажмите кнопку ниже, чтобы переключить приветственные и прощальные сообщения, а также авто-принятие."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_auto_accept(query.from_user.id, False)
            if await db.get_bool_welc(query.from_user.id) and await db.get_bool_leav(query.from_user.id):
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            elif await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_leav(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

            elif await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_welc(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))
        else:
            await db.set_bool_auto_accept(query.from_user.id, True)
            if await db.get_bool_welc(query.from_user.id) and await db.get_bool_leav(query.from_user.id):
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

            elif await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_leav(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

            elif await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_welc(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

            else:
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

    elif data == 'help':
        await query.message.edit(TxT.HELP_MSG, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✘ Закрыть ✘', callback_data='close')]]))

    elif data == 'close':
        await query.message.delete()
        await query.message.continue_propagation()
