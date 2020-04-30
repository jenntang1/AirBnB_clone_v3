#!/usr/bin/python3
""" Creates a view for Place objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def places_id(city_id):
    """ Route retrieves list of all Place objects or creates Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        list_places = []
        for item in city.places:
            list_places.append(item.to_dict())
        return jsonify(list_places)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("user_id") is None:
            return "Missing user_id", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        if data.get("name") is None:
            return "Missing name", 400
        place = Place()
        for key, value in data.items():
            setattr(place, key, value)
        setattr(place, "city_id", city_id)
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
            if key is not key_list:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """ Route retrieves Place objects depending on JSON """
    data = request.get_json()
    if data is None:
        return "Not a JSON", 400
    cities_ids = data["cities"]
    places_ids = []
    places_list = []
    places = storage.all(Place)
    if len(data.keys()) == 0 or all([len(i) == 0 for i in data.values()]):
        for places_obj in places.values():
            places_list.append(places_obj.to_dict())
        return jsonify(places_list)
    if "states" in data.keys() and len(data["states"]) > 0:
        for state_id in data["states"]:
            for city_obj in storage.get(State, state_id).cities:
                cities_ids.append(city_obj.id)
        cities_ids = list(set(cities_ids))
    if "cities" in data.keys() and len(cities_ids) > 0:
        for city_id in cities_ids:
            for item in storage.get(City, city_id).places:
                places_ids.append(item.id)
    if "amenities" in data.keys() and len(data["amenities"]) > 0:
        for places_obj in places.values():
            amenities_list = []
            for item in places_obj.amenities:
                amenities_list.append(item.id)
            if all(item in amenities_list for item in data["amenities"]):
                places_ids.append(places_obj.id)
    places_ids = list(set(places_ids))
    for ids in places_ids:
        obj_dict = storage.get(Place, ids).to_dict()
        if "amenities" in obj_dict:
            del obj_dict["amenities"]
        places_list.append(obj_dict)
    return jsonify(places_list)
