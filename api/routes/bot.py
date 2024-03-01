'''
This file contains the `/bot` endpoints, which handle interfacing with
the Discord bot.
'''

from fastapi import APIRouter

from api import models

router = APIRouter()

@router.post('/create')
async def create_server():
    '''
    Uses the bot to create a Discord server.
    '''

@router.put('/apply')
async def apply_config(config: models.ServerConfig):
    '''
    Applies a server template configuration to an existing server.
    '''
