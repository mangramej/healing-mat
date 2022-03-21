from flask import Blueprint, render_template, request, redirect, session, url_for
from models import Staff, db_save, db_delete
from helper.functions import request_validation, is_authenticated

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/')
@auth_bp.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':

        fields = request_validation(request.form)

        if not fields['emailErr']:
            user = Staff.query.filter_by(staff_email=fields['email']).first()
            if not user:
                fields['emailErr'] = "Email do not exist."
            else:
                if user.staff_password != fields['password']:
                    fields['passwordErr'] = "Incorrect password."

        if fields["emailErr"] or fields["passwordErr"]:
            return render_template('login_page.html', fields=fields)

        session.permanent = True
        session["signedin"] = True
        session["email"] = user.staff_email
        return redirect(url_for('dashboard_bp.dashboard'))

    if is_authenticated():
        return redirect(url_for('dashboard_bp.dashboard'))

    return render_template('login_page.html')


@auth_bp.route('/register', methods=['POST', 'GET'])
def register_page():
    if request.method == 'POST':

        fields = request_validation(request.form)

        if not fields['emailErr']:
            user = Staff.query.filter_by(staff_email=fields['email']).first()
            if user:
                fields['emailErr'] = "Email already exist."

        if fields["emailErr"] or fields["passwordErr"]:
            return render_template('register_page.html', fields=fields)

        new_staff = Staff().setEmail(request.form['email']).setPassword(request.form['password'])

        try:
            db_save(new_staff)
            return redirect(url_for('auth_bp.login_page'))

        except Exception as e:
            return f'Issue adding your data {e}'

    else:
        if is_authenticated():
            return redirect(url_for('dashboard_bp.dashboard'))

        return render_template('register_page.html')


@auth_bp.route('/logout')
def logout():
    if is_authenticated():
        session.clear()
    return redirect(url_for('auth_bp.login_page'))
