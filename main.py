import sqlite3

from flask import Flask, render_template

from functions import *


app = Flask('__name__')


@app.route('/movie/<title>')
def title_page(title):
    search_title(title)
    return render_template('movie_title_page.html', movie=search_title(title))

@app.route('/movie/year/to/year')
def year_to_year_page():
    pass



if __name__ == '__main__':
    app.run()
