'''
Main file for backend testing.
'''

# import asyncio
# from fastapi.security import  OAuth2PasswordRequestForm
# from api.db import Database
# db = Database('test-db')
#
# # pylint: disable=wrong-import-position
# from api.routes import auth, users, config, bot
# import models
#
# # pylint: disable=missing-function-docstring
# async def main():
#     cred = OAuth2PasswordRequestForm(username='alice', password='password')
#     token: models.Token = await auth.signup(cred)
#     alice_in_db: models.UserInDB = await auth.get_current_user_from_db(token)
#
# if __name__ == '__main__':
#     asyncio.run(main())

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.db import Database
db = Database('test-db')

# pylint: disable=wrong-import-position
from api.routes import auth, users, config, bot
from api.tests import clean_tests

app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/users')
app.include_router(config.router, prefix='/config')
app.include_router(bot.router, prefix='/bot')
app.include_router(clean_tests.router, prefix='/clean')

client = TestClient(app)

def test_add_user():
    cred = {'username': 'alice', 'password': 'password'}
    response = client.post('/auth/signup', data=cred)
    assert response.status_code == 200

def test_clean():
    response = client.delete('/clean')
    assert response.status_code == 200
