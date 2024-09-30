from fastapi import Body, HTTPException, status
from fastapi.responses import Response
from typing import Optional
from models import Recipe, RecipeCollection
from bson import ObjectId
from db import get_database


class RecipeCRUD:
    def __init__(self, db):
        self.collection = db.get_collection("recipes")
    
    """
        Insert a new recipe record.

        A unique `id` will be created and provided in the response.
    """
    async def create_recipe(self, recipe: Recipe = Body(...)) -> Recipe:
        new_recipe = await self.collection.insert_one(
            recipe.model_dump(by_alias=True, exclude=["id"])
        )
        created_recipe = await self.collection.find_one(
            {"_id": new_recipe.inserted_id}
        )
        return created_recipe


    """
        Returns a list of recipes.

        The response is unpaginated and limited to 1000 results.
    """
    async def list_recipes(self) -> RecipeCollection:
        return RecipeCollection(recipes = await self.collection.find().to_list(1000))


    """
        Get one recipe by `id`.
    """
    async def get_recipe(self, id: str) -> Optional[Recipe]:
        if (
            recipe := await self.collection.find_one({"_id": ObjectId(id)})
        ) is not None:
            return recipe
        
        raise HTTPException(status_code=404, detail=f"Recipe not found with id={id} ")
    

    """
        Remove one recipe by `id`.
    """
    async def delete_recipe(self, id: str):
        delete_result = await self.collection.delete_one({"_id":ObjectId(id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=404, detail=f"Recipe not found with id={id} ")

recipe_crud = RecipeCRUD(get_database())