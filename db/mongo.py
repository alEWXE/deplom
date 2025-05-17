from pymongo import MongoClient
from core.settings import settings

server = MongoClient(settings.MONGODB_URL, settings.MONGODB_PORT)

recipe_site = server[settings.MONGODB_DB_NAME]

recipes_collection = recipe_site[settings.MONGODB_COLLECTION_RECEPIES]


data = recipes_collection.find({})

