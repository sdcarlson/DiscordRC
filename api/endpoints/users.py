from typing import Annotated

from fastapi import APIRouter, Depends

import models
from endpoints.auth import get_current_active_user

router = APIRouter()

### USER ENDPOINTS #############################################################

@router.get('/me', response_model=models.User)
async def get_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    '''
    Returns information about the current user based on the user's login token.
    '''
    return current_user
