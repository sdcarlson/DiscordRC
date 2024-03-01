'''
This file contains the Pydantic data models for Users, server configs, etc.
'''

from pydantic import BaseModel

### API Models #################################################################

class Response(BaseModel):
    '''
    Simple response model. Note that for errors, it's better to raise
    an HTTPException.
    '''
    msg: str = 'Success'

### Server Config Models #######################################################

class Channel(BaseModel):
    '''
    A single text or voice channel. Each element of `permissions` maps a
    permission name to a dict of roles => bool.
    '''
    name: str
    id: int | None = None
    permissions: dict[str, dict[str, bool]] = dict()

class Category(BaseModel):
    '''
    A group of channels, with some permissions that the channels might inherit.
    '''
    name: str
    id: int | None = None
    permissions: dict[str, dict[str, bool]] = dict()
    text_channels: list[Channel] = list()
    voice_channels: list[Channel] = list()

class Role(BaseModel):
    '''
    A role for a server. Has some settings and permissions.
    '''
    name: str
    id: int | None = None
    display_separately: bool = False
    allow_mention: bool = False
    permissions: dict[str, bool] = dict()

class ServerConfig(BaseModel):
    '''
    A configuration for a single server.
    '''
    name: str
    id: int | None = None
    roles: list[Role] = list()
    categories: list[Category] = list()

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

class UserConfigMapping(BaseModel):
    '''
    Used to map server names to config uids for a certain user.
    '''
    name: str
    config_uid: str

class User(BaseModel):
    '''
    Data about a user. `servers` maps `ServerConfigInDB.name` to
    `ServerConfigInDB.uid`.
    '''
    username: str
    servers: list[UserConfigMapping] = list()

class UserInDB(User):
    '''
    Additional information about a user that is hidden in the DB.
    '''
    hashed_password: str
