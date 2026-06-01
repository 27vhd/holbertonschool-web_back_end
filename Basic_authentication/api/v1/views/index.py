#!/usr/bin/env python3
"""
Index views module providing status and stats endpoints for the API.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    Returns a JSON response indicating the API status is OK.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    Returns a JSON response with the count of each object type in storage.
    """
    from models.user import User
    stats = {'users': User.count()}
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> str:
    """
    Raises a 401 Unauthorized error for testing purposes.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> str:
    """
    Raises a 403 Forbidden error for testing purposes.
    """
    abort(403)
