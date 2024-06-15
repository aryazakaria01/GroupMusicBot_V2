from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS

from GroupMusicBot import app
from GroupMusicBot.utils.inline import close_markup
from GroupMusicBot.plugins.tools.queue import get_duration
from GroupMusicBot.utils.decorators import AdminRightsCheck
from GroupMusicBot.core.call import stream_call, stop_stream
from GroupMusicBot.utils.database import get_loop, set_loop, is_music_playing

@app.on_message(filters.command(["loop", "cloop"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(cli: Client, message: Message, _, chat_id: int):
    usage = _["admin_17"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    
    state = message.text.split(None, 1)[1].strip()
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if state > 10:
                state = 10
            await set_loop(chat_id, state)
            await message.reply_text(
                text=_["admin_18"].format(state, message.from_user.mention),
                reply_markup=close_markup(_),
            )
            await handle_loop(cli, chat_id, state)
        else:
            return await message.reply_text(usage)
    elif state.lower() == "enable":
        await set_loop(chat_id, 10)
        await message.reply_text(
            text=_["admin_18"].format(10, message.from_user.mention),
            reply_markup=close_markup(_),
        )
        await handle_loop(cli, chat_id, 10)
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        return await message.reply_text(
            _["admin_19"].format(message.from_user.mention),
            reply_markup=close_markup(_),
        )
    else:
        return await message.reply_text(usage)


async def handle_loop(cli: Client, chat_id: int, loop_count: int):
    """Handles the looping of the music based on loop_count."""
    for _ in range(loop_count):
        is_playing = await is_music_playing(chat_id)
        if not is_playing:
            await stream_call(cli, chat_id)
        await asyncio.sleep(await get_duration(chat_id))  # Wait for the current song to finish
        current_loop = await get_loop(chat_id)
        if current_loop <= 0:
            break
        await set_loop(chat_id, current_loop - 1)
    await stop_stream(cli, chat_id)
