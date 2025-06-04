import sys
from werkzeug.security import generate_password_hash
from app import app
from app.database import db
from app.models.user import User
from app.models.constants.enums import PermissionLevel, ValidationLevel
from app import create_app



def seed_users():
    """Seed initial users into the database with proper error handling"""
    app = create_app()
    users = [
        # Admins (should be approved)
        {
            "username": "admin_1",
            "email": "admin1@example.com",
            "password": "AdminSecurePass1!",
            "permission": PermissionLevel.ADMIN,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
        {
            "username": "admin_2",
            "email": "admin2@example.com",
            "password": "AdminSecurePass2!",
            "permission": PermissionLevel.ADMIN,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
        # Practitioners (mix of statuses)
        {
            "username": "therapist_alex",
            "email": "alex@therapy.com",
            "password": "SecureAlex123!",
            "permission": PermissionLevel.PRACTITIONER,
            "is_validated": ValidationLevel.PENDING,
            "is_active": True
        },
        {
            "username": "therapist_kim",
            "email": "kim@therapy.com",
            "password": "SecureKim123!",
            "permission": PermissionLevel.PRACTITIONER,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
        {
            "username": "therapist_lee",
            "email": "lee@therapy.com",
            "password": "SecureLee123!",
            "permission": PermissionLevel.PRACTITIONER,
            "is_validated": ValidationLevel.REJECTED,
            "is_active": False
        },
        # Patients (mix of statuses)
        {
            "username": "patient_mike",
            "email": "mike@patients.com",
            "password": "MikeSecure123!",
            "permission": PermissionLevel.PATIENT,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
        {
            "username": "patient_nina",
            "email": "nina@patients.com",
            "password": "NinaSecure123!",
            "permission": PermissionLevel.PATIENT,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
        {
            "username": "patient_omar",
            "email": "omar@patients.com",
            "password": "OmarSecure123!",
            "permission": PermissionLevel.PATIENT,
            "is_validated": ValidationLevel.PENDING,
            "is_active": False
        },
        {
            "username": "patient_zoe",
            "email": "zoe@patients.com",
            "password": "ZoeSecure123!",
            "permission": PermissionLevel.PATIENT,
            "is_validated": ValidationLevel.REJECTED,
            "is_active": False
        },
        {
            "username": "patient_sam",
            "email": "sam@patients.com",
            "password": "SamSecure123!",
            "permission": PermissionLevel.PATIENT,
            "is_validated": ValidationLevel.APPROVED,
            "is_active": True
        },
    ]

    with app.app_context():
        try:
            # Check if users already exist
            if User.query.first():
                print("Users already exist in database. Aborting seed.")
                return

            # Create users in transaction
            for user_data in users:
                if User.query.filter_by(email=user_data["email"]).first():
                    print(f"User with email {user_data['email']} already exists. Skipping.")
                    continue

                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    permission=user_data["permission"],
                    is_validated=user_data["is_validated"],
                    is_active=user_data.get("is_active", True)
                )
                user.password_hash = generate_password_hash(user_data["password"])
                db.session.add(user)

            db.session.commit()
            print(f"Successfully seeded {len(users)} users.")

        except Exception as e:
            db.session.rollback()
            print(f"Error seeding users: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    seed_users()