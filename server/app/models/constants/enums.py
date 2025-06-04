import enum

class PermissionLevel(str, enum.Enum):
    ADMIN = "ADMIN"
    PRACTITIONER = "PRACTITIONER"
    PATIENT = "PATIENT"

class ValidationLevel(str, enum.Enum):
    PENDING ='PENDING',
    APPROVED = 'APPROVED',
    REJECTED = 'REJECTED'
  

class AuditActionType(enum.Enum):
    APPROVED = "APPROVED"
    SET_TO_PENDING = "SET_TO_PENDING"
    REJECTED = "REJECTED"
