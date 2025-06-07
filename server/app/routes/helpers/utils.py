

import logging
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

logger = logging.getLogger(__name__)

def get_current_user_object():
    try:
        current_user_id = get_jwt_identity()
        if current_user_id is None:
            logger.warning("get_jwt_identity returned None despite @jwt_required passing. Unexpected.")
            return None

        user = User.query.get(current_user_id) 

        if user is None:
            logger.warning(f"User with ID {current_user_id} from JWT not found in database.")
            return None

        return user
    except Exception as e:

        logger.exception(f"Unexpected error retrieving current user object for ID {get_jwt_identity()}: {e}")
        return None #