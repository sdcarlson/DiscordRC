from fastapi import APIRouter
from api.db import Database

user_collection = Database.instance.get_collection('users')
config_collection = Database.instance.get_collection('configs')

router = APIRouter()

@router.delete('/')
async def clear():
    # await user_collection.drop()
    # await config_collection.drop()
    await user_collection.insert_one({'asdf': 123})
