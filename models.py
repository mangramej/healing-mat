from helper.db import db


def db_delete(model):
    db.session.delete(model)
    db.session.commit()


def db_save(model):
    db.session.add(model)
    db.session.commit()


class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_email = db.Column(db.String(200), unique=True)
    staff_password = db.Column(db.String(200), nullable=False)

    def setId(self, id):
        self.staff_id = id
        return self

    def setEmail(self, email):
        self.staff_email = email
        return self

    def setPassword(self, password):
        self.staff_password = password
        return self


class Transaction(db.Model):
    __tablename__ = 'transaction'
    cust_id = db.Column(db.Integer, primary_key=True)
    cust_firstname = db.Column(db.Text)
    cust_lastname = db.Column(db.Text)
    trans_date = db.Column(db.Date)
    trans_location = db.Column(db.Text)

    def setId(self, id):
        self.cust_id = id
        return self

    def setFirstname(self, firstname):
        self.cust_firstname = firstname
        return self

    def setLastname(self, lastname):
        self.cust_lastname = lastname
        return self

    def setDate(self, date):
        self.trans_date = date
        return self

    def setLocation(self, location):
        self.trans_location = location
        return self


class Product(db.Model):
    __tablename__ = 'product'
    prod_id = db.Column('prod_id', db.Integer, primary_key=True)
    prod_unit_qty = db.Column(db.Integer)
    prod_retail_price = db.Column(db.Float)
    prod_total_price = db.Column(db.Float)

    def setId(self, id):
        self.prod_id = id
        return self

    def setUnit(self, unit):
        self.prod_unit_qty = unit
        return self

    def setRetail(self, retail):
        self.prod_retail_price = retail
        return self

    def setTotal(self, total):
        self.prod_total_price = total
        return self
