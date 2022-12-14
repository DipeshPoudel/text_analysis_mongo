from pymongo import MongoClient
from . import env_config_reader


def get_database():
    connection_string = f"mongodb+srv://{env_config_reader.MONGO_USER_NAME}:{env_config_reader.MONGO_PASSWORD}@{env_config_reader.MONGO_HOST}/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    return client[env_config_reader.MONGO_DATABASE]


if __name__ == '__main__':
    dbname = get_database()
