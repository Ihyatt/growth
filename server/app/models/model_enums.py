import enum

class PermissionLevel(str, enum.Enum):
    ADMIN = "ADMIN"
    PRACTITIONER = "PRACTITIONER"
    PATIENT = "PATIENT"