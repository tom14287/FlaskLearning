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


def create_app(configfile=None):
	app = Flask(__name__)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)

	app.config['BOOTSTRAP_SERVE_LOCAL'] = True

	#blueprint

	from module_a import app as DesignerPrint
	app.register_blueprint(DesignerPrint, url_prefix='/module_a')

	from module_b import app as GamerPrint
	app.register_blueprint(GamerPrint, url_prefix='/module_b')

	return app

