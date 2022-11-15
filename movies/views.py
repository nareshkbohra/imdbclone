from flask.views import MethodView
from flask import jsonify, Blueprint, request
from flask_login import login_required

from .models import Movies, Genre
from .. import db
from ..decorators import admin_check


class MovieView(MethodView):

    def get(self, id):
        movie = Movies.query.get(id)

        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        return jsonify({"movie": movie.to_dict()}), 200

    @login_required
    @admin_check
    def put(self, id):
        movie = Movies.query.get(id)

        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        if "name" in request.args:
            movie.name = request.args["name"]

        if "director" in request.args:
            movie.director = request.args["director"]

        if "popularity" in request.args:
            movie.popularity = request.args["popularity"]

        if "imdb_score" in request.args:
            movie.imdb_score = request.args["imdb_score"]

        if "genres" in request.args:
            new_genres = request.args["genres"].split(",")

            movie.genres.clear()
            for genre in new_genres:
                genre_obj = Genre.query.filter_by(name=genre).first()
                if not genre_obj:
                    genre_obj = Genre(name=genre)
                movie.genres.append(genre_obj)

        db.session.commit()

        return jsonify({"movie": movie.to_dict()}), 204

    @login_required
    @admin_check
    def delete(self, id):
        movie = Movies.query.get(id)

        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        db.session.delete(movie)

        db.session.commit()
        return jsonify({"msg": "Movie deleted successfully"}), 200


movies_blueprint = Blueprint("movies_blueprint", __name__)


@movies_blueprint.route("/search", methods=["GET"])
def search():
    required_params = ["name", "director", "popularity", "imdb_score"]

    if not any(param in request.args for param in required_params):
        return (
            jsonify(
                {
                    "error": f"Atleast one param of {', '.join(required_params)} need to be provided"
                }
            ),
            401,
        )

    query = Movies.query
    if "name" in request.args:
        query = query.filter_by(name=request.args["name"])
    if "director" in request.args:
        query = query.filter_by(director=request.args["director"])
    if "popularity" in request.args:
        query = query.filter(Movies.popularity >= request.args["popularity"])
    if "imdb_score" in request.args:
        query = query.filter(Movies.imdb_score >= request.args["imdb_score"])

    return jsonify([item.to_dict() for item in query.all()])
