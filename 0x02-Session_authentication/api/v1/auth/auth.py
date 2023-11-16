#!/usr/bin/env python3

"""
    create a class named Auth
"""
import os
import re
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
        if path is not None and excluded_paths is not None:
            for excluded_path in excluded_paths:
                excluded_regex = '^{}$'.format(re.escape(
                    excluded_path.rstrip('/')).replace('\\*', '.*') + '/?.*')
                if re.match(excluded_regex, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
            returns None - request will be the Flask request object
        """
        if request:
            return request.headers.get('Authorization')
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request:"""
        if request:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
