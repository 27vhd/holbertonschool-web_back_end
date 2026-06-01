#!/usr/bin/env python3
"""
Views package initializer that registers the Blueprint for the API views.
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index  # noqa: E402 import *
from api.v1.views.users  # noqa: E402 import *
