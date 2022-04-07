from flask import Blueprint, session, render_template, redirect, url_for
from sqlalchemy import extract
from datetime import date, datetime

from helper.functions import is_authenticated
from models import Staff, Transaction, Product

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login_page'))

    date_now = datetime.utcnow()
    year_now = date_now.year
    month_now = date_now.month
    prev_month = month_now - 1

    this_year = extract('year', Transaction.trans_date) == year_now
    this_month = extract('month', Transaction.trans_date) == month_now
    this_prev_month = extract('month', Transaction.trans_date) == prev_month

    staff_count = len(Staff.query.all())

    trans_month_count = len(
        Transaction.query.filter(this_year, this_month).all())
    prev_trans_month_count = len(
        Transaction.query.filter(this_year, this_prev_month).all())

    prod_trans_data = Transaction.query \
        .join(Product, Transaction.prod_id == Product.prod_id) \
        .with_entities(
            Transaction.trans_quantity,
            Product.prod_retail_price
        ) \
        .filter(Transaction.prod_id == Product.prod_id)

    prod_month_data = prod_trans_data.filter(this_year, this_month).all()
    prod_prev_month_data = prod_trans_data.filter(
        this_year, this_prev_month).all()

    # recent_prod_trans_data = prod_trans_data.order_by(Transaction.cust_id.desc()).limit(10).all()

    recent_trans_data = Transaction.query\
        .order_by(Transaction.cust_id.desc())\
        .join(Product, Transaction.prod_id == Product.prod_id)\
        .with_entities(
            Product.prod_retail_price,
            Transaction.cust_firstname,
            Transaction.cust_lastname,
            Transaction.trans_location,
            Transaction.trans_date,
            Transaction.trans_quantity
        )\
        .filter(Transaction.prod_id == Product.prod_id)\
        .limit(10)\
        .all()

    prod_month_total_earn = 0
    for item in prod_month_data:
        prod_month_total_earn += item[0] * item[1]

    prod_prev_month_total_earn = 0
    for item in prod_prev_month_data:
        prod_prev_month_total_earn += item[0] * item[1]

    data = {
        "staff_count": staff_count,
        "trans_month_count": trans_month_count,
        "prev_trans_month_count": prev_trans_month_count,
        "prod_month_total_earn": prod_month_total_earn,
        "prod_prev_month_total_earn": prod_prev_month_total_earn,
        "recent_trans_data": recent_trans_data,
        "datetime": datetime
    }

    return render_template('auth/dashboard_page.html', data=data)
