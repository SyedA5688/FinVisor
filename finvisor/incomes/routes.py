from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from finvisor import db
from finvisor.incomes.forms import IncomeForm
from finvisor.models import Income

incomes = Blueprint('incomes', __name__)


@incomes.route('/income/new', methods=['GET', 'POST'])
@login_required
def new_income():
    form = IncomeForm()
    if form.validate_on_submit():
        if form.date.data:
            income = Income(date_of_income=form.date.data, title=form.title.data, amount=form.amount.data, saver=current_user)
        else:
            income = Income(title=form.title.data, amount=form.amount.data, saver=current_user)
        db.session.add(income)
        db.session.commit()
        flash('Income was added.', 'success')
        return redirect(url_for('main.home'))
    return render_template('input_income.html', form=form, legend='Add New Income')

@incomes.route('/income/<int:income_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.saver != current_user:
        abort(403)
    form = IncomeForm()
    if form.validate_on_submit():
        income.date_of_income = form.date.data
        income.title = form.title.data
        income.amount = form.amount.data
        db.session.commit()
        flash('Income Updated.', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.date.data = income.date_of_income
        form.title.data = income.title
        form.amount.data = income.amount
    return render_template('input_income.html', form=form, legend='Edit Income')

@incomes.route('/income/<int:income_id>/delete', methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.saver != current_user:
        abort(403)
    db.session.delete(income)
    db.session.commit()
    flash('Income Deleted.', 'success')
    return redirect(url_for('main.home'))