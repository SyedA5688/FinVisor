from flask import render_template, url_for, flash, redirect, request, Blueprint
from finvisor import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from finvisor.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from finvisor.models import User
from finvisor.users.utils import send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    # If already logged in, don't let user get back to register page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a user
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # Add user to database
        db.session.add(user)
        db.session.commit()
        # Give confirmation msg of creating an account
        flash('Successfully Created Account!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if password matches hashed password stored in DB
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # go to page user was trying to access if applicable using query param
            next = request.args.get('next') 
            # If correct email and password, log user in
            login_user(user, remember=form.remember.data)
            if next:
               return redirect(next)
            else: 
                return redirect(url_for('main.home'))
        else:
            flash('Login was unsuccessful. Check your email and password', 'danger')
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Information Updated.', 'success')
        return redirect(url_for('users.account'))
    image_file = url_for('static', filename='profile_pics/' + 'default1.jpg')
    return render_template('account.html', image_file=image_file, form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Send user email to reset password
        send_reset_email(user)
        flash('Reset email sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None: # Took too long to click email, or not user
        flash('Invalid or Expired Token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Successfully Updated Password!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)

