from flask import Blueprint, session, render_template, redirect, url_for
from sqlalchemy import extract, text
from datetime import date, datetime

from helper.db import db
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
            Transaction.trans_quantity,
            Transaction.trans_discount
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
        "datetime": datetime,
        "this_year_chart_data": {
            "year":             str(year_now),
            "month":            [],
            "order_placed":     [],
            "quantity_sold":    [],
            "total_discount":   [],
            "final_total":      [],
        },
        "last_year_chart_data": {
            "year":             str(year_now-1),
            "month":            [],
            "order_placed":     [],
            "quantity_sold":    [],
            "total_discount":   [],
            "final_total":      [],
        }
    }

    this_year_sql = text("SELECT strftime('%m', t.trans_date) AS 'MONTH_YEAR', COUNT(t.cust_id) AS 'ORDER_PLACED', SUM(t.trans_quantity) AS 'QUANTITY_SOLD', SUM(t.trans_quantity * t.trans_discount) AS 'TOTAL_DISCOUNT', SUM(t.trans_quantity * p.prod_retail_price) - SUM(t.trans_quantity * t.trans_discount) AS 'FINAL_TOTAL' FROM 'transaction' AS t INNER JOIN product AS p ON p.prod_id = t.prod_id WHERE strftime('%Y', trans_date) = '" + str(year_now) + "' GROUP BY strftime('%m', trans_date)")

    last_year_sql = text("SELECT strftime('%m', t.trans_date) AS 'MONTH_YEAR', COUNT(t.cust_id) AS 'ORDER_PLACED', SUM(t.trans_quantity) AS 'QUANTITY_SOLD', SUM(t.trans_quantity * t.trans_discount) AS 'TOTAL_DISCOUNT', SUM(t.trans_quantity * p.prod_retail_price) - SUM(t.trans_quantity * t.trans_discount) AS 'FINAL_TOTAL' FROM 'transaction' AS t INNER JOIN product AS p ON p.prod_id = t.prod_id WHERE strftime('%Y', trans_date) = '" + str(year_now - 1) + "' GROUP BY strftime('%m', trans_date)")


    this_year_chart_result = db.engine.execute(this_year_sql)

    for row in this_year_chart_result:
        data["this_year_chart_data"]["month"].append(row[0])
        data["this_year_chart_data"]["order_placed"].append(row[1])
        data["this_year_chart_data"]["quantity_sold"].append(row[2])
        data["this_year_chart_data"]["total_discount"].append(row[3])
        data["this_year_chart_data"]["final_total"].append(row[4])


    last_year_chart_result = db.engine.execute(last_year_sql)

    for row in last_year_chart_result:
        data["last_year_chart_data"]["month"].append(row[0])
        data["last_year_chart_data"]["order_placed"].append(row[1])
        data["last_year_chart_data"]["quantity_sold"].append(row[2])
        data["last_year_chart_data"]["total_discount"].append(row[3])
        data["last_year_chart_data"]["final_total"].append(row[4])
    

    return render_template('auth/dashboard_page.html', data=data)
