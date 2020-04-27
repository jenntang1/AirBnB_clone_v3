#!/usr/bin/python3
""" Create web application """

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Ends the current session """
    storage.close()

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
