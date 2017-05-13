from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])


class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(15))
    UserEmail = db.Column(db.String(45))
    UserTEL = db.Column(db.String(11))
    UserPassword = db.Column(db.String(200))
    UserType = db.Column(db.Enum("Consumer", "Designer", "Company"), default="Consumer")
    UserImage = db.Column(db.BLOB)
    UserConfirm = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, pwd, type_, confirm):
        self.UserEmail = email
        self.UserName = name
        self.UserPassword = pwd
        self.UserType = type_
        self.UserConfirm = confirm

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.UserName)

