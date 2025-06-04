from flask import g

def get_current_user_id():
    # Assumes g.user_id is set by your JWT validation middleware
    return g.user_id if hasattr(g, 'user_id') else None