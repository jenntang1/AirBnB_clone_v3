#!/usr/bin/python3
""" Creates a view for Place objects """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def states_cities(state_id):
    """ Route retrieves list of all City objects or creates City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        list_cities = []
        for item in state.cities:
            list_cities.append(item.to_dict())
        return jsonify(list_cities)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("name") is None:
            return "Missing name", 400
        city = City()
        setattr(city, "name", data["name"])
        setattr(city, "state_id", state_id)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def cities_id(city_id):
    """ Route retrieves a City object, deletes it or update it """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
