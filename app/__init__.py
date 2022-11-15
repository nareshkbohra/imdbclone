import os

from flask import Flask
from flask_login import LoginManager

from ..auth import UserView, UserManagementView, login_blueprint, Users
from ..movies import MovieView, movies_blueprint
from .. import db, login_manager


def create_app():
    app = Flask(__name__)

    db_dir = "./database/db.sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SECRET_KEY"] = "some-secret-key"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    app.register_blueprint(login_blueprint)

    app.add_url_rule("/users/<int:id>", view_func=UserView.as_view("users"))
    app.add_url_rule("/users", view_func=UserManagementView.as_view("user_management"))

    app.add_url_rule("/movies/<int:id>", view_func=MovieView.as_view("movies"))
    app.register_blueprint(movies_blueprint, url_prefix="/movies")

    return app


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
