from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from helper.database import db
from config import Config
from helper.utils import OnWelcBtn, OnLeavBtn, OffWelcBtn, OffLeavBtn

@Client.on_message(filters.private & filters.command('start'))
async def handle_start(bot:Client, message:Message):
    
    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    # Add user to database if not exist
    await db.add_user(b=bot, m=message)
    
    text = f"Hi, {message.from_user.mention}\n\n I'm Auto Accept Bot I can accpet user from any channel and group just make me admin there."

    if Config.START_PIC:
        await SnowDev.delete()
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Developer 👨‍💻", url="https://t.me/Snowball_Official")]]))
    
    else:
        await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Developer 👨‍💻", url="https://t.me/Snowball_Official")]]))



@Client.on_message(filters.private & filters.command('set_welcome') & filters.user(Config.ADMIN))
async def set_WelcomeMsg(bot:Client, message:Message):
    welcomeMsg = message.reply_to_message
    if welcomeMsg:
        SnowDev = message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
        await db.set_welcome(message.from_user.id, welcomeMsg.text)
        await SnowDev.edit("Successfully Set Your Welcome Message ✅")
    else:
        await message.reply_text("Invalid Command !\n⚠️ Format ➜ `Hey, {user} Welcome to {title}` \n\n **Reply to message**")



@Client.on_message(filters.private & filters.command('set_leave') & filters.user(Config.ADMIN))
async def set_LeaveMsg(bot:Client, message:Message):
    
    leaveMsg = message.reply_to_message
    if leaveMsg:
        SnowDev = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
        await db.set_leave(message.from_user.id, leaveMsg.text)
        await SnowDev.edit("Successfully Set Your Leave Message ✅")
    else:
        await message.reply_text("Invalid Command !\n⚠️ Format ➜ `Hey, {user} By See You Again from {title}` \n\n **Reply to message**")


@Client.on_message(filters.private & filters.command('option') & filters.user(Config.ADMIN))
async def set_bool_welc(bot:Client, message:Message):
    
    SnowDev = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    
    if await db.get_bool_welc(message.from_user.id):
        if await db.get_bool_leav(message.from_user.id):
            await SnowDev.edit(text="Click the button from below to toggle Welcome & Leaving Message", reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn]]))
        
        else:
            await SnowDev.edit(text="Click the button from below to toggle Welcome & Leaving Message", reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn]]))
            
    
    elif await db.get_bool_leav(message.from_user.id):
        
        if await db.get_bool_welc(message.from_user.id):
            await SnowDev.edit(text="Click the button from below to toggle Welcome & Leaving Message", reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn]]))
        
        else:
            await SnowDev.edit(text="Click the button from below to toggle Welcome & Leaving Message", reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn]]))
    
    else:
        await SnowDev.edit(text="Click the button from below to toggle Welcome & Leaving Message", reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn]]))
    


@Client.on_callback_query()
async def handle_CallbackQuery(bot:Client, query:CallbackQuery):
    
    data = query.data
    
    if data.startswith('welc'):
        text = "Click the button from below to toggle Welcome & Leaving Message"
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_welc(query.from_user.id, False)
            if await db.get_bool_leav(query.from_user.id):
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn]]))
            
            else:
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn]]))

        elif boolean == 'off':
            await db.set_bool_welc(query.from_user.id, True)
            if await db.get_bool_leav(query.from_user.id):
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn]]))
            
            else:
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn]]))

    elif data.startswith('leav'):
        text = "Click the button from below to toggle Welcome & Leaving Message"
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_leav(query.from_user.id, False)
            if await db.get_bool_welc(query.from_user.id):
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn]]))
            
            else:
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn]]))

        elif boolean == 'off':
            await db.set_bool_leav(query.from_user.id, True)
            if await db.get_bool_welc(query.from_user.id):
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn]]))
            
            else:
                await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn]]))

