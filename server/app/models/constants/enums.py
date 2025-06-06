import enum

class UserLevel(str, enum.Enum):
    ADMIN = "ADMIN"
    PRACTITIONER = "PRACTITIONER"
    PATIENT = "PATIENT"

class ApprovalStatus(str, enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class ProfileStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
  

class AuditActionStatus(enum.Enum):
    APPROVED = "APPROVED"
    SET_TO_PENDING = "SET_TO_PENDING"
    REJECTED = "REJECTED"
