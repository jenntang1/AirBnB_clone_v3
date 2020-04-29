#!/usr/bin/python3
""" Creates a view for linked Place/Amenity objects """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def place_id(place_id):
    """ Route retrieves Amenity objects connected to a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        list_amenities = []
        for item in place.amenities:
            list_amenities.append(item.to_dict())
        return jsonify(list_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"],
                 strict_slashes=False)
def amenity_id(place_id, amenity_id):
    """ Route deletes or updates an Amenity object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "DELETE":
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity.id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity.id)
        delattr(amenity, place_id)
        amenity.save()
        place.save()
        storage.save()
        return jsonify({}), 200
    else:
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
        else:
            if amenity.id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        setattr(amenity, "place_id", place_id)
        amenity.save()
        place.save()
        storage.save()
        return jsonify(amenity.to_dict()), 201
