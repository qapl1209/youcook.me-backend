from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import os
from dotenv import load_dotenv
# from db import db, get_database

load_dotenv()

app = FastAPI(title = "youcook.me API", version = "0.1.0")

@app.get('/')
def root():
    return {"msg": "Hello World!"}

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "False").lower() == 'true'

    uvicorn.run("main:app", host=host, port=port, reload=debug)