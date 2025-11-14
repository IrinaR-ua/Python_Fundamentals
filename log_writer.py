# логирование В MongoDB

from pymongo import MongoClient
from datetime import datetime
from config import mongodb_config

def get_mongo_collection():
    """
    Подключается к MongoDB и возвращает коллекцию для логирования поисковых запросов.
    """
    try:
        client = MongoClient(**mongodb_config)
        db = client["ich_edit"]
        collection = db["final_project_230525-dam_RomanovaIrin"]
        return collection
    except Exception as e:
        print("❌ Ошибка подключения к MongoDB:", e)
        raise


def log_a_search(search_type: str, params: dict, results_count: int) -> None:
    """
    Сохраняет один лог в MongoDB.    
    Пример документа:
    {
        "timestamp": "2025-05-01T15:34:00",
        "search_type": "keyword",
        "params": {"keyword": "matrix"},
        "results_count": 3
    }
    """
    try:
        collection = get_mongo_collection()

        # Формируем данные для записи
        log_data = {
            "timestamp": datetime.now(),                 # текущее время
            "search_type": search_type,                  # тип запроса
            "params": params,                            # параметры поиска
            "results_count": results_count               # сколько найдено фильмов
        }

        # Записываем в MongoDB
        collection.insert_one(log_data)
        print("Search log saved to MongoDB")

    except Exception as e:
        print("Error while saving log:", e)