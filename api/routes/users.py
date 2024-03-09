'''
This file contains the `/users` endpoints, which give information about users.
'''

from typing import Annotated

from fastapi import APIRouter, Depends

from api import models
from api.routes.auth import get_current_user

router = APIRouter()

### USER ENDPOINTS #############################################################

@router.get('/me', response_model=models.User)
async def get_users_me(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    '''
    Returns information about the current user based on the user's login token.
    '''
    return current_user
