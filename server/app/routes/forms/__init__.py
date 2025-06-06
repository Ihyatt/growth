from flask import Blueprint

bp = Blueprint('forms', __name__)

from app.routes.forms import routes