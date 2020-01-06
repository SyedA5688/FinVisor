from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from finvisor import db
from finvisor.expenses.forms import ExpenseForm
from finvisor.models import Expense

expenses = Blueprint('expenses', __name__)


@expenses.route('/expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        if form.date.data:
            expense = Expense(date_of_expense=form.date.data, title=form.title.data, amount=form.amount.data, spender=current_user)
        else:
            # If no date entered, dont pass one in, so form uses default time of current time
            expense = Expense(title=form.title.data, amount=form.amount.data, spender=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Expense was added.', 'success')
        return redirect(url_for('main.home'))
    return render_template('input_expense.html', form=form, legend='Add New Expense')

@expenses.route('/expense/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.spender != current_user:
        abort(403)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.date_of_expense = form.date.data
        expense.title = form.title.data
        expense.amount = form.amount.data
        db.session.commit()
        flash('Expense Updated.', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.date.data = expense.date_of_expense
        form.title.data = expense.title
        form.amount.data = expense.amount
    return render_template('input_expense.html', form=form, legend='Edit Expense')

@expenses.route('/expense/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.spender != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense Deleted.', 'success')
    return redirect(url_for('main.home'))

