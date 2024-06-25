import os
import sys
import GroupMusicBot.config as config
import shutil
import socket
import asyncio
import urllib3
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from GroupMusicBot import app, LOGGER
from GroupMusicBot.utils.pastebin import GMBBin
from GroupMusicBot.misc import HAPP, XCB
from GroupMusicBot.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from GroupMusicBot.utils.decorators.language import language


SUDOERS = [
    645739169,
    870471128,
    1249591948,
    2088106582,
    1663258664,
    1416529201,
    2075788563,
    945137470,
    2137482758,
    5094813212,
]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


@app.on_message(filters.command(["getlog", "logs", "getlogs"]) & filters.user(SUDOERS))
async def log_(client, message: Message):
    try:
        await client.send_document(
            chat_id=message.chat.id,
            document="MusicLogs.txt",
            caption="Here are the logs.",
        )
    except Exception as e:
        LOGGER.error(f"Failed to send logs: {e}")
        await client.send_message(
            chat_id=message.chat.id,
            text="Failed to get logs. Please check the server logs for more details.",
        )


@app.on_message(filters.command(["update", "gitpull"]) & SUDOERS)
@language
async def update_(client, message, _):
    if await is_heroku():
        if HAPP is None:
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID, text=_["server_2"]
            )
    response = await app.send_message(chat_id=config.LOG_GROUP_ID, text=_["server_3"])
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit(_["server_4"])
    except InvalidGitRepositoryError:
        return await response.edit(_["server_5"])
    to_exc = f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    for checks in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit(_["server_6"])
    updates = ""

    def ordinal(format):
        return "%d%s" % (
            format,
            "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
        )

    for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        updates += f"<b>#{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> By: {info.author}</b>\n\t\t\t\t<b>Commited on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>A new update is available for this bot!</b>\n\nPushing the updates right now\n\n<b><u>Updates:</u></b>\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        url = await GMBBin(updates)
        nrs = await response.edit(
            f"<b>A new update is available for this bot!</b>\n\nPushing the updates right now\n\n<u><b>Updates:</b></u>\n\n<a href={url}>Check updates</a>"
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
    os.system("git stash &> /dev/null && git pull")

    try:
        served_chats = await get_active_chats()
        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text=_["server_8"].format(app.mention),
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except (ValueError, AttributeError):
                pass
        await response.edit(f"{nrs.text}\n\n{_['server_7']}")
    except (ValueError, AttributeError):
        pass

    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(f"{nrs.text}\n\n{_['server_9']}")
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=_["server_10"].format(err),
            )
    else:
        os.system("pip3 install -U -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        sys.exit()


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def restart_(client, message: Message):
    response = await message.reply_text("Restarting the bots...")

    ac_chats = await get_active_chats()
    for chat_id in ac_chats:
        try:
            await client.send_message(
                chat_id=int(chat_id),
                text=f"{client.mention} is restarting...\n\nYou can start playing again after 15-20 seconds.",
            )
            await remove_active_chat(chat_id)
            await remove_active_video_chat(chat_id)
        except Exception as e:
            print(f"Failed to notify chat {chat_id}: {e}")

    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")
    except Exception as e:
        print(f"Failed to remove directories: {e}")

    await response.edit_text(
        "Restart process started, please wait for a few seconds until the bot starts..."
    )
    os.system(f"kill -9 {os.getpid()} && bash start")
