import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[ %(asctime)s: %(levelname)s ] %(name)-15s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("MusicLogs.txt"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
