#!/usr/bin/env python3

"""
    define a _hash_password method that takes in a password
    string arguments and returns bytes.
"""

import bcrypt
import base64
from db import DB
from user import User
from typing import ByteString
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
        The returned bytes is a salted hash of the input password
        hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(
        self,
        email: str,
        password: str
    ) -> User:
        """
            If a user already exist with the passed email, raise a
            ValueError with the message User <user's email> already exists.
            hash the password with _hash_password,
            save the user to the database using self._db
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")
