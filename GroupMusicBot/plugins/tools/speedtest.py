from GroupMusicBot import config
import asyncio
import speedtest

from pyrogram import filters
from pyrogram.types import Message

from GroupMusicBot import app
from GroupMusicBot.misc import SUDOERS
from GroupMusicBot.utils.decorators.language import language

def testspeed(m, strings):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m.edit_text(strings["server_12"])
        test.download()
        m.edit_text(strings["server_13"])
        test.upload()
        test.results.share()
        result = test.results.dict()
        m.edit_text(strings["server_14"])
    except AttributeError as e:
        m.edit_text(f"<code>{e.with_traceback(e.__traceback__)}</code>")
        return None
    return result


@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, strings: dict):
    m = await app.send_message(chat_id=message.chat.id, text=strings["server_11"])
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, strings)

    if result is None:
        return  # Exit if there was an error in testspeed function

    output = strings["server_15"].format(
        result["client"]["isp"],
        result["client"]["country"],
        result["server"]["name"],
        result["server"]["country"],
        result["server"]["cc"],
        result["server"]["sponsor"],
        result["server"]["latency"],
        result["ping"],
    )
    await app.send_photo(chat_id=message.chat.id, photo=result["share"], caption=output)
    await m.delete()
