from flask import Blueprint, session, render_template, redirect, url_for
from helper.functions import is_authenticated

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login_page'))

    email = session["email"]
    return render_template('auth/dashboard_page.html', email=email)
