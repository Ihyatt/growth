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

class Responses(enum.Enum):
    NOT_AT_ALL = "NOT_AT_ALL"
    SEVERAL_DAYS = "SEVERAL_DAYS" 
    MORE_THAN_HALF_THE_DAYS = "MORE_THAN_HALF_THE_DAYS" 
    NEARLY_EVERY_DAY = "NEARLY_EVERY_DAY"

class ResponsesWeights(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
