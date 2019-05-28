from functools import wraps
from flask import g, request, redirect, url_for, flash
from flask_login import current_user, logout_user
from app.models import *


def publisher_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role.index != 'publisher':
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)

    return decorated_function


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('account.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


def check_profile(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role.index == 'publisher' and not current_user.publisher:
            flash('You need to finish editig your profile', 'cyan')
            return redirect(url_for('publisher.edit_profile'))
        elif current_user.role.index == 'publisher' and not current_user.publisher.banner \
         or not current_user.publisher.banner:
            flash('You need to finish editig your profile', 'cyan')
            return redirect(url_for('publisher.edit_cover'))
        return func(*args, **kwargs)

    return decorated_function
