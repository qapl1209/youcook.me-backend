from fastapi import FastAPI, Body, HTTPException
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from db import get_database, init_db, close_db
from crud import RecipeCRUD
from models import Recipe

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(title="youcook.me API", version="0.1.0", lifespan=lifespan)

db = get_database()
recipe_crud = RecipeCRUD(db)

@app.get('/')
async def root():
    collections = await db.list_collection_names()
    return {"collections": collections}

@app.post('/recipes', response_model=Recipe)
async def create_recipe(recipe: Recipe = Body(...)):
    try:
        created_recipe = await recipe_crud.create_recipe(recipe)
        return created_recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/recipes')
async def get_all_recipes():
    try: 
        recipe_collection = await recipe_crud.list_recipes()
        return recipe_collection
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "False").lower() == 'true'

    uvicorn.run("main:app", host=host, port=port, reload=debug)