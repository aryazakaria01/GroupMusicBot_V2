import sys

from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient

from GroupMusicBot.config import MONGO_DB_URI as MONGO_DB
from GroupMusicBot.logging import LOGGER

LOGGER(__name__).info("Connecting to your Mongo Database...")
try:
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB)
    mongodb = _mongo_async_.GroupMusicBot
    LOGGER(__name__).info("Connected to your Mongo Database.")
except PyMongoError as e:
    LOGGER(__name__).error(f"Failed to connect to your Mongo Database, due to {e}")
    sys.exit()
