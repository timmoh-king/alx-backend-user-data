#!/usr/bin/env python3

"""
    define a _hash_password method that takes in a password
    string arguments and returns bytes.
"""

import bcrypt
import base64
from typing import ByteString


def _hash_password(password: str) -> bytes:
    """
        The returned bytes is a salted hash of the input password
        hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
