import logging

logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s: %(levelname)s ] %(name)-15s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("MusicLogs.txt"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.syncer").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
