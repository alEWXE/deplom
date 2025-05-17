import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from typing import Optional, List

class RecipeModel(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5)
    ingredients: str = Field(..., min_length=5)
    instructions: str = Field(..., min_length=5)
    image_url: Optional[HttpUrl]

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.recipes_db
collection = db.recipes

sample_recipes = [
    {
        "title": "Плов",
        "description": "Ароматный узбекский плов.",
        "ingredients": "Рис, мясо, морковь, лук, специи",
        "instructions": "Обжарить мясо, добавить овощи, варить с рисом.",
        "image_url": "https://example.com/plov.jpg"
    },
    {
        "title": "Борщ",
        "description": "Традиционный украинский суп.",
        "ingredients": "Свекла, капуста, картошка, мясо",
        "instructions": "Все сварить на медленном огне.",
        "image_url": "https://example.com/borscht.jpg"
    },
    {
        "title": "Оливье",
        "description": "Популярный новогодний салат.",
        "ingredients": "Картошка, морковь, колбаса, горошек, майонез",
        "instructions": "Все отварить, нарезать и перемешать с майонезом.",
        "image_url": "https://menunedeli.ru/wp-content/uploads/2023/08/6C061981-26CA-4FD4-BE9A-F8D63C0206C7-467x350.jpeg1933"
    }
]

async def seed():
    await collection.delete_many({})
    valid_recipes: List[dict] = []

    for recipe in sample_recipes:
        try:
            validated = RecipeModel(**recipe)
            recipe_dict = validated.dict()
            if recipe_dict.get("image_url") is not None:
                recipe_dict["image_url"] = str(recipe_dict["image_url"])
            valid_recipes.append(recipe_dict)
        except ValidationError as e:
            print(f"[!] Ошибка валидации: {e}")

    if valid_recipes:
        await collection.insert_many(valid_recipes)
        print(f"[✓] Добавлено {len(valid_recipes)} рецептов.")
    else:
        print("[!] Нет валидных рецептов.")

if __name__ == "__main__":
    asyncio.run(seed())