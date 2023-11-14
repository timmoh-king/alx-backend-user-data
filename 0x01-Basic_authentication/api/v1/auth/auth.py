#!/usr/bin/env python3

"""
    create a class named Auth
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """class Auth"""
    def __init__(self):
        pass

    def require_auth(
        self,
        path: str,
        excluded_paths: List[str]
    ) -> bool:
        """
            returns False - path and excluded_paths will be used later
        """
        return (
            path is None or
            excluded_paths is None or
            path not in excluded_paths
        )

    def authorization_header(self, request=None) -> str:
        """
            returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns None - request will be the Flask request object
        """
        return None
