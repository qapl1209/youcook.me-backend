from fastapi import FastAPI
from contextlib import asynccontextmanager
# from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import os
from dotenv import load_dotenv
from db import get_database, init_db, close_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield

    await close_db()

app = FastAPI(title="youcook.me API", version="0.1.0", lifespan=lifespan)

db = get_database()

@app.get('/')
async def root():
    collections = await db.list_collection_names()
    return {"collections": collections}

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "False").lower() == 'true'

    uvicorn.run("main:app", host=host, port=port, reload=debug)