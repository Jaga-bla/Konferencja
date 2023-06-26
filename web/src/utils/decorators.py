from functools import wraps
from flask import session, request, redirect, url_for, flash

from src.models.models import Attendant

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'email' in session:
            flash("Aby kontynuować, zaloguj się.")
            return redirect(url_for('konf.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['email'] != 'admin@admin.pl':
            flash("Dostęp tylko dla administratora.")
            return redirect(url_for('konf.lectures'))
        return f(*args, **kwargs)
    return decorated_function