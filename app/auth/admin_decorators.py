from functools import wraps
from flask import g, request, redirect, url_for
from flask_login import current_user
from app.models import *


def publisher_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role.index != 'publisher':
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorated_function
