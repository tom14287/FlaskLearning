from flask import g, flash
import datetime
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint
from app import lm, db
from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token
from app.auth.models import User, LoginForm, RegisterForm, ChangePasswordForm
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

auth_ = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    return User.query.filter(User.UserID == int(id)).first()

@lm.before_request
def before_request():
    g.user = current_user

@auth_.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data,
                    form.password.data, form.type_.data,
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

    return render_template('register.html', form=form)

@auth_.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(UserEmail=email).first_or_404()
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


@auth_.route('/login', methods = ["GET", "POST"])
def login_index():
     if g.user is not None and g.user.is_authenticated:
         return render_template('index.html')
     if request.method == 'POST':
         user = User.query.filter_by(username=request.form['username']).first()
         login_user(user)
         return render_template('index.html')
     else:
         return render_template('login.html')
     form = LoginForm()
     if form.validate_on_submit():
         if User.query.filter_by(username=form.openid.data).first():
             user = User.query.filter_by(username=form.openid.data).first_or_404()
             login_user(user)
             return render_template('index.html')
         else:
             return render_template('login.html', title="Log in", form=form)

@auth_.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('index.html')
