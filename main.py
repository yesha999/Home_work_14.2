from flask import Flask, render_template, request, redirect

from functions import *

app = Flask('__name__')

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/movie/<title>')
def title_page(title):
    search_title(title)
    return render_template('movie_title_page.html', movie=search_title(title))


@app.route('/movie/year/to/year', methods=["GET"])
def year_to_year_form():
    return render_template('year_to_year_form.html')


@app.route('/movie/year/to/year', methods=["POST"])
def year_to_year_page():
    year_1 = request.values.get("year_1")
    year_2 = request.values.get("year_2")
    if year_1.isdigit() and year_2.isdigit():
        found_results = search_years(year_1, year_2)
        return render_template("/year_to_year_page.html", year_1=year_1, year_2=year_2, movies=found_results)
    return redirect("/movie/year/to/year")


@app.route('/rating')
def rating_page():
    return render_template('rating_choice.html')


@app.route('/rating/<rating>')
def rating_page_chosen(rating):
    movies = search_rating(rating)
    movies_count = len(movies)
    if rating == 'children':
        header = 'для детей'
    elif rating == 'adult':
        header = 'для взрослых'
    elif rating == 'family':
        header = 'для семейного просмотра'
    else:
        return redirect("/rating")
    return render_template('rating_page_chosen.html', movies=movies,
                           header=header, movies_count=movies_count)


@app.route('/genre/<genre>')
def genre_page(genre):
    movies = search_genre(genre)
    movies_count = len(movies)
    return render_template('genre_page.html', movies=movies,
                           movies_count=movies_count, genre=genre)


if __name__ == '__main__':
    app.run()
