from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# Constants for hashing/tokens

SECRET_KEY = 'ac000a43df3fddd51817ea851e864b9a4b30888c27d0d47b32281ad751aec53f'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# This is just a fake database because idk how to use SQLAlchemy

fake_users_db = {
    'alice': {
        'username': 'alice',
        'configs': {
            'testserver': {
                'name': 'testserver',
                'channels': {
                    'Server Information': [ {'name': 'Announcements'} ],
                    'General': [ {'name': 'Chat'}, {'name': 'Photos'} ],
                },
            }
        },
        'hashed_password': '$2a$12$AVr5uFxaUKTHn4UyqJBsGu2luHwgnVM0nhOaMQqP9Bs/DQblbrmYG',  # password1
    },
}


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


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

app = FastAPI()


# Helper functions

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str) -> User | None:
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise unauthorized_exception
        token_data = TokenData(username=str(username))
    except JWTError:
        raise unauthorized_exception
    user = get_user(fake_users_db, username=str(token_data.username))
    if user is None:
        raise unauthorized_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user

async def get_token(username: str, password: str) -> Token:
    user = authenticate_user(fake_users_db, username, password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')

### AUTH ENDPOINTS #############################################################

@app.post('/auth/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    '''
    To use this endpoint, pass in `username` and `password` as form data.
    If login is successful, we return a bearer token.
    '''
    return await get_token(form_data.username, form_data.password)

@app.post('/auth/signup')
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    '''
    To use this endpoint, pass in `username` and `password` as form data.
    If signup is successful, we return a bearer token.
    '''
    username, password = form_data.username, form_data.password
    if username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User `{username}` already exists',
        )
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        'username': username,
        'hashed_password': hashed_password,
    }
    return await get_token(username, password)

### USER ENDPOINTS #############################################################

@app.get('/users/me', response_model=User)
async def get_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    '''
    Returns information about the current user based on the user's login token.
    '''
    return current_user

### CONFIG ENDPOINTS ###########################################################

@app.get('/config/export', response_model=ServerConfig)
async def export_config(
    current_user: Annotated[User, Depends(get_current_active_user)],
    server_name: str
) -> ServerConfig:
    '''
    Returns a server config as json.
    '''
    if server_name not in current_user.configs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User does not have server config `{server_name}`'
        )
    return fake_users_db[current_user.username]['configs'][server_name]

@app.post('/config/import')
async def import_config(
    current_user: Annotated[User, Depends(get_current_user)],
    config: ServerConfig
):
    '''
    Sets a server config for the current user.
    '''
    server_name = config.name
    fake_users_db[current_user.username]['configs'][server_name] = config.model_dump()
    return 'Success'
