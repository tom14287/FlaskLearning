from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash
from app import lm, db, app
from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token
from app.auth.models import User, LoginForm, RegisterForm, ChangePasswordForm
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

auth_ = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    return User.query.filter(User.UserID == int(id)).first()

@app.before_request
def before_request():
    g.user = current_user

@auth_.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print form.email.data, form.password.data
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data,
                    form.password.data, form.type.data,
                    False)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.UserEmail)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.UserEmail, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("auth.unconfirmed"))

    return render_template('auth/register.html', form=form)

@auth_.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(UserEmail=email).first_or_404()
    print email
    if user.UserConfirm:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.UserConfirm = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('index.html')


@auth_.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.UserConfirm:
        return render_template('index.html')
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html')


@auth_.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(UserEmail=form.email.data).first()
        if user and check_password_hash(
                user.UserPassword, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return render_template('index.html')
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)

@auth_.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('index.html')
