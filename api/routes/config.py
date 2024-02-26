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
    Returns one of the user's server configs based on the server name.
    '''
    for mapping in current_user.servers:
        if server_name == mapping.name:
            server_in_db = await db.config_collection.find_one(
                {'_id': ObjectId(mapping.config_uid)}
            )
            return server_in_db
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User does not have server config `{server_name}`'
    )

@router.post('/import')
async def import_config(
    current_user: Annotated[models.User, Depends(get_current_user)],
    config: models.ServerConfig
) -> models.Response:
    '''
    Sets a server config for the current user. If the user already has
    a config with the same name, then this endpoint will update that config.
    '''
    server_name = config.name
    server_uid = None
    for mapping in current_user.servers:
        if server_name == mapping.name:
            server_uid = mapping.config_uid
            break

    if server_uid is not None:
        await db.config_collection.find_one_and_update(
            {'_id': ObjectId(server_uid)},
            {"$set": config.model_dump()}
        )
    else:
        config_in_db = models.ServerConfigInDB(
            **config.model_dump(),
            owner=current_user.username
        )
        new_config = await db.config_collection.insert_one(
            config_in_db.model_dump()
        )

        server_uid = str(new_config.inserted_id)
        current_user.servers.append(models.UserConfigMapping(
            name=server_name,
            config_uid=server_uid
        ))

        db.user_collection.find_one_and_update(
            {'username': current_user.username},
            {'$set': {
                'servers': [mapping.model_dump() for mapping in current_user.servers]
            }}
        )
    return models.Response(msg='Success')
