from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client: AsyncIOMotorClient = None

# Create the url for mongodb connection, from .env variables
def create_mdb_url():
    user = os.environ.get("MDB_USER", "")
    pw = os.environ.get("MDB_PW","")
    host = os.environ.get("MDB_HOST")
    port = os.environ.get("MDB_PORT")
    return f"mongodb://{user}:{pw}@{host}:{port}"

# Return the db cursor, creating first if doesn't exist
def get_database():
    global client
    if client is None:
        client = AsyncIOMotorClient(create_mdb_url())
    return client.kitchen

# Initialize the database, initializing collections that don't currently exist
async def init_db():
    db = get_database()
    collection_names = ["recipes"]

    existing_names = await db.list_collection_names()
    for name in collection_names:
        if name not in existing_names:
            await db.create_collection(name)

# Close the database connection
async def close_db():
    global client
    if client is not None:
        client.close()
