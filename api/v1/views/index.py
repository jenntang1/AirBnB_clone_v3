#!/usr/bin/python3
""" Creates an url route for blueprint """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """ Route returns "status": "OK" """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """ Route returns count of each obj """
    classes = [Amenity, City, Place, Review, State, User]
    total = []
    for cls in classes:
        total.append(storage.count(cls))
    return jsonify(amenities=total[0], cities=total[1],
                   places=total[2], reviews=total[3],
                   states=total[4], users=total[5])
