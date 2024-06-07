import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)-7s] %(name)-15s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler("MusicLogs.txt"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
