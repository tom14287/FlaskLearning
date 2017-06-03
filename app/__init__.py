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
	app.config['MAIL_USERNAME'] = 'tymt_test_1@163.com'
	app.config['MAIL_PASSWORD'] = '888qqq'
	app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SECRET_KEY'] = 'sekrit!'
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

	from designer import designer_ as des
	app.register_blueprint(des, url_prefix='/designer')

	from company import company_ as compa
	app.register_blueprint(compa, url_prefix='/company')

	from qa import qa_ as QA
	app.register_blueprint(QA, url_prefix='/qa')

	from main import main_ as MainPrint
	app.register_blueprint(MainPrint)

	return app

