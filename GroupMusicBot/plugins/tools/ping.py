from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from GroupMusicBot.config import BANNED_USERS

from GroupMusicBot import app
from GroupMusicBot.core.call import GMB
from GroupMusicBot.utils import bot_sys_stats
from GroupMusicBot.utils.inline import supp_markup
from GroupMusicBot.utils.decorators.language import language


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await app.send_message(
        chat_id=message.chat.id, caption=_["ping_1"].format(app.mention)
    )
    pytgping = await GMB.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
