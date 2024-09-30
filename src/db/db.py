from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_mdb_url():
    with os.environ as env:
        user = env.get("MDB_USER", "")
        pw = env.get("MDB_PW","")
        host = env.get("MDB_HOST")
        port = env.get("MDB_PORT")
    return f"mongodb://{user}:{pw}@{host}:{port}"

client = AsyncIOMotorClient(create_mdb_url())
db = client.kitchen

def get_database():
    return db