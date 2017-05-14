from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import render_template

app = create_app()

@app.route('/')
def info():
    return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True)