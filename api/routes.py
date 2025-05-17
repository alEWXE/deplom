from fastapi import APIRouter, Request, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase,AsyncIOMotorClient
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_mongo_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    return client["recipe_site"]

@router.get("/")
async def show_all_recipes(
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    try:
        cursor = db.recipes.find({}) 
        recipes = []
        
        async for recipe in cursor:
            recipe["_id"] = str(recipe["_id"])
            recipes.append(recipe)
            
        return templates.TemplateResponse(
            "recepie_page.html",
            {"request": request, "recipes": recipes}
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")  
        return templates.TemplateResponse(
            "recepie_page.html",
            {"request": request, "error": str(e)}
        )