# formatter.py
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
from datetime import datetime

def print_results(results: list, search_type: str = "general") -> None:
    """
    Выводит результаты поиска в виде красивой таблицы с использованием Rich.
    Поддерживает пагинацию по 10 фильмов.
    :param results: Список кортежей с результатами.
    :param search_type: Тип поиска ("keyword" или "genre_year") для определения столбцов.
    """
    console = Console()
    
    if not results:
        console.print("❌ No films found.", style="bold red")
        return

    # Определяем заголовки и столбцы в зависимости от типа поиска
    if search_type == "keyword":
        headers = ["ID", "Title", "Year", "Genre", "Rate"]
        columns = [0, 1, 2, 3, 4]  # Индексы в кортеже
    elif search_type == "genre_year":
        headers = ["ID", "Title", "Year", "Genre"]
        columns = [0, 1, 2, 3]
    else:
        headers = ["Data"]
        columns = list(range(len(results[0])))  # Для общего случая

    index = 0
    while index < len(results):
        next_slice = results[index:index + 10]
        
        # Создаем таблицу
        table = Table(title=f"🎥 Search Results (Page {index // 10 + 1})", box=ROUNDED, title_style="bold cyan")
        for header in headers:
            table.add_column(header, style="cyan", justify="center")
        
        # Добавляем строки
        for row in next_slice:
            table.add_row(*[str(row[col]) for col in columns])
        
        # Выводим таблицу
        console.print(table)
        
        index += 10
        if index >= len(results):
            console.print("\n🏁 End of results.", style="bold green")
            break
        
        try:
            if input("Show next 10? (y/n): ").strip().lower() != "y":
                break
        except KeyboardInterrupt:
            console.print("\n🏁 Interrupted by user.", style="bold yellow")
            break


def print_top5_most_popular_searches(searches: list) -> None:
    """Печатает 5 самых популярных поисковых запросов в понятном формате."""
    console = Console()
    
    table = Table(title="🏆 Top 5 Popular Searches", box=ROUNDED, title_style="bold cyan")
    table.add_column("Search Type", style="cyan", justify="left")
    table.add_column("Details", style="cyan", justify="left")
    table.add_column("Times Searched", style="cyan", justify="center")
    
    if not searches:
        console.print("❌ No searches yet.", style="bold red")
        return
    
    for log in searches:
        search_id = log["_id"]
        count = log["count_query"]
        
        # Определяем тип поиска и детали
        if search_id.get("keyword"):
            search_type = "Keyword Search"
            details = f"Keyword: {search_id['keyword']}"
        elif search_id.get("category_id"):
            search_type = "Genre Search"
            details = f"Genre ID: {search_id['category_id']}"
        else:
            search_type = "Unknown"
            details = "N/A"
        
        table.add_row(search_type, details, str(count))
    
    console.print(table)


def print_last_5_unique_searches(searches: list) -> None:
    """Печатает последние 5 уникальных поисковых запросов в понятном формате."""
    console = Console()
    
    table = Table(title="📅 Last 5 Unique Searches", box=ROUNDED, title_style="bold cyan")
    table.add_column("Time", style="cyan", justify="left")
    table.add_column("Search Type", style="cyan", justify="center")
    table.add_column("Details", style="cyan", justify="left")
    table.add_column("Results Found", style="cyan", justify="center")
    
    if not searches:
        console.print("❌ No recent searches found.", style="bold red")
        return
    
    for log in searches:
        # Преобразуем timestamp в читаемый формат
        timestamp_obj = log.get("last_search_time")
        if isinstance(timestamp_obj, datetime):
            time_str = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = str(timestamp_obj) if timestamp_obj else "N/A"
        
        search_type_raw = log.get("search_type", "N/A")
        if search_type_raw == "keyword":
            search_type = "Keyword Search"
        elif search_type_raw == "genre_year":
            search_type = "Genre & Year Search"
        else:
            search_type = search_type_raw
        
        # Разбираем params в понятный текст
        params = log.get("search_params", {})
        if search_type_raw == "keyword":
            details = f"Keyword: {log['_id']}"  # _id теперь keyword
        elif search_type_raw == "genre_year":
            year_start = params.get("year_start", "N/A")
            year_end = params.get("year_end", "N/A")
            if year_start == year_end:
                year_str = str(year_start)
            else:
                year_str = f"{year_start}-{year_end}"
            details = f"Genre ID: {log['_id']}, Year: {year_str}"  # _id теперь category_id
        else:
            details = str(params)  # На случай неизвестного типа
        
        results_count = str(log.get("results_count", 0))
        
        table.add_row(time_str, search_type, details, results_count)
    
    console.print(table)