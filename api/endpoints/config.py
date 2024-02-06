from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import models
from endpoints.auth import get_current_user, fake_users_db

router = APIRouter()

### CONFIG ENDPOINTS ###########################################################

@router.get('/config/export', response_model=models.ServerConfig)
async def export_config(
    current_user: Annotated[models.User, Depends(get_current_user)],
    server_name: str
) -> models.ServerConfig:
    '''
    Returns a server config as json.
    '''
    for server in current_user.configs:
        if server.name == server_name:
            return server

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User does not have server config `{server_name}`'
    )

@router.post('/config/import')
async def import_config(
    current_user: Annotated[models.User, Depends(get_current_user)],
    config: models.ServerConfig
):
    '''
    Sets a server config for the current user.
    '''
    user_configs = fake_users_db[current_user.username]['configs']
    for i, server in enumerate(user_configs):
        if server['name'] == config.name:
            # Updating an existing server
            user_configs[i] = config.model_dump()
            return 'Success'

    # Adding a new server
    user_configs.append(config.model_dump())
    return 'Success'
