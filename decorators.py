from functools import wraps

from flask import jsonify
from flask_login import current_user

def admin_check(func):

    @wraps(func)
    def wrapper(obj, **kwargs):
        if not current_user.is_admin:
            return jsonify({"error": "User is not authorized to perform this operation"}), 403
        return func(obj, **kwargs)

    return wrapper

def owner_check(func):
    @wraps(func)
    def wrapper(obj, **kwargs):
        if (not current_user.is_admin) and (current_user.id != kwargs["id"]):
            return jsonify({"error": "User is not authorized to perform this operation"}), 403
        return func(obj, **kwargs)

    return wrapper




