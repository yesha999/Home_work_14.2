import json
import sqlite3

__all__ = ['search_title', 'search_years', 'search_rating', 'search_genre']


def search_title(title):
    """Результат - один фильм для @app.route('/movie/<title>')"""
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


def search_years(year_1, year_2):
    """Результат - список словарей фильмов между указанными годами"""
    year_1 = int(year_1)
    year_2 = int(year_2)
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    found_results = []
    search_years_query = ("""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN ? AND ?
        ORDER BY release_year DESC
        LIMIT 100
        """)
    cursor.execute(search_years_query, (year_1, year_2))
    results = cursor.fetchall()
    connection.close()
    for result in results:
        found_result = {'title': result[0], 'release_year': result[1]}
        found_results.append(found_result)
    return found_results


def search_rating(rating):
    """Результат - список словарей фильмов с необходимым рейтингом"""
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    found_results = []
    search_rating_query = ("""
        SELECT title, rating, description
        FROM netflix 
        WHERE rating != '' AND (rating=? OR rating=? OR rating=?)
        LIMIT 100
        """)
    if rating == 'children':
        cursor.execute(search_rating_query, ('G', 'G', 'G'))  # ну костыльно и шо :)
        results = cursor.fetchall()
    elif rating == 'adult':
        cursor.execute(search_rating_query, ('R', 'RC-17', 'R'))
        results = cursor.fetchall()
    elif rating == 'family':
        cursor.execute(search_rating_query, ('G', 'PG', 'PG-13'))
        results = cursor.fetchall()
    else:
        results = []
    connection.close()

    for result in results:
        found_result = {'title': result[0], 'rating': result[1], 'description': result[2]}
        found_results.append(found_result)

    return found_results


def search_genre(genre):
    """Результат - список словарей фильмов, содержащих необходмый жанр"""
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    found_results = []
    search_genre_query = ("""
    SELECT title, description, release_year
    FROM netflix
    WHERE listed_in LIKE '%'||?||'%'
    ORDER BY release_year DESC
    LIMIT 10
    """)
    cursor.execute(search_genre_query, (genre,))
    results = cursor.fetchall()
    connection.close()
    for result in results:
        found_result = {'title': result[0], 'description': result[1], }
        found_results.append(found_result)
    return found_results


def step_five_function(actor_1, actor_2):
    """Напишите функцию, которая получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    Для этого задания не требуется создавать вьюшку
    В качестве теста можно передать: Rose McIver и Ben Lamb, Jack Black и Dustin Hoffman."""
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    search_actor_query = ("""
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE '%'||?||'%' AND "cast" LIKE '%'||?||'%'
        """)
    cursor.execute(search_actor_query, (actor_1, actor_2))
    results = cursor.fetchall()
    connection.close()
    actors = []
    for result in results:
        for actor_cast in result:
            actor_cast_list = actor_cast.split(', ')
            for actor in actor_cast_list:
                if actor != actor_1 and actor != actor_2:
                    actors.append(actor)
    actor_friends = [actor for actor in set(actors) if actors.count(actor) > 2]
    return actor_friends


print(step_five_function('Rose McIver', 'Ben Lamb'))


def step_six_sql(type, release_year, listed_in):
    """Напишите функцию, с помощью которой можно будет
     передавать тип картины (фильм или сериал), год выпуска и ее жанр и
     получать на выходе список названий картин с их описаниями в JSON."""
    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    found_results = []
    search_all_query = ("""
    SELECT title, description
    FROM netflix
    WHERE type LIKE '%'||?||'%' AND release_year LIKE '%'||?||'%' AND listed_in LIKE '%'||?||'%'
    """)
    cursor.execute(search_all_query, (type, release_year, listed_in))
    results = cursor.fetchall()
    connection.close()
    for result in results:
        found_result = {'title': result[0], 'description': result[1]}
        found_results.append(found_result)
    with open('step_6.json', 'w') as file:
        json.dump(found_results, file)
    return found_results
