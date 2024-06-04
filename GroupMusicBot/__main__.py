import sys
import config
import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

from config import BANNED_USERS
from GroupMusicBot.misc import sudo
from GroupMusicBot.core.call import GMB
from GroupMusicBot.plugins import ALL_MODULES
from GroupMusicBot import LOGGER, app, userbot
from GroupMusicBot.utils.database import get_banned_users, get_gbanned


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        sys.exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("GroupMusicBot.plugins" + all_module)
    LOGGER("GroupMusicBot.plugins").info("Successfully imported modules...")
    await userbot.start()
    await GMB.start()
    try:
        await GMB.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("GroupMusicBot").error(
            "Please turn on the video chat of your logs group\channel.\n\nShuting down the bot system..."
        )
        sys.exit()
    except:
        pass
    await GMB.decorators()
    LOGGER("GroupMusicBot").info(
        "\x41\x76\x69\x61\x78\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x41\x76\x69\x61\x78\x4f\x66\x66\x69\x63\x69\x61\x6c"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("GroupMusicBot").info("Stopping the bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
