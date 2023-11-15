#!/usr/bin/env python3

"""Create the class BasicAuth that inherits from Auth"""

import base64
import binascii
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Create a class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
            returns the Base64 part of the Authorization header
            for a Basic Authentication:
        """
        if authorization_header is None \
                or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        base64_part = authorization_header[len("Basic "):].strip()
        return base64_part

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
            decoded value of a Base64 string base64_authorization_header:
        """
        if base64_authorization_header is None \
                or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_value
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """
            returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None \
                or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        # parts = decoded_base64_authorization_header.split(":")
        # if len(parts) != 2:
        #     return (None, None)
        #     else:
        #         return tuple(parts)
        parts = decoded_base64_authorization_header.split(':')
        if len(parts) != 2:
            return (None, None)
        else:
            return tuple(parts)
