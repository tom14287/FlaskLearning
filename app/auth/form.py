from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,SelectField
from wtforms.validators import DataRequired, Email
from app.sql_operation.mysql import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

    def validate(self):
        return True

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    type = SelectField('type',validators=[DataRequired()],choices=[('0','Consumer'),('1','Company'),('2','Designer')])

    def validate(self):
        if self.email.data != None and self.password.data != None:
            return True
        return False


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate(self):
        if(self.password == self.confirm):
            return True
        else:
            return False