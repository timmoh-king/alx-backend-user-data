#!/usr/bin/env python3

"""
    Create a Flask app that has a single GET route ("/")
    use flask.jsonify to return a JSON payload of the form:
"""
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """return a JSON payload of the form"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
