# log_stats.py
from pymongo import MongoClient
from config import mongodb_config

def get_top5_most_popular_searches() -> list:
    """
    Возвращает 5 самых популярных поисковых запросов из MongoDB.
    :return: Список документов MongoDB с данными о запросах.
    """
    pipeline_top5 = [
        {
            "$group": {
                "_id": {
                    "keyword": "$params.keyword",
                    "category_id": "$params.category_id"
                },
                "count_query": {"$sum": 1}
            }
        },
        {"$sort": {"count_query": -1}},
        {"$limit": 5}
    ]

    try:
        with MongoClient(**mongodb_config) as client:
            db = client["ich_edit"]
            collection = db["final_project_230525-dam_RomanovaIrin"]
            return list(collection.aggregate(pipeline_top5))
    except Exception as e:
        print(f"Error fetching top 5 popular searches: {e}")
        return []


def get_last_5_unique_searches() -> list:
    """Возвращает последние 5 уникальных запросов по ключевому слову или жанру."""
    pipeline_last_5 = [
        {"$sort": {"timestamp": -1}},
        {"$addFields": {
            "unique_key": {
                "$cond": {
                    "if": {"$eq": ["$search_type", "keyword"]},
                    "then": "$params.keyword",
                    "else": "$params.category_id"
                }
            }
        }},
        {"$group": {
            "_id": "$unique_key",
            "last_search_time": {"$first": "$timestamp"},
            "search_type": {"$first": "$search_type"},
            "search_params": {"$first": "$params"},
            "results_count": {"$first": "$results_count"}
        }},
        {"$sort": {"last_search_time": -1}},  # Сортировка по времени после группировки
        {"$limit": 5}
    ]
    try:
        with MongoClient(**mongodb_config) as client:
            db = client["ich_edit"]
            coll = db["final_project_230525-dam_RomanovaIrin"]
            return list(coll.aggregate(pipeline_last_5))
    except Exception as e:
        print(f"Error fetching last 5 searches: {e}")
        return []