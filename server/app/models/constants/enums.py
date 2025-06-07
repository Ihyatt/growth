import enum

class UserLevel(str, enum.Enum):
    ADMIN = "ADMIN"
    PRACTITIONER = "PRACTITIONER"
    PATIENT = "PATIENT"

class UserApprovalStatus(str, enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class ProfileStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
  

class AuditActionStatus(enum.Enum):
    SET_TO_APPROVED = "SET_TO_APPROVED"
    SET_TO_PENDING = "SET_TO_PENDING"
    SET_TO_REJECTED = "SET_TO_REJECTED"
    SET_TO_INACTIVE = "SET_TO_REJECTED"
    SET_TO_ACTIVE = "SET_TO_ACTIVE"


class FormStatus(str, enum.Enum):
    TODO = 'TODO'
    IN_PROCESS = 'IN_PROCESS'
    COMPLETED = 'COMPLETED'
    ARCHIVED = 'ARCHIVED'


class FormResponses(str, enum.Enum):
    NOT_AT_ALL = 'NOT_AT_ALL'
    SEVERAL_DAYS = 'SEVERAL_DAYS'
    MORE_THAN_HALF_THE_DAYS = 'MORE_THAN_HALF_THE_DAYS'
    NEARLY_EVERY_DAY = 'NEARLY_EVERY_DAY'

