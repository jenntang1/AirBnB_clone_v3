#!/usr/bin/python3
""" Creates a view for Review objects """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def place_reviews():
    """ Route retrieves list of all Review objects or creates Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        list_reviews = []
        for item in place.reviews:
            list_reviews.append(item.to_dict())
        return jsonify(list_reviews)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("user_id") is None:
            return "Missing user_id", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        if data.get("text") is None:
            return "Missing text", 400
        review = Review()
        for key, value in data.items():
            setattr(review, key, value)
        setattr(review, "place_id", place_id)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def reviews_id(review_id):
    """ Route retrieves a Review object, deletes it or update it """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
