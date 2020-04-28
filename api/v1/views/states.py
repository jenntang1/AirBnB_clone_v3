#!/usr/bin/python3
""" Creates a view for State objects """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def states():
    """ Route retrieves list of all State objects """
    states = storage.all(State)
    print(states)
    return states


if __name__ == '__main__':
    app.run(debug=True)
