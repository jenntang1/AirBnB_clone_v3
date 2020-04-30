#!/usr/bin/python3
""" Creates a view for User objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"],
                 strict_slashes=False)
def users():
    """ Route retrieves list of all User objects or creates User """
    if request.method == "GET":
        users = storage.all(User)
        new_list = []
        for values in users.values():
            new_list.append(values.to_dict())
        return jsonify(new_list)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("email") is None:
            return "Missing email", 400
        if data.get("password") is None:
            return "Missing password", 400
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def users_id(user_id):
    """ Route retrieves a User object, deletes it or update it """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        key_list = ["id", "email", "created_at", "updated_at"]
        for key, value in data.items():
            if key != key_list:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
