from telethon import Button
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot.database import Database 

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: NewMessage.Event | Message):
    
    await event.reply(
        message=WelcomeText % {'first_name': event.sender.first_name}
    )
    if not await Database.is_inserted("users", event.sender.id):
        await Database.insert("users", event.sender.id)

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/info$'))
@verify_user(private=True)
async def user_info(event: Message):
    await event.reply(UserInfoText.format(sender=event.sender))
    
@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/logs$'))
async def send_log(event: NewMessage.Event | Message):
    await event.reply(file='event-log.txt')
    
@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/users$'))
@verify_user(private=True)
async def users(event: Message):
    await event.reply('Total Users Count:', len(fetch_all("users")))

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/bcast$'))
@verify_user(private=True)
async def bcast(event: Message):
    await event.reply('Total Users Count:', len(fetch_all("users")))

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/ban$'))
@verify_user(private=True)
async def ban(event: Message):
    user_id = 
    if not await Database.is_inserted("ban", user_id):
        await Database.insert("ban", user_id)
    await event.reply('Done banned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/unban$'))
@verify_user(private=True)
async def unban(event: Message):
    user_id =
    if await Database.is_inserted("ban", user_id):
        await Database.delete("ban", user_id)
    await event.reply('User unbanned!')

