from typing import Optional, Set, List
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


"""
Container for a single recipe. 

recipe: {
    id: String
    name: String
    preptime (min's): int
    ingredients: set(String) -> String[] in Mongo
    instructions: String
    tags: set(String) -> String[] in Mongo
}
"""
class Recipe(BaseModel):

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    preptime: int = Field(...)
    ingredients: Set[str] = Field(...)
    instructions: str = Field(...)
    tags: Set[str] = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Fried Rice",
                "preptime": 4,
                "ingredients": {"Oil, Rice, Egg"},
                "instructions": "1. Put the oil and heat in the pan until glistening. \n 2. Cook your scrambled egg in the pan. \n 3. Add your rice and serve when thoroughly mixed.",
                "tags": {"Vegan, Gluen-free"},
            }
        }
    )

    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name})>"


"""
    A container holding a list of `Recipe` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)

    idk, just copied from https://github.com/mongodb-developer/mongodb-with-fastapi/blob/master/app.py#L9
"""
class RecipeCollection(BaseModel):
    recipes: List[Recipe]