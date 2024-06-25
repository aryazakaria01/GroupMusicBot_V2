import sys
import config
from motor.motor_asyncio import AsyncIOMotorClient

from GroupMusicBot.logging import LOGGER

LOGGER(__name__).info("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_.GroupMusicBot
    LOGGER(__name__).info("Connected to your Mongo Database.")
except:
    LOGGER(__name__).error("Failed to connect to your Mongo Database.")
    sys.exit()
