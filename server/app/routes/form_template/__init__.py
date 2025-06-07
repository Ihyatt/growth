from flask import Blueprint

form_bp = Blueprint('form_template', __name__, url_prefix='/form_templates/<int:form_template_id>')