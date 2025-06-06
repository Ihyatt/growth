from flask import request, jsonify
from app.routes.medications import medications_bp
from app.models.user import User, Medication
from app.database import db
from server.app.utils.decorators import enforce_role_practioner, enforce_role_patient, enforce_role_practioner, set_versioning_user
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils.decorators import 

from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import jwt_required_with_role


@medications_bp.route('/<str:username>', methods=['GET'])
@jwt_required
def get_medications():
    patient_username = request.args.get('username')
    patient_user =  User.query.get(username=patient_username)
    medications = patient_user.medications


    return jsonify({
        "medications": [medication.to_dict() for medication in medications.items]
    })

@medications_bp.route('<str:username>/<int:medication_id>', methods=['GET'])
@jwt_required()
def get_medication():
    medication_id = request.args.get('medication_id')
    medication =  Medication.query.get(medication_id)


    return jsonify({"medication": medication.to_dict()})
    


@medications_bp.route('<str:username>/add', methods=['POST'])
@set_versioning_user
@jwt_required()
@enforce_role_practioner
def add():
    practitioner_user_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')

    dosage = data.get('dosage')
    frequency = data.get('frequency') 
    instructions = data.get('instructions') 
    
    patient_user = User.query.get(username=patient_username)

    new_medication = Medication(
        patient_id=patient_user.id,
        practitioner_id=practitioner_user_id,
        dosage=dosage,
        frequency=frequency,
        instructions=instructions  
    )

    db.session.commit()
    


@medications_bp.route('<str:username>/<int:medication_id>/edit', methods=['POST'])
@set_versioning_user
@enforce_role_practioner
def edit():
    practitioner_user_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    medication_id = request.args.get('medication_id')
    dosage = data.get('dosage')
    frequency = data.get('frequency') 
    instructions = data.get('instructions') 
    
    medication = Medication.query.get(medication_id)
    medication.dosage = dosage
    medication.frequency = frequency
    medication.instructions = instructions

    db.session.commit()
    

@medications_bp.route('<str:username>/<int:medication_id>/delete', methods=['POST'])
@set_versioning_user
@enforce_role_practioner
def delete():
    practitioner_user_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    medication_id = request.args.get('medication_id')

    medication = Medication.query.get(medication_id)
    medication.is_active = False
    db.session.commit()
    
