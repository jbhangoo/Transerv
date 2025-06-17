"""
decorators.py
Define decorators for use by Flask routes.
"""
from functools import wraps
from flask import abort
from flask_login import current_user
from models.data import db, UserRole, Role

# Security middleware
def role_required(required_level:UserRole):
    """ Role-based access control  """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            role = db.session.query(Role).filter(Role.id == current_user.role_id).first()
            if role and role.level > required_level.value:
                abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
