from flask import request, jsonify
from app.routes.medication import medication_bp
from server.app.models.form_template import User, Medication, MedicationComment
from app.database import db
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user
from flask_jwt_extended import get_jwt_identity, jwt_required



@medication_bp.route('/edit', methods=['POST'])
def edit(medication_id):
    practitioner_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    medication_id = request.args.get('medication_id')
    dosage = data.get('dosage')
    frequency = data.get('frequency') 
    instructions = data.get('instructions') 
    
    medication = Medication.query.filter_by(medication_id).first()
    medication.dosage = dosage
    medication.frequency = frequency
    medication.instructions = instructions

    db.session.commit()
    

@medication_bp.route('/delete', methods=['POST'])
def delete(patient_username, medication_id):
    practitioner_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    medication_id = request.args.get('medication_id')

    medication = Medication.query.filter_by(medication_id).first()
    medication.is_active = False
    db.session.commit()



@medication_bp.route('/comment', methods=['POST'])
@jwt_required()
def create(medication_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('text')

    new_comment = MedicationComment(
        text=comment_text,
        user_id=current_user_id,
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201