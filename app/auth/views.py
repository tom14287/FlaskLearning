
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, g, flash, session
from app import lm, db, app
from app.auth.email import send_email
from app.auth.token import generate_confirmation_token, confirm_token
from app.auth.form import LoginForm, RegisterForm, ChangePasswordForm
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.sql_operation.mysql import Consumer, Company, Designer, User

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
    print form.username.data, form.email.data, form.password.data, form.type.data
    if form.validate_on_submit():
        ret = register_func(form.username.data, form.email.data, form.password.data, form.confirm, form.type)
        if ret == "SUCCEED":
            return redirect(url_for("auth.unconfirmed"))
    return render_template('auth/login.html', form=form, page='register')

def register_func(username, email, password, confirm, type):
    if not username or not email or not password or not type or not confirm:
        return "INPUTERR"
    if confirm != password:
        return "PWDERR"
    if type != "Company" and type != 'Consumer' and type != 'Designer':
        return "TYPEERR"
    user = User.query.filter_by(UserEmail=email).first()
    if user != None and user.UserEmail == email:
        print email
        return "REPEAT"
    user = User(username, email,
                password, type,
                False)
    db.session.add(user)
    db.session.commit()
    temp = None
    if type == 'Consumer':
        temp = Consumer(ConsumerID=user.UserID)
    elif type == 'Company':
        temp = Company(CompanyID=user.UserID)
    elif type == 'Designer':
        temp = Designer(DesignerID=user.UserID)
    db.session.add(temp)
    db.session.commit()
    token = generate_confirmation_token(user.UserEmail)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.UserEmail, subject, html)
    login_user(user)
    # flash('A confirmation email has been sent via email.', 'success')
    return "SUCCEED"

@auth_.route('/confirm/<token>')
@login_required
def confirm_email(token):
    ret = is_confirm(token)
    if  ret == "CONFIRM" or ret == "HAVECONFIRM":
        return redirect(url_for('auth.login'))
    return redirect(url_for('module_a.index_view'))

def is_confirm(token):
    email = None
    try:
        email = confirm_token(token)
    except:
        return "TOKENERR"
    user = User.query.filter_by(UserEmail=email).first()
    if user == None:
        return "EMAILERR"
    elif user.UserConfirm:
        return "HAVECONFIRM"
    else:
        db.session.execute("update User set UserConfirm=%d where UserID=%d"% (1, user.UserID))
        db.session.commit()
    return "CONFIRM"

@auth_.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.UserConfirm:
        return redirect(url_for('module_a.index_view'))
    flash('Please confirm your account!', 'warning')
    return redirect(url_for('module_a.index_view'))


@auth_.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.form:
        if request.form['action'] == 'login':
            if g.user is not None and g.user.is_authenticated:
                print g.user.UserName, g.user.UserPassword
                return redirect(url_for('module_a.index_view'))
            if form.validate_on_submit():
                ret = login_func(form.email.data, form.password.data)
                print "login ret : ", ret
                if ret == 'NOACCOUNT' or ret == 'WRONGPWD':
                    flash('Invalid email and/or password.', 'danger')
                    return render_template('login.html', form=form, page='login')
                else:
                    return redirect(url_for('module_a.index_view'))
        elif request.form['action'] == 'register':
            if form.validate_on_submit():
                print "reg"
                ret = register_func(form.username.data, form.email.data, form.password.data, form.confirm.data, form.type.data)
                print ret
                if ret == "SUCCEED":
                    return redirect(url_for("auth.unconfirmed"))
            return render_template('login.html', form=form, page='register')

    return render_template('login.html', form=form, page='login')

def login_func(email, password):
    user = User.query.filter_by(UserEmail=email).first()
    if user == None:
        return "NOACCOUNT"
    else:
        if check_password_hash(user.UserPassword, password):
            login_user(user)
            session['userid'] = user.UserID
            session['usertype'] = user.UserType
            return "SUCCEED"
        else:
            return "WRONGPWD"


@auth_.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('module_a.index_view'))

@auth_.route('/change_password', methods= ['POST'])
@login_required
def change_password():
    user = g.user
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        if user and check_password_hash(
            user.UserPassword, request.form['old_password']):
            pwd = generate_password_hash(form.password)
            db.session.execute("update User set UserPassword='%s' where UserID=%d" % (pwd, user.UserID))
            db.session.commit()
            user.UserPassword = pwd
        return redirect(url_for("auth.login"))
    return render_template('auth/change_password.html', form=form)


@auth_.route('/product/<id>')
def product_display(id):
    class Product():
        def __init__(self):
            self.name = "id"
            self.description = "test_description"
            self.price = "400u"
            self.procedure = "fdsafdsaf"
            self.img = "/static/img/product/2.jpg"
    product = Product()
    class Comment():
        def __init__(self):
            self.name = "ljh"
            self.time = "2017.6.6"
            self.content = "not wrong"
            self.img = "/static/img/client/1.jpg"
    comment = Comment()
    comments = [comment]
    test = "product dfadsfdsfdsadsfdsdfs"
    return render_template('product.html', product=product, comments=comments, test=test)

def update_user(id, name, email, tel, pwd):
    user = User.query.filter_by(UserID=id).first()
    if name != None:
        user.UserName = name
    if email != None:
        user.UserEmail = email
    if tel != None:
        user.UserTEL = tel
    if pwd != None:
        user.UserPassword = pwd
    db.session.execute("update User set UserPassword='%s',UserName='%s',"
                       "UserEmail='%s',UserTEL='%s' where UserID=%d" % (user.UserPassword,
                        user.UserName, user.UserEmail, user.UserTEL, user.UserID))
    db.session.commit()
