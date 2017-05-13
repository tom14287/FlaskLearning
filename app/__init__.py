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


def create_app(configfile=None):
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:123456@localhost:3306/TYMT?charset=utf8'
	app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮件服务器地址
	app.config['MAIL_PORT'] = 587  # 邮件服务器端口
	app.config['MAIL_USE_TLS'] = True  # 启用 TLS
	app.config['MAIL_USERNAME'] = 'me@example.com'
	app.config['MAIL_PASSWORD'] = '123456'
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

	from auth import auth_ as LoginPrint
	app.register_blueprint(LoginPrint, url_prefix='/auth')

	return app

