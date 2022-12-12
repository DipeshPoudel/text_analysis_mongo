from pymongo import MongoClient
from . import config_reader


def get_database():
    CONNECTION_STRING = f"mongodb+srv://{config_reader.MONGO_USER_NAME}:{config_reader.MONGO_PASSWORD}@cluster0.wpooz7j.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client[config_reader.MONGO_DATABASE]


if __name__ == '__main__':
    dbname = get_database()
