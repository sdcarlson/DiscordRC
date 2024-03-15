'''
This file contains the Pydantic data models for Users, server configs, etc.
'''

from enum import Enum
from pydantic import BaseModel

### API Models #################################################################

class Response(BaseModel):
    '''
    Simple response model. Note that for errors, it's better to raise
    an HTTPException.
    '''
    msg: str = 'Success'

class InviteLink(BaseModel):
    '''
    Response data for the `/bot/create` endpoint.
    '''
    invite_link: str

### Server Config Models #######################################################

class ChannelType(str, Enum):
    '''
    Types of channels.
    '''
    TEXT = 'TEXT'
    VOICE = 'VOICE'
    RULES = 'RULES'
    UPDATES = 'UPDATES'
    FORUM = 'FORUM'
    STAGE = 'STAGE'
    ANNOUNCEMENTS = 'ANNOUNCEMENTS'

class Channel(BaseModel):
    '''
    A single text or voice channel. Each element of `permissions` maps a
    rol name to a dict of permission => bool.
    '''
    name: str
    id: int | None = None
    channel_type: ChannelType
    permissions: dict[str, dict[str, bool]] = {}

class Category(BaseModel):
    '''
    A group of channels, with some permissions that the channels might inherit.
    '''
    name: str | None
    id: int | None = None
    permissions: dict[str, dict[str, bool]] | None = None
    text_based_channels: list[Channel] = []
    voice_based_channels: list[Channel] = []

class Role(BaseModel):
    '''
    A role for a server. Has some permissions.
    '''
    name: str
    id: int | None = None
    permissions: list[str] = []

class ServerConfig(BaseModel):
    '''
    A configuration for a single server.
    '''
    name: str
    id: int | None = None
    community: bool = False
    roles: list[Role] = []
    categories: list[Category] = []

class ServerConfigInDB(ServerConfig):
    '''
    Additional information about a server config that is hidden in the DB.
    `owner` is the username of the `User` that owns this config.
    '''
    owner: str


### Authentication/User Models #################################################

class Token(BaseModel):
    '''
    Login tokens. `token_type` should be `bearer`.
    '''
    access_token: str
    token_type: str

class TokenData(BaseModel):
    '''
    The data to store in each jwt token. `username` is stored as `sub` in
    the token.
    '''
    username: str | None

class User(BaseModel):
    '''
    Data about a user. `servers` is a list of server names.
    '''
    username: str
    servers: list[str] = []

class UserInDB(User):
    '''
    Additional information about a user that is hidden in the DB.
    '''
    hashed_password: str
