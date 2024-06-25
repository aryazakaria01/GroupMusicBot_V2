import re
from os import getenv

from pyrogram import filters
from base64 import b64decode
from dotenv import load_dotenv

load_dotenv()

if not BLACKLIST_CHAT:
    BLACKLIST_CHAT = [
        -1001662591986,
        -1001591431784,
        -1001772837601,
        -1001736027940,
        -1001578091827,
        -1002227190877,
        -1001339411100,
    ]

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))
BLACKLIST_GCAST = {int(x) for x in getenv("BLACKLIST_GCAST", "").split()}
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", None))
OWNER_ID = list(map(int, getenv("OWNER_ID", "").split()))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! . ~ - _ = > < ) * :").split())

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    b64decode(
        "aHR0cHM6Ly9hcnlhemFrYXJpYTAxOmdpdGh1Yl9wYXRfMTFBVUdUMjdRMFNTYmNha25yaUY3aF9VNGVnTHJXUGRHd29MSW1vSnZ4R2N6bkNxVVRVYnRGd1JZYlFGWkdNWVhYV0FSNldSSVB4Z1oyS2FTckBnaXRodWIuY29tL2FyeWF6YWthcmlhMDEvR3JvdXBNdXNpY0JvdF9WMi5naXQ="
    ).decode("utf-8"),
)
GIT_TOKEN = getenv(
    "GIT_TOKEN",
    b64decode("Z2l0aHViX3BhdF8xMUFVR1QyN1EwU1NiY2FrbnJpRjdoX1U0ZWdMcldQZEd3b0xJbW9KdnhHY3puQ3FVVFVidEZ3UlliUUZaR01ZWFhXQVI2V1JJUHhnWjJLYVNy").decode(
        "utf-8"
    ),
)
REPO_URL = getenv(
    "REPO_URL",
    b64decode(
        "aHR0cHM6Ly9naXRodWIuY29tL2FyeWF6YWthcmlhMDEvR3JvdXBNdXNpY0JvdF9WMg=="
    ).decode("utf-8"),
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/SakuraEmpireTeam")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/FumikaSupportGroup")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "10"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org//file/25115719697ed91ef5672.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org//file/3dfcffd0c218ead96b102.png"
STATS_IMG_URL = "https://graph.org//file/99a8a9c13bb01f9ac7d98.png"
TELEGRAM_AUDIO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
TELEGRAM_VIDEO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNDCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
