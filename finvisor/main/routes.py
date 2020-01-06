from flask import render_template, request, Blueprint, url_for
from finvisor.models import User, Expense, Income
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    #expenses = Expense.query.all()
    #income = Income.query.all()
    # Query for expenses and incomes by specific user, not all in DB
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date_of_expense.desc()).paginate(page=page, per_page=10)
        income = Income.query.filter_by(user_id=current_user.id).order_by(Income.date_of_income.desc())
        # Get sum of all users expenses and incomes, number of, etc variables
        explist = list(Expense.query.filter_by(user_id=current_user.id))
        explen = len(explist)
        expsum = 0
        for e in explist:
            expsum += e.amount
        incsum = 0
        for i in list(income):
            incsum += i.amount
        
    else:
        # Will not show any data on home screen if user isnt logged in
        expenses = []
        income = []
        explen = 0
        expsum = 0
        incsum = 0
    return render_template('home.html', expenses=expenses, income=income, explen=explen, expsum=expsum, incsum=incsum)

@main.route('/about')
def about():
    author_pic = url_for('static', filename='profile_pics/' + 'author.jpg')
    return render_template('about.html', author_pic=author_pic)