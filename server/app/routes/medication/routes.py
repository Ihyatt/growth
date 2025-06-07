from flask import request, jsonify
from app.routes.medication import medication_bp
from app.models.user import User, Medication
from app.database import db
from server.app.utils.decorators import enforce_elite_user, enforce_elite_user, set_versioning_user
from flask_jwt_extended import get_jwt_identity, jwt_required


@medication_bp.route('/<str:username>', methods=['GET'])
def get_medications():
    patient_username = request.args.get('username')
    patient_user =  User.query.filter_by(username=patient_username).first()
    medications = patient_user.medications


    return jsonify({
        "medications": [medication.to_dict() for medication in medications.items]
    })

@medication_bp.route('<str:username>/<int:medication_id>', methods=['GET'])
def get_medication():
    medication_id = request.args.get('medication_id')
    medication =  Medication.query.filter_by(medication_id).first()


    return jsonify({"medication": medication.to_dict()})
    


@medication_bp.route('<str:username>/add', methods=['POST'])
def add():
    practitioner_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')

    dosage = data.get('dosage')
    frequency = data.get('frequency') 
    instructions = data.get('instructions') 
    
    patient_user = User.query.filter_by(username=patient_username).first()

    new_medication = Medication(
        patient_id=patient_user.id,
        practitioner_id=practitioner_id,
        dosage=dosage,
        frequency=frequency,
        instructions=instructions  
    )

    db.session.commit()
    


@medication_bp.route('<str:username>/medication/<int:medication_id>/edit', methods=['POST'])
def edit():
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
    

@medication_bp.route('<str:username>/medication/<int:medication_id>/delete', methods=['POST'])
@set_versioning_user
@enforce_elite_user
def delete():
    practitioner_id = get_jwt_identity()
    data = request.get_json()
    patient_username = request.args.get('username')
    medication_id = request.args.get('medication_id')

    medication = Medication.query.filter_by(medication_id).first()
    medication.is_active = False
    db.session.commit()