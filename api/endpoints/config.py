from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

import models
from endpoints.auth import get_current_active_user, fake_users_db

router = APIRouter()

### CONFIG ENDPOINTS ###########################################################

@router.get('/config/export', response_model=models.ServerConfig)
async def export_config(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    server_name: str
) -> models.ServerConfig:
    '''
    Returns a server config as json.
    '''
    if server_name not in current_user.configs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User does not have server config `{server_name}`'
        )
    return fake_users_db[current_user.username]['configs'][server_name]

@router.post('/config/import')
async def import_config(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    config: models.ServerConfig
):
    '''
    Sets a server config for the current user.
    '''
    server_name = config.name
    fake_users_db[current_user.username]['configs'][server_name] = config.model_dump()
    return 'Success'
