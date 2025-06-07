from flask import Blueprint

assigned_form_bp = Blueprint('assigned_form', __name__, url_prefix='/assigned_forms/<int:assigned_form_id>')