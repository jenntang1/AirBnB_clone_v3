#!/usr/bin/python3
""" Creates a view for Place objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def places_id(city_id):
    """ Route retrieves list of all Place objects or creates Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all(Place)
        new_list = []
        for values in places.values():
            new_list.append(values.to_dict())
        return jsonify(new_list)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("user_id") is None:
            return "Missing user_id", 400
        if data.get("name") is None:
            return "Missing name", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        place = Place()
        for key, value in data.items():
            settattr(place, key, value)
        setattr(place, "name", data["name"])
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def places(place_id):
    """ Route retrieves a Place object, deletes it or updates it """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        key_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key != key_list:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
