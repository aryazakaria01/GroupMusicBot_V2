import logging
import pytz
from datetime import datetime
from logging.handlers import RotatingFileHandler

from GroupMusicBot import LOG_FILE_NAME

timezone = pytz.timezone('Asia/Jakarta')

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt=datetime.now(timezone).strftime("%d - %b - %y | %H:%M:%S"),
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("ntgcalls").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
LOGS = logging.getLogger(__name__)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
