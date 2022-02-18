import sqlite3

__all__ = ['search_title']


def search_title(title):
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    found_result = ['Фильм не найден :(']
    search_title_query = ("""
    SELECT title, country, release_year, listed_in, description
    FROM netflix
    ORDER BY release_year DESC """)
    cursor.execute(search_title_query)
    results = cursor.fetchall()
    connection.close()
    for result in results:
        if title.lower() in result[0].lower():
            found_result = result
            break
    return found_result
