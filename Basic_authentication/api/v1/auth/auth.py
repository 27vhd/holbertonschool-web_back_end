#!/usr/bin/env python3
"""
Auth module providing the base authentication class for the API.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    Base authentication class that defines the interface for authentication
    mechanisms used in the API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if authentication is required for the given path.

        Paths in excluded_paths (with optional trailing wildcard) are
        considered public and do not require authentication.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
            elif path == excluded or path == excluded + '/':
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header value from the request, or None
        if the header is not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user associated with the request, or None if
        no user is authenticated.
        """
        return None
