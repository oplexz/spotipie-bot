import os


class Config:
    API_KEY = os.getenv('API_KEY')
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_DB = os.getenv('MONGO_DB')
    TEMP_CHANNEL = os.getenv('TEMP_CHANNEL')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    BOT_USERNAME = os.getenv('BOT_USERNAME')
    BOT_URL = f"t.me/{BOT_USERNAME}"
