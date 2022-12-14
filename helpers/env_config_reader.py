import os
from dotenv import load_dotenv

try:
    load_dotenv()

    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
    TWITTER_API_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    MONGO_USER_NAME = os.getenv("MONGO_USER_NAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    MONGO_HOST = os.getenv("MONGO_HOST")
except Exception as e:
    print(f"Unable to Load the Config Variables. {e}")
