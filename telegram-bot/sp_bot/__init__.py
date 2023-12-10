import logging
import os
import sys
import telegram.ext as tg
from sp_bot.config import Config

from pymongo import MongoClient

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# import ENV variables
TOKEN = Config.API_KEY

# spotify secrets
CLIENT_ID = Config.SPOTIFY_CLIENT_ID
CLIENT_SECRET = Config.SPOTIFY_CLIENT_SECRET
REDIRECT_URI = Config.REDIRECT_URI

# MongoDB secrets
MONGO_USER = Config.MONGO_USER
MONGO_PASSWORD = Config.MONGO_PASSWORD
MONGO_DB = Config.MONGO_DB

TEMP_CHANNEL = Config.TEMP_CHANNEL

updater = tg.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

SESSION = MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongo:27017/{MONGO_DB}")
