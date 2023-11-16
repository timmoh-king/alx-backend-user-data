#!/usr/bin/env python3

"""
    Create a class SessionAuth that inherits from Auth
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """class SessionAuth that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(
        self,
        user_id: str = None
    ) -> str:
        """
            creates a Session ID for a user_id:
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
