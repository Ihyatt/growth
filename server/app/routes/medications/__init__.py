from flask import Blueprint

bp = Blueprint('medications', __name__)

from app.routes.medications import routes