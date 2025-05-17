from pymongo import MongoClient
from datetime import datetime

# Данные для подключения (измените при необходимости)
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "recipe_site"
COLLECTION_NAME = "recipes"

# Тестовые рецепты
sample_recipes = [
    {
        "title": "Спагетти Карбонара",
        "ingredients": [
            "спагетти 200г",
            "бекон 150г",
            "яйца 3 шт",
            "пармезан 50г"
        ],
        "description": "1. Отварите пасту\n2. Обжарьте бекон\n3. Смешайте с соусом",
        "created_at": datetime.utcnow()
    },
    {
        "title": "Салат Цезарь",
        "ingredients": [
            "куриное филе 300г",
            "листья салата 1 пучок",
            "сухарики 100г",
            "соус Цезарь"
        ],
        "description": "1. Обжарьте курицу\n2. Соберите слои салата\n3. Полейте соусом",
        "created_at": datetime.utcnow()
    },
    {
        "title": "Шоколадный торт",
        "ingredients": [
            "мука 200г",
            "какао 50г",
            "яйца 4 шт",
            "сахар 150г"
        ],
        "description": "1. Смешайте сухие ингредиенты\n2. Добавьте яйца\n3. Выпекайте 40 минут",
        "created_at": datetime.utcnow()
    },
    {
        "title": "Омлет с овощами",
        "ingredients": [
            "яйца 5 шт",
            "помидоры 2 шт",
            "лук 1 шт",
            "перец болгарский 1 шт"
        ],
        "description": "1. Нарежьте овощи\n2. Взбейте яйца\n3. Жарьте на сковороде 10 минут",
        "created_at": datetime.utcnow()
    },
    {
        "title": "Тыквенный суп",
        "ingredients": [
            "тыква 500г",
            "лук 1 шт",
            "сливки 200мл",
            "овощной бульон 1л"
        ],
        "description": "1. Обжарьте овощи\n2. Добавьте бульон\n3. Пюрируйте блендером",
        "created_at": datetime.utcnow()
    }
]

def insert_sample_recipes():
    try:
        # Подключение к MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Вставка данных
        result = collection.insert_many(sample_recipes)
        
        print(f"Успешно добавлено {len(result.inserted_ids)} рецептов!")
        print("ID добавленных рецептов:", result.inserted_ids)
        
    except Exception as e:
        print("Ошибка при добавлении рецептов:", str(e))
    finally:
        client.close()

if __name__ == "__main__":
    insert_sample_recipes()