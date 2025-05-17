from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from db.mongo import recipes_collection
from bson.objectid import ObjectId

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/register")
async def read_root(request: Request):
    cursor = recipes_collection.find()
    recipes = []
    async for recipe in cursor:
        recipe["_id"] = str(recipe["_id"])
        recipes.append(recipe)
    return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})