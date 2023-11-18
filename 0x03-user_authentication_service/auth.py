#!/usr/bin/env python3

"""
    define a _hash_password method that takes in a password
    string arguments and returns bytes.
"""
import uuid
import bcrypt
import base64
from db import DB
from user import User
from typing import ByteString, Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
        The returned bytes is a salted hash of the input password
        hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
            Try locating the user by email. If it exists,
            check the password with bcrypt.checkpw
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
            returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                user_id = user.id
                session_id = _generate_uuid()
                self._db.update_user(user_id=user_id, session_id=session_id)
                return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            If the session ID is None or no user is found return None else User
        """
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                if user is not None:
                    return user
            except NoResultFound:
                return None
        else:
            return None

    def destroy_session(self, user_id: int) -> None:
        """The method updates the corresponding user’s session ID to None"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
            Find the user corresponding to the email
            If the user does not exist, raise a ValueError exception
            If it exists, generate a UUID and update the user’s
            reset_token database field. Return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                reset_token = _generate_uuid()
                self._db.update_user(user_id=user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """
            Use the reset_token to find the corresponding user.
            If it does not exist, raise a ValueError exception.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is not None:
                updated_password = _hash_password(password)
                self._db.update_user(
                    user_id=user.id, hashed_password=updated_password, reset_token=None)
        except NoResultFound:
            raise ValueError()
