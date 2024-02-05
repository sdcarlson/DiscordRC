from pydantic import BaseModel

# Pydantic models

class Channel(BaseModel):
    '''
    A single text channel. Later, we might need to store info about roles, etc.
    '''
    name: str

class ServerConfig(BaseModel):
    '''
    A configuration for a server. `channels` maps channel category names to
    lists of channels.
    '''
    name: str
    channels: dict[str, list[Channel]] = dict()

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
    username: str | None = None

class User(BaseModel):
    '''
    Data about a user. `configs` maps server names to `ServerConfig`s.
    '''
    username: str
    configs: dict[str, ServerConfig] = dict()

class UserInDB(User):
    '''
    Additional information about a user that is hidden in the DB.
    '''
    hashed_password: str
