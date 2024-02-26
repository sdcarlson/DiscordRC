# This is a demo of how to connect to MongoDB instance from FastAPI
# run FastAPI application with uvicorn main:app --reload and then navigate to http://127.0.0.1:8000/ in browser to test
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGO_URI = "mongodb://admin:2BLfv2tcQnSa@localhost:27017"
DATABASE_NAME = "db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

@app.get("/")
async def read_root():
    try:
        await db.command("ping")
        return {"message": "Connection to MongoDB successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {str(e)}")
