#!/usr/bin/env python3

"""
    Flask view that handles all routes for the Session authentication.
"""

import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
        Flask view that handles all routes for the Session authentication.
    """
    error_not_found = {"error": "no user found for this email"}

    email = request.form.get('email')
    if not email or not email.strip():
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or not password.strip():
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(error_not_found), 404
    if len(users) <= 0:
        return jsonify(error_not_found), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
