from flask import request, jsonify
from app.routes.reports import reports_bp
from app.models.user import User, Report
from app.database import db
from server.app.utils.decorators import jwt_required_with_role,set_versioning_user
from flask_jwt_extended import get_jwt_identity
from server.app.utils.decorators import enforce_elite_user, enforce_role_patient, enforce_elite_user, set_versioning_user


from app.models.constants.enums import PermissionLevel, ValidationLevel, AuditActionType
from server.app.utils.decorators import jwt_required_with_role


@reports_bp.route('/search', methods=['GET'])
@set_versioning_user
@enforce_elite_user
def get_patients_reports():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    username = request.args.get('username')
    is_archived = request.args.get('is_archived')
    query = Report.query

    query = query.filter_by(practitioner_id=current_user_id, status=status)

    if title:
        query = query.filter(PractitionerForm.title.ilike(f'%{title}%'))

    query = query.order_by(PractitionerForm.created_at.desc())
    
    forms_pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "forms": [form.to_dict() for form in forms_pagination.items],
        "total": forms_pagination.total,
        "page": forms_pagination.page,
        "pages": forms_pagination.pages,
        "has_next": forms_pagination.has_next,
        "has_prev": forms_pagination.has_prev,
    })

@reports_bp.route('/<int:report_id>', methods=['GET'])
@set_versioning_user
@enforce_elite_user
def get_report():
    pass

@reports_bp.route('/<int:report_id>/delete', methods=['GET'])
@set_versioning_user
@enforce_elite_user
def delete_report():
    pass



    id = Column(db.Integer, primary_key=True)
    report_name = Column(String(255), nullable=False)
    report_type = Column(
        Enum('weekly_summary', 'monthly_analytics', 'ad_hoc', name='report_types'),
        nullable=False
    )
    report_data = Column(Text, nullable=False)
    file_format = Column(String(10), default='json')
    generated_by = Column(db.Integer, ForeignKey('users.id'))
    is_archived = Column(db.Boolean, default=False, nullable=False)
    created_at = Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
