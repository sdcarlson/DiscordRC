import os
from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient


def _mongo_uri() -> str:
    '''
    Builds the MongoDB connection URI from environment variables.
    '''
    try:
        username = quote_plus(os.environ['MONGO_USERNAME'])
        password = quote_plus(os.environ['MONGO_PASSWORD'])
    except KeyError as e:
        raise RuntimeError(
            f'Environment variable {e.args[0]} must be set (see .env.example).'
        ) from None
    host = os.environ.get('MONGO_HOST', 'localhost:27017')
    return f'mongodb://{username}:{password}@{host}'

MONGO_URI = _mongo_uri()
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'db')

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

user_collection = db.get_collection('users')
config_collection = db.get_collection('configs')
