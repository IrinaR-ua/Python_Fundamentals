# user_interaction.py
import sys
from mysql_connector import keyword_find, genre_year_find, display_genres
from log_writer import log_a_search
from formatter import print_results, print_top5_most_popular_searches, print_last_5_unique_searches
from log_stats import get_top5_most_popular_searches, get_last_5_unique_searches

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def pick_menu_option() -> str:
    """
    Отображает главное меню и возвращает выбор пользователя.
    :return: Номер выбранного пункта меню.
    """
    console = Console()
    
    # Создаем красивый заголовок с панелью
    title = Text("FILM SEARCH APP - SAKILA -", style="bold cyan")
    panel = Panel(title, title_align="center", border_style="blue")
    console.print(panel)
    
    # Выводим меню с эмоджи и стилями
    console.print("\n[bold green]📋  Выберите действие:[/bold green]")
    console.print("   [yellow]➤[/yellow]  [bold]1.[/bold] Search films by keyword")
    console.print("   [yellow]➤[/yellow]  [bold]2.[/bold] Search films by genre and year")
    console.print("   [yellow]➤[/yellow]  [bold]3.[/bold] View top 5 popular searches")
    console.print("   [yellow]➤[/yellow]  [bold]4.[/bold] View last 5 unique searches")
    console.print("   [yellow]➤[/yellow]  [bold]5.[/bold] Exit")
    
    # Запрос ввода с подсказкой
    return input("\n Choose an option (1-5): ").strip()


# Функция для обработки поиска по ключевому слову (choice == 1)
def handle_search_by_keyword() -> None:
    """
    Обрабатывает поиск фильмов по ключевому слову: ввод, проверка, поиск, логирование и вывод.
    """
    try:
        keyword = input("👉 Enter a keyword (part of film title): ").strip()
        if not keyword:
            print("❌ Keyword cannot be empty.")
            return  # Выходим из функции, если ошибка

        result = keyword_find(keyword)  # Вызываем поиск
        log_a_search("keyword", {"keyword": keyword}, len(result))  # Логируем
        print_results(result, search_type="keyword")  # Печатаем результаты с типом
    except Exception as e:
        print(f"❌ Error during keyword search: {e}")


# Функция для обработки поиска по жанру и году (choice == 2)
def handle_search_by_genre_and_year() -> None:
    """
    Обрабатывает поиск фильмов по жанру и году: показ жанров, ввод, проверка, поиск, логирование и вывод.
    """
    try:
        # Показываем список жанров (теперь через отдельную функцию)
        display_genres()

        category_id = input("Enter genre ID: ").strip()
        year_input = input("Enter year or range (e.g. 2005 or 1990-2025): ").strip()

        if not category_id or not year_input:
            print("Genre ID and year input cannot be empty.")
            return  # Выходим из функции, если ошибка

        try:
            if "-" in year_input:
                year_start, year_end = map(int, year_input.split("-"))
            else:
                year_start = year_end = int(year_input)
        except ValueError:
            print("❌ Invalid year input. Please use digits (e.g., 2005) or range (e.g., 2000-2010).")
            return  # Выходим из функции, если ошибка

        result = genre_year_find(category_id, year_start, year_end)  # Вызываем поиск
        log_a_search("genre_year",
                     {"category_id": category_id, "year_start": year_start, "year_end": year_end},
                     len(result))  # Логируем
        print_results(result, search_type="genre_year")  # Печатаем результаты с типом
    except Exception as e:
        print(f"❌ Error during genre and year search: {e}")


def user_interaction_loop() -> None:
    """
    Основной цикл взаимодействия с пользователем.
    """
    while True:
        try:
            choice = pick_menu_option()

            if choice == "1":
                # вызываем функцию 
                handle_search_by_keyword()

            elif choice == "2":
                # вызываем функцию 
                handle_search_by_genre_and_year()
                
            elif choice == "3":
                try:
                    top5 = get_top5_most_popular_searches()
                    print_top5_most_popular_searches(top5)
                except Exception as e:
                    print(f"❌ Error fetching top 5 searches: {e}")              

            elif choice == "4":
                try:
                    last5 = get_last_5_unique_searches()
                    print_last_5_unique_searches(last5)
                except Exception as e:
                    print(f"❌ Error fetching last 5 searches: {e}")           

            elif choice == "5":
                print("👋 Goodbye!")
                break  # Выходим из цикла, без sys.exit()

            else:
                print("❌ Invalid option, please choose 1–5.")

        except KeyboardInterrupt:
            print("\n🏁  Program stopped by user.")
            sys.exit()
        except Exception as e:
            print(f"Unexpected error: {e}")