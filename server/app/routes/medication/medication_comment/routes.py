
from flask import request, jsonify
from app.routes.medication.medication_comment import medication_comment_bp
from app.database import db
from app.models.user import User, MedicationComment

from app.utils.decorators import get_resource_model
from flask_jwt_extended import get_jwt_identity, jwt_required


#only practitioners can update comments
@medication_comment_bp.route('/edit', methods=['POST'])
def edit(medication_comment_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()

    comment_text = data.get('text')


    medication_comment = MedicationComment.query.filter_by(medication_comment_id).first()
    medication_comment.text = comment_text
    db.session.commit()

    return jsonify({'success': 'success'}), 201


@medication_comment_bp.route('delete', methods=['POST'])
def edit(medication_comment_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')


    medication_comment = MedicationComment.query.filter_by(medication_comment_id).first()
    medication_comment.text = comment_text
    db.session.commit()

    return jsonify({'success': 'success'}), 201