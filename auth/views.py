from flask import jsonify
from flask import request
from flask.views import MethodView
from flask import Blueprint
from flask_login import login_user, login_required, current_user

from .models import Users
from .validators import validate_email, validate_password
from .. import db, password_hasher
from ..decorators import admin_check, owner_check


class UserView(MethodView):

    init_every_request = False

    @login_required
    @owner_check
    def get(self, id):
        user = Users.query.get(id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    @login_required
    @owner_check
    def put(self, id):
        user = Users.query.get(id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if "name" in request.args:
            user.name = request.args["name"]

        if "email" in request.args:
            email = request.args["email"]
            if Users.query.filter_by(email=email).first():
                return jsonify({"error": "This email already exists"}), 403

            user.email = email

        if "password" in request.args:
            user.password = password_hasher.hash(request.args["password"])

        db.session.commit()

        return jsonify(user.to_dict()), 200

    @login_required
    @owner_check
    def delete(self, id):
        user = Users.query.get(id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"msg": "User deleted successfully"}), 200

class UserManagementView(MethodView):

    init_every_request = False

    def post(self):
        error = self.validate_post_request()

        if error:
            return jsonify({"error": error}), 400

        request_args = request.args
        name = request_args["name"]
        email = request_args["email"]
        password = password_hasher.hash(request_args["password"])

        user = Users(email=email, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify("New user created"), 201

    def validate_post_request(self):
        required_params = ["name", "email", "password"]

        missing_params = []
        for param in required_params:
            if param not in request.args:
                missing_params.append(param)

        if missing_params:
            return f"Required params {', '.join(missing_params)} not found"

        request_args = request.args
        email = request_args["email"]
        password = request_args["password"]

        user = Users.query.filter_by(email=request_args["email"]).first()
        if user:
            return f"Email {user.email} already exists"

        if not validate_email(email):
            return f"Invalid email {email}"

        if not validate_password(password):
            return f"Invalid password {password}"


login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/login", methods=["POST"])
def login():
    required_params = ["email", "password"]

    if ("email" not in request.args) or ("password" not in request.args):
        return jsonify({"error": "Email or password is missing"}), 400

    user = Users.query.filter_by(email=request.args["email"]).first()
    if not user:
        return jsonify({"error": "user not found"}), 401
    try:
        password_hasher.verify(user.password, request.args["password"])
    except Exception as ex:
        return jsonify({"error": f"invalid password"}), 401

    login_user(user)

    return jsonify({"user": user.to_dict()}), 200
