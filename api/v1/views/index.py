#!/usr/bin/python3
""" Creates a index for blueprint """

from api.v1.views import app_views
import jsonify

@app_views.route("/status")
def status():
    """ Route returns "status": "OK" """
    return jsonify({"status": "OK"})
