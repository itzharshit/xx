from telethon import Button
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot.database import db

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: NewMessage.Event | Message):
    if await db.is_inserted("ban", event.sender.id):
        return await event.reply("You are banned")
    await event.reply(
        message=WelcomeText % {'first_name': event.sender.first_name}
    )
    if not await db.is_inserted("users", event.sender.id):
        await db.insert("users", event.sender.id)

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
    await event.reply('Total Users Count:', len(db.fetch_all("users")))

@TelegramBot.on(events.NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/ban (\d+)$'))
@verify_user(private=True)
async def ban(event: Message):
    match = re.match(r'^/ban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid user ID.")
        return
    user_id = int(match.group(1))
    if not await db.is_inserted("ban", user_id):
        await db.insert("ban", user_id)
    await event.reply('Done banned!')

@TelegramBot.on(events.NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/unban (\d+)$'))
@verify_user(private=True)
async def ban(event: Message):
    match = re.match(r'^/unban (\d+)$', event.raw_text)
    if not match:
        await event.reply("Please provide a valid user ID.")
        return
    user_id = int(match.group(1))
    if await db.is_inserted("ban", user_id):
        await db.delete("ban", user_id)
    await event.reply('User unbanned!')

@TelegramBot.on(NewMessage(chats=Telegram.OWNER_ID, incoming=True, pattern=r'^/bcast$'))
@verify_user(private=True)
async def bcast(event: Message):
    if not event.reply_to_msg_id:
        return await event.reply(
            "Please use `/broadcast` as reply to the message you want to broadcast."
        )
    msg = await event.get_reply_message()
    xx = await event.reply("In progress...")
    users = await db.fetch_all('users')
    done = error = 0
    for i in users:
        try:
            await TelegramBot.send_message(
                int(i),
                msg.text.format(user=(await TelegramBot.get_entity(int(i))).first_name),
                file=msg.media,
                buttons=msg.buttons,
                link_preview=False,
            )
            done += 1
        except Exception as brd_er:
            log.error("Broadcast error:\nChat: %d\nError: %s", int(i), brd_er)
            error += 1
    await xx.edit("Broadcast completed.\nSuccess: {}\nFailed: {}".format(done, error))
