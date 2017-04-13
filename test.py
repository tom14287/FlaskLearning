from flask import *
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap


app = Flask(__name__)
AppConfig(app)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True



my1list = [1, 2, 3, 4, 5, 6]

@app.route('/')
def index():
	#response = make_response('<h1>this page needs a cookie</h1>')
	#response.set_cookie('answer', '42');
	#return response
	#user_agent = request.headers.get('User-Agent')
	return render_template('index.html')

@app.route('/navbar')
def navbar():
	return render_template('navbar.html')

@app.route('/navbar2')
def navbar2():
	return render_template('navbar2.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name, value=my1list, comments=my1list)

@app.route('/extend')
def extend():
	return render_template('extend.html')

@app.route("/login",methods=['POST','GET'])
def login():
	error = None


	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin123':
			error = "sorry"
		else:
			return redirect(url_for('index'))
	return render_template('login.html', error=error)

if __name__ == '__main__' :
	app.debug = True
	app.run()



