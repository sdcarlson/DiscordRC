'''
This file contains the `/bot` endpoints, which handle interfacing with
the Discord bot.
'''

from typing import Annotated

from fastapi import APIRouter, Depends

from api import models
from api.routes.auth import get_current_user
from DiscordBot.DiscordInterface import DiscordInterface

router = APIRouter()
discord_interface = DiscordInterface()

@router.post('/create', response_model=models.InviteLink)
async def create_server(
    _: Annotated[models.User, Depends(get_current_user)],
    config: models.ServerConfig
) -> models.InviteLink:
    '''
    Uses the bot to create a Discord server. Returns an invite link to the
    newly created server.
    '''
    config_dict = config.model_dump()
    invite_string = await discord_interface.create_guild(config_dict)
    return models.InviteLink(invite_link=invite_string)
