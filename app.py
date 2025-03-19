from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Movie Model Class
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    watched = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Movie id={self.id} title={self.title} watched={self.watched} added_at={self.added_at}>'

# Create the database and table with initial movies
with app.app_context():
    db.create_all()
    initial_movies = ['Titanic', 'Labyrinth', 'Gone with the Wind', 'Terminator', 'Blade Runner', 'Aliens']
    for movie_title in initial_movies:
        if not Movie.query.filter_by(title=movie_title).first():
            db.session.add(Movie(title=movie_title))
    db.session.commit()

# Home route to display movie checklist
@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.added_at.desc()).all()
    return render_template('index.html', movies=movies)

# Add a new movie
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_movie = Movie(title=title)
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('index'))

# Mark a movie as watched/unwatched
@app.route('/toggle/<int:movie_id>')
def toggle(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.watched = not movie.watched
    db.session.commit()
    return redirect(url_for('index'))

# Delete a movie
@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
