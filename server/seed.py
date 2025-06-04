from app import create_app
from app.database import db
from app.models.user import User
from app.models.constants.enums import PermissionLevel, ValidationLevel

def seed_users():
    app = create_app()
    with app.app_context():
        db.session.query(User).delete()
        users = [
            # Admins
            {
                "username": "admin_1",
                "email": "admin1@example.com",
                "password": "adminpass1",
                "permission": PermissionLevel.ADMIN,
                "is_validated": ValidationLevel.APPROVED,
            },
            {
                "username": "admin_2",
                "email": "admin2@example.com",
                "password": "adminpass2",
                "permission": PermissionLevel.ADMIN,
                "is_validated": ValidationLevel.APPROVED,
            },
            # Practitioners
            {
                "username": "therapist_alex",
                "email": "alex@therapy.com",
                "password": "securealex",
                "permission": PermissionLevel.PRACTITIONER,
                "is_validated": ValidationLevel.PENDING,
            },
            {
                "username": "therapist_kim",
                "email": "kim@therapy.com",
                "password": "securekim",
                "permission": PermissionLevel.PRACTITIONER,
                "is_validated": ValidationLevel.PENDING,
            },
            {
                "username": "therapist_lee",
                "email": "lee@therapy.com",
                "password": "securelee",
                "permission": PermissionLevel.PRACTITIONER,
                "is_validated": ValidationLevel.PENDING,
            },
            # Patients
            {
                "username": "patient_mike",
                "email": "mike@patients.com",
                "password": "mikepass",
                "permission": PermissionLevel.PATIENT,
                "is_validated": ValidationLevel.APPROVED,
            },
            {
                "username": "patient_nina",
                "email": "nina@patients.com",
                "password": "ninapass",
                "permission": PermissionLevel.PATIENT,
                "is_validated": ValidationLevel.APPROVED,
            },
            {
                "username": "patient_omar",
                "email": "omar@patients.com",
                "password": "omarpass",
                "permission": PermissionLevel.PATIENT,
                "is_validated": ValidationLevel.PENDING,
            },
            {
                "username": "patient_zoe",
                "email": "zoe@patients.com",
                "password": "zoepass",
                "permission": PermissionLevel.PATIENT,
                "is_validated": ValidationLevel.REJECTED,
            },
            {
                "username": "patient_sam",
                "email": "sam@patients.com",
                "password": "sampass",
                "permission": PermissionLevel.PATIENT,
                "is_validated": ValidationLevel.APPROVED,
            },
        ]

        for u in users:
            user = User(
                username=u["username"],
                email=u["email"],
                permission=u["permission"],
                is_validated=u["is_validated"],
            )
            user.set_password(u["password"])
            db.session.add(user)

        db.session.commit()
        print("Seeded 10 users successfully.")

if __name__ == "__main__":
    seed_users()