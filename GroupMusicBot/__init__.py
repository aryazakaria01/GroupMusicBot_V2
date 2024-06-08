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
app = Client(
    name="Gcp",
    in_memory=True,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

from .platforms import *

Apple = AppleAPI()
Resso = RessoAPI()
Carbon = CarbonAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
Spotify = SpotifyAPI()
SoundCloud = SoundAPI()
