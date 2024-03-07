'''
This file contains the `/config` endpoints, which handle importing and
exporting server template configurations.
'''

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api import db, models
from api.routes.auth import get_current_user

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
    if server_name not in current_user.servers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User does not have server config `{server_name}`'
        )

    server_in_db = await db.config_collection.find_one(
        {'name': server_name, 'owner': current_user.username}
    )
    return server_in_db

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

    if server_name in current_user.servers:
        await db.config_collection.find_one_and_update(
            {'name': server_name, 'owner': current_user.username},
            {"$set": config.model_dump()}
        )

    else:
        new_config = models.ServerConfigInDB(
            **config.model_dump(),
            owner=current_user.username
        )
        await db.config_collection.insert_one(new_config.model_dump())

        db.user_collection.find_one_and_update(
            {'username': current_user.username},
            {'$set': {
                'servers': current_user.servers + [server_name]
            }}
        )
    return models.Response(msg='Success')
