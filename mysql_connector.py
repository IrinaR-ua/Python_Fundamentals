# mysql_connector

import pymysql
from config import mysql_config

def keyword_find(keyword: str) -> list:
    """
    Выполняет поиск фильмов по части названия (ключевому слову).
    :param keyword: Строка для поиска в названии фильма.
    :return: Список кортежей с результатами запроса (id, title, year, rate).
    """
    sql = """
        SELECT 
            film.film_id,
            film.title,
            film.release_year,
            category.name AS genre,
            film.rental_rate
        FROM film
        LEFT JOIN film_category ON film.film_id = film_category.film_id
        LEFT JOIN category ON film_category.category_id = category.category_id
        WHERE film.title LIKE %s
        ORDER BY film.release_year DESC, film.title;
    """
    try:
        with pymysql.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (f"%{keyword}%",))
                return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error during keyword search: {e}")
        return []


def genre_year_find(category_id: str, year_start: int, year_end: int) -> list:
    """
    Выполняет поиск фильмов по жанру и диапазону годов.
    :param category_id: ID категории (жанра).
    :param year_start: Начальный год диапазона.
    :param year_end: Конечный год диапазона.
    :return: Список фильмов, соответствующих запросу.
    """
    sql = """
        SELECT 
            film.film_id,
            film.title,
            film.release_year,
            category.name AS genre
        FROM film
        LEFT JOIN film_category 
            ON film.film_id = film_category.film_id
        LEFT JOIN category 
            ON film_category.category_id = category.category_id
        WHERE 
            category.category_id = %s
            AND (film.release_year BETWEEN %s AND %s OR film.release_year = %s)
        ORDER BY film.release_year DESC, film.title;
    """
    try:
        with pymysql.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (category_id, year_start, year_end, year_start))
                return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error during genre/year search: {e}")
        return []


def display_genres() -> None:
    """
    Подключается к базе данных, получает список жанров и печатает их.
    """
    try:
        with pymysql.connect(**mysql_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT category_id, name FROM category ORDER BY category_id;")
                genres = cursor.fetchall()
                for g in genres:
                    print(f"{g[0]} - {g[1]}")
    except pymysql.MySQLError as e:
        print(f"❌ Database error while fetching genres: {e}")
    except Exception as e:
        print(f"❌ Unexpected error while displaying genres: {e}")