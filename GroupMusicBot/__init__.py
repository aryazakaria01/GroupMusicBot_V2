from GroupMusicBot.core.bot import GMB
from GroupMusicBot.core.dir import dirr
from GroupMusicBot.core.git import git
from GroupMusicBot.core.userbot import Userbot
from GroupMusicBot.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = GMB()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
