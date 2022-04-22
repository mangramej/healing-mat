from flask import Flask

from helper.db import db

from blueprint.auth import auth_bp
from blueprint.dashboard import dashboard_bp
from blueprint.staff import staff_bp
from blueprint.transaction import transaction_bp
from blueprint.help import help_bp

app = Flask(__name__)
app.secret_key = "HealingMATFinalSECRETCODE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hmat.db'
app.config['SQLALCHEMY TRACK_MODIFICATIONS'] = True

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(help_bp)

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=False)
