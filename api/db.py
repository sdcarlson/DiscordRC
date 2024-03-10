from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    '''
    This class handles the database connection & collections. Singleton class.
    '''
    MONGO_URI = 'mongodb://admin:2BLfv2tcQnSa@localhost:27017'

    def __init__(self, database_name='db'):
        Database.instance = self

        client = AsyncIOMotorClient(Database.MONGO_URI)
        self.db = client[database_name]
        self.database_name = database_name
        self.collections = {}

    def get_collection(self, collection_name, *args):
        # if collection_name not in self.collections:
        #     self.collections[collection_name] = self.db.get_collection(collection_name, *args)
        # return self.collections[collection_name]
        return self.db.get_collection(collection_name, *args)
