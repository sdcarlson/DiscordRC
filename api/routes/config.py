from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

import db
import models
from routes.auth import get_current_user

router = APIRouter()

### CONFIG ENDPOINTS ###########################################################

@router.get('/export', response_model=models.ServerConfig)
async def export_config(
    current_user: Annotated[models.User, Depends(get_current_user)],
    server_name: str
) -> models.ServerConfig:
    '''
    Returns a server config as json.
    '''
    if server_name not in current_user.config_uids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User does not have server config `{server_name}`'
        )

    server_uid = current_user.config_uids[server_name]
    server_in_db = await db.config_collection.find_one({'_id': ObjectId(server_uid)})
    return server_in_db

@router.post('/import')
async def import_config(
    current_user: Annotated[models.User, Depends(get_current_user)],
    config: models.ServerConfig
):
    '''
    Sets a server config for the current user.
    '''
    server_name = config.name
    if server_name in current_user.config_uids:
        server_uid = current_user.config_uids[server_name]
        server = {
            k: v for k, v in config.model_dump(by_alias=True).items() if v is not None
        }
        await db.config_collection.find_one_and_update(
            {'_id': ObjectId(server_uid)},
            {"$set": server}
        )
    else:
        new_config = await db.config_collection.insert_one(config.model_dump())
        server_uid = new_config.inserted_id
        current_user.config_uids[server_name] = str(server_uid)

        db.user_collection.find_one_and_update(
            {'username': current_user.username},
            {'$set': {'config_uids': current_user.config_uids}}
        )
    return 'Success'
