from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class Recipe(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5)
    ingredients: str = Field(..., min_length=5)
    instructions: str = Field(..., min_length=5)
    image_url: Optional[HttpUrl]