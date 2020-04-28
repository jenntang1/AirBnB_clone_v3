#!/usr/bin/python3
""" Creates a view for State objects """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """ Route retrieves list of all State objects """
    states = storage.all(State)
    new_list = []
    for values in states.values():
        new_list.append(values.to_dict())
    return jsonify(new_list)



