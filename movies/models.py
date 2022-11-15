from .. import db


movie_genre = db.Table(
    "movie_genre",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
)


class Movies(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    imdb_score = db.Column(db.Float)
    director = db.Column(db.String(100))
    popularity = db.Column(db.Float)

    genres = db.relationship("Genre", secondary=movie_genre, backref="movies")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "imdb_score": self.imdb_score,
            "director": self.director,
            "popularity": self.popularity,
            "genres": [genre.name for genre in self.genres],
        }


class Genre(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    def to_dict(self):
        return {"id": self.id, "name": self.name}
