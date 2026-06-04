#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path = path + '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user """
        return None

    def session_cookie(self, request=None):
        """ Returns cookie value from request """
        if request is None:
            return None
        session_name = getenv("SESSION_NAME")
        return request.cookies.get(session_name)
