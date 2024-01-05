import logging

from pymongo import MongoClient
from telegram.ext import ApplicationBuilder

from sp_bot.config import Config

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARN)

LOGGER = logging.getLogger(__name__)

# Importing environment variables
TOKEN = Config.API_KEY
CLIENT_ID = Config.SPOTIFY_CLIENT_ID
CLIENT_SECRET = Config.SPOTIFY_CLIENT_SECRET
REDIRECT_URI = Config.REDIRECT_URI
MONGO_USER = Config.MONGO_USER
MONGO_PASSWORD = Config.MONGO_PASSWORD
MONGO_DB = Config.MONGO_DB
TEMP_CHANNEL = Config.TEMP_CHANNEL
BOT_USERNAME = Config.BOT_USERNAME
BOT_URL = Config.BOT_URL

app = ApplicationBuilder().token(TOKEN).build()

SESSION = MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongo:27017/{MONGO_DB}")
