'''
Main file for the FastAPI backend.
'''

try:
    import api.documentation
except ModuleNotFoundError:
    ERROR_MSG = \
'''\033[91mERROR\033[0m: You didn't run this correctly. While you're inside of the `api/`
directory, you should run:

sh -c 'cd .. && uvicorn api.main:app --reload'

In PR #33, I changed all the import paths so that `DiscordRC/` is the root
directory. This lets us use the code in `DiscordBot/`. For more information,
see `api/README.md` or message me (biquando) on Discord.'''
    print(ERROR_MSG)
    exit(1)

from fastapi import FastAPI
from api.db import Database
db = Database()

# pylint: disable=wrong-import-position
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
