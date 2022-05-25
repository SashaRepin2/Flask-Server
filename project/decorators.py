from functools import wraps
from flask import request, current_app, url_for
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


def login_not_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif current_user.is_authenticated:
            return redirect(url_for('main.all_blogs', page=1))
        return func(*args, **kwargs)
    return decorated_view


def permission_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permissions(role):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator