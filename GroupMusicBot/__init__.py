from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from GroupMusicBot.core.bot import GMB
from GroupMusicBot.core.git import git
from GroupMusicBot.core.dir import dirr
from GroupMusicBot.logging import LOGGER
from GroupMusicBot.misc import dbb, heroku
from GroupMusicBot.core.userbot import Userbot

git()
dbb()
dirr()
heroku()

app = GMB()
userbot = Userbot()
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

from .platforms import *

Apple = AppleAPI()
Resso = RessoAPI()
Carbon = CarbonAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
Spotify = SpotifyAPI()
SoundCloud = SoundAPI()
