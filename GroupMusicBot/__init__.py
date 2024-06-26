from GroupMusicBot.core.bot import GMB
from GroupMusicBot.core.git import git
from GroupMusicBot.core.dir import dirr
from GroupMusicBot.misc import dbb, heroku
from GroupMusicBot.core.userbot import Userbot
from GroupMusicBot.platforms import (
    AppleAPI,
    RessoAPI,
    CarbonAPI,
    TeleAPI,
    YouTubeAPI,
    SpotifyAPI,
    SoundAPI,
)

git()
dbb()
dirr()
heroku()

app = GMB()
userbot = Userbot()


Apple = AppleAPI()
Resso = RessoAPI()
Carbon = CarbonAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
Spotify = SpotifyAPI()
SoundCloud = SoundAPI()
