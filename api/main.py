'''
Main file for the FastAPI backend.
'''

from fastapi import FastAPI
from api.routes import auth, users, config, bot

app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/users')
app.include_router(config.router, prefix='/config')
app.include_router(bot.router, prefix='/bot')
