from flask import Flask, render_template
from DataMovies import MovieList
from Similarity import similar

app = Flask(__name__)

MovieList = MovieList()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/movie/<string:title>/')
def movie(title):
    sim = similar(title)
    return render_template('movie.html', t1=title, m=MovieList, s1=sim)

@app.route('/movies')
def movies():
    return render_template('movies.html', ml=MovieList)






if __name__ == '__main__':
    app.run(debug=True)

