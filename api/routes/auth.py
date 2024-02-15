from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

import models

SECRET_KEY = 'ac000a43df3fddd51817ea851e864b9a4b30888c27d0d47b32281ad751aec53f'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

fake_users_db = {
    'alice': {
        'username': 'alice',
        'configs': [{
            'name': 'MyServer',
            'id': 123055866,
            'roles': [
                {
                    'name': 'role1',
                    'id': 1000000022,
                    'display_separately': True,
                    'allow_mention': False,
                    'permissions': {
                        'roleperm1': True,
                        'roleperm2': False
                    }
                },
                {
                    'name': 'role2',
                    'id': 1000023022,
                    'display_separately': False,
                    'allow_mention': True,
                    'permissions': {}
                },
                {
                    'name': 'role3',
                    'id': None,
                    'display_separately': False,
                    'allow_mention': False,
                    'permissions': {}
                }
            ],
            'categories': [
                {
                    'name': 'MyCategory',
                    'id': 1000000000,
                    'permissions': {
                        'perm1': { 'role1': True, 'role3': False }
                    },
                    'text_channels': [
                    {
                        'name': 'MyTextChannel',
                        'id': None,
                        'permissions': {
                            'perm1': { 'role2': False, 'role3': True }
                        }
                    }
                    ],
                    'voice_channels': [
                    {
                        'name': 'MyVoiceChannel',
                        'id': 1111111111,
                        'permissions': {
                            'perm2': { 'role2': True, 'role3': False }
                        }
                    }
                    ]
                }
            ]
        }],
        'hashed_password': '$2a$12$AVr5uFxaUKTHn4UyqJBsGu2luHwgnVM0nhOaMQqP9Bs/DQblbrmYG',  # password1
    }
}

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
router = APIRouter()

# Helper functions

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def get_user_from_db(db, username: str) -> models.UserInDB | None:
    if username in db:
        user_dict = db[username]
        return models.UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str) -> models.User | None:
    user = get_user_from_db(fake_db, username)
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


async def get_current_user_from_db(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> models.UserInDB:
    '''
    Don't use this function directly, because it includes DB data
    (i.e. the hashed password). Instead, use `get_current_user`.
    '''
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
        token_data = models.TokenData(username=str(username))
    except JWTError:
        raise unauthorized_exception

    user = get_user_from_db(fake_users_db, username=str(token_data.username))
    if user is None:
        raise unauthorized_exception
    return user

async def get_current_user(
    current_user: Annotated[models.User, Depends(get_current_user_from_db)]
) -> models.User:
    '''
    Returns the current user based on the oauth token as a `models.User`.
    '''
    return current_user

async def get_token(username: str, password: str) -> models.Token:
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
    return models.Token(access_token=access_token, token_type='bearer')

### AUTH ENDPOINTS #############################################################

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> models.Token:
    '''
    To use this endpoint, pass in `username` and `password` as form data.
    If login is successful, we return a bearer token.
    '''
    return await get_token(form_data.username, form_data.password)

@router.post('/signup')
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> models.Token:
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
    fake_users_db[username] = models.UserInDB(**{
        'username': username,
        'hashed_password': hashed_password,
    }).model_dump()
    return await get_token(username, password)