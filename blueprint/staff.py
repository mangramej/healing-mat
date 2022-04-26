from flask import Blueprint, render_template, redirect, url_for, request
from helper.functions import is_authenticated
from models import Staff, db_save, db_delete

staff_bp = Blueprint('staff_bp', __name__)


def staff_bp_middleware():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login_page'))


staff_bp.before_request(staff_bp_middleware)


@staff_bp.route('/staff')
def staff():
    return render_template('staff/index_page.html', staffs=Staff.query.all())


@staff_bp.route('/staff/<id>/update', methods=['GET', 'POST'])
def staff_update(id):
    staff = Staff.query.filter_by(staff_id=id).first()
    if request.method == 'POST':
        if staff:

            if(not request.form['email'] or not request.form['password']):
                return redirect(request.url)


            db_delete(staff)

            prev_id = staff.staff_id
            new_email = request.form['email']
            new_password = request.form['password']

            new_staff = Staff().setId(prev_id).setEmail(new_email).setPassword(new_password)
            db_save(new_staff)

            return redirect(url_for('staff_bp.staff'))

    return render_template('staff/update_page.html', staff=staff)


@staff_bp.route('/staff/<id>/delete', methods=['GET', 'POST'])
def staff_delete(id):
    staff = Staff.query.filter_by(staff_id=id).first()
    if request.method == 'POST':
        if staff:
            db_delete(staff)
            return redirect(url_for('staff_bp.staff'))

    return render_template('staff/delete_page.html', staff=staff)
