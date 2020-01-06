from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from finvisor import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Each class (model) represents a table in the database
class User(db.Model, UserMixin):
    # columns in table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # User profile image option would go here
    password = db.Column(db.String(60), nullable=False)
    expenses = db.relationship('Expense', backref='spender', lazy=True)
    incomes = db.relationship('Income', backref='saver', lazy=True)

    # Reset password methods
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self): # Representation of object when it is printed out
        return f"User('{self.username}', '{self.email}')"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Changed date from db.DateTime to a string
    date_of_expense = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): 
        return f"Expense('{self.date_of_expense}', '{self.amount}')"

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_income = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): 
        return f"Income('{self.date_of_income}', '{self.amount}')"
