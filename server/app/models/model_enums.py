import enum

class PermissionLevel(str, enum.Enum):
    ADMIN = "ADMIN"
    PRACTITIONER = "PRACTITIONER"
    PATIENT = "PATIENT"

class ValidationLevel(str, enum.Enum):
    PENDING ='PENDING',
    APPROVED = 'APPROVED',
    REJECTED = 'REJECTED'
  