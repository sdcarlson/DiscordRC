from fastapi import FastAPI
from endpoints import auth, users, config

app = FastAPI()

app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/users')
app.include_router(config.router, prefix='/config')
