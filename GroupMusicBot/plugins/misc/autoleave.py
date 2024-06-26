from GroupMusicBot import config
import asyncio

from datetime import datetime
from pyrogram.enums import ChatType

from GroupMusicBot import app
from GroupMusicBot.core.call import GMB, autoend
from GroupMusicBot.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT:
        while not await asyncio.sleep(900):
            from GroupMusicBot.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        if i.chat.type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            if (
                                i.chat.id != config.LOG_GROUP_ID
                                and i.chat.id != -1001662591986
                                and i.chat.id != -1001577053940
                            ):
                                if left == 20:
                                    continue
                                if not await is_active_chat(i.chat.id):
                                    try:
                                        await client.leave_chat(i.chat.id)
                                        left += 1
                                    except(ValueError, AttributeError):
                                        continue
                except(ValueError, AttributeError):
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        ender = await is_autoend()
        if not ender:
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await GMB.stop_stream(chat_id)
                except(ValueError, AttributeError):
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "Bot automatically left video chat because no one was listening on video chat.",
                    )
                except(ValueError, AttributeError):
                    continue


asyncio.create_task(auto_end())
