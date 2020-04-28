#!/usr/bin/python3
""" Creates a view for State objects """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states(self):
    """ Route retrieves list of all State objects or creates State """
    if request.method is "GET":
        states = storage.all(State)
        new_list = []
        for values in states.values():
            new_list.append(values.to_dict())
        return jsonify(new_list)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if data.get("name") is None:
            return "Missing name", 400
        obj = State(data)
        print(obj)
        return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states_id(state_id):
    """ Route retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def states_id_delete(state_id):
    """ Route deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
