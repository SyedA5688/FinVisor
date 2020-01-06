from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from finvisor.config import Config


# Extensions
# Instance of Database, using sqlite DB for building app (just a file in project folder)
db = SQLAlchemy()
# Instance of bcrypt, extension used to hash passwords for security
bcrypt = Bcrypt()
# Instance of Login manager extension
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# Reset password email, mail configs moved to config.py
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from finvisor.users.routes import users
    from finvisor.expenses.routes import expenses
    from finvisor.incomes.routes import incomes
    from finvisor.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(expenses)
    app.register_blueprint(incomes)
    app.register_blueprint(main)

    return app
