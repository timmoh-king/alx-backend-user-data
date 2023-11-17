#!/usr/bin/env python3

"""
complete the DB class provided below to implement the add_user method.
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user.
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """
            returns the first row found in the users table
            as filtered by the method’s input arguments
        """
        columns, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                columns.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()

        first_record = self._session.query(User).filter(
            tuple_(*columns).in_([tuple(values)])
        ).first()
        if first_record is None:
            raise NoResultFound()
        return first_record
