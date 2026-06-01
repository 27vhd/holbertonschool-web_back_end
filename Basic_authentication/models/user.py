#!/usr/bin/env python3
"""
User model module defining the User class with password hashing support.
"""
import hashlib
from models.base import Base


class User(Base):
    """
    User class representing an authenticated user with email and password.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a User instance with optional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email', "")
        self._password = kwargs.get('_password', "")
        self.first_name = kwargs.get('first_name', "")
        self.last_name = kwargs.get('last_name', "")

    @property
    def password(self) -> str:
        """
        Returns the hashed password of the user.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """
        Sets the password by hashing it with SHA256, or sets empty string
        if pwd is None or not a string.
        """
        if pwd is None or type(pwd) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """
        Returns True if the given password matches the stored hashed password.
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        return hashlib.sha256(
            pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """
        Returns a display name for the user based on available name fields.
        """
        if self.email is None and self.first_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        return "{} {}".format(self.first_name, self.last_name)
