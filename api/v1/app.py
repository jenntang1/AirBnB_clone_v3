#!/usr/bin/python3
""" Create web application """

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Ends the current session """
    storage.close()


@app.errorhandler(404)
def 404_error():
    """ Returns a json 404 error message """
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"),
            threaded=True)
