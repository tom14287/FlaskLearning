from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()

if __name__ == '__main__':
	app.run(debug=True)