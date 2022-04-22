from flask import Blueprint, render_template, redirect, url_for

from helper.functions import is_authenticated

help_bp = Blueprint('help_bp', __name__)


@help_bp.route('/help')
def help():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login_page'))

    return render_template('help/help1.html')