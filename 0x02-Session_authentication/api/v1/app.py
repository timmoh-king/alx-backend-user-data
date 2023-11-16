#!/usr/bin/env python3
"""
Route module for the API
"""

import os
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = getenv('AUTH_TYPE', 'auth')

if auth_type == 'auth':
    auth = Auth()

if auth_type == 'basic_auth':
    auth = BasicAuth()

if auth_type == 'session_auth':
    auth = SessionAuth()


@app.before_request
def authenticate_user():
    """ a method in api/v1/app.py to handler before_request"""
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if auth and auth.require_auth(request.path, excluded_paths):
        user = auth.current_user(request)

        if auth.authorization_header(request) is None:
            abort(401)

        if user is None:
            abort(403)

        request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """No access handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
