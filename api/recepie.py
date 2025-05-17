# from fastapi import APIRouter, Request
# from fastapi.templating import Jinja2Templates
# from db.mongo import recipes_collection
# from bson.objectid import ObjectId
# from db.mongo import recipes


# templates = Jinja2Templates(directory="templates")
# router = APIRouter()

# @router.get("/recepies")
# async def show_recipes(request: Request):
#     recipes = recipes.find({})
#     return templates.TemplateResponse("index.html", {"request": request, "recipes": recipes})