import tweepy
from helpers import config_reader
from helpers import pymongo_get_database

db_name = pymongo_get_database.get_database()
topic = "apple"
items_limit = 1000
collection_name = db_name[f'tweet_extract_{topic}']

api_key = config_reader.TWITTER_API_KEY
api_key_secret = config_reader.TWITTER_API_KEY_SECRET
bearer_token = config_reader.TWITTER_API_BEARER_TOKEN
access_token = config_reader.TWITTER_ACCESS_TOKEN
access_token_secret = config_reader.TWITTER_ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

extracted_tweets = []

for status in tweepy.Cursor(api.search_tweets,
                            topic,
                            lang="en").items(items_limit):
    extracted_tweets.append({'_id': status.id, 'tweet_text': status.text})

collection_name.insert_many(extracted_tweets)
