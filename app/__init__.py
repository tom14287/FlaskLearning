from flask import *
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap


def create_app(configfile=None):
	app = Flask(__name__)

	AppConfig(app)

	Bootstrap(app)

	app.config['BOOTSTRAP_SERVE_LOCAL'] = True

	#blueprint

	from designer import app as DesignerPrint
	from gamer import app as GamerPrint
	app.register_blueprint(DesignerPrint, url_prefix='/designer')
	app.register_blueprint(GamerPrint, url_prefix='/gamer')

	return app

