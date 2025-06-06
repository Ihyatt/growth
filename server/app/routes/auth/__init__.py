# my_blog/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/')

from . import routes # Import routes to associate them with this blueprint