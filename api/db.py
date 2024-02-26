from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = 'mongodb://admin:2BLfv2tcQnSa@localhost:27017'
DATABASE_NAME = 'db'

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

user_collection = db.get_collection('users')
config_collection = db.get_collection('configs')
