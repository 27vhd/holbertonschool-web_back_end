#!/usr/bin/env python3
"""
Main Flask application module with error handlers and authentication setup.
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

try:
    from flask_cors import CORS
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
except ImportError:
    pass


@app.before_request
def bef_req():
    """
    Validates authentication before each request and aborts with 401 or 403
    if the request is not authorized.
    """
    if auth is None:
        return
    excluded = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, excluded):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Returns a JSON 404 error response for not found resources.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Returns a JSON 401 error response for unauthorized requests.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Returns a JSON 403 error response for forbidden requests.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
