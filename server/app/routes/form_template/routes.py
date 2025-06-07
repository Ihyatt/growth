from flask import request, jsonify
from app.routes.form_template import form_template_bp
from server.app.models import FormTemplate, User
from app.database import db
from flask_jwt_extended import get_jwt_identity
from app.models.constants.enums import FormStatus
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user


 
@form_template_bp.route('/', methods=['GET'])
def get_form_template(form_template_id):
    
    current_user_id = get_jwt_identity() 
    form_id = request.args.get('form_id')
    form = FormTemplate.query.filter_by(practitioner_id=current_user_id, id=form_id).first()

    return jsonify({'form':form})
     
     


@form_template_bp.route('/archive', methods=['POST'])
def archive_form_template():
    form_id = request.args.get('form_id')
    form = FormTemplate.query.filter_by(id=form_id).first()
    form.status = FormStatus.ARCHIVED
    db.session.commit()


@form_template_bp.route('/assign', methods=['POST'])
def assign_form_template():
    form_id = request.args.get('form_id')
    form = FormTemplate.query.filter_by(id=form_id).first()
    form.status = FormStatus.ARCHIVED
    db.session.commit()