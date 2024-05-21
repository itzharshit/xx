from telethon import Button
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot.database import is_inserted, insert, fetch_all, delete 

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: NewMessage.Event | Message):
    await event.reply(
        message=WelcomeText % {'first_name': event.sender.first_name}
    )

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/info$'))
@verify_user(private=True)
async def user_info(event: Message):
    await event.reply(UserInfoText.format(sender=event.sender))
    
@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/logs$'))
async def send_log(event: NewMessage.Event | Message):
    await event.reply(file='event-log.txt')
