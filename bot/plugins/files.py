from telethon import Button
from telethon.events import NewMessage
from telethon.errors import MessageAuthorRequiredError, MessageNotModifiedError, MessageIdInvalidError
from telethon.tl.custom import Message
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.telegram import send_message, filter_files
from bot.modules.static import *
from bot.database import db
import pyshorteners

s = pyshorteners.Shortener()

@TelegramBot.on(NewMessage(incoming=True, func=filter_files))
@verify_user(private=True)
async def user_file_handler(event: NewMessage.Event | Message):
    #m = await event.reply("One moment please...")
    if await db.is_inserted("ban", event.sender.id):
        return await m.edit("You are banned.")
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    event.message.text = f'`{secret_code}`'
    message = await send_message(event.message)
    message_id = message.id
    dl_link = s.dagd.short(f'{Server.BASE_URL}/dl/{message_id}?code={secret_code}')
    tg_link = s.dagd.short(f'{Server.BASE_URL}/file/{message_id}?code={secret_code}')
    deep_link = f'https://t.me/{Telegram.BOT_USERNAME}?start=file_{message_id}_{secret_code}'

    if (event.document and 'video' in event.document.mime_type) or event.video:
        stream_link = s.dagd.short(f'{Server.BASE_URL}/stream/{message_id}?code={secret_code}')
        await event.reply(
            message= MediaLinksText % {'dl_link': dl_link, 'tg_link': tg_link, 'tg_link': tg_link, 'stream_link': stream_link},
            buttons=[
                [
                    Button.url('📥 Download file', dl_link),
                    Button.url('💻 Stream file', stream_link)
                ],
                [
                    Button.inline('🗑️ Delete File', f'rm_{message_id}_{secret_code}')
                ]
            ]
        )
    else:
        await event.reply(
            message=FileLinksText % {'dl_link': dl_link},
            buttons=[
                [
                    Button.url('📥 Download File', dl_link)
                ],
                [
                    Button.inline('🗑️ Delete File', f'rm_{message_id}_{secret_code}')
                ]
            ]
        )

@TelegramBot.on(NewMessage(incoming=True, func=filter_files, forwards=False))
@verify_user()
async def channel_file_handler(event: NewMessage.Event | Message):
    if await db.is_inserted("ban", event.sender.id):
        return await event.reply("You are banned.")
    if event.raw_text and '#pass' in event.raw_text:
        return
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    event.message.text = f"`{secret_code}`"
    message = await send_message(event.message)
    message_id = message.id

    dl_link = s.dagd.short(f"{Server.BASE_URL}/dl/{message_id}?code={secret_code}")
    tg_link = s.dagd.short(f"{Server.BASE_URL}/file/{message_id}?code={secret_code}")

    if (event.document and "video" in event.document.mime_type) or event.video:
        stream_link = f"{Server.BASE_URL}/stream/{message_id}?code={secret_code}"

        try:
            await event.edit(
                buttons=[
                    [Button.url("📥 Download File", dl_link), Button.url("Stream File", stream_link)]
                ]
            )
        except (
            MessageAuthorRequiredError,
            MessageIdInvalidError,
            MessageNotModifiedError,
        ):
            pass
    else:
        try:
            await event.edit(
                buttons=[
                    [Button.url("📥 Download File", dl_link), Button.url("Retrieve File", tg_link)]
                ]
            )
        except (
            MessageAuthorRequiredError,
            MessageIdInvalidError,
            MessageNotModifiedError,
        ):
            pass
