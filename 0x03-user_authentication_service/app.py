#!/usr/bin/env python3

"""
    Create a Flask app that has a single GET route ("/")
    use flask.jsonify to return a JSON payload of the form:
"""
from flask import Flask, jsonify, request
from flask_cors import (CORS, cross_origin)
from auth import Auth

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """return a JSON payload of the form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        function that implements the POST /users route.
        The end-point should expect two form data fields:
        "email" and "password".
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "email", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
