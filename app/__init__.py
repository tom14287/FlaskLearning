from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
lm = LoginManager()
app = Flask(__name__)

def create_app(configfile=None):
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:daijiarun553@localhost:3306/TYMT?charset=utf8'
	app.config['MAIL_SERVER'] = 'smtp.163.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USE_SSL'] = True
	app.config['MAIL_USERNAME'] = 'TYMT_SevenLords@163.com'
	app.config['MAIL_PASSWORD'] = '123456q'
	app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
	app.config['SECRET_KEY'] = 'notsecret'
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)
	lm.init_app(app)
	lm.login_view = 'auth.login'

	app.config['BOOTSTRAP_SERVE_LOCAL'] = True

	#blueprint

	from module_a import module_a_ as ModuleAPrint
	app.register_blueprint(ModuleAPrint, url_prefix='/module_a')

	from module_b import module_b_ as ModuleBPrint
	app.register_blueprint(ModuleBPrint, url_prefix='/module_b')

	from app.auth.views import auth_ as AuthPrint
	app.register_blueprint(AuthPrint, url_prefix='/auth')

	from consumer import consumer_ as CS
	app.register_blueprint(CS, url_prefix='/consumer')

	from main import main_ as MainPrint
	app.register_blueprint(MainPrint)

	return app

