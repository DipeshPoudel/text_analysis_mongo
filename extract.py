import tweepy
from helpers import env_config_reader
from helpers import pymongo_get_database
from helpers import ini_config_reader


def auth(api_key, api_key_secret, access_token, access_token_secret):
    try:
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except Exception as e:
        print(e)


def get_api(auth):
    try:
        api = tweepy.API(auth)
        return api
    except Exception as e:
        print(e)


def extract_data(db_name, topic, api, items_limit=100):
    try:
        collection_name = db_name[f'tweet_extract_{topic}']
        extracted_tweets = []
        for status in tweepy.Cursor(api.search_tweets,
                                    topic,
                                    lang="en").items(items_limit):
            extracted_tweets.append({'_id': status.id, 'tweet_text': status.text})

        collection_name.insert_many(extracted_tweets)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    config = ini_config_reader.read_config()
    tweet_topic = config['topic_config']['topic_title']
    tweet_items_limit = int(config['topic_config']['topic_title'])
    api_key = env_config_reader.TWITTER_API_KEY
    api_key_secret = env_config_reader.TWITTER_API_KEY_SECRET
    bearer_token = env_config_reader.TWITTER_API_BEARER_TOKEN
    access_token = env_config_reader.TWITTER_ACCESS_TOKEN
    access_token_secret = env_config_reader.TWITTER_ACCESS_TOKEN_SECRET
    api_auth = auth(api_key, api_key_secret, access_token, access_token_secret)
    api = get_api(api_auth)
    extract_data(pymongo_get_database.get_database(), tweet_topic, api, items_limit=tweet_items_limit)
