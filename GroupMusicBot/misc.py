import socket
import heroku3


from pyrogram import filters
from GroupMusicBot.logging import LOGGER
from GroupMusicBot.core.mongo import mongodb

SUDOERS = filters.user()

HAPP = None


def is_heroku():
    return "heroku" in socket.getfqdn()

from GroupMusicBot import config as conf
# XCB = [
#     "/",
#     "@",
#     ".",
#     "com",
#     ":",
#     "git",
#     "heroku",
#     "push",
#     str(conf.HEROKU_API_KEY),
#     "https",
#     str(conf.HEROKU_APP_NAME),
#     "HEAD",
#     "main",
# ]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Local database initialized...")


async def sudo():
    global SUDOERS
    SUDOERS.add(conf.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if conf.OWNER_ID not in sudoers:
        sudoers.append(conf.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info("Loaded Sudo Users Successfully.")


def heroku():
    global HAPP
    if is_heroku:
        if conf.HEROKU_API_KEY and conf.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(conf.HEROKU_API_KEY)
                HAPP = Heroku.app(conf.HEROKU_APP_NAME)
                LOGGER(__name__).info("Heroku app configured")
            except BaseException:
                LOGGER(__name__).warning(
                    "Please make sure your HEROKU_API_KEY and HEROKU_APP_NAME are configured correctly in the heroku."
                )

