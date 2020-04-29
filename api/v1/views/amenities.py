#!/usr/bin/python3
""" Creates a view for Place objects """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"],
                 strict_slashes=False)
def amenities():
    """ Route retrieves list of all Amenity objects or creates Amenity """
    if request.method == "GET":
        amenity_dict = storage.all(Amenity)
        amenity_list = []
        for value in amenity_dict.values():
            amenity_list.append(value.to_dict())
        return jsonify(amenity_list)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("name") is None:
            return "Missing name", 400
        amenity = Amenity()
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """ Route retrieves an Amenity object, deletes it or update it """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
