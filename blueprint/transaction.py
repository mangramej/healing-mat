from flask import Blueprint, session, render_template, redirect, url_for, request
from helper.functions import is_authenticated
from models import Transaction, Product, db_save, db_delete
from datetime import datetime
from sqlalchemy import or_

transaction_bp = Blueprint('transaction_bp', __name__)


def transaction_bp_middleware():
    if not is_authenticated():
        return redirect(url_for('auth_bp.login_page'))


transaction_bp.before_request(transaction_bp_middleware)


@transaction_bp.route('/transaction', methods=['GET','POST'])
@transaction_bp.route('/transaction/<int:page>', methods=['GET'])
def transaction(page=1):
    per_page = 11

    if request.method == 'POST':
        search = request.form['search_text']
        search = "%{}%".format(search)

        if(request.form['search_type'] == 'name'):
            transactions = Transaction.query.filter(or_(Transaction.cust_firstname.like(search), Transaction.cust_lastname.like(search))).paginate(page, per_page, error_out=False)


        if request.form['search_type'] == 'location':
            transactions = Transaction.query.filter(Transaction.trans_location.like(search)).paginate(page, per_page, error_out=False)


    if request.method == 'GET':
        transactions = Transaction.query.paginate(page, per_page, error_out=False)

    return render_template('transaction/index_page.html', transactions=transactions)



@transaction_bp.route('/transaction/show', methods=['POST'])
def transaction_show():
    # trans = Transaction.query.filter_by(cust_id=id).first()



    return request.form['search_text']


@transaction_bp.route('/transaction/create', methods=['GET', 'POST'])
def transaction_create():
    if request.method == 'GET':
        products = Product.query.all()
        return render_template('transaction/create_page.html', products=products)

    if request.method == 'POST':

        if (
                not request.form['firstname'] or 
                not request.form['lastname'] or
                not request.form['date'] or 
                not request.form['location'] or 
                not request.form['quantity'] or 
                not request.form['discount'] or 
                not request.form['prod_id'] or
                not (request.form['quantity']).isnumeric()):
                return redirect(request.url);
                
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        location = request.form['location']
        prod_id = request.form['prod_id']
        trans_qty = request.form['quantity']
        trans_discount = request.form['discount']

        new_trans = Transaction().setFirstname(firstname).setLastname(
            lastname).setDate(date).setLocation(location)
        new_trans.setProdId(prod_id)
        new_trans.setQuantity(trans_qty)
        new_trans.setDiscount(trans_discount)

        db_save(new_trans)
        return redirect(url_for('transaction_bp.transaction'))


@transaction_bp.route('/transaction/<id>/update', methods=['GET', 'POST'])
def transaction_update(id):
    trans = Transaction.query.filter_by(cust_id=id).first()

    if request.method == 'POST':
        if trans:
            if (
                not request.form['firstname'] or 
                not request.form['lastname'] or
                not request.form['date'] or 
                not request.form['location'] or 
                not request.form['quantity'] or 
                not request.form['discount'] or 
                not request.form['prod_id'] or
                not (request.form['quantity']).isnumeric()):
                return redirect(request.url)


            prev_cust_id = trans.cust_id
            new_firstname = request.form['firstname']
            new_lastname = request.form['lastname']
            new_date = datetime.strptime(
                request.form['date'], '%Y-%m-%d')
            new_location = request.form['location']
            new_trans_quantity = request.form['quantity']
            new_prod_id = request.form['prod_id']
            new_discount = request.form['discount']

            db_delete(trans)

            new_trans = Transaction()
            new_trans.setId(prev_cust_id)
            new_trans.setFirstname(new_firstname)
            new_trans.setLastname(new_lastname)
            new_trans.setDate(new_date)
            new_trans.setLocation(new_location)
            new_trans.setQuantity(new_trans_quantity)
            new_trans.setProdId(new_prod_id)
            new_trans.setDiscount(new_discount)
            db_save(new_trans)

            return redirect(url_for('transaction_bp.transaction'))

    if request.method == 'GET':
        products = Product.query.all()
        return render_template('transaction/update_page.html', transaction=trans, products=products)


@transaction_bp.route('/transaction/<id>/delete', methods=['GET', 'POST'])
def transaction_delete(id):
    trans = Transaction.query.filter_by(cust_id=id).first()
    if request.method == 'POST':
        if trans:
            db_delete(trans)
            return redirect(url_for('transaction_bp.transaction'))
    else:
        return render_template('transaction/delete_page.html', transaction=trans)