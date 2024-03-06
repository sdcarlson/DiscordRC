'''
Main file for the FastAPI backend.
'''

from fastapi import FastAPI
import api.documentation
from api.routes import auth, users, config, bot

app = FastAPI(
    title='DiscordRC',
    description='This is the documentation for the backend API of DiscordRC.'
)

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/users')
app.include_router(config.router, prefix='/config')
app.include_router(bot.router, prefix='/bot')

api.documentation.generate(app, 'documentation/api.html')
